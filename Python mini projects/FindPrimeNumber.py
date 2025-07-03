snum = input("Enter the Starting number: ")
enum = input("Enter the Last number: ")

num1 = int(snum)
num2 = int(enum)

for i in range(num1, num2 + 1):  # include num2 by adding 1
    if i < 2:  # Ignore numbers less than 2, not primes
        continue
    for j in range(2, i,  1):
        if i % j == 0:
            break
    else:
        print(i)



