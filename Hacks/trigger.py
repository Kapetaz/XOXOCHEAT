
from time import sleep
from ctypes import *
from keyboard import is_pressed

from offsets import *

wait = lambda ms: sleep(ms/1000)

class TRIGGER():

	def main(self):

		client = self.handler.modules["CLIENT_PANORAMA.DLL"]

		while(True):

			wait(1)

			if(self.running and is_pressed("shift")):

				pLocalPlayer = self.handler.RPM(client + dwLocalPlayer, c_int)
				localPlayerTeam = self.handler.RPM(pLocalPlayer + m_iTeamNum, c_int)

				inCXID = self.handler.RPM(pLocalPlayer + m_iCrosshairId, c_int)

				if(inCXID == 0): continue

				pEntity = self.handler.RPM(client + dwEntityList + ((inCXID - 1) * 0x10), c_int)
				entityTeam = self.handler.RPM(pEntity + m_iTeamNum, c_int)

				if(entityTeam == 0): continue

				if(entityTeam != localPlayerTeam):
					self.handler.WPM(client + dwForceAttack, 1, c_int)
					wait(5)
					self.handler.WPM(client + dwForceAttack, 0, c_int)



	def __init__(self, handler):

		self.running = True
		self.handler = handler









