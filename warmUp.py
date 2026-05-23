
#L1.1
def tempCtoF():

	getFahrenheit = int(input("Give me the temp in F : "))

	print(getFahrenheit)


	result = (getFahrenheit - 32) * 5/9

	result = round(result, 3)
	print(f"F {result}")




#L1.2
import random

def tip():
	Bill = random.randint(10, 210)
	print(f"Bill is {Bill}")
	tip = int(input("Enter the percentage of the tip : "))
	AmountTip = Bill * (tip / 100)
	totalBill = Bill + AmountTip
	print(f"Total Bill : {totalBill}")
	
	
#L1.3

def oddOrEven():
	number = random.randint(1, 1000)
	if number % 2 == 0:
		print(f"{number} is even")
	else:
		print(f"{number} is odd")
		
		
