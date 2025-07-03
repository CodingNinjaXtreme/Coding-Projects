principal = 0
rate = 0
time = 0

while principal <= 0:
    principal = float(input("Enter the principal: "))
    if principal <= 0:
        print("Principal cannot be less than or equal to 0.")

while rate <= 0:
    rate = float(input("Enter the interest rate: "))
    if rate <= 0:
        print("Rate cannot be less than or equal to 0.")

while time <= 0:
    time = int(input("Enter the time in years: "))
    if time <= 0:
        print("Time cannot be less than or equal to 0.")

total = principal * pow(1 + rate / 100, time)
print(f"Total amount after {time} years is {total:.2f}")
