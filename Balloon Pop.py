import pygame
import random
import sys

pygame.init()

pop_sound = pygame.mixer.Sound('../image/party-balloon-pop-323588.mp3')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Balloon Pop')
clock = pygame.time.Clock()

background_image = pygame.image.load('../image/4156248.jpg').convert()
background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

balloon_image = pygame.image.load('../image/balloon-1111368_1280.png').convert_alpha()
balloon_image = pygame.transform.smoothscale(
    balloon_image,
    (balloon_image.get_width() // 2, balloon_image.get_height() // 2)
)

font = pygame.font.Font(None, 36)
score = 0
lives = 10

class Balloon:
    def __init__(self, x, y, speed, image):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.y -= self.speed
        self.rect.centery = self.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        rel_x = pos[0] - self.rect.left
        rel_y = pos[1] - self.rect.top
        if 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height:
            return self.mask.get_at((int(rel_x), int(rel_y)))
        return False

def draw_life_lost_message():
    message = font.render("Life Lost!", True, (255, 0, 0))
    rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(message, rect)

def draw_game_over_screen():
    screen.fill((255, 255, 255))
    game_over_text = font.render("Game Over!", True, (0, 0, 0))
    play_again_text = font.render("Play Again", True, (0, 0, 255))
    quit_text = font.render("Quit", True, (0, 0, 255))

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(play_again_text, play_again_rect)
    screen.blit(quit_text, quit_rect)

    return play_again_rect, quit_rect

balloons = []
SPAWN_BALLOON = pygame.USEREVENT + 1

# Initial spawn interval and balloon speed range
spawn_interval = 600  # milliseconds
min_spawn_interval = 200
pygame.time.set_timer(SPAWN_BALLOON, spawn_interval)

base_speed_min = 2.0
base_speed_max = 5.0
max_speed = 10.0

life_lost_time = 0
show_life_lost = False

game_over = False

difficulty_increase_time = pygame.time.get_ticks() + 15000  # first increase at 15 seconds
last_pop_sound_time = 0
pop_sound_cooldown = 150  # milliseconds cooldown between pop sounds

while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if event.type == SPAWN_BALLOON and lives > 0:
                # Spawn 1 or 2 balloons randomly
                for _ in range(random.choice([1, 1, 2])):
                    x = random.randint(30, SCREEN_WIDTH - 30)
                    y = SCREEN_HEIGHT + balloon_image.get_height() // 2
                    # Increase balloon speed gradually over time
                    elapsed = (current_time - (difficulty_increase_time - 15000)) / 15000
                    speed_min = min(base_speed_min + elapsed, max_speed)
                    speed_max = min(base_speed_max + elapsed, max_speed)
                    speed = random.uniform(speed_min, speed_max)
                    balloons.append(Balloon(x, y, speed, balloon_image))

            elif event.type == pygame.MOUSEBUTTONDOWN and lives > 0:
                pos = pygame.mouse.get_pos()
                for balloon in balloons[:]:
                    if balloon.is_clicked(pos):
                        # Play pop sound with cooldown to prevent overlap
                        if current_time - last_pop_sound_time > pop_sound_cooldown:
                            pop_sound.play()
                            last_pop_sound_time = current_time
                        balloons.remove(balloon)
                        score += 1
                        break
        else:
            # Game over screen mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(pos):
                    # Reset game
                    score = 0
                    lives = 10
                    balloons.clear()
                    spawn_interval = 600
                    pygame.time.set_timer(SPAWN_BALLOON, spawn_interval)
                    difficulty_increase_time = pygame.time.get_ticks() + 15000
                    game_over = False
                elif quit_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

    if not game_over:
        screen.blit(background, (0, 0))

        for balloon in balloons[:]:
            balloon.move()
            if balloon.y + balloon.image.get_height() // 2 < 0:
                balloons.remove(balloon)
                lives -= 1
                # Play pop sound with cooldown
                if current_time - last_pop_sound_time > pop_sound_cooldown:
                    pop_sound.play()
                    last_pop_sound_time = current_time
                show_life_lost = True
                life_lost_time = current_time
                break
            else:
                balloon.draw(screen)

        # Draw score and lives
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        lives_text = font.render(f'Lives: {lives}', True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

        if show_life_lost:
            draw_life_lost_message()
            if current_time - life_lost_time > 1000:
                show_life_lost = False

        if lives <= 0:
            game_over = True

        # Increase difficulty every 15 seconds
        if current_time >= difficulty_increase_time and spawn_interval > min_spawn_interval:
            spawn_interval = max(min_spawn_interval, spawn_interval - 50)
            pygame.time.set_timer(SPAWN_BALLOON, spawn_interval)
            difficulty_increase_time = current_time + 15000
    else:
        # Show game over screen and buttons
        play_again_rect, quit_rect = draw_game_over_screen()

    pygame.display.flip()
    clock.tick(60)
