fare = 0
p_count = input("How many passengers are travelling? ")
p_count = int(p_count)
for _ in range(0, p_count, +1):
    age = input("Enter your age: ")
    age =     int(age)
    if age < 12 or age >= 60:
        print("Your fare is £0")
    else:
        if age <= 18:
            print("Your fare is £3")
            fare =              fare + 3
        else:
            print("Your fare is £5")
            fare =              fare + 5
    print("")
print( "Total fare for all passengers: £"+str(fare))
