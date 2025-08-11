def start_adventure():
    print("You awaken in a dark, cold dungeon cell with two doors.")
    choice = input("Do you go through the left door or the right door? (left/right): ").lower()

    if choice == "left":
        treasure_room()
    elif choice == "right":
        dragon_room()
    else:
        print("You hesitate and the cell floods with water. Game over.")

def treasure_room():
    print("\nYou enter a glittering treasure room filled with gold and jewels!")
    print("In the center is a pedestal with a glowing red gem.")
    action = input("Do you take the gem or leave it? (take/leave): ").lower()

    if action == "take":
        print("\nThe gem pulses with energy and the room starts shaking!")
        escape = input("Do you run for the exit or examine the gem? (run/examine): ").lower()

        if escape == "run":
            print("\nYou barely escape before the ceiling collapses. You survive with treasure!")
            secret_staircase()
        elif escape == "examine":
            print("\nThe gem releases a burst of energy and you are turned into stone. Game over.")
        else:
            print("\nParalyzed by indecision, the room collapses. Game over.")

    elif action == "leave":
        print("\nYou wisely leave the gem and find a hidden door behind a tapestry.")
        secret_staircase()
    else:
        print("\nYou hesitate too long and the floor opens beneath you. Game over.")

def secret_staircase():
    print("\nYou find a spiral staircase going down into darkness.")
    choice = input("Do you descend the stairs or go back? (descend/back): ").lower()

    if choice == "descend":
        underground_library()
    elif choice == "back":
        print("\nYou return to the dungeon entrance but a guard spots you.")
        fight_guard()
    else:
        print("\nYou trip on the stairs and break your neck. Game over.")

def underground_library():
    print("\nYou enter an ancient library filled with dusty books and scrolls.")
    print("A mysterious book glows on a pedestal.")
    choice = input("Do you read the book or leave it alone? (read/leave): ").lower()

    if choice == "read":
        print("\nThe book grants you magical knowledge and powers! You win with wisdom!")
    elif choice == "leave":
        print("\nYou leave the library and find a secret exit leading outside.")
        freedom()
    else:
        print("\nA trap triggers and you are trapped forever. Game over.")

def fight_guard():
    print("\nThe guard approaches, sword drawn.")
    action = input("Do you fight or try to talk your way out? (fight/talk): ").lower()

    if action == "fight":
        print("\nYou bravely fight the guard.")
        outcome = input("Do you strike fast or defend carefully? (strike/defend): ").lower()

        if outcome == "strike":
            print("\nYour quick attack surprises the guard and you win the fight!")
            freedom()
        elif outcome == "defend":
            print("\nThe guard overpowers you while you hesitate. Game over.")
        else:
            print("\nYou hesitate and the guard kills you. Game over.")
    elif action == "talk":
        print("\nYou try to convince the guard you mean no harm.")
        trust = input("Do you tell the truth or lie? (truth/lie): ").lower()

        if trust == "truth":
            print("\nThe guard believes you and lets you go. You escape!")
            freedom()
        elif trust == "lie":
            print("\nThe guard sees through your lie and arrests you. Game over.")
        else:
            print("\nYour silence angers the guard. Game over.")
    else:
        print("\nFrozen with fear, the guard attacks you. Game over.")

def freedom():
    print("\nYou step out into the sunlight, free at last!")
    print("Congratulations, you have escaped the dungeon and won the game!")

def dragon_room():
    print("\nYou enter a huge cavern with a sleeping dragon.")
    print("There is a shining sword on the wall and a small door behind the dragon.")
    action = input("Do you grab the sword or sneak through the door? (sword/door): ").lower()

    if action == "sword":
        print("\nYou grab the sword and prepare to fight the dragon!")
        fight = input("Do you attack the dragon or try to run away? (attack/run): ").lower()

        if fight == "attack":
            print("\nThe dragon wakes and breathes fire!")
            dodge = input("Do you dodge or block with the sword? (dodge/block): ").lower()

            if dodge == "dodge":
                print("\nYou dodge the flames and strike the dragon's weak spot. You win!")
            elif dodge == "block":
                print("\nThe fire burns through your sword. You perish. Game over.")
            else:
                print("\nYou hesitate and are burned to ashes. Game over.")
        elif fight == "run":
            print("\nYou try to run but the dragon catches you. Game over.")
        else:
            print("\nFrozen in fear, the dragon incinerates you. Game over.")

    elif action == "door":
        print("\nYou sneak through the door and find a peaceful garden.")
        rest = input("Do you rest in the garden or search for an exit? (rest/search): ").lower()

        if rest == "rest":
            print("\nWhile resting, poisonous plants put you to eternal sleep. Game over.")
        elif rest == "search":
            print("\nYou find a gate leading outside.")
            gate = input("Do you open the gate or turn back? (open/back): ").lower()

            if gate == "open":
                freedom()
            elif gate == "back":
                print("\nYou return to the dragon’s lair, where it wakes up. Game over.")
            else:
                print("\nConfused, you get lost and never escape. Game over.")
        else:
            print("\nYour indecision leads to your doom. Game over.")
    else:
        print("\nYou stand frozen as the dragon wakes. Game over.")

if __name__ == "__main__":
    print("Welcome to the Epic Dungeon Adventure!")
    start_adventure()
    print("\nThanks for playing!")
