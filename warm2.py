from bs4 import BeautifulSoup
import requests as rq
from pprint import pprint

#html_doc = rq.get("https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub")
#print(html_doc.text)
html_doc = rq.get("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")
soup = BeautifulSoup(html_doc.text, 'html.parser')


table = soup.find("table")



values = {}

for row in table.find_all("tr")[1:]:
	col = row.find_all("td")
	
	x = col[0].get_text().strip()
	char = col[1].get_text().strip()
	y = col[2].get_text().strip()
	
	#print(f"VALUES : {x}, {char}, {y} ") 
	values[(int(x), int(y))] = char

#print(values)
#print(a.find_all("td")[0].get_text().strip())

max_x = max([x for x, y in values.keys()])
max_y = max([y for x, y in values.keys()])

#print(max_x)
#print(max_y)

grid = []

for y in range(max_y + 1):
	row = []
	
	for x in range(max_x + 1):
		row.append(" ")
	grid.append(row)

#print(grid)


for (x, y), char in values.items():
	grid[y][x] = char
	
	
#print(grid)

for r in range(max_y, -1, -1):
	print("".join(grid[r]))








"""
for value in values:
	if value == (2, 2):
		print(values[value])
matrix = [0, 0, 0, 0
	  0, 0, 0, 0
	  0, 0, 0, 0
	  0, 0, 0, 0]
	  
 ███
  ▀▀
 ▀▀
  ▀	
  
  
Am not sure if this one should be the letter that represents, or if its even a message that am not sure about, but its probably this should be the output if I put it as a matrix.  
  
 grid[y][x]
[['█', ' ', ' ', ' '], 
 ['█', '▀', '▀', ' '], 
 ['█', '▀', '▀', '▀']]
 
 
 
 
[

grid[x][y]
['█', '█', '█'], 
[' ', '▀', '▀'], 
[' ', '▀', '▀'], 
[' ', ' ', '▀']

]




	
"""		

