import time, random

counter = 0
player1 = 0
player2 = 0


def player1_win():
    print("Greeks win the battle")
    global player1
    player1 += 1


def player2_win():
    print("Indians win the battle")
    global player2
    player2 += 1


while True:
    print("The War between the Greeks and the Indians rages on.You are the new commander of the Indian army; you must "
          "allocate 100 men in the battle to defeat the Greeks." )



    while True:
        Horsemen = input("how many Knights ?")
        try:
            int(Horsemen)
            break
        except:
            print("This is not a number")

    while True:
        War_Elephants = input("how many Farmers ?")
        try:
            int(War_Elephants)
            break
        except:
            print("This is not a number")

    while True:
        Archers = input("how many Defenders ?")
        try:
            int(Archers)
            break
        except:
            print("This is not a number")

    tog = int(War_Elephants) + int(Archers) + int(Horsemen)

    if tog > 100:
        print("You have allocated over 100")
    else:
        print("You have", str(War_Elephants), "War Elephants.You have", str(Archers), "Archers and"
              , str(Horsemen), "Horsemen.")
        break

while True:
    while True:
        counter += 1
        print("The battle rages on and on ..")
        time.sleep(.5)
        print("...")
        time.sleep(.5)
        print("...")
        time.sleep(.5)
        print("...")
        if counter == 3:
            break

    print("A victor has been decided")
    x = random.randint(1, 3)
    time.sleep(x)

    War_Elephants_1 = int(War_Elephants) + random.randint(1, 15)
    Archers_1 = int(Archers) + random.randint(1, 10)
    Horsemen_1 = int(Horsemen) + random.randint(1, 15)

    if War_Elephants_1 >= 35 and Archers_1 >= 15 and Horsemen_1 >= 50:
        player2_win()
    else:
        player1_win()

    print("Greek victory:" + str(player1) + " Indian victory:" + str(player2))
    counter = 0

    if player1 == 5:
        print("""The Greeks has won the war. You have been badly defeated !!""")
        break

    if player2 == 5:
        print("The Indians has won the war, congratulations on your strategic victory!!")
        break

input("Press enter to exit")