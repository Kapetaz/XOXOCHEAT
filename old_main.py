import pymem
import sys
import time
import keyboard
import math
import win32api
import os
from threading import Thread

from pynput.mouse import Button, Controller
mouse = Controller()


import updateOffsets
updateOffsets.init()
from offsets import *

csHandle = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(csHandle.process_handle, "client_panorama.dll").lpBaseOfDll
engine = pymem.process.module_from_name(csHandle.process_handle, "engine.dll").lpBaseOfDll

'''

Classes

'''

class Entity():

    def getEntBase(index):
        return csHandle.read_int(client + dwEntityList + index * 0x10)

    def getEntHp(entity):
        return csHandle.read_int(entity + m_iHealth)

    def isAlive(entity):

        entHealth = Entity.getEntHp(entity)

        if(entHealth > 0 and entHealth < 101):
            return True

        return False

    def getEntTeam(entity):

        '''
        2 -> Terrorist Team
        3 -> Counter terrorist Team
        '''

        return csHandle.read_int(entity + m_iTeamNum)

    def getGlowIndex(entity):
        return csHandle.read_int(entity + m_iGlowIndex)

    def getGlowObj():
        return csHandle.read_int(client + dwGlowObjectManager)

    def isValid(entity):

        if((Entity.isAlive(entity) and Entity.getEntTeam(entity) != 0) and not csHandle.read_int(entity + m_bDormant)):
            return True

        return False

    def glowEsp(gObj, gIndex, r, g, b, a):

        csHandle.write_float(gObj + (gIndex * 0x38) + 0x4, r)
        csHandle.write_float(gObj + (gIndex * 0x38) + 0x8, g)
        csHandle.write_float(gObj + (gIndex * 0x38) + 0xC, b)
        csHandle.write_float(gObj + (gIndex * 0x38) + 0x10, a)

        csHandle.write_int(gObj + (gIndex * 0x38) + 0x24, 1)
        #csHandle.write_int(gObj + (gIndex * 0x38) + 0x25, 0)

    def getSpoted(entity):
        return csHandle.read_int(entity + m_bSpottedByMask)

    def setSpoted(entity, flag):

        if flag == True:
            flag = 1
        elif flag == False:
            flag = 0

        csHandle.write_int(entity + m_bSpotted, flag)

    def getEntPos(entity):

        #print(hex(entity + m_vecOrigin))

        entX = csHandle.read_float(entity + m_vecOrigin)
        entY = csHandle.read_float(entity + m_vecOrigin + 0x4)
        entZ = csHandle.read_float(entity + m_vecOrigin + 0x8)

        return [entX, entY, entZ]

    def getEntName(entity):
        return csHandle.read_string(entity + m_szCustomName)

    def getEntBoneMatrix(entity):
        return csHandle.read_int(entity + m_dwBoneMatrix)

    def getEntEyePos(entity):

        entX, entY, entZ = Entity.getEntPos(entity)

        viewX = csHandle.read_float(client + m_vecViewOffset)
        viewY = csHandle.read_float(client + m_vecViewOffset + 0x4)
        viewZ = csHandle.read_float(client + m_vecViewOffset + 0x8)

        return [entX + viewX, entY + viewY, entZ + viewZ]

    def getEntScoped(entity):
        return csHandle.read_int(entity + m_bIsScoped)

    def getEntDefusing(entity):
        return csHandle.read_int(entity + m_bIsDefusing)

    def getEntReloading(entity):
        return csHandle.read_int(entity + m_bInReload)

    def getEntHelmet(entity):
        return csHandle.read_int(entity + m_bHasHelmet)

    def getEntDefuser(entity):
        return csHandle.read_int(entity + m_bHasDefuser)

    def getEntImmunity(entity):
        return csHandle.read_int(entity + m_bGunGameImmunity)

    def getActiveWeapon(entity):
        weaponIndex = csHandle.read_int(entity + m_hActiveWeapon) & 0xFFF
        return csHandle.read_int((client + dwEntityList + weaponIndex * 0x10) - 0x10);

    def getEntClassId(entity):

        try:
            one = csHandle.read_int(entity + 0x8)
            two = csHandle.read_int(one + 2 * 0x4)
            three = csHandle.read_int(two + 0x1)
            return csHandle.read_int(three + 0x14)
        except pymem.exception.MemoryReadError:
            pass

    def getEntBonePos(entity, boneId):

        #print(hex(Entity.getEntBoneMatrix(entity) + (boneId * 0x30)))

        xPos = csHandle.read_float(Entity.getEntBoneMatrix(entity) + (boneId * 0x30)  + 0x0C)
        yPos = csHandle.read_float(Entity.getEntBoneMatrix(entity) + (boneId * 0x30)  + 0x1C)
        zPos = csHandle.read_float(Entity.getEntBoneMatrix(entity) + (boneId * 0x30)  + 0x2C)

        return [xPos, yPos, zPos]

    def getEntAmmo(entity):

        weapon = Entity.getActiveWeapon(entity)
        return csHandle.read_int(weapon + m_iClip1)

class LocalPlayer:

    LocalBaseAdress = 0

    def getLocalPlayer():
        return LocalPlayer.LocalBaseAdress

    def setLocalPlayer():
        LocalPlayer.LocalBaseAdress = csHandle.read_int(client + dwLocalPlayer)

    def getLocalFlags():
        return csHandle.read_int(LocalPlayer.getLocalPlayer() + m_fFlags)

    def getLocalHealth():
        return csHandle.read_int(LocalPlayer.getLocalPlayer() + m_iHealth)

    def getLocalTeam():
        return csHandle.read_int(LocalPlayer.getLocalPlayer() + m_iTeamNum)

    def forceJump(waitTime):
        csHandle.write_int(client + dwForceJump, 1)
        wait(waitTime)
        csHandle.write_int(client + dwForceJump, 0)

    def getLocalCrossID():

        entityInCrosshair = csHandle.read_int(LocalPlayer.getLocalPlayer() + m_iCrosshairId) - 1

        if(entityInCrosshair < 1 or entityInCrosshair > 32):
            return None

        return entityInCrosshair

    def getLocalPos():

        #print(hex(LocalPlayer.getLocalPlayer() + m_vecOrigin))

        localX = csHandle.read_float(LocalPlayer.getLocalPlayer() + m_vecOrigin)
        localY = csHandle.read_float(LocalPlayer.getLocalPlayer() + m_vecOrigin + 0x4)
        localZ = csHandle.read_float(LocalPlayer.getLocalPlayer() + m_vecOrigin + 0x8)

        return [localX, localY, localZ]

    def getLocalViewMatrix():

        X = csHandle.read_float(client + dwViewMatrix)
        Y = csHandle.read_float(client + dwViewMatrix + 0x4)

        return [X, Y]

    def getLocalViewAngles():

        clientState = csHandle.read_int(engine + dwClientState)

        X = csHandle.read_float(clientState + dwClientState_ViewAngles)
        Y = csHandle.read_float(clientState + dwClientState_ViewAngles + 0x4)

        return [X, Y]

    def setLocalViewAngles(viewAnglesList):

        X, Y = viewAnglesList

        clientState = csHandle.read_int(engine + dwClientState)

        csHandle.write_float(clientState + dwClientState_ViewAngles, X)
        csHandle.write_float(clientState + dwClientState_ViewAngles + 0x4, Y)

    def getLocalPunchAngles():

        X = csHandle.read_float(LocalPlayer.getLocalPlayer() + m_aimPunchAngle)
        Y = csHandle.read_float(LocalPlayer.getLocalPlayer() + m_aimPunchAngle + 0x4)

        return [X, Y]

    def getShotsFired():
        return csHandle.read_int(LocalPlayer.getLocalPlayer() + m_iShotsFired)

    def shot(shotFlag=None):

        if(shotFlag == None):
            csHandle.write_int(client + dwForceAttack, 1)
            wait(20)
            csHandle.write_int(client + dwForceAttack, 0)

        elif(shotFlag):
            csHandle.write_int(client + dwForceAttack, 1)

        elif(not shotFlag):
            csHandle.write_int(client + dwForceAttack, 0)

'''

Menu

'''

import pygame
pygame.init()
from random import randint

class Utility:

    def drawBorder(surface, borderSize=4, borderColor=(0, 0, 0)):

        width, height = surface.get_rect()[2:]

        pos = 	[
        ((0, 0), (width - borderSize // 2, 0)),
        ((width - borderSize // 2, 0), (width - borderSize // 2, height)),
        ((width - borderSize // 2, height - borderSize // 2), (0, height - borderSize // 2)),
        ((0, height - borderSize // 2), (0, 0))
                ]

        for i in range(4):
            startPos	=	pos[i][0]
            endPos		=	pos[i][1]
            pygame.draw.line(surface, borderColor, startPos, endPos, borderSize)

    def drawAdaptativeText(surface, label):

        tempFont = pygame.font.SysFont("Arial", 15)
        tempFont.set_bold(True)

        TEXT = tempFont.render(label, True, Colors.black)

        tw, th = TEXT.get_rect()[2:]
        sw, sh = surface.get_rect()[2:]

        x = sw // 2 - tw // 2
        y = sh // 2 - th // 2

        surface.blit(TEXT, (x, y))


class Colors:

    def getRandomColor():

        R = randint(0, 255)
        G = randint(0, 255)
        B = randint(0, 255)

        return (R, G, B)



    black	=	(0, 0, 0)
    white 	=	(255, 255, 255)
    red 	=	(255, 0, 0)
    green	=	(0, 255, 0)
    blue	=	(0, 0, 255)

    backgroundPurple = (63, 0, 117)


chrLettersNums = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]

class myButton():

    def setState(self, flag):
        self.active = flag
        activeList[self.index] = flag


    def onClick(self):
        self.active = False if self.active == True else True

        activeList[self.index] = self.active

        self.surface = self.getSurface()

    def checkClick(self, mousePos):

        x, y = mousePos

        if((x > self.x and x < self.x + self.width) and (y > self.y and y < self.y + self.height)):
            self.onClick()

    def draw(self, screen):
        screen.blit(self.surface, self.pos)


    def getSurface(self):

        surface = pygame.Surface(self.size)

        ## Surface color
        if self.active == True:
            color = Colors.green
        else:
            color = Colors.red

        surface.fill(color)


        Utility.drawBorder(surface)
        Utility.drawAdaptativeText(surface, self.label)

        return surface


    def __init__(self, index, pos, buttonSize, label = "?"):

        self.index = index
        self.active = False

        self.pos = self.x, self.y = pos
        self.size = self.width, self.height = buttonSize
        self.label = label

        self.surface = self.getSurface()




class Menu():

    def run(self):

        while(running):

            self.clock.tick(6)

            LocalPlayer.setLocalPlayer()

            self.events()
            self.draw()

            self.setRandomCaption()
            self.setRandomIcon()

    def exit(self):

        global running

        for button in Buttons:
            button.setState(False)

        running = False


    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.exit()

            if event.type == pygame.MOUSEBUTTONUP:

                mousePos = event.pos

                for button in Buttons:
                    button.checkClick(mousePos)



    def draw(self):
        self.screen.fill(Colors.backgroundPurple)


        self.screen.blit(self.title, (self.titleX, self.titleY))


        for button in Buttons:
            button.draw(self.screen)


        pygame.display.update()


    def getFps(self):
        return self.clock.get_fps()


    def setRandomCaption(self):
        if(time.time() - self.lastCaptionChange > self.captionChangeInterval):

            result = ""

            for i in range(randint(10, 30), randint(41, 61)):
                result += chr(chrLettersNums[randint(0, len(chrLettersNums) - 1)])

            pygame.display.set_caption(result)

            self.lastCaptionChange = time.time()

    def setRandomIcon(self):
        if(time.time() - self.lastIconChange > self.iconChangeInterval):


            iconSize = [randint(5, 20), randint(5, 20)]

            iconSurface = pygame.Surface(iconSize).convert()
            iconSurface.fill(Colors.getRandomColor())

            pygame.display.set_icon(iconSurface)

            self.lastIconChange = time.time()



    def __init__(self):

        # Vars
        self.screenSize = self.screenW, self.screenH = [380, 300]

        # Pygame objects
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screenSize)




        titleFont = pygame.font.SysFont("Arial", 30)
        titleFont.set_bold(True)
        titleFont.set_italic(True)
        self.title = titleFont.render("DR3AMCH3AT V2", True, (0, 0, 0))
        titleW, titleH = self.title.get_rect()[2:]
        self.titleX = self.screenW // 2 - titleW // 2
        self.titleY = titleH // 2


        self.lastCaptionChange = 0
        self.captionChangeInterval = 3.0

        self.lastIconChange = 0
        self.iconChangeInterval = 3.0

menu = Menu()




'''

Enums

'''

# Flags
inGround	=	257
inAir 		=	256

# Weapons

## Pistols
uspClassID = 245
r8RevolverClassID = 46
cZClassID = 257
deagleClassID = 46
dualBerettasClassID = 238
fiveSevenClassID = 240
glockClassID = 244
p2000ClassID = 245
p250ClassID = 257
tec9ClassID = 268

pistolsClassIdList = [	uspClassID,
                        r8RevolverClassID,
                        cZClassID,
                        deagleClassID,
                        dualBerettasClassID,
                        fiveSevenClassID,
                        glockClassID,
                        p2000ClassID,
                        p250ClassID,
                        tec9ClassID]


# Bone Id's
headBoneID = 8
neckBoneID = 7
handBoneID = 13




'''

Cheat Modules

'''

def BHOP():
    while(running):

        wait(50)

        while(activeList[BUNNYHOPINDEX]):

            wait(1)

            if(isPressed("space") and LocalPlayer.getLocalFlags() == inGround):
                LocalPlayer.forceJump(10)

def TRIGGERBOT():
    while(running):

        wait(50)

        while(activeList[TRIGGERBOTINDEX]):

            wait(10)

            if(isPressed("shift") and not leftMouseButtonPressed()):

                entityIndex = LocalPlayer.getLocalCrossID()

                if(entityIndex):

                    entity = Entity.getEntBase(entityIndex)

                    if(Entity.isValid(entity) and Entity.getEntTeam(entity) != LocalPlayer.getLocalTeam()):

                        wait(randint(TRIGGERBOTDELAYMIN, TRIGGERBOTDELAYMAX))

                        shotsQueue = [LocalPlayer.shot for i in range(randint(MINSHOTS, MAXSHOTS))]

                        for shot in shotsQueue:

                            if(leftMouseButtonPressed()):
                                break

                            shot()
                            wait(80)


def GLOWESP():
    while(running):

        wait(50)

        while(activeList[GLOWESPINDEX]):
            glow_manager = csHandle.read_int(client + dwGlowObjectManager)

            for i in range(1, 32):  # Entities 1-32 are reserved for players.

                entity = csHandle.read_int(client + dwEntityList + i * 0x10)

                if entity:

                    entity_team_id = csHandle.read_int(entity + m_iTeamNum)

                    entity_glow = csHandle.read_int(entity + m_iGlowIndex)

                    if entity_team_id == 2:  # Terrorist

                        csHandle.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))  # R

                        csHandle.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))  # G

                        csHandle.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))  # B

                        csHandle.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha

                        csHandle.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)  # Enable glow

                    elif entity_team_id == 3:  # Counter-terrorist

                        csHandle.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))  # R

                        csHandle.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))  # G

                        csHandle.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))  # B

                        csHandle.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha

                        csHandle.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)  # Enable glow


def RCS():
    while(running):

        wait(50)

        while(activeList[RCSINDEX]):

            wait(5)

            shotsFired = LocalPlayer.getShotsFired()

            if(shotsFired > 1):

                viewAngles = LocalPlayer.getLocalViewAngles()
                aimPunch = LocalPlayer.getLocalPunchAngles()

                viewAngles = [	viewAngles[0] + oldAimPunch[0],
                                viewAngles[1] + oldAimPunch[1]]

                angle = [	viewAngles[0] - aimPunch[0] * 2.0,
                            viewAngles[1] - aimPunch[1] * 2.0]

                oldAimPunch[0] = aimPunch[0] * 2.0
                oldAimPunch[1] = aimPunch[1] * 2.0

                LocalPlayer.setLocalViewAngles(angle)

            else:
                oldAimPunch = [0, 0]

def AUTOPISTOL():
    while(running):

        wait(50)

        while(activeList[AUTOPISTOLINDEX]):

            wait(10)

            weaponClassID = Entity.getEntClassId(Entity.getActiveWeapon(LocalPlayer.getLocalPlayer()))

            if(weaponClassID in pistolsClassIdList and weaponClassID != cZClassID and weaponClassID != r8RevolverClassID):
                if(leftMouseButtonPressed()):
                    LocalPlayer.shot()
def NOFLASH():
    while(running):

        wait(10)


        while(activeList[NOFLASHINDEX]):

            wait(10)

            player = csHandle.read_int(client + dwLocalPlayer)

            flash_value = player + m_flFlashMaxAlpha

            csHandle.write_float(flash_value, float(0))

            time.sleep(0.002)

'''

Utility functions

'''

wait = lambda ms: time.sleep(ms/1000)

def isPressed(key):
    return keyboard.is_pressed(key)

def newThread(function):
    threadList.append(	Thread(target=function)	)

def startThreads():
    for thread in threadList:
        thread.start()

def HP2RGB(entHealth):

    G = entHealth
    R = (100 - G)

    G = float(G) / 100
    R = float(R) / 100

    return [R, G, 0.0]

def leftMouseButtonPressed():
    return win32api.GetAsyncKeyState(0x01)

def checkConnected():
    try:
        LocalPlayer.setLocalPlayer()
        LocalPlayer.getLocalHealth()
        return True
    except:
        return False



'''

Global vars

'''

running = True
threadList = []
activeList = [False] * 2**5



TRIGGERBOTINDEX = 0
TRIGGERBOTDELAYMIN = 60
TRIGGERBOTDELAYMAX = 98
MINSHOTS = 1
MAXSHOTS = 4

GLOWESPINDEX = 1
RCSINDEX = 2
AUTOPISTOLINDEX = 3
NOFLASHINDEX = 4
BUNNYHOPINDEX = 5


# Menu

buttonPadding = 5
startingX = 0
startingY = 70
buttonSize = buttonWidth, buttonHeight = [120, 50]

posList = [

[(startingX + buttonPadding) + buttonWidth * 0, (startingY + buttonPadding) + buttonHeight * 0],
[(startingX + buttonPadding) + buttonWidth * 0, (startingY + buttonPadding * 2) + buttonHeight * 1],
[(startingX + buttonPadding) + buttonWidth * 0, (startingY + buttonPadding * 3) + buttonHeight * 2],
[(startingX + buttonPadding) + buttonWidth * 0, (startingY + buttonPadding * 4) + buttonHeight * 3],
[(startingX + buttonPadding * 2) + buttonWidth * 1, (startingY + buttonPadding * 4) + buttonHeight * 3],
[(startingX + buttonPadding * 3) + buttonWidth * 2, (startingY + buttonPadding * 4) + buttonHeight * 3],
[(startingX + buttonPadding * 2) + buttonWidth * 1, (startingY + buttonPadding) + buttonHeight * 0]


]


Buttons = [

myButton(TRIGGERBOTINDEX, posList[0], buttonSize, "TRIGGER"),
myButton(GLOWESPINDEX, posList[1], buttonSize, "GLOW"),
myButton(RCSINDEX, posList[2], buttonSize, "RCS"),
myButton(AUTOPISTOLINDEX, posList[3], buttonSize, "AUTOPISTOL"),
myButton(BUNNYHOPINDEX, posList[4], buttonSize, "BUNNYHOP"),
myButton(NOFLASHINDEX, posList[5], buttonSize, "NOFLASH")

]


'''

Main function

'''

def main():

    global running

    while(not checkConnected()):
        wait(500)

        if(isPressed("insert")):
            return

    newThread(BHOP)
    newThread(TRIGGERBOT)
    newThread(GLOWESP)
    newThread(RCS)
    newThread(AUTOPISTOL)
    newThread(NOFLASH)

    startThreads()

    menu.run()

    running = False


main()
