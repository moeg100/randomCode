import time
import os
import pyfiglet
import random

# ANSI color codes
colors = []

for i in range(random.randint(1,10)):
    colorNumber = random.randint(30, 99)
    color = "\033[{}m".format(colorNumber)
    colors.append(color) 


RESET = "\033[0m"

# Ask for text
text = input("Enter text: ")

# Convert input into ASCII art
ascii_text = pyfiglet.figlet_format(text, font="big")

i = 0

try:
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(colors[i % len(colors)] + ascii_text + RESET)

        time.sleep(1)

        i += 1

except KeyboardInterrupt:
    print(RESET)
