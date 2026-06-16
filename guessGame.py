import random 


row = 3
col = 4

size = row * col

listNumbers = random.sample(range(1, 20), size // 2)


print(listNumbers)

#getInput1 = int(input("Pick the first value"))
#getInput2 = int(input("Guess the second value"))

#print(getInput1)
#print(getInput2)


#board = []

pool = []

for n in listNumbers:
	pool += [n] * 2
print(pool)
	
board = [["[*]" for _ in range(col)] for _ in range(row)]
"""
for i in range(row):
	for j in range(col):
		print("[*]", end="")
		board.append(["[*]"])
		
	print("\n")
"""

for i in range(row):
	for j in range(col):
		print(board[i][j], end=" ")
	print()
		
#print(board)

	

for i in range(row):
	for j in range(col):
		print(board[i][j], end=" ")
	print()
	
	
print("-" * 50)	


for r in range(row):
    for c in range(col):
        board[r][c] = random.choice(listNumbers)



for i in range(row):
	for j in range(col):
		print(f"[{board[i][j]}]", end=" ")
	print()
	

positions = random.sample(range(size), len(pool))

for p, value in zip(positions, pool):
	r = p // col
	c = p % col
	board[r][c] = value

	
print("-" * 50)	


for i in range(row):
	for j in range(col):
		print(f"[{board[i][j]}]", end=" ")
	print()
#for i in range(len(board) - 1):
#	board[random.randint(0, len(board) - 1)] = random.choice(listNumbers)


"""
for 0rows in board:
	for col in rows:	
		print(f"{item:2}", end=" ")	
	print("\n")
"""
