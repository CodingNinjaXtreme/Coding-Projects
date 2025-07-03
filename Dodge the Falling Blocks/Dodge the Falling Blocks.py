import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 36)

# Player setup
player_size = 50
player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - player_size - 10, player_size, player_size)
player_speed = 7

# Falling block setup
block_width = 50
block_height = 50
block_speed = 5
blocks = []

# Spawn blocks periodically
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 700)  # Spawn every 700ms

score = 0
game_over = False

def draw_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_EVENT and not game_over:
            # Spawn a new block at a random x position at the top
            x_pos = random.randint(0, WIDTH - block_width)
            new_block = pygame.Rect(x_pos, 0, block_width, block_height)
            blocks.append(new_block)

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        # Move blocks down
        for block in blocks[:]:
            block.y += block_speed
            if block.top > HEIGHT:
                blocks.remove(block)
                score += 1  # Increase score for each block dodged

        # Check collision
        for block in blocks:
            if player.colliderect(block):
                game_over = True
                break

    # Drawing
    screen.fill((30, 30, 30))  # Dark background
    pygame.draw.rect(screen, (0, 255, 0), player)  # Player in green

    for block in blocks:
        pygame.draw.rect(screen, (255, 0, 0), block)  # Blocks in red

    draw_text(f"Score: {score}", 10, 10)

    if game_over:
        draw_text("GAME OVER! Press R to Restart", WIDTH // 6, HEIGHT // 2)

    pygame.display.flip()
    clock.tick(60)

    # Restart game
    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player.x = WIDTH // 2 - player_size // 2
            blocks.clear()
            score = 0
            game_over = False
