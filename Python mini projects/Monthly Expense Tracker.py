monthly_income = float(input("Please enter the monthly income: "))
print(f"Monthly Income: {monthly_income}")
expenses = []

while True:
    category = input("Enter expense category: ")
    amount = float(input("Enter amount: "))
    expense = {"category": category, "amount": amount}
    expenses.append(expense)

    more = input("Add another? (yes/no): ").lower()
    if more != "yes":
        break

print(f"Expenses: {expenses}")
