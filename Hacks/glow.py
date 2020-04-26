
import time
import math

from ctypes import *

from offsets import *

wait = lambda ms: time.sleep(ms/1000)



class GLOW():

	def old_main(self):

		client = self.handler.modules["CLIENT_PANORAMA.DLL"]

		while(True):

			if(self.running):

				pGlowObj = self.handler.RPM(client + dwGlowObjectManager, c_int)

				for i in range(0, 32):
					
					pEntBase = self.handler.RPM(client + dwEntityList + i * 0x10, c_int)

					if self.handler.RPM(pEntBase + m_iHealth, c_int) < 1: continue

					index = self.handler.RPM(pEntBase + m_iGlowIndex, c_int)

					#continue

					self.handler.WPM(pGlowObj + index * 0x38 + 0x04, 1.0, c_float)	# R
					self.handler.WPM(pGlowObj + index * 0x38 + 0x08, 0.0, c_float)	# G
					self.handler.WPM(pGlowObj + index * 0x38 + 0x0C, 0.0, c_float)	# B

					self.handler.WPM(pGlowObj + index * 0x38 + 0x10, 0.8, c_float)	# A

					self.handler.WPM(pGlowObj + index * 0x38 + 0x24, 1, c_int)
					self.handler.WPM(pGlowObj + index * 0x38 + 0x25, 0, c_int)


			wait(1)

	def main(self):

		client = self.handler.modules["CLIENT_PANORAMA.DLL"]

		while(True):

			wait(1)

			if(self.running):
				
				pLocalPlayer = self.handler.RPM(client + dwLocalPlayer, c_int)
				pGlowObj = self.handler.RPM(client + dwGlowObjectManager, c_int)
				playerTeamID = self.handler.RPM(pLocalPlayer + m_iTeamNum, c_int)

				#newMaxUsedEntity = self.handler.RPM(client + dwEntityList + 0x24, c_int)
				#if not newMaxUsedEntity == -1:
				#	maxUsedEntity = newMaxUsedEntity

				for i in range(1, 32):

					pEntity = self.handler.RPM(client + dwEntityList + (i * 0x10), c_int)

					if(pEntity == 0): continue

					entHealth = self.handler.RPM(pEntity + m_iHealth, c_int)
					entTeamID = self.handler.RPM(pEntity + m_iTeamNum, c_int)

					if(entHealth > 0 and (not entTeamID == playerTeamID)):

						playerXPos = self.handler.RPM(pLocalPlayer + m_vecOrigin, c_float)
						playerYPos = self.handler.RPM(pLocalPlayer + m_vecOrigin + 0x04, c_float)

						entXPos = self.handler.RPM(pEntity + m_vecOrigin, c_float)
						entYPos = self.handler.RPM(pEntity + m_vecOrigin + 0x04, c_float)

						index = self.handler.RPM(pEntity + m_iGlowIndex, c_int)
						dormant = self.handler.RPM(pEntity + m_bDormant, c_int)
						spotted = self.handler.RPM(pEntity + m_bSpotted, c_int)

						entitySpeed = self.handler.RPM(pEntity + m_vecVelocity, "Vec3")

						distX = playerXPos - entXPos
						distY = playerYPos - entYPos
						cosLawDist = math.sqrt(distX**2 + distY**2)
						
						entitySpeed = (abs(entitySpeed[0]) + abs(entitySpeed[1])) / 2
						entHealth = entHealth / 100

						if(cosLawDist < 1300 and entitySpeed > 100):
							
							self.handler.WPM(pGlowObj + index * 0x38 + 0x04, 1.0 - entHealth, c_float)	# R
							self.handler.WPM(pGlowObj + index * 0x38 + 0x08, entHealth, c_float)	# G
							self.handler.WPM(pGlowObj + index * 0x38 + 0x0C, 0.0, c_float)	# B

							self.handler.WPM(pGlowObj + index * 0x38 + 0x10, 0.8, c_float)	# A

							self.handler.WPM(pGlowObj + index * 0x38 + 0x24, 1, c_int)
							self.handler.WPM(pGlowObj + index * 0x38 + 0x25, 0, c_int)

						elif(dormant > 0 or spotted != 0):

							self.handler.WPM(pGlowObj + index * 0x38 + 0x04, 1.0 - entHealth, c_float)	# R
							self.handler.WPM(pGlowObj + index * 0x38 + 0x08, entHealth, c_float)	# G
							self.handler.WPM(pGlowObj + index * 0x38 + 0x0C, 0.0, c_float)	# B

							self.handler.WPM(pGlowObj + index * 0x38 + 0x10, 0.8, c_float)	# A

							self.handler.WPM(pGlowObj + index * 0x38 + 0x24, 1, c_int)
							self.handler.WPM(pGlowObj + index * 0x38 + 0x25, 0, c_int)


	def __init__(self, handler):
		
		self.handler = handler
		self.running = True

