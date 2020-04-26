
# Author: Lusqueta
# Discord: Lusqueta#2808

import time

from threading import Thread
from keyboard import is_pressed

# My modules

import Hacks

from Process import Process



def main():

	handler = Process("csgo.exe")

	hackDict = {

	"BHOP"		:	Hacks.BHOP(handler),
	"GLOW"		:	Hacks.GLOW(handler),
	"TRIGGER"	:	Hacks.TRIGGER(handler),
	"AIMBOT"	:	Hacks.AIMBOT(handler)

	}


	Thread(target = hackDict["BHOP"].main, daemon = True).start()
	Thread(target = hackDict["GLOW"].main, daemon = True).start()
	Thread(target = hackDict["TRIGGER"].main, daemon = True).start()
	Thread(target = hackDict["AIMBOT"].main, daemon = True).start()




if __name__ == "__main__":

	main()

	wait = lambda ms: time.sleep(ms/1000)

	while not is_pressed("insert"):
		wait(1)
