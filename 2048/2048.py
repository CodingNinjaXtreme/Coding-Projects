import pygame
import random
import sys

pygame.init()

# Constants
GRID_SIZE = 4
CELL_SIZE = 100
GRID_PADDING = 10
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * GRID_PADDING
SCREEN_HEIGHT = SCREEN_WIDTH + 100

# Colors
BACKGROUND = (187, 173, 160)
EMPTY_CELL = (205, 193, 180)
CELL_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

TEXT_COLORS = {
    2: (119, 110, 101),
    4: (119, 110, 101),
    8: (249, 246, 242),
    16: (249, 246, 242),
    32: (249, 246, 242),
    64: (249, 246, 242),
    128: (249, 246, 242),
    256: (249, 246, 242),
    512: (249, 246, 242),
    1024: (249, 246, 242),
    2048: (249, 246, 242)
}


class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_won = False
        self.game_over = False

        # Add two initial tiles
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_cells = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            # Compress row (move all non-zero elements to the left)
            row = [cell for cell in self.grid[i] if cell != 0]

            # Merge adjacent equal elements
            merged_row = []
            skip_next = False
            for j in range(len(row)):
                if skip_next:
                    skip_next = False
                    continue

                if j < len(row) - 1 and row[j] == row[j + 1]:
                    merged_row.append(row[j] * 2)
                    self.score += row[j] * 2
                    if row[j] * 2 == 2048 and not self.game_won:
                        self.game_won = True
                    skip_next = True
                else:
                    merged_row.append(row[j])

            # Pad with zeros
            merged_row.extend([0] * (GRID_SIZE - len(merged_row)))

            # Check if row changed
            if merged_row != self.grid[i]:
                moved = True
                self.grid[i] = merged_row

        return moved

    def move_right(self):
        # Reverse, move left, reverse back
        for i in range(GRID_SIZE):
            self.grid[i] = self.grid[i][::-1]

        moved = self.move_left()

        for i in range(GRID_SIZE):
            self.grid[i] = self.grid[i][::-1]

        return moved

    def move_up(self):
        # Transpose, move left, transpose back
        self.grid = list(map(list, zip(*self.grid)))
        moved = self.move_left()
        self.grid = list(map(list, zip(*self.grid)))
        return moved

    def move_down(self):
        # Transpose, move right, transpose back
        self.grid = list(map(list, zip(*self.grid)))
        moved = self.move_right()
        self.grid = list(map(list, zip(*self.grid)))
        return moved

    def can_move(self):
        # Check if any move is possible
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return True

                # Check adjacent cells for possible merges
                if i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return True
                if j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return True

        return False

    def make_move(self, direction):
        if self.game_over:
            return

        moved = False
        if direction == 'left':
            moved = self.move_left()
        elif direction == 'right':
            moved = self.move_right()
        elif direction == 'up':
            moved = self.move_up()
        elif direction == 'down':
            moved = self.move_down()

        if moved:
            self.add_random_tile()
            if not self.can_move():
                self.game_over = True


def draw_game(screen, game):
    screen.fill(BACKGROUND)

    # Draw grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * CELL_SIZE + (j + 1) * GRID_PADDING
            y = i * CELL_SIZE + (i + 1) * GRID_PADDING + 80

            value = game.grid[i][j]

            # Draw the cell background
            if value == 0:
                color = EMPTY_CELL
            else:
                color = CELL_COLORS.get(value, (60, 58, 50))

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), border_radius=5)

            # Draw number
            if value != 0:
                font_size = 48 if value < 100 else 36 if value < 1000 else 30
                font = pygame.font.Font(None, font_size)
                text_color = TEXT_COLORS.get(value, (249, 246, 242))
                text = font.render(str(value), True, text_color)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    # Draw score
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Score: {game.score}", True, (119, 110, 101))
    screen.blit(score_text, (10, 10))

    # Draw game status and restart/quit instructions
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 24)
    if game.game_won and not game.game_over:
        win_text = font_large.render("You Win!", True, (119, 110, 101))
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(win_text, text_rect)

        instr_text = font_small.render("Press R to restart or Q to quit", True, (119, 110, 101))
        instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(instr_text, instr_rect)

    elif game.game_over:
        game_over_text = font_large.render("Game Over!", True, (119, 110, 101))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(game_over_text, text_rect)

        instr_text = font_small.render("Press R to restart or Q to quit", True, (119, 110, 101))
        instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(instr_text, instr_rect)

    # Draw instructions if the game is ongoing
    if not game.game_over and not game.game_won:
        font_inst = pygame.font.Font(None, 24)
        instructions = "Use arrow keys to move tiles"
        inst_text = font_inst.render(instructions, True, (119, 110, 101))
        screen.blit(inst_text, (10, SCREEN_HEIGHT - 30))


# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")

# Game setup
game = Game2048()
clock = pygame.time.Clock()

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.make_move('left')
            elif event.key == pygame.K_RIGHT:
                game.make_move('right')
            elif event.key == pygame.K_UP:
                game.make_move('up')
            elif event.key == pygame.K_DOWN:
                game.make_move('down')
            elif event.key == pygame.K_r:
                # Restart game
                game = Game2048()
            elif event.key == pygame.K_q:
                # Quit game
                running = False

    draw_game(screen, game)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()