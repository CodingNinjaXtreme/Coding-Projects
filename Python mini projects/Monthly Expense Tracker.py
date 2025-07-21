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
total_expenses = sum(expense["amount"] for expense in expenses)

remaining = monthly_income - total_expenses
print(f"\nTotal Expenses: ₹{total_expenses:.2f}")
print(f"Remaining Balance: ₹{remaining:.2f}")

if total_expenses > 0.8 * monthly_income:
    print("⚠️ Warning: You have spent more than 80% of your income!")

print("\nBreakdown:")
category_totals = {}

for expense in expenses:
    category = expense["category"]
    amount = expense["amount"]
    if category in category_totals:
        category_totals[category] += amount
    else:
        category_totals[category] = amount

for category, total in category_totals.items():
    print(f"{category}: ₹{total:.2f}")
