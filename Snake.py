import pygame
import time
import random

# Snake speed
snake_speed = 20

# Window size (customized)
window_x = 800
window_y = 600

# defining colors (feel free to adjust these)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window with new size
pygame.display.set_caption(' Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Function to reset the game with new starting coordinates
def restart_game():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score
    snake_position = [300, 150]  # New starting position of snake
    snake_body = [[300, 150],
                  [290, 150],
                  [280, 150],
                  [270, 150]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

# displaying Score function with a new font
def show_score(color, font, size):
    # creating font object score_font with custom font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # create a rectangular object for the text surface object
    score_rect = score_surface.get_rect()

    # displaying text
    game_window.blit(score_surface, score_rect)

# game over function with customized message
def game_over():
    # creating font object with a custom font
    my_font = pygame.font.SysFont('arial', 60)

    # creating a text surface on which text will be drawn
    game_over_surface = my_font.render(
        'Game Over! Score: ' + str(score), True, red)

    # create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds, we will quit the program
    time.sleep(2)

    # asking the user if they want to restart or quit
    font = pygame.font.SysFont('arial', 40)
    restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, white)
    game_window.blit(restart_text, (window_x / 4, window_y / 2))
    pygame.display.flip()

    # Loop waiting for user to restart or quit
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()  # Restart the game
                    waiting_for_input = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Main Function
def main():
    global score, snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to

    # defining snake default position
    snake_position = [300, 150]

    # defining the first 4 blocks of snake body
    snake_body = [[300, 150],
                  [290, 150],
                  [280, 150],
                  [270, 150]]

    # fruit position (starting position for fruit)
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True

    # setting the default snake direction towards right
    direction = 'RIGHT'
    change_to = direction

    # initial score
    score = 0

    # Game loop
    while True:
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # If two keys pressed are pressed simultaneously.
        # We don't want the snake to move into two directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        # displaying score continuously
        show_score(white, 'arial', 30)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second / Refresh Rate
        fps.tick(snake_speed)

# Run the game
main()

# Quit pygame window
pygame.quit()
