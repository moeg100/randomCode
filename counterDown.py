def prRed(s): print("\033[91m {}\033[00m".format(s), end="\r")
def prGreen(s): print("\033[92m {}\033[00m".format(s), end="\r")
def prYellow(s): print("\033[93m {}\033[00m".format(s), end="\r")
def prLightPurple(s): print("\033[94m {}\033[00m".format(s), end="\r")
def prPurple(s): print("\033[95m {}\033[00m".format(s), end="\r")
def prCyan(s): print("\033[96m {}\033[00m".format(s), end="\r")
def prLightGray(s): print("\033[97m {}\033[00m".format(s), end="\r")
def prBlack(s): print("\033[90m {}\033[00m".format(s), end="\r")



import time
def counterDown(t):
         while t:
             mins, sec = divmod(t, 60)
             timePrint = '{:02d}:{:02d}'.format(mins, sec)
             colorPrint = timePrint
             if mins == 0 and sec <= 10:
             	prYellow(colorPrint)
             	time.sleep(1)
             	t -= 1
             else:
             	prGreen(colorPrint)
             	time.sleep(1)
             	t -= 1
         prRed("00:00")
         time.sleep(2)
         
         
counterDown(15)
