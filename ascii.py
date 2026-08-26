import time
import os
import pyfiglet
import random
from pyfiglet import FigletFont
# ANSI color codes
colors = []

for i in range(random.randint(1,10)):
    colorNumber = random.randint(80, 99)
    color = "\033[{}m".format(colorNumber)
    colors.append(color) 


RESET = "\033[0m"

# Ask for text
text = input("Enter text: ")


fonts = FigletFont.getFonts()

i = 0

try:
    while True:
        ascii_text = pyfiglet.figlet_format(text, font=fonts[i % len(fonts)])
        os.system("cls" if os.name == "nt" else "clear")

        print(colors[i % len(colors)] + ascii_text + RESET)

        time.sleep(1)

        i += 1

except KeyboardInterrupt:
    print(RESET)
