import pygame
import sys
import random

# --- Initialization ---
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Mini Adventure")
clock = pygame.time.Clock()

# --- Colors ---
BLUE1 = (0, 0, 255)
BLUE2 = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BG_COLOR = (20, 20, 20)
WHITE = (255, 255, 255)


# --- Player Class ---
class Player:
    def __init__(self):
        self.size = 50
        self.rect = pygame.Rect(WIDTH // 2 - self.size // 2, HEIGHT - self.size - 10, self.size, self.size)
        self.speed = 7
        self.color_frames = [BLUE1, BLUE2]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 10  # ticks per color change

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.left > 0:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.right < WIDTH:
                self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.top > 0:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.bottom < HEIGHT:
                self.rect.y += self.speed

    def animate(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.color_frames)
            self.frame_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color_frames[self.current_frame], self.rect)

# --- Falling Block Class ---
class FallingBlock:
    def __init__(self, x, y, w, h, speed, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.color = color

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# --- Game Variables ---
player = Player()
falling_red_blocks = []
falling_green_blocks = []

RED_SPAWN_EVENT = pygame.USEREVENT + 1
GREEN_SPAWN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(RED_SPAWN_EVENT, 900)    # Red block every 900 ms
pygame.time.set_timer(GREEN_SPAWN_EVENT, 1500) # Green block every 1500 ms

score = 0
game_over = False
font = pygame.font.SysFont('Arial', 36)

def draw_text(text, x, y):
    surf = font.render(text, True, WHITE)
    screen.blit(surf, (x, y))

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == RED_SPAWN_EVENT and not game_over:
            x_pos = random.randint(0, WIDTH - 50)
            falling_red_blocks.append(FallingBlock(x_pos, -50, 50, 50, random.randint(4, 7), RED))
        if event.type == GREEN_SPAWN_EVENT and not game_over:
            x_pos = random.randint(0, WIDTH - 30)
            falling_green_blocks.append(FallingBlock(x_pos, -30, 30, 30, random.randint(3, 6), GREEN))

    if not game_over:
        player.move()
        player.animate()

        # Update red blocks
        for block in falling_red_blocks[:]:
            block.update()
            if block.rect.top > HEIGHT:
                falling_red_blocks.remove(block)
            elif block.rect.colliderect(player.rect):
                game_over = True

        # Update green blocks
        for block in falling_green_blocks[:]:
            block.update()
            if block.rect.top > HEIGHT:
                falling_green_blocks.remove(block)
            elif block.rect.colliderect(player.rect):
                falling_green_blocks.remove(block)
                score += 1
                # Play beep sound on collect
                pygame.mixer.Sound.play(pygame.mixer.Sound(buffer=b'\x00'*100))  # silent placeholder (see note below)

    # Drawing
    screen.fill(BG_COLOR)
    player.draw(screen)
    for block in falling_red_blocks:
        block.draw(screen)
    for block in falling_green_blocks:
        block.draw(screen)
    draw_text(f"Score: {score}", 10, 10)

    if game_over:
        draw_text("GAME OVER! Press R to Restart", WIDTH // 5, HEIGHT // 2)

    pygame.display.flip()
    clock.tick(60)

    # Restart game
    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player = Player()
            falling_red_blocks.clear()
            falling_green_blocks.clear()
            score = 0
            game_over = False
