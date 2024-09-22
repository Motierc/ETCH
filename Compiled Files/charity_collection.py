total = 0
p_count = input("How many people have raised money? ")
p_count = int(p_count)
for i in range(0, p_count, +1):
    print(
                    "Please enter ammount "+str(i+1)+": "
                , end = "")
    money = input("")
    total =     total+int(money) 
print("A total of £"+str(total)+" was raised")
if total < 2000:
    total =     total*2
else:
    total =     total+2000
print("With the bonus this comes to:")
for _ in range(0, 3, +1):
    print(str(total)+"!!!")
