import time
import os
import pyfiglet

# ANSI color codes
colors = [
    "\033[91m",  # Red
    "\033[93m",  # Yellow
    "\033[92m",  # Green
    "\033[96m",  # Cyan
    "\033[94m",  # Blue
    "\033[95m",  # Magenta
]

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