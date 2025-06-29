print("You are a hacker and attempting to hack Vihaan's bank account")
print("                                                                   ")
input("                 press enter to continue")
print("                                                                   ")
print("You know he is 13 years old and like cats and likes programming")
print("                                                                   ")

input("                 press enter to continue")

print("Welcome to FortField Security System")

raw = input("Enter the Password ")

password = raw.lower() 

attempt = 0

while password != 'python':
    print("Access denied")  #
    attempt += 1

    if attempt == 1:
        print(" Tip(It has 6 letters)")

    if attempt == 3:
        print(" Tip(Begins with a 'P')")

    if attempt == 5:
        print(" Tip( Relates to programming)")

    if attempt == 7:
        print(" Tip( Ends with a 'n')")

    if attempt == 8:
        break

    raw = input("Enter the Password ")

    password = raw.lower()

if attempt != 8:
    print("Access granted")
    input("press enter to exit")

else:
    print("too many attempts")
    input("press enter to quit")

