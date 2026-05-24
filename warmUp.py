
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
		
		

#L2.1
def FizzBuzz():
	for i in range(1, 100):
		if i % 3 == 0 and i % 5 == 0:
			print(i, "FizzBuzz")
		elif i % 5 == 0:
			print(i, "Buzz")
		elif i % 3 == 0:
			print(i, "Fizz")
			


#L2.2
def guessNumber():
	number = random.randint(1, 100)
	guessBool = True
	while guessBool:
		guess = int(input("Guess the number : "))
		if guess == number:
			print(f"You got it, number is {number}")
			guessBool = False
		elif guess > number:
			print("Too High")
		elif guess < number:
			print("Too Low")
			

#L2.3

def wordCountDict():
	a = "apple orange blueberry apple apple grape apple orange"
	listWords = a.split()
	wordDict = {}
	for word in listWords:
		if word in wordDict:
			wordDict[word] += 1
		else:
			wordDict[word] = 1
	print(wordDict)


			
