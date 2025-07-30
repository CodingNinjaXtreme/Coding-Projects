import sys
import random
import math
import pygame

# Initializations
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 400, 500
FPS = 60
GRAVITY = 0.35
JUMP_STRENGTH = -14
PLATFORM_WIDTH, PLATFORM_HEIGHT = 70, 15
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 60
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 40

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Load assets
BG_IMG = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
PLAYER_IMG = pygame.transform.scale(pygame.image.load("pngegg.png").convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
PLATFORM_IMG = pygame.transform.scale(pygame.image.load("platform (1).png").convert_alpha(), (PLATFORM_WIDTH, PLATFORM_HEIGHT))
ENEMY_IMG = pygame.transform.scale(pygame.image.load("green_little_bug.png").convert_alpha(), (ENEMY_WIDTH, ENEMY_HEIGHT))
UFO_IMG = pygame.transform.scale(pygame.image.load("Daco_5686022.png").convert_alpha(), (40, 40))
BULLET_IMG = pygame.transform.scale(pygame.image.load("bullet (1).png").convert_alpha(), (16, 20))
SQUASH_SOUND = pygame.mixer.Sound("squish-pop-256410.mp3")

# Track kills
enemies_stomped = 0

class Platform:
    def __init__(self, x, y, sway=True):
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.sway = sway
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(1, 2) if sway else 0
        self.enemy = None

    def update(self):
        if self.sway:
            self.rect.x += self.direction * self.speed
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.direction *= -1
        if self.enemy:
            self.enemy.update(self)

    def draw(self, surface):
        surface.blit(PLATFORM_IMG, (self.rect.x, self.rect.y))
        if self.enemy:
            self.enemy.draw(surface)

class Enemy:
    def __init__(self, platform):
        self.platform = platform
        self.direction = 1
        self.speed = 1.5
        self.offset_x = (PLATFORM_WIDTH - ENEMY_WIDTH) // 2
        self.rect = pygame.Rect(0, 0, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.dead = False
        self.death_timer = 0
        self.update_rect()

    def update_rect(self):
        self.rect.x = self.platform.rect.x + self.offset_x
        self.rect.y = self.platform.rect.y - ENEMY_HEIGHT

    def update(self, platform):
        if self.dead:
            self.death_timer += 1
            if self.death_timer > 15:
                self.platform.enemy = None
            return

        self.offset_x += self.direction * self.speed
        if self.offset_x <= 0 or self.offset_x >= PLATFORM_WIDTH - ENEMY_WIDTH:
            self.direction *= -1
            self.offset_x += self.direction * self.speed

        self.update_rect()

    def draw(self, surface):
        if self.dead:
            squashed_img = pygame.transform.scale(ENEMY_IMG, (ENEMY_WIDTH, ENEMY_HEIGHT // 3))
            surface.blit(squashed_img, (self.rect.x, self.rect.y + ENEMY_HEIGHT * 2 // 3))
        else:
            surface.blit(ENEMY_IMG, (self.rect.x, self.rect.y))

    def kill(self):
        self.dead = True
        SQUASH_SOUND.play()

class FloatingUFO:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.start_x = x
        self.hover_time = 0
        self.bullets = []
        self.bullet_timer = 0
        self.burst_cooldown = random.randint(120, 200)
        self.burst_shots_left = 0
        self.burst_shot_delay = 0

    def update(self):
        self.hover_time += 0.05
        self.rect.x = self.start_x + math.sin(self.hover_time) * 30

        if self.burst_shots_left > 0:
            self.burst_shot_delay -= 1
            if self.burst_shot_delay <= 0:
                self.shoot()
                self.burst_shots_left -= 1
                self.burst_shot_delay = 10
        else:
            self.bullet_timer -= 1
            if self.bullet_timer <= 0:
                self.burst_shots_left = 3
                self.burst_shot_delay = 0
                self.bullet_timer = self.burst_cooldown
                self.burst_cooldown = random.randint(120, 200)

        for bullet in self.bullets:
            bullet.y += 5
        self.bullets = [b for b in self.bullets if b.y < HEIGHT]

    def shoot(self):
        bullet = pygame.Rect(self.rect.centerx - 8, self.rect.bottom, 16, 20)
        self.bullets.append(bullet)

    def draw(self, surface):
        surface.blit(UFO_IMG, self.rect.topleft)
        for bullet in self.bullets:
            surface.blit(BULLET_IMG, bullet.topleft)


def reset_game():
    global player_x, player_y, player_vel_y, platforms, score, max_height, game_over, ufos
    player_x = WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = HEIGHT - PLAYER_HEIGHT - 10
    player_vel_y = 0
    score = 0
    max_height = player_y
    game_over = False

    platforms = []
    for i in range(6):
        plat_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        plat_y = i * 100
        sway = random.choice([True, False])
        new_platform = Platform(plat_x, plat_y, sway)
        if sway and random.random() < 0.2:
            new_platform.enemy = Enemy(new_platform)
        platforms.append(new_platform)

    platforms[0] = Platform(player_x, player_y + PLAYER_HEIGHT, sway=False)

    # Spawn UFOs
    ufos = [FloatingUFO(random.randint(0, WIDTH - 40), random.randint(50, 200))]
    ufos = []


reset_game()

while True:
    clock.tick(FPS)
    screen.blit(BG_IMG, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                reset_game()
            elif quit_button.collidepoint(event.pos):
                pygame.quit()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5

        if player_x > WIDTH:
            player_x = -PLAYER_WIDTH
        elif player_x < -PLAYER_WIDTH:
            player_x = WIDTH

        player_vel_y += GRAVITY
        player_y += player_vel_y
        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

        if player_vel_y > 0:
            for plat in platforms:
                if player_rect.colliderect(plat.rect) and player_y + PLAYER_HEIGHT - 10 < plat.rect.y:
                    player_vel_y = JUMP_STRENGTH

        if player_y < HEIGHT // 3:
            scroll = HEIGHT // 3 - player_y
            player_y = HEIGHT // 3
            score += scroll


            # Spawn UFOs based on score BEFORE shifting platforms
            ufo_spawn_chance = min(0.005 + (score // 1000) * 0.002, 0.03)  # max 3%
            if len(ufos) < 3 and random.random() < ufo_spawn_chance:
                ufo_x = random.randint(0, WIDTH - 40)
                ufo_y = random.randint(-100, -40)  # spawn above screen
                ufos.append(FloatingUFO(ufo_x, ufo_y))

            for plat in platforms:
                plat.rect.y += scroll
                if plat.enemy:
                    plat.enemy.rect.y += scroll
            for ufo in ufos:
                ufo.rect.y += scroll
                for bullet in ufo.bullets:
                    bullet.y += scroll



            while len(platforms) < 6:
                plat_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                plat_y = random.randint(-PLATFORM_HEIGHT, 0)
                sway = random.choice([True, False])
                new_plat = Platform(plat_x, plat_y, sway)
                if sway and random.random() < 0.2:
                    new_plat.enemy = Enemy(new_plat)
                platforms.append(new_plat)

        platforms = [plat for plat in platforms if plat.rect.y < HEIGHT]
        ufos = [ufo for ufo in ufos if ufo.rect.y < HEIGHT]

        for plat in platforms:
            plat.update()
            plat.draw(screen)

        for ufo in ufos:
            ufo.update()
            ufo.draw(screen)

            for bullet in ufo.bullets:
                if player_rect.colliderect(bullet):
                    game_over = True

        screen.blit(PLAYER_IMG, (player_x, player_y))
        score_text = font.render(f"Score: {int(score // 10)}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        for plat in platforms:
            if plat.enemy and player_rect.colliderect(plat.enemy.rect):
                enemy = plat.enemy
                if player_vel_y > 0 and player_rect.bottom - enemy.rect.top < 20:
                    player_vel_y = JUMP_STRENGTH
                    enemy.kill()
                    enemies_stomped += 1
                else:
                    game_over = True

        if player_y > HEIGHT:
            game_over = True

    else:
        game_over_text = font.render("Game Over!", True, (0, 0, 0))
        restart_text = font.render("Restart", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        stomp_text = font.render(f"Stomps: {enemies_stomped}", True, (0, 0, 0))
        screen.blit(stomp_text, (10, 35))

        restart_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 40)
        quit_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 60, 120, 40)

        pygame.draw.rect(screen, (0, 150, 0), restart_button)
        pygame.draw.rect(screen, (200, 0, 0), quit_button)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(restart_text, (restart_button.x + 30, restart_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 40, quit_button.y + 10))

    pygame.display.flip()
