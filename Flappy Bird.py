import pygame
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('../image/game-music-loop-7-145285.mp3')
pygame.mixer.music.play(-1)

# Screen settings
WIDTH, HEIGHT = 800, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird ")

# Clock and font
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsans", 40)

# Load images
bg_img = pygame.image.load("../image/bg (2).png").convert()
ground_img = pygame.image.load("../image/ground (1).png").convert_alpha()
bird_img = pygame.image.load("../image/bird1.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 30))  # resize if needed
pipe_img = pygame.image.load("../image/NicePng_pipes-png_388476.png").convert_alpha()


ground_height = ground_img.get_height()

# Game variables
bird_x = 50
bird_radius = 13
gravity = 0.3
flap_power = -6
pipe_width = 60
pipe_gap = 200
pipe_vel = 4


# Function to create a new pipe
def create_pipe():
    pipe_img_height = random.randint(100, 400)
    top = pygame.Rect(WIDTH, 0, pipe_width, pipe_img_height)
    bottom = pygame.Rect(WIDTH, pipe_img_height + pipe_gap, pipe_width, HEIGHT - pipe_img_height - pipe_gap - ground_height)
    return {"top": top, "bottom": bottom, "scored": False}


# Function to draw everything
def draw_screen(bird_y, pipes, score):
    SCREEN.blit(bg_img, (0, 0))

    for pipe in pipes:
        # Scale and flip the top pipe image to match the top pipe rect
        top_img = pygame.transform.flip(pipe_img, False, True)
        top_img = pygame.transform.scale(top_img, (pipe['top'].width, pipe['top'].height))
        SCREEN.blit(top_img, (pipe['top'].x, pipe['top'].y))

        # Scale the bottom pipe image to match the bottom pipe rect
        bottom_img = pygame.transform.scale(pipe_img, (pipe['bottom'].width, pipe['bottom'].height))
        SCREEN.blit(bottom_img, (pipe['bottom'].x, pipe['bottom'].y))

    # Draw bird
    SCREEN.blit(bird_img, (bird_x - bird_img.get_width()//2, int(bird_y - bird_img.get_height()//2)))

    # Draw ground
    SCREEN.blit(ground_img, (0, HEIGHT - ground_height))

    # Draw score
    text = FONT.render(str(score), True, (0, 0, 0))
    SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, 20))

    pygame.display.update()


# Game Over of the text
def show_game_over(score):
    text1 = FONT.render("Game Over!", True, (0, 0, 0))
    text2 = FONT.render("R - Restart | Q - Quit", True, (0,0, 0))
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 60))
    SCREEN.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2))
    SCREEN.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 40))
    pygame.display.update()

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_loop()
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

def game_loop():
    bird_y = HEIGHT // 2
    bird_vel = 0
    pipes = [create_pipe()]
    score = 0
    running = True

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

        # Move pipes
        for pipe in pipes:
            pipe['top'].x -= pipe_vel
            pipe['bottom'].x -= pipe_vel

        if pipes[-1]['top'].x < WIDTH - 200:
            pipes.append(create_pipe())
        if pipes[0]['top'].x < -pipe_width:
            pipes.pop(0)

        # Collision detection
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

# Start the game
game_loop()
