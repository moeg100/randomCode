import random 


row = 2
col = 2

size = row * col

listNumbers = random.sample(range(1, 20), size // 2)


print(listNumbers)

#getInput1 = int(input("Pick the first value"))
#getInput2 = int(input("Guess the second value"))

print(getInput1)
print(getInput2)


board = []
for i in range(row):
	for j in range(col):
		print("[*]", end="")
		board.append("[*]")
		
	print("\n")
	
print(board)


for i in range(len(board)):
	print(board[i])

