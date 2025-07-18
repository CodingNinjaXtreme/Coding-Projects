import pygame
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()

# Load sounds
wing_sound = pygame.mixer.Sound('wing.wav')
hit_sound = pygame.mixer.Sound('hit.wav')
point_sound = pygame.mixer.Sound('point.wav')
point_sound.set_volume(0.25)
die_sound = pygame.mixer.Sound('die.wav')

pygame.mixer.music.load('game-music-loop-7-145285.mp3')
pygame.mixer.music.play(-1)

# Screen settings
WIDTH, HEIGHT = 800, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock and font
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsans", 40)

# Colors (used for buttons)
BLACK = (0, 0, 0)

# Load images
bg_img = pygame.image.load("bg (2).png").convert()
ground_img = pygame.image.load("ground (1).png").convert_alpha()
bird_images = [
    pygame.image.load('yellowbird-downflap.png').convert_alpha(),
    pygame.image.load('yellowbird-midflap.png').convert_alpha(),
    pygame.image.load('yellowbird-upflap.png').convert_alpha()
]

pipe_img = pygame.image.load("NicePng_pipes-png_388476.png").convert_alpha()
logo_img = pygame.image.load('pngwing.com.png').convert_alpha()

ground_height = ground_img.get_height()

# Constants
bird_x = 50
bird_radius = 13
pipe_width = 60

# Draw button function
def draw_button(surface, rect, text, font, base_color, hover_color, mouse_pos):
    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)  # border
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def create_pipe(pipe_gap):
    pipe_img_height = random.randint(100, 400)
    top = pygame.Rect(WIDTH, 0, pipe_width, pipe_img_height)
    bottom = pygame.Rect(WIDTH, pipe_img_height + pipe_gap, pipe_width, HEIGHT - pipe_img_height - pipe_gap - ground_height)
    return {"top": top, "bottom": bottom, "scored": False}

def draw_screen(bird_y, pipes, score, bird_img):
    SCREEN.blit(bg_img, (0, 0))

    for pipe in pipes:
        top_img = pygame.transform.flip(pipe_img, False, True)
        top_img = pygame.transform.scale(top_img, (pipe['top'].width, pipe['top'].height))
        SCREEN.blit(top_img, (pipe['top'].x, pipe['top'].y))

        bottom_img = pygame.transform.scale(pipe_img, (pipe['bottom'].width, pipe['bottom'].height))
        SCREEN.blit(bottom_img, (pipe['bottom'].x, pipe['bottom'].y))

    SCREEN.blit(bird_img, (bird_x - bird_img.get_width() // 2, int(bird_y - bird_img.get_height() // 2)))
    SCREEN.blit(ground_img, (0, HEIGHT - ground_height))

    text = FONT.render(str(score), True, (0, 0, 0))
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

    pygame.display.update()

def show_menu():
    easy_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 50)
    medium_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)
    hard_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)

    while True:
        SCREEN.fill((135, 206, 235))  # Sky blue
        mouse_pos = pygame.mouse.get_pos()

        scaled_logo = pygame.transform.scale(logo_img, (400, 200))
        SCREEN.blit(scaled_logo, (WIDTH // 2 - scaled_logo.get_width() // 2, HEIGHT // 2 - 300))

        title = FONT.render("Flappy Bird - Choose Difficulty", True, (0, 0, 0))
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

        draw_button(SCREEN, easy_btn, "Easy", FONT, (0, 200, 0), (0, 255, 0), mouse_pos)
        draw_button(SCREEN, medium_btn, "Medium", FONT, (255, 140, 0), (255, 180, 0), mouse_pos)
        draw_button(SCREEN, hard_btn, "Hard", FONT, (200, 0, 0), (255, 0, 0), mouse_pos)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(mouse_pos):
                    return {'gravity': 0.2, 'flap_power': -5, 'pipe_gap': 250, 'pipe_vel': 3}
                elif medium_btn.collidepoint(mouse_pos):
                    return {'gravity': 0.3, 'flap_power': -6, 'pipe_gap': 200, 'pipe_vel': 4}
                elif hard_btn.collidepoint(mouse_pos):
                    return {'gravity': 0.4, 'flap_power': -7, 'pipe_gap': 150, 'pipe_vel': 5}

def show_game_over(score):
    restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50)
    quit_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 110, 200, 50)

    while True:
        SCREEN.fill((135, 206, 235))
        mouse_pos = pygame.mouse.get_pos()

        title = FONT.render("Game Over!", True, (0, 0, 0))
        score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
        SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))

        draw_button(SCREEN, restart_btn, "Restart", FONT, (0, 120, 200), (0, 160, 255), mouse_pos)
        draw_button(SCREEN, quit_btn, "Quit", FONT, (200, 0, 0), (255, 0, 0), mouse_pos)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(mouse_pos):
                    return
                elif quit_btn.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def game_loop(settings):
    bird_y = HEIGHT // 2
    bird_vel = 0
    pipes = [create_pipe(settings['pipe_gap'])]
    score = 0

    gravity = settings['gravity']
    flap_power = settings['flap_power']
    pipe_gap = settings['pipe_gap']
    pipe_vel = settings['pipe_vel']

    frame = 0

    running = True
    while running:
        clock.tick(60)
        bird_vel += gravity
        bird_y += bird_vel

        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vel = flap_power
                    wing_sound.play()

        for pipe in pipes:
            pipe['top'].x -= pipe_vel
            pipe['bottom'].x -= pipe_vel

        if pipes[-1]['top'].x < WIDTH - 200:
            pipes.append(create_pipe(pipe_gap))
        if pipes[0]['top'].x < -pipe_width:
            pipes.pop(0)

        bird_rect = pygame.Rect(
            bird_x - bird_images[0].get_width() // 2,
            int(bird_y - bird_images[0].get_height() // 2),
            bird_images[0].get_width(),
            bird_images[0].get_height()
        )
        for pipe in pipes:
            if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
                hit_sound.play()
                running = False
            if pipe['top'].x + pipe_width < bird_x and not pipe['scored']:
                score += 1
                pipe['scored'] = True
                point_sound.play()

        if bird_y > HEIGHT - ground_height or bird_y < 0:
            die_sound.play()
            running = False

        bird_img = bird_images[(frame // 5) % len(bird_images)]

        draw_screen(bird_y, pipes, score, bird_img)

    return score

running = True

while running:
    settings = show_menu()
    score = game_loop(settings)
    show_game_over(score)
