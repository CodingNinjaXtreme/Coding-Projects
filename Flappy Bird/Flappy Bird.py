import pygame
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('game-music-loop-7-145285.mp3')
pygame.mixer.music.play(-1)

# Screen settings
WIDTH, HEIGHT = 800, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird ")

# Clock and font
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsans", 40)

# Load images
bg_img = pygame.image.load("bg (2).png").convert()
ground_img = pygame.image.load("ground (1).png").convert_alpha()
bird_img = pygame.image.load("bird1.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 30))
pipe_img = pygame.image.load("NicePng_pipes-png_388476.png").convert_alpha()

ground_height = ground_img.get_height()

# Constants
bird_x = 50
bird_radius = 13
pipe_width = 60


# Function to create a new pipe
def create_pipe(pipe_gap):
    pipe_img_height = random.randint(100, 400)
    top = pygame.Rect(WIDTH, 0, pipe_width, pipe_img_height)
    bottom = pygame.Rect(WIDTH, pipe_img_height + pipe_gap, pipe_width, HEIGHT - pipe_img_height - pipe_gap - ground_height)
    return {"top": top, "bottom": bottom, "scored": False}


# Function to draw everything
def draw_screen(bird_y, pipes, score):
    SCREEN.blit(bg_img, (0, 0))

    for pipe in pipes:
        top_img = pygame.transform.flip(pipe_img, False, True)
        top_img = pygame.transform.scale(top_img, (pipe['top'].width, pipe['top'].height))
        SCREEN.blit(top_img, (pipe['top'].x, pipe['top'].y))

        bottom_img = pygame.transform.scale(pipe_img, (pipe['bottom'].width, pipe['bottom'].height))
        SCREEN.blit(bottom_img, (pipe['bottom'].x, pipe['bottom'].y))

    SCREEN.blit(bird_img, (bird_x - bird_img.get_width()//2, int(bird_y - bird_img.get_height()//2)))
    SCREEN.blit(ground_img, (0, HEIGHT - ground_height))

    text = FONT.render(str(score), True, (0, 0, 0))
    SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, 20))

    pygame.display.update()


# Game Over screen
def show_game_over(score):
    text1 = FONT.render("Game Over!", True, (0, 0, 0))
    text2 = FONT.render("R - Restart | Q - Quit", True, (0, 0, 0))
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 60))
    SCREEN.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2))
    SCREEN.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 40))
    pygame.display.update()


def show_menu():
    while True:
        SCREEN.fill((135, 206, 235))  # Light sky blue
        title = FONT.render("Flappy Bird - Choose Difficulty", True, (0, 0, 0))
        easy = FONT.render("1 - Easy", True, (0, 128, 0))
        medium = FONT.render("2 - Medium", True, (255, 165, 0))
        hard = FONT.render("3 - Hard", True, (255, 0, 0))

        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        SCREEN.blit(easy, (WIDTH//2 - easy.get_width()//2, HEIGHT//2 - 20))
        SCREEN.blit(medium, (WIDTH//2 - medium.get_width()//2, HEIGHT//2 + 30))
        SCREEN.blit(hard, (WIDTH//2 - hard.get_width()//2, HEIGHT//2 + 80))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return {'gravity': 0.2, 'flap_power': -5, 'pipe_gap': 250, 'pipe_vel': 3}
        elif keys[pygame.K_2]:
            return {'gravity': 0.3, 'flap_power': -6, 'pipe_gap': 200, 'pipe_vel': 4}
        elif keys[pygame.K_3]:
            return {'gravity': 0.4, 'flap_power': -7, 'pipe_gap': 150, 'pipe_vel': 5}


def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            settings = show_menu()
            game_loop(settings)
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()


def game_loop(settings):
    bird_y = HEIGHT // 2
    bird_vel = 0
    pipes = [create_pipe(settings['pipe_gap'])]
    score = 0
    running = True

    gravity = settings['gravity']
    flap_power = settings['flap_power']
    pipe_gap = settings['pipe_gap']
    pipe_vel = settings['pipe_vel']

    while running:
        clock.tick(60)
        bird_vel += gravity
        bird_y += bird_vel

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vel = flap_power

        for pipe in pipes:
            pipe['top'].x -= pipe_vel
            pipe['bottom'].x -= pipe_vel

        if pipes[-1]['top'].x < WIDTH - 200:
            pipes.append(create_pipe(pipe_gap))
        if pipes[0]['top'].x < -pipe_width:
            pipes.pop(0)

        bird_rect = pygame.Rect(bird_x - bird_img.get_width()//2, int(bird_y - bird_img.get_height()//2), bird_img.get_width(), bird_img.get_height())
        for pipe in pipes:
            if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
                running = False
            if pipe['top'].x + pipe_width < bird_x and not pipe['scored']:
                score += 1
                pipe['scored'] = True

        if bird_y > HEIGHT - ground_height or bird_y < 0:
            running = False

        draw_screen(bird_y, pipes, score)

    show_game_over(score)
    wait_for_restart()


# Start the game with menu
settings = show_menu()
game_loop(settings)
