import tkinter as tk
import random
from english_words import get_english_words_set

# --- Load dictionary and filter 5-letter words ---
# "web2" is a standard word list source in the package
words = get_english_words_set(["web2"])
five_letter_words = {word.upper() for word in words if len(word) == 5}

# Pick a random target word
target = random.choice(list(five_letter_words))
print(f"(For debugging, target word is: {target})")  # Remove in real game

# --- Tkinter setup ---
root = tk.Tk()
root.title("Wordle Clone")

# Create a 5x6 grid for guesses
labels = [[tk.Label(root, text="", width=4, height=2, font=("Helvetica", 24),
                    borderwidth=2, relief="solid") for _ in range(5)] for _ in range(6)]
for i in range(6):
    for j in range(5):
        labels[i][j].grid(row=i, column=j, padx=5, pady=5)

current_row = 0

# --- Function to check guesses ---
def check_guess(event=None):
    global current_row
    guess = entry.get().upper()
    if len(guess) != 5 or guess not in five_letter_words:
        print("Invalid guess")
        entry.delete(0, tk.END)
        return

    for i, letter in enumerate(guess):
        labels[current_row][i]['text'] = letter
        if letter == target[i]:
            labels[current_row][i]['bg'] = "green"
        elif letter in target:
            labels[current_row][i]['bg'] = "yellow"
        else:
            labels[current_row][i]['bg'] = "grey"

    if guess == target:
        print("Congratulations! You guessed the word!")
        entry.config(state="disabled")
    else:
        current_row += 1
        if current_row >= 6:
            print(f"Game over! The word was {target}.")
            entry.config(state="disabled")

    entry.delete(0, tk.END)

# --- Entry box for typing guesses ---
entry = tk.Entry(root, font=("Helvetica", 24))
entry.grid(row=6, column=0, columnspan=5, pady=10)
entry.bind("<Return>", check_guess)

root.mainloop()
