
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


			

#L3
def reverse_word(word):
	reversed = ""
	for letter in word:
		reversed = letter + reversed
	return reversed


#print(reverse_word("noonracecarcivic"))
	

def is_palindrome(word):
	return word == reverse_word(word)



#print(is_palindrome("noon"))


def check_all_palindrome(words):
	for word in words:
		if is_palindrome(word) == False:
			return False
		else:
			return True

words = ["night", "racecar", "civic"] # return false in check_all_palindrome

words_2 = ["noon", "racecar", "civic"] # return true in check_all_palindrome

#print(check_all_palindrome(words))



def digit_freq_counter(n):
	freq = {}
	while n > 0:
		digit = n % 10
		if digit in freq:
			freq[digit] += 1
		else:
			freq[digit] = 1
		n = n // 10
	return freq
	
#print(digit_freq_counter(29328))



def gcd(a, b):
	if a == 0:
		return b
	if b == 0:
		return a
	return gcd(b, a % b)
	
#print(gcd(24, 4))



def calAgeToDays(age):
	return 365 * age

#print(calAgeToDays(60))

def findPerimeterRect(l, w):
	return 2 * (l + w)

#print(findPerimeterRect(10, 20))

def triangleArea(base, height):
	return (base * height) / 2
	
#print(triangleArea(3, 2))

def to_binary(hexValue):
	result = bin(hexValue)
	result = result.strip("0b")
	if len(result) > 8:
		print("Only in 8 bit")
    	return 0
    
    return result

#print(to_binary(0xFF))


# First Occurrence in String

class Solution:
    def strStr(self, haystack, needle):
        return haystack.find(needle)



a = Solution()
a.strStr("needforspeed", "need")



# Longest Common Prefix

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        common = []
        preFix = ""
        v = 1
        while True:
            for st in strs:
                common.append(st[:v])
            if len(set(common)) <= 1:
                if len(common[0]) == len(strs[0]):
                    return common[0]
                preFix = common[0]
                common = []
                v += 1
            else:
            	return preFix
        return ""






