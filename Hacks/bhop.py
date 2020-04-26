
from time import sleep
from ctypes import *
from keyboard import is_pressed

from offsets import *


## Flags
#
#	256 - Air
#	257 - Floor
#	261 - Mid Counch
#	262 - Air Crouched
#	263 - Crouched

wait = lambda ms: sleep(ms/1000)

class BHOP():

	def main(self):

		client = self.handler.modules["CLIENT_PANORAMA.DLL"]
		inFloorFlags = [257, 261, 262, 263]

		while(True):

			localPlayer = self.handler.RPM(client + dwLocalPlayer, c_int)

			if(self.running):
				
				flag = self.handler.RPM(localPlayer + m_fFlags, c_int)

				if (flag > 256 and flag < 264) and is_pressed("space"):
					self.handler.WPM(client + dwForceJump, 1, c_int)
					wait(5)
					self.handler.WPM(client + dwForceJump, 0, c_int)


			wait(1)


	def switch(self):
		self.running = not self.running

	def __init__(self, handler):

		self.running = True
		self.handler = handler









