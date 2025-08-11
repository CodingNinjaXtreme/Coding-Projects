First_Number = input("Please enter the first number: ")
Second_Number = input("Please enter the second number: ")
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
try:
    First_Number = int(First_Number)
    Second_Number = int(Second_Number)
    if First_Number <= 0 or Second_Number <= 0:
        raise ValueError("Numbers must be positive integers.")
    result = gcd(First_Number, Second_Number)
    print(f"The greatest common divisor of {First_Number} and {Second_Number} is: {result}")
except ValueError as e:
    print(f"Invalid input: {e}. Please enter positive integers only.")
except Exception as e:
    print(f"An unexpected error occurred: {e}. Please try again.")
