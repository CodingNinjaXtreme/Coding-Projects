import pygame
import random
import sys

pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Stars")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load images with colorkey transparency for JPG player image
player_image = pygame.image.load('oozr_fe7r_210520.jpg').convert()
player_image.set_colorkey((255, 255, 255))  # Make white transparent
player_image = pygame.transform.scale(player_image, (120, 60))

star_image = pygame.image.load('star.png').convert_alpha()
star_image = pygame.transform.scale(star_image, (40, 40))

powerup_image = pygame.image.load('app_13764316.png').convert_alpha()
powerup_image = pygame.transform.scale(powerup_image, (40, 40))

background_image = pygame.image.load('2303.w026.n002.3330B.p1.3330.jpg').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen.blit(background_image, (0, 0))

catch_sound = pygame.mixer.Sound('8-bit-video-game-points-version-1-145826.mp3')
catch_sound.play()
catch_sound.set_volume(0.2)  # Volume range: 0.0 to 1.0

# For background music
pygame.mixer.music.load('space-ambient-351305.mp3')
pygame.mixer.music.play(-1)  # Loop forever


# Masks for collision
player_mask = pygame.mask.from_surface(player_image)
star_mask = pygame.mask.from_surface(star_image)
powerup_mask = pygame.mask.from_surface(powerup_image)

# Game variables
score = 0
lives = 10

SPAWN_STAR = pygame.USEREVENT + 1
SPAWN_POWERUP = pygame.USEREVENT + 2

pygame.time.set_timer(SPAWN_STAR, 1000)       # every second
pygame.time.set_timer(SPAWN_POWERUP, 10000)  # every 10 seconds

class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 10

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class FallingObject:
    def __init__(self, image, mask, speed_range=(3, 6)):
        self.image = image
        self.mask = mask
        self.rect = self.image.get_rect(midtop=(random.randint(20, SCREEN_WIDTH - 20), -40))
        self.speed = random.uniform(*speed_range)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def check_collision(obj1, obj2):
    offset = (obj2.rect.left - obj1.rect.left, obj2.rect.top - obj1.rect.top)
    return obj1.mask.overlap(obj2.mask, offset) is not None

# Player instance
player = Player(player_image)

stars = []
powerups = []

# Control star speed globally for ramp effect
star_speed_min = 2.0
star_speed_max = 6.0
current_star_speed_min = star_speed_min
current_star_speed_max = star_speed_max

# We'll gradually ramp speed back up after powerup slow down
SPEED_RAMP_RATE = 0.005  # Increase per frame

def create_star():
    # Create a star with current speed range
    return FallingObject(star_image, star_mask, speed_range=(current_star_speed_min, current_star_speed_max))

running = True
while running:
    clock.tick(60)
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_STAR:
            stars.append(create_star())

        if event.type == SPAWN_POWERUP:
            powerups.append(FallingObject(powerup_image, powerup_mask, speed_range=(2, 4)))

    keys = pygame.key.get_pressed()
    player.move(keys)

    # Update stars
    for star in stars[:]:
        star.fall()
        if star.rect.top > SCREEN_HEIGHT:
            stars.remove(star)
            lives -= 1
        elif check_collision(player, star):
            stars.remove(star)
            score += 1
            catch_sound.play()

    # Update powerups
    for powerup in powerups[:]:
        powerup.fall()
        if powerup.rect.top > SCREEN_HEIGHT:
            powerups.remove(powerup)
        elif check_collision(player, powerup):
            powerups.remove(powerup)
            # Powerup slows down stars by lowering speed range
            current_star_speed_min = max(star_speed_min, current_star_speed_min - 1.5)
            current_star_speed_max = max(star_speed_min + 1, current_star_speed_max - 1.5)

    # Gradually ramp star speed back up each frame towards max
    if current_star_speed_min < star_speed_min:
        current_star_speed_min = min(star_speed_min, current_star_speed_min + SPEED_RAMP_RATE)
    if current_star_speed_max < star_speed_max:
        current_star_speed_max = min(star_speed_max, current_star_speed_max + SPEED_RAMP_RATE)

    # Draw everything
    player.draw(screen)
    for star in stars:
        star.draw(screen)
    for powerup in powerups:
        powerup.draw(screen)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

    # Game over
    if lives <= 0:
        game_over_text = font.render("GAME OVER! Press R to Restart or Q to Quit", True, (255, 255, 255))
        rect = game_over_text.get_rect(midtop=(SCREEN_WIDTH // 2, 20))  # 20 pixels from top
        screen.blit(game_over_text, rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # reset
                        score = 0
                        lives = 5
                        stars.clear()
                        powerups.clear()
                        current_star_speed_min = star_speed_min
                        current_star_speed_max = star_speed_max
                        waiting = False
                    if event.key == pygame.K_q:
                        waiting = False
                        running = False
            clock.tick(15)
        continue

    pygame.display.flip()

pygame.quit()
sys.exit()