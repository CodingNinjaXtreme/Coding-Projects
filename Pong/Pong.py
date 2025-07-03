import pygame
import sys
import random
import platform


def get_platform():
    system = platform.system()

    if system == 'Darwin':  # This works for both macOS and iOS
        if 'iPhone' in platform.platform() or 'iPad' in platform.platform():
            return 'iOS'
        else:
            return 'macOS'

    elif system == 'Windows':
        return 'Windows'
    else:
        return 'unknown'


# Initialize mixer and play background music
pygame.mixer.init()
pygame.mixer.music.load('pong-pong-193380.mp3')
pygame.mixer.music.play(-1)

# Initialize game
pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
small_font = pygame.font.SysFont('Comic Sans MS', 20)




# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Paddle and ball setup
paddle_width, paddle_height = 10, 100
left_paddle_x = 10
left_paddle_y = HEIGHT // 2 - paddle_height // 2
right_paddle_x = WIDTH - 10 - paddle_width
right_paddle_y = HEIGHT // 2 - paddle_height // 2
Ball_size = 15
ball_x = WIDTH // 2 - Ball_size // 2
ball_y = HEIGHT // 2 - Ball_size // 2
ball_speed_x = 5
ball_speed_y = 5
paddle_speed = 10
MAX_BALL_SPEED = 12
MAX_PADDLE_SPEED = 12
left_score = 0
right_score = 0

clock = pygame.time.Clock()
last_speedup_time = pygame.time.get_ticks()
BALL_SPEED_INCREMENT = 0.5
PADDLE_SPEED_INCREMENT = 0.3

# Game mode: None = menu, 'bot' or '1v1'
game_mode = None

# Countdown control
countdown_active = False
countdown_start_time = 0
countdown_duration = 3000  # milliseconds, 3 seconds

# Pause control
paused = False

# Game Over control
game_over = False
WINNING_SCORE = 10

# Button setup
button_width, button_height = 200, 60
button_bot_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 80, button_width, button_height)
button_1v1_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height)

# AI settings
AI_REACTION_DELAY = 30  # milliseconds
last_ai_move_time = 0

current_platform = get_platform()


def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = WIDTH // 2 - Ball_size // 2
    ball_y = HEIGHT // 2 - Ball_size // 2
    ball_speed_x = 5 if ball_speed_x > 0 else -5
    ball_speed_y = 5 if ball_speed_y > 0 else -5


def draw_text_center(text, fount, color, y_pos):
    text_surf = fount.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, y_pos))
    screen.blit(text_surf, text_rect)


def draw_center_line():
    line_width = 4
    segment_height = 20
    segment_gap = 15
    y = 0
    while y < HEIGHT:
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - line_width // 2, y, line_width, segment_height))
        y += segment_height + segment_gap


# Main game loop
while True:
    current_time = pygame.time.get_ticks()
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Pause toggle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game_over and not countdown_active and game_mode is not None:
                paused = not paused

        # Menu button click detection
        if game_mode is None and event.type == pygame.MOUSEBUTTONDOWN and not countdown_active:
            if button_bot_rect.collidepoint(event.pos):
                game_mode = 'bot'
                countdown_active = True
                countdown_start_time = current_time
                left_score = 0
                right_score = 0
                reset_ball()
                left_paddle_y = HEIGHT // 2 - paddle_height // 2
                right_paddle_y = HEIGHT // 2 - paddle_height // 2
                paused = False
                game_over = False
            elif button_1v1_rect.collidepoint(event.pos):
                game_mode = '1v1'
                countdown_active = True
                countdown_start_time = current_time
                left_score = 0
                right_score = 0
                reset_ball()
                left_paddle_y = HEIGHT // 2 - paddle_height // 2
                right_paddle_y = HEIGHT // 2 - paddle_height // 2
                paused = False
                game_over = False

        # If game over, allow restart on any key
        if game_over and event.type == pygame.KEYDOWN:
            game_mode = None
            countdown_active = False
            paused = False
            game_over = False

    # Draw the menu if no mode selected
    if game_mode is None:
        draw_text_center('PONG GAME', font, (255, 255, 255), 150)
        pygame.draw.rect(screen, (50, 150, 50), button_bot_rect)
        pygame.draw.rect(screen, (50, 50, 150), button_1v1_rect)
        draw_text_center('You vs AI Bot', font, (255, 255, 255), button_bot_rect.centery)
        draw_text_center('1v1 Player', font, (255, 255, 255), button_1v1_rect.centery)
        draw_text_center('Select mode to start', small_font, (200, 200, 200), HEIGHT // 2 + 120)
        pygame.display.flip()
        clock.tick(60)
        continue

    # Draw center line for classic Pong look
    draw_center_line()

    # If countdown active, display countdown and pause gameplay
    if countdown_active:
        elapsed = current_time - countdown_start_time
        seconds_left = 3 - elapsed // 1000
        if seconds_left > 0:
            draw_text_center(f"Game starts in {seconds_left}...", font, (255, 255, 255), HEIGHT // 2)
            pygame.display.flip()
            clock.tick(60)
            continue
        else:
            countdown_active = False  # Countdown finished, start game

    # If game over, display winner and options
    if game_over:
        winner = "Left Player" if left_score >= WINNING_SCORE else "Right Player"
        if game_mode == 'bot' and winner == "Right Player":
            winner = "AI Bot"
        draw_text_center(f"{winner} Wins!", font, (255, 255, 0), HEIGHT // 2 - 40)
        draw_text_center("Press any key to return to menu", small_font, (255, 255, 255), HEIGHT // 2 + 10)
        pygame.display.flip()
        clock.tick(60)
        continue

    # Pause message
    if paused:
        draw_text_center("Paused - Press P to resume", font, (255, 255, 255), HEIGHT // 2)
        pygame.display.flip()
        clock.tick(60)
        continue

    # Speed increase over time every 60 seconds
    if current_time - last_speedup_time >= 60000:
        last_speedup_time = current_time
        if abs(ball_speed_x) < MAX_BALL_SPEED:
            ball_speed_x += BALL_SPEED_INCREMENT if ball_speed_x > 0 else -BALL_SPEED_INCREMENT
        if abs(ball_speed_y) < MAX_BALL_SPEED:
            ball_speed_y += BALL_SPEED_INCREMENT if ball_speed_y > 0 else -BALL_SPEED_INCREMENT
        if paddle_speed < MAX_PADDLE_SPEED:
            paddle_speed += PADDLE_SPEED_INCREMENT

    keys = pygame.key.get_pressed()

    # Left paddle control
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - paddle_height:
        left_paddle_y += paddle_speed

    # Right paddle control
    if game_mode == '1v1':
        if keys[pygame.K_UP] and right_paddle_y > 0:
            right_paddle_y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
            right_paddle_y += paddle_speed
    elif game_mode == 'bot':
        if current_time - last_ai_move_time > AI_REACTION_DELAY:
            last_ai_move_time = current_time
            miss_range = 8
            target_y = ball_y + Ball_size / 2 + random.uniform(-miss_range, miss_range)

            # Smooth movement toward target_y with max paddle_speed movement
            center_diff = target_y - (right_paddle_y + paddle_height / 2)
            right_paddle_y += max(min(center_diff * 0.25, paddle_speed), -paddle_speed)
            right_paddle_y = max(0, min(HEIGHT - paddle_height, right_paddle_y))

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball bounce off top and bottom
    if ball_y <= 0 or ball_y >= HEIGHT - Ball_size:
        ball_speed_y *= -1
        ball_y = max(0, min(ball_y, HEIGHT - Ball_size))


    # Ball collisions with paddles
    if (ball_x <= left_paddle_x + paddle_width and
        left_paddle_y < ball_y + Ball_size and
        ball_y < left_paddle_y + paddle_height and
        ball_speed_x < 0):
        ball_speed_x *= -1
        ball_x = left_paddle_x + paddle_width


    if (ball_x + Ball_size >= right_paddle_x and
        right_paddle_y < ball_y + Ball_size and
        ball_y < right_paddle_y + paddle_height and
        ball_speed_x > 0):
        ball_speed_x *= -1
        ball_x = right_paddle_x - Ball_size


    # Score check and ball reset
    if ball_x < 0:
        right_score += 1
        reset_ball()
    elif ball_x > WIDTH:
        left_score += 1
        reset_ball()

    # Check for winner
    if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
        game_over = True

    # Draw paddles, ball, and scores
    pygame.draw.rect(screen, (255, 255, 255), (left_paddle_x, int(left_paddle_y), paddle_width, paddle_height))
    pygame.draw.rect(screen, (255, 255, 255), (right_paddle_x, int(right_paddle_y), paddle_width, paddle_height))
    pygame.draw.ellipse(screen, (255, 255, 255), (int(ball_x), int(ball_y), Ball_size, Ball_size))

    left_score_text = font.render(str(left_score), True, (255, 255, 255))
    right_score_text = font.render(str(right_score), True, (255, 255, 255))
    screen.blit(left_score_text, (WIDTH // 4, 20))
    screen.blit(right_score_text, (WIDTH * 3 // 4, 20))

    # Instructions bottom left
    draw_text_center("Press P to Pause/Resume", small_font, (180, 180, 180), HEIGHT - 30)

    pygame.display.flip()
    clock.tick(60)