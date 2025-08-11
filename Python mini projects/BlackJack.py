import random

def deal_card():
    """Return a random card from the deck."""
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return random.choice(cards)

def card_value(card):
    """Return the numeric value of a card."""
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11  # Initially count Ace as 11
    else:
        return int(card)

def calculate_score(cards):
    """Calculate the total score of the hand, counting Aces as 1 or 11."""
    total = sum(card_value(card) for card in cards)
    # Adjust for Aces if total > 21
    ace_count = cards.count('A')
    while total > 21 and ace_count:
        total -= 10  # Count one Ace as 1 instead of 11
        ace_count -= 1
    return total

def display_hand(name, cards):
    """Display a player's or dealer's cards and score."""
    print(f"{name}'s cards: {', '.join(cards)}. Total: {calculate_score(cards)}")

def player_turn(player_cards):
    while True:
        display_hand("Your", player_cards)
        if calculate_score(player_cards) > 21:
            print("You busted! You lose.")
            return False
        choice = input("Do you want to Hit or Stand? (hit/stand): ").lower()
        if choice == 'hit':
            player_cards.append(deal_card())
        elif choice == 'stand':
            return True
        else:
            print("Invalid input, please type 'hit' or 'stand'.")

def dealer_turn(dealer_cards):
    while calculate_score(dealer_cards) < 17:
        dealer_cards.append(deal_card())
    display_hand("Dealer", dealer_cards)
    if calculate_score(dealer_cards) > 21:
        print("Dealer busted! You win!")
        return False
    return True

def blackjack_game():
    print("Welcome to Blackjack!")

    while True:
        player_cards = [deal_card(), deal_card()]
        dealer_cards = [deal_card(), deal_card()]

        # Show one dealer card
        print(f"Dealer's visible card: {dealer_cards[0]}")

        # Player's turn
        if not player_turn(player_cards):
            pass  # Player busted, game over

        else:
            # Dealer's turn
            print("\nDealer's turn:")
            if not dealer_turn(dealer_cards):
                pass  # Dealer busted, player wins

            else:
                # Compare scores
                player_score = calculate_score(player_cards)
                dealer_score = calculate_score(dealer_cards)
                if player_score > dealer_score:
                    print(f"You win! Your {player_score} beats dealer's {dealer_score}.")
                elif player_score < dealer_score:
                    print(f"You lose! Dealer's {dealer_score} beats your {player_score}.")
                else:
                    print(f"It's a tie at {player_score}!")

        play_again = input("\nPlay again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break
        print("\n" + "-"*30 + "\n")

if __name__ == "__main__":
    blackjack_game()
