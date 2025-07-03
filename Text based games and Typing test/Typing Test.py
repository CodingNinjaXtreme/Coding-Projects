import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Speed Test")

# Fonts and Colors
FONT = pygame.font.Font(None, 48)
BIG_FONT = pygame.font.Font(None, 64)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Word list (can expand this later)
WORDS = ["python", "developer", "keyboard", "function", "variable",
         "object", "pygame", "loop", "condition", "input", "output"]

# Clock
clock = pygame.time.Clock()

def draw_text(surface, text, font, color, pos):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, pos)


running = True
while running:
    input_text = ''
    target_word = random.choice(WORDS)
    start_time = None
    total_time = 0
    correct = 0
    total = 0
    game_over = False

    while running:
        win.fill(WHITE)

        if not game_over:
            if start_time is None:
                start_time = time.time()

            draw_text(win, "Type the word:", FONT, BLACK, (50, 100))
            draw_text(win, target_word, BIG_FONT, GRAY, (50, 150))

            draw_text(win, input_text, BIG_FONT, BLACK, (50, 250))

            elapsed = round(time.time() - start_time, 1)
            draw_text(win, f"Time: {elapsed}s", FONT, BLACK, (50, 50))

        else:
            wpm = round((correct / total_time) * 60) if total_time > 0 else 0
            accuracy = round((correct / total) * 100) if total > 0 else 0

            draw_text(win, "Test Completed!", BIG_FONT, BLACK, (50, 100))
            draw_text(win, f"WPM: {wpm}", FONT, GREEN, (50, 200))
            draw_text(win, f"Accuracy: {accuracy}%", FONT, GREEN, (50, 250))
            draw_text(win, "Press ENTER to restart", FONT, RED, (50, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip() == target_word:
                            correct += 1
                        total += 1
                        target_word = random.choice(WORDS)
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

                    # End the game after 10 words
                    if total == 10:
                        total_time = time.time() - start_time
                        game_over = True

                else:
                    if event.key == pygame.K_RETURN:
                        # Reset game
                        input_text = ''
                        target_word = random.choice(WORDS)
                        start_time = None
                        total_time = 0
                        correct = 0
                        total = 0
                        game_over = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


