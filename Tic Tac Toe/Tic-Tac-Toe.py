import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("Tic Tac Toe")

# Screen setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800  # extra space below grid for messages and buttons
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREY = (150, 150, 150)
RED = (255,0,0)
VIOLET = (127,0,255)

# Fonts
font = pygame.font.SysFont("comicsans", 180)  # bigger font for X/O
button_font = pygame.font.SysFont("comicsans", 60)
message_font = pygame.font.SysFont("comicsans", 50)
game_over_font = pygame.font.SysFont("comicsans", 100)

# Cell size
CELL_SIZE = SCREEN_WIDTH // 3  # 200

# Game state
board = [[None] * 3 for _ in range(3)]
current_player = "X"
game_over = False
winner = None

# Buttons for menu
buttons = {
    "1v1": pygame.Rect(150, 150, 300, 100),
    "vs_ai": pygame.Rect(150, 350, 300, 100)
}

# Buttons for game screen
restart_button = pygame.Rect(100, CELL_SIZE * 3 + 120, 220, 60)
menu_button = pygame.Rect(350, CELL_SIZE * 3 + 120, 150, 60)
mode = None  # "1v1" or "vs_ai"

# AI delay variables
ai_turn = False
ai_move_time = 0
AI_DELAY = 1000  # milliseconds

#Variables for timer
TIME_LIMIT = 10
current_time_left = TIME_LIMIT
timer_start_time = pygame.time.get_ticks()
timer_rect = pygame.Rect(SCREEN_WIDTH // 2 - 110, CELL_SIZE * 3 + 40, 220, 60) 

def draw_menu():
    screen.fill(WHITE)
    title = button_font.render("Select Game Mode", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    mouse_pos = pygame.mouse.get_pos()
    for label, rect in buttons.items():
        hovered = rect.collidepoint(mouse_pos)
        color = DARK_GREY if hovered else GREY
        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=12)  # border
        text = button_font.render("1v1" if label == "1v1" else "Vs AI", True, BLACK)
        screen.blit(text, (rect.x + rect.width // 2 - text.get_width() // 2,
                           rect.y + rect.height // 2 - text.get_height() // 2))

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, VIOLET, (CELL_SIZE * i, 0), (CELL_SIZE * i, CELL_SIZE * 3), 8)
        pygame.draw.line(screen, VIOLET, (0, CELL_SIZE * i), (CELL_SIZE * 3, CELL_SIZE * i), 8)

def draw_marks():
    for row in range(3):
        for col in range(3):
            if board[row][col] is not None:
               
                mark_value = board[row][col]

                if mark_value == "O":
                    mark = font.render(board[row][col], True, RED)
                else:
                    mark = font.render(board[row][col], True, BLACK)

                mark_rect = mark.get_rect()
                # Center in cell
                cell_x = col * CELL_SIZE
                cell_y = row * CELL_SIZE
                # Position so the mark's center aligns with the cell center
                pos_x = cell_x + (CELL_SIZE - mark_rect.width) // 2
                pos_y = cell_y + (CELL_SIZE - mark_rect.height) // 2
                screen.blit(mark, (pos_x, pos_y))

def draw_game_buttons():
    mouse_pos = pygame.mouse.get_pos()

    for rect, text_str in [(restart_button, "Restart"), (menu_button, "Menu")]:
        hovered = rect.collidepoint(mouse_pos)
        color = DARK_GREY if hovered else GREY
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=10)  # visible border
        text = button_font.render(text_str, True, BLACK)
        screen.blit(text, (rect.x + rect.width // 2 - text.get_width() // 2,
                           rect.y + rect.height // 2 - text.get_height() // 2))
        
def draw_timer():
    global current_time_left,timer_start_time,game_over

    elapsed_time = pygame.time.get_ticks() - timer_start_time

    current_time_left = TIME_LIMIT - (elapsed_time/1000)

    if current_time_left < 0 and not game_over and not in_menu:

        global winner, current_player
        winner = "O" if current_player == 'X' else "O"
        game_over = True
        current_time_left = 0

    text_color = RED if current_time_left < 3 and current_time_left > 0 else BLACK

    time_str = f"Time: {max(0, current_time_left):.1f}"
    
    timer_text = message_font.render(time_str, True, text_color)
    
    pygame.draw.rect(screen, GREY, timer_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, timer_rect, 3, border_radius=10)
    
    text_x = timer_rect.x + (timer_rect.width - timer_text.get_width()) // 2
    text_y = timer_rect.y + (timer_rect.height - timer_text.get_height()) // 2
    screen.blit(timer_text, (text_x, text_y))


def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] is not None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] is not None:
        return board[0][2]
    return None

def check_tie():
    for row in board:
        if None in row:
            return False
    return True

def reset_game():
    global board, current_player, game_over, winner, ai_turn, timer_start_time
    board = [[None] * 3 for _ in range(3)]
    current_player = "X"
    game_over = False
    winner = None
    ai_turn = False
    timer_start_time = pygame.time.get_ticks()

def find_winning_move(player):
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = player
                if check_winner() == player:
                    board[row][col] = None
                    return row, col
                board[row][col] = None
    return None

def ai_move():
    move = find_winning_move("O")
    if move:
        board[move[0]][move[1]] = "O"
        return
    move = find_winning_move("X")
    if move:
        board[move[0]][move[1]] = "O"
        return
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]
    if empty:
        move = random.choice(empty)
        board[move[0]][move[1]] = "O"

running = True
in_menu = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["1v1"].collidepoint(event.pos):
                    mode = "1v1"
                    in_menu = False
                    reset_game()
                elif buttons["vs_ai"].collidepoint(event.pos):
                    mode = "vs_ai"
                    in_menu = False
                    reset_game()

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    reset_game()
                elif menu_button.collidepoint(event.pos):
                    in_menu = True
                elif not game_over:
                    if mode == "1v1" or (mode == "vs_ai" and current_player == "X"):
                        x, y = pygame.mouse.get_pos()
                        row = y // CELL_SIZE
                        col = x // CELL_SIZE
                        if row < 3 and col < 3 and board[row][col] is None:
                            board[row][col] = current_player
                            winner = check_winner()  # <- FIX HERE
                            if winner:
                                game_over = True
                            elif check_tie():
                                winner = "Tie"
                                game_over = True
                            else:
                                current_player = "O" if current_player == "X" else "X"
                                timer_start_time = pygame.time.get_ticks()
                                if mode == "vs_ai" and current_player == "O" and not game_over:
                                    ai_turn = True
                                    ai_move_time = pygame.time.get_ticks()

    if mode == "vs_ai" and ai_turn and not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - ai_move_time >= AI_DELAY:
            ai_move()
            winner = check_winner()  # <- FIX HERE
            if winner:
                game_over = True
            elif check_tie():
                winner = "Tie"
                game_over = True
            else:
                current_player = "X"
                timer_start_time = pygame.time.get_ticks()
            ai_turn = False

    if in_menu:
        draw_menu()
    else:
        draw_grid()
        draw_marks()
        draw_game_buttons()
        if not game_over and not ai_turn :
            draw_timer()
        if game_over:
            msg = f"{winner} wins!" if winner != "Tie" else "It's a tie!"
            msg_render = game_over_font.render(msg, True, BLACK)
            # Put the message above buttons to avoid overlap
            message_y = CELL_SIZE * 3 - 20  # bottom of grid + 20 px padding
            screen.blit(msg_render, (SCREEN_WIDTH // 2 - msg_render.get_width() // 2, message_y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
