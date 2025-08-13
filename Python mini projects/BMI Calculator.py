def get_BMI(weight, height):

#  Calculate BMI given weight in kg and height in meters.
    if height <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight / (height ** 2)

def get_BMI_category(bmi):

# Return BMI category.

    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def input_height():

# Ask user for height input in meters or feet/inches and convert to meters.

    while True:
        unit = input("Will you enter height in meters or feet? (m/f): ").strip().lower()
        if unit == 'm':
            try:
                height_m = float(input("Enter your height in meters (e.g., 1.75): "))
                if height_m <= 0:
                    print("Height must be positive.")
                    continue
                return height_m
            except ValueError:
                print("Please enter a valid number.")
        elif unit == 'f':
            try:
                feet = int(input("Enter feet: "))
                inches = int(input("Enter inches: "))
                if feet < 0 or inches < 0:
                    print("Feet and inches must be non-negative.")
                    continue
                # Convert feet/inches to meters
                total_inches = feet * 12 + inches
                height_m = total_inches * 0.0254
                return height_m
            except ValueError:
                print("Please enter valid integers for feet and inches.")
        else:
            print("Please type 'm' for meters or 'f' for feet.")

def main():
    try:
        weight = float(input("Enter your weight in kg: "))
        if weight <= 0:
            print("Weight must be positive.")
            return

        height = input_height()
        bmi = get_BMI(weight, height)
        category = get_BMI_category(bmi)

        print(f"\nYour BMI is: {bmi:.2f}")
        print(f"You are classified as: {category}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
