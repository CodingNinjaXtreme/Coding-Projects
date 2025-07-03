import random

def play_guessing_game(min_range, max_range):

  computer_number = random.randint(min_range, max_range)
  attempts = 0

  while True:
    try:
      guess = int(input(f"Guess a number between {min_range} and {max_range}: "))
      attempts += 1
    except ValueError:
      print("Invalid input. Please enter a number.")
      continue

    if guess < computer_number:
      print("Too low!")
    elif guess > computer_number:
      print("Too high!")
    else:
      print(f"Congratulations! You guessed it in {attempts} attempts.")
      break

play_guessing_game(1, 100) 