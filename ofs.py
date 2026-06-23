import time
import re

# Obfuscated image string using Run-Length Encoding (RLE)
# 'b' represents spaces (blanks) and 's' represents symbols
data = (
    "32b2s1b2s2b1s15b|30b1s1b2s2b1s2b2s11b|29b1s1b4s1b2s1b4s10b|"
    "28b1s2b4s1b2s1b5s8b|27b1s2b14s7b|27b1s1b15s6b|26b2s17s4b|26b21s2b|"
    "12b3s11b22s1b|11b1s2b1s9b24s|10b1s4b1s8b24s|10b1s4b1s7b25s|"
    "10b1s4b2s5b26s|10b1s4b2s5b26s|11b1s4b2s3b27s|11b2s4b2s2b27s|"
    "12b6s3b27s|13b5s3b27s|14b4s4b26s|15b2s6b25s|16b8b24s|17b7b24s|"
    "18b5b25s|19b4b25s|20b2b26s"
)

print("Processing data string...\n")
time.sleep(1.0)

# Unpack the data string row by row
for row in data.split('|'):
    line = ""
    # Identify patterns such as '32b' or '2s'
    tokens = re.findall(r'(\d+)([bs])', row)
    
    for count, char_type in tokens:
        char = " " if char_type == 'b' else "*"
        line += char * int(count)
        
    print(line)
    time.sleep(0.05)  # Animation effect
