import random
User_Choice = input("Enter Rock, Paper, or Scissors: ").lower()
Computer_Choice = "rock"  # Placeholder for computer choice
choices = ["rock", "paper", "scissors"]
if User_Choice not in choices:
    print("Invalid choice. Please enter Rock, Paper, or Scissors.")
else:
    Computer_Choice = random.choice(choices)
    print(f"Computer chose: {Computer_Choice}")

    if User_Choice == Computer_Choice:
        print("It's a tie!")
    elif (User_Choice == "rock" and Computer_Choice == "scissors") or \
         (User_Choice == "paper" and Computer_Choice == "rock") or \
         (User_Choice == "scissors" and Computer_Choice == "paper"):
        print("You win!")
    else:
        print("You lose!")
