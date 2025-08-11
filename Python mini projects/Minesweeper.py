import random

grid = []
player_grid = []

# Initialize grids
for _ in range(5):
    grid.append(['-' for _ in range(5)])
    player_grid.append(['-' for _ in range(5)])

def place_mines(num_mines):
    count = 0
    while count < num_mines:
        row = random.randint(0, 4)
        col = random.randint(0, 4)
        if grid[row][col] == '-':
            grid[row][col] = 'M'
            count += 1

def count_adjacent_mines():
    for row in range(5):
        for col in range(5):
            if grid[row][col] == 'M':
                continue
            count = 0
            for r in range(max(0, row - 1), min(5, row + 2)):
                for c in range(max(0, col - 1), min(5, col + 2)):
                    if grid[r][c] == 'M':
                        count += 1
            grid[row][col] = str(count)

def display_player_grid():
    print("Current Minesweeper Grid:")
    for row in player_grid:
        print(" ".join(row))
    print()

def play_minesweeper():
    num_mines = 5
    place_mines(num_mines)
    count_adjacent_mines()

    while True:
        display_player_grid()
        try:
            row = int(input("Enter row (0-4): "))
            col = int(input("Enter column (0-4): "))

            if player_grid[row][col] != '-':
                print("Cell already revealed. Try again.")
                continue

            if grid[row][col] == 'M':
                print("Game Over! You hit a mine.")
                break
            else:
                player_grid[row][col] = grid[row][col]
                print(f"You revealed cell ({row}, {col}) with {grid[row][col]} adjacent mines.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers between 0 and 4.")

play_minesweeper()
