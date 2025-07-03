weight = float(input("Enter your weight: "))
unit = input("Kilograms or Pounds? (K or L): ").upper()  # Convert input to uppercase

if unit == "K":
    weight = weight * 2.205
    unit = "Lbs."
elif unit == "L":
    weight = weight / 2.205
    unit = "Kgs."
else:
    exit()

print(f'Your weight is: {weight:.2f} {unit}')

