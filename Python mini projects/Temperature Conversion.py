unit = input("Is the temperature in Celsius or Fahrenheit? (F/C): ")
temp = float(input("Enter the temperature"))

if unit == "C":
    temp = round (( 9 * temp) / 5 + 32, 1)
    print(f'Your temperature in Fahrenheit is: {temp:.2f} °F')
elif unit == "F":
    temp = round (( 9 * temp) / 5 -32, 1)
    print(f'Your temperature in Celsius is: {temp:.2f} °C')
else:
    print(f"{unit} is not a valid input")