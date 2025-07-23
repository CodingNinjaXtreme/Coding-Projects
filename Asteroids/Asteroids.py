import pygame
import random
import math

# === Init ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 20)

# === Constants ===
ASTEROID_COUNT = 5
BULLET_LIFETIME = 60
SHIP_SPEED = 0.1
ROTATE_ANGLE = 5
MAX_BULLETS = 5
POWERUP_SPAWN_TIME = 600  # frames (10 seconds)

# === Images ===
SPACESHIP_IMG = pygame.image.load('spaceship_small_blue.png').convert_alpha()
ASTEROID_IMG = pygame.image.load('133580-broken-asteroid-photos-free-hd-image.png').convert_alpha()
ASTEROID_IMG = pygame.transform.scale(ASTEROID_IMG, (60, 60))  # Resize from 500x445
BG_IMG = pygame.image.load('bg.jpeg').convert()

# === Helper Functions ===
def wrap_position(x, y):
    return x % WIDTH, y % HEIGHT

def angle_to_vector(angle):
    rad = math.radians(angle - 90)  # Align 0° to UP
    return math.cos(rad), math.sin(rad)

def draw_text(text, x, y, center=False):
    surface = font.render(text, True, (255, 255, 255))
    if center:
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)
    else:
        screen.blit(surface, (x, y))

# === Classes ===
class Ship:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.angle = 0  # 0 is up
        self.dx = 0
        self.dy = 0
        self.lives = 3
        self.score = 0
        self.radius = 15
        self.shield = False
        self.shield_timer = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dx *= 0.99
        self.dy *= 0.99
        self.x, self.y = wrap_position(self.x, self.y)

        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False

    def draw(self):
        rotated = pygame.transform.rotate(SPACESHIP_IMG, -self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)

        if self.shield:
            pygame.draw.circle(screen, (0, 255, 255), (int(self.x), int(self.y)), self.radius + 5, 2)

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360

    def thrust(self):
        thrust_x, thrust_y = angle_to_vector(self.angle)
        self.dx += thrust_x * SHIP_SPEED
        self.dy += thrust_y * SHIP_SPEED

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        vec = angle_to_vector(angle)
        self.dx = vec[0] * 8
        self.dy = vec[1] * 8
        self.frames = BULLET_LIFETIME

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.frames -= 1

    def is_alive(self):
        return self.frames > 0 and 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), (self.x - 2, self.y - 2, 4, 4))

class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.radius = 30

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.x, self.y = wrap_position(self.x, self.y)

    def draw(self):
        rect = ASTEROID_IMG.get_rect(center=(self.x, self.y))
        screen.blit(ASTEROID_IMG, rect)

class PowerUp:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = 10
        self.type = random.choice(["life", "shield"])

    def draw(self):
        color = (0, 255, 0) if self.type == "life" else (0, 255, 255)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

def reset_game():
    global ship, bullets, asteroids, powerups, powerup_timer
    ship = Ship()
    bullets = []
    asteroids = [Asteroid() for _ in range(ASTEROID_COUNT)]
    powerups = []
    powerup_timer = POWERUP_SPAWN_TIME

# === Game Start ===
reset_game()
game_over = False

# === Main Loop ===
running = True
while running:
    clock.tick(60)
    screen.blit(BG_IMG, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_over = False
            reset_game()

    if not game_over:
        # --- Input ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: ship.rotate(-ROTATE_ANGLE)
        if keys[pygame.K_RIGHT]: ship.rotate(ROTATE_ANGLE)
        if keys[pygame.K_UP]: ship.thrust()
        if keys[pygame.K_SPACE] and len(bullets) < MAX_BULLETS:
            bullets.append(Bullet(ship.x, ship.y, ship.angle))

        # --- Update ---
        ship.update()
        for bullet in bullets[:]:
            bullet.update()
            if not bullet.is_alive():
                bullets.remove(bullet)

        for asteroid in asteroids:
            asteroid.update()

        for powerup in powerups[:]:
            if math.hypot(ship.x - powerup.x, ship.y - powerup.y) < ship.radius + powerup.radius:
                if powerup.type == "life":
                    ship.lives += 1
                elif powerup.type == "shield":
                    ship.shield = True
                    ship.shield_timer = 300
                powerups.remove(powerup)

        powerup_timer -= 1
        if powerup_timer <= 0:
            powerups.append(PowerUp())
            powerup_timer = POWERUP_SPAWN_TIME

        # --- Collisions ---
        for asteroid in asteroids:
            if math.hypot(ship.x - asteroid.x, ship.y - asteroid.y) < ship.radius + asteroid.radius:
                if not ship.shield:
                    ship.x, ship.y = WIDTH / 2, HEIGHT / 2
                    ship.dx = ship.dy = 0
                    ship.lives -= 1
                    if ship.lives <= 0:
                        game_over = True
                asteroids.remove(asteroid)
                asteroids.append(Asteroid())
                break

        for bullet in bullets[:]:
            for asteroid in asteroids:
                if math.hypot(bullet.x - asteroid.x, bullet.y - asteroid.y) < asteroid.radius:
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    asteroids.append(Asteroid())
                    ship.score += 10
                    break

        # --- Draw ---
        ship.draw()
        for bullet in bullets:
            bullet.draw()
        for asteroid in asteroids:
            asteroid.draw()
        for powerup in powerups:
            powerup.draw()

        draw_text(f"Score: {ship.score}  Lives: {ship.lives}", 10, 10)
    else:
        draw_text("GAME OVER", WIDTH // 2, HEIGHT // 2 - 30, center=True)
        draw_text("Press R to Restart", WIDTH // 2, HEIGHT // 2 + 10, center=True)

    pygame.display.flip()

pygame.quit()
