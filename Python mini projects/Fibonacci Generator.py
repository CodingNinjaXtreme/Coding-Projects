def Get_Fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib_sequence = [0, 1]
    for i in range(2, n):
        next_fib = fib_sequence[i - 1] + fib_sequence[i - 2]
        fib_sequence.append(next_fib)

    return fib_sequence
def main():
    try:
        n = int(input("Enter the number of Fibonacci numbers to generate: "))
        if n < 0:
            print("Please enter a non-negative integer.")
            return
        fib_sequence = Get_Fibonacci(n)
        print(f"The first {n} Fibonacci numbers are: {fib_sequence}")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
if __name__ == "__main__":
    main()
# This code generates the first n Fibonacci numbers and handles user input errors.
# It uses a simple iterative approach to build the Fibonacci sequence.
