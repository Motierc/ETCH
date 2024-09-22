total = 0
num_count = input("How many people have raised money? ")
num_count = int(num_count)
for _ in range(0, num_count, +1):
    num = input("Enter a number: ")
    if num <= 100 and num >= 0:
        total =          total + int(num) 
print(total)
