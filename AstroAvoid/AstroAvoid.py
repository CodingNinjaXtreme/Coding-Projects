import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

# New play again buttons
yes_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 90, 50)
no_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 50, 90, 50)

def draw(player, elapsed_time, stars, game_over=False):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    if game_over:
        lost_text = FONT.render("You lost! Do you want to play again?", 1, "white")
        WIN.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - 100))

        # Draw "Yes" and "No" buttons
        pygame.draw.rect(WIN, (0, 255, 0), yes_button)
        pygame.draw.rect(WIN, (255, 0, 0), no_button)

        yes_text = FONT.render("Yes", 1, "black")
        no_text = FONT.render("No", 1, "black")

        WIN.blit(yes_text, (yes_button.x + (yes_button.width - yes_text.get_width()) // 2,
                           yes_button.y + (yes_button.height - yes_text.get_height()) // 2))
        WIN.blit(no_text, (no_button.x + (no_button.width - no_text.get_width()) // 2,
                          no_button.y + (no_button.height - no_text.get_height()) // 2))

    pygame.display.update()

def check_play_again():
    # Check if the player clicked on the "Yes" or "No" button
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if yes_button.collidepoint(mouse_x, mouse_y):
        return "yes"
    elif no_button.collidepoint(mouse_x, mouse_y):
        return "no"
    return None

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            draw(player, elapsed_time, stars, game_over=True)

            pygame.display.update()

            # Wait for the player to click "Yes" or "No"
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting_for_restart = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        result = check_play_again()
                        if result == "yes":
                            main()  # Restart the game by calling main() again
                            waiting_for_restart = False
                        elif result == "no":
                            waiting_for_restart = False

            break  # Break out of the main loop after game over and restart/exit

        draw(player, elapsed_time, stars)

    pygame.quit()

# Run the game
main()
