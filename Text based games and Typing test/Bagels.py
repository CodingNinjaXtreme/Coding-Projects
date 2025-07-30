import random

MAX_DIGITS = 3
MAX_GUESSES = 5


def get_secret_number():
    digits = list('0123456789')
    random.shuffle(digits)
    return ''.join(digits[:MAX_DIGITS])

def get_clues(guess, secret):
    if guess == secret:
        return "You got it!"
    clues = []
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            clues.append("Fermi")
        elif guess[i] in secret:
            clues.append("Pico")
    if not clues:
        return "Bagels"
    clues.sort()
    return ' '.join(clues)

def main():
    guesses = 0
    secret_num = get_secret_number()
    print("Welcome to the Bagels game!")
    print(f"I'm thinking of a {MAX_DIGITS}-digit number with no repeated digits.")
    print("Try to guess what it is. Here are some clues:")
    print("- 'Fermi' means one digit is correct and in the right position.")
    print("- 'Pico' means one digit is correct but in the wrong position.")
    print("- 'Bagels' means no digit is correct.")

    while guesses < MAX_GUESSES:
        guess = input(f"Guess #{guesses + 1}: ")
        if len(guess) != MAX_DIGITS or not guess.isdigit() or len(set(guess)) != MAX_DIGITS:
            print(f"Please enter a {MAX_DIGITS}-digit number with no repeated digits.")
            continue
        guesses += 1

        clues = get_clues(guess, secret_num)
        print(clues)

        if guess == secret_num:
            print(f"Congratulations! You guessed it in {guesses} tries.")
            break
    else:
        print(f"Sorry, you've run out of guesses. The number was {secret_num}.")


if __name__ == "__main__":
    main()