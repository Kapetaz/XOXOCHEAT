import ctypes
import os
from ctypes import *
from ctypes.wintypes import *
import psutil
import sys
import win32api
import win32con
from ctypes import wintypes
import time
import struct
from threading import Thread
import random
import math
import numpy
import binascii



clear = lambda: os.system('cls')

off_teamnum = 0xF0
off_flags = 0x100
off_incrosshair = 0xB2B4
off_health = 0xFC
off_glowindex = 0xA320
off_vecorigin = 0x134
off_velocity = 0x110
off_shotsfired = 0xA2C0
off_spotted = 0x00000939
off_dormant = 0x000000E9
off_aimpunch = 0x301C
off_vecviewoffset = 0x104
off_bonematrix = 0x00002698
off_dwviewangle = 0x4D10
off_clientdll = 0

off_localplayer = 0xAAFFEC
off_entitylist = 0x4A8C844
off_forcejump =  0x4F237DC
off_glowobject = 0x4FA9848
off_clientstate = 0x5A3334


off_activeweapon = 0x2EE8
off_itemidlow = 0x2FA4
off_itemidhigh = 0x2FA0
off_fallbackpaintkit = 0x3170
off_fallbackseed = 0x3174
off_fallbackwear = 0x3178
off_itemdefinition = 0x2F88
off_weaponid = 0x000032EC


switch = True
triggeronoff = False
glowonoff = True
bhoponoff = True
cleverglowonoff = False
aimonoff = False
rcsonoff = True
test = True

aimbone = 8
aimfov = 1.5
triggerdelay = 0.0



class THREADENTRY32(Structure):
    _fields_ = [
        ('dwSize' , c_long ),
        ('cntUsage' , c_long),
        ('th32ThreadID' , c_long),
        ('th32OwnerProcessID' , c_long),
        ('tpBasePri' , c_long),
        ('tpDeltaPri' , c_long),
        ('dwFlags' , c_long) ]

class MODULEENTRY32(Structure):
    _fields_ = [ ( 'dwSize' , c_long ) , 
                ( 'th32ModuleID' , c_long ),
                ( 'th32ProcessID' , c_long ),
                ( 'GlblcntUsage' , c_long ),
                ( 'ProccntUsage' , c_long ) ,
                ( 'modBaseAddr' , c_long ) ,
                ( 'modBaseSize' , c_long ) , 
                ( 'hModule' , c_void_p ) ,
                ( 'szModule' , c_char * 256 ),
                ( 'szExePath' , c_char * 260 ) ]

Module32First = windll.kernel32.Module32First
Module32First.argtypes = [ c_void_p , POINTER(MODULEENTRY32) ]
Module32First.rettype = c_int
## Module32Next
Module32Next = windll.kernel32.Module32Next
Module32Next.argtypes = [ c_void_p , POINTER(MODULEENTRY32) ]
Module32Next.rettype = c_int
## Thread32First
Thread32First = windll.kernel32.Thread32First
Thread32First.argtypes = [ c_void_p , POINTER(THREADENTRY32) ]
Thread32First.rettype = c_int
## Thread32Next
Thread32Next = windll.kernel32.Thread32Next
Thread32Next.argtypes = [ c_void_p , POINTER(THREADENTRY32) ]
Thread32Next.rettype = c_int
## GetLastError
GetLastError = windll.kernel32.GetLastError
GetLastError.rettype = c_long




CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
def GetModuleBase(PID,ModuleName):

    hModuleSnap = CreateToolhelp32Snapshot( 0x00000008, PID )

    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)

    Module32First( hModuleSnap, byref(me32))
    
    base = None
    while True:
        if (me32.szModule.lower()==ModuleName.lower()):
            base=me32.modBaseAddr
            break
        if not Module32Next(hModuleSnap, byref(me32)):
            break
    CloseHandle(hModuleSnap)
    return base

taskid = "nothing"
OpenProcess = windll.kernel32.OpenProcess
CloseHandle = windll.kernel32.CloseHandle
PROCESS_ALL_ACCESS = 0x1F0FFF

for proc in psutil.process_iter():

    try:
        name = proc.name()
    except:
        continue

    if name == "csgo.exe":
        taskid = proc.pid
        print("Found csgo, script will start...")
        
if taskid == "nothing":
    input("Please make sure csgo is running, script will exit now...")
    quit()




off_clientdll = GetModuleBase(taskid, "client.dll")
off_enginedll = GetModuleBase(taskid, "engine.dll")

buffer1 = c_char_p(b"")
val1 = c_int()
bufferSize1 = len(buffer1.value)
bytesRead1 = c_ulong(0)

buffer2 = c_char_p(b"")
val2 = c_int()
bufferSize2 = len(buffer2.value)
bytesRead2 = c_ulong(0)




    
game = windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, 0, taskid)
ReadProcessMemory = windll.kernel32.ReadProcessMemory
WriteProcessMemory = windll.kernel32.WriteProcessMemory



def getlenght(type):
    if type == "i":
        return 4
    elif type == "f":
        return 4
    elif type == "c":
        return 1

def float_to_hex(f):
    return struct.pack('f', f)

def read_memory(game, address, type):
    buffer = (ctypes.c_byte * getlenght(type))()
    bytesRead = ctypes.c_ulonglong(0)
    readlenght = getlenght(type)
    ReadProcessMemory(game, address, buffer, readlenght, byref(bytesRead))
    return struct.unpack(type, buffer)[0]

def write_memory(game, address, data, type):
    count = c_ulong(0)
    if type == "f":
        buffer = (float_to_hex(data))

    elif type == "i":
        buffer = struct.pack("i", data)
        
    elif type == "c":
        buffer = chr(data)

    lenght = getlenght(type)
    WriteProcessMemory(game, address, buffer, lenght, byref(count))


def printer():
    clear()
    print("Settings: +++ Aimfov = " + str(aimfov) + " +++ Aimbone: " + str(aimbone) + " +++ Triggerdelay: " + str(triggerdelay) + " +++")
    print("")
    print("")
    print("")
    print("")
    print("                   - Bunnyhop: " + str(bhoponoff))
    print("")
    print("                   - Triggerbot: " + str(triggeronoff))
    print("")
    print("                   - Glow: " + str(glowonoff))
    print("")
    print("                   - Cleverglow: " + str(cleverglowonoff))
    print("")
    print("                   - Recoilsystem: " + str(rcsonoff))
    print("")
    print("                   - Aimbot: " + str(aimonoff))
    print("")




def triggerthread():
    while switch:
        if triggeronoff:
            time.sleep(0.01)
            locaplayer =  read_memory(game,(off_clientdll + off_localplayer), "i")
            myteam = read_memory(game,(locaplayer + off_teamnum), "i")
            incrosshair = read_memory(game,(locaplayer + off_incrosshair), "i")
            if incrosshair != 0:
                incrosshair_entity = read_memory(game,(off_clientdll + off_entitylist + ((incrosshair -1) * 0x10)), "i")
                incrosshair_team = read_memory(game,(incrosshair_entity + off_teamnum), "i")
                #one = read_memory(game,(incrosshair_entity + 0x8), "i")
                #two = read_memory(game,(one + 2 * 0x4), "i")
                #three = read_memory(game,(two + 0x1), "i")
                #classid = read_memory(game,(three + 0x14), "i")


                if myteam != incrosshair_team: #and classid == 35:
                    if triggerdelay > 0:
                        time.sleep(triggerdelay)

                    if win32api.GetAsyncKeyState(0x39) == False:

                        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0)
                        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0)
                


def bhopthread():
    while switch:
        if bhoponoff:
            time.sleep(0.01)
            locaplayer1 =  read_memory(game,(off_clientdll + off_localplayer), "i")
            flags =  read_memory(game,(locaplayer1 + off_flags), "i")
            
            if flags & (1 << 0) and win32api.GetAsyncKeyState(0x12):
                write_memory(game, (off_clientdll + off_forcejump), 6, "i")


def glowthread():
    while switch:
        if glowonoff:
            time.sleep(0.01)
            glowlocalplayer =  read_memory(game,(off_clientdll + off_localplayer), "i")

            glowpointer =  read_memory(game,(off_clientdll + off_glowobject), "i")

            glowteam =  read_memory(game,(glowlocalplayer + off_teamnum), "i")

            for i in range(1, 64):
              
                player =  read_memory(game,(off_clientdll + off_entitylist +  ((i -1) * 0x10)), "i")

                
               
                health =  read_memory(game,(player + off_health), "i")
        
               
                glowteam_enemy =  read_memory(game,(player + off_teamnum), "i")


                inject =  read_memory(game,(player + off_glowindex), "i")
        

                if health > 0 and glowteam != glowteam_enemy:


                    red = ((255 - 2.55 * health) / 255)
                    if red > 1:
                        red = 1.0
                    green = ((2.55*health) / 255)
                    if green > 1.0:
                        green = 1.0
                    
                    write_memory(game, (glowpointer + (inject * 0x38 + 0x4)), red, "f")
                    write_memory(game, (glowpointer + (inject * 0x38 + 0x8)), green, "f")
                    write_memory(game, (glowpointer + (inject * 0x38 + 0xC)), 0.0, "f")
                    write_memory(game, (glowpointer + (inject * 0x38 + 0x10)), 0.8, "f")
                    write_memory(game, (glowpointer + (inject * 0x38 + 0x24)), True, "c")
                    write_memory(game, (glowpointer + (inject * 0x38 + 0x25)), False, "c")
                    write_memory(game, (glowpointer + (inject * 0x38 + 0x26)), False, "c")



def cleverglow():
    while switch:
        if cleverglowonoff:
            time.sleep(0.01)

            cleverglowlocalplayer =  read_memory(game,(off_clientdll + off_localplayer), "i")

            cleverglowpointer =  read_memory(game,(off_clientdll + off_glowobject), "i")

            cleverglowteam =  read_memory(game,(cleverglowlocalplayer + off_teamnum), "i")

            for z in range(1, 64):
              
                cleverglowplayer =  read_memory(game,(off_clientdll + off_entitylist +  ((z -1) * 0x10)), "i")

                

                

                cleverglowhealth =  read_memory(game,(cleverglowplayer + off_health), "i")
                cleverglowteam_enemy =  read_memory(game,(cleverglowplayer + off_teamnum), "i")
                
                

                if cleverglowhealth > 0 and cleverglowteam != cleverglowteam_enemy:

                    localplayerx = read_memory(game,(cleverglowlocalplayer + off_vecorigin), "f")
                    localplayery = read_memory(game,(cleverglowlocalplayer + off_vecorigin + 0x04), "f")
                    

                    
                    enemyx = read_memory(game,(cleverglowplayer + off_vecorigin), "f")
                    enemyy = read_memory(game,(cleverglowplayer + off_vecorigin + 0x04), "f")


                    distx = localplayerx - enemyx
                    disty = localplayery - enemyy

                    finaldist = ((distx * distx) + (disty * disty))
                    finaldist = (math.sqrt(finaldist))
                    cleverglowpointer =  read_memory(game,(off_clientdll + off_glowobject), "i")
                    cleverinject =  read_memory(game,(cleverglowplayer + off_glowindex), "i")
                    dormant =  read_memory(game,(cleverglowplayer + off_dormant), "i")
                    spotted = read_memory(game,(cleverglowplayer + off_spotted), "i")
                    cleverglowspeed = read_memory(game,(cleverglowplayer + off_velocity), "f")

                    if finaldist < 1300 and cleverglowspeed > 130:
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x4)), 1.0, "f")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x8)), 0.0, "f")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0xC)), 1.0, "f")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x10)), 0.7, "f")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x24)), True, "c")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x25)), False, "c")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x26)), False, "c")
                    elif dormant > 0 or spotted != 0:
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x4)), 0.0, "f")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x8)), 1.0, "f")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0xC)), 1.0, "f")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x10)), 0.7, "f")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x24)), True, "c")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x25)), False, "c")
                        write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x26)), False, "c")


                if cleverglowhealth > 0 and cleverglowteam == cleverglowteam_enemy:
                    cleverinject =  read_memory(game,(cleverglowplayer + off_glowindex), "i")
                    write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x4)), 1.0, "f")
                    write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x8)), 1.0, "f")
                    write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0xC)), 1.0, "f")
                    write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x10)), 0.7, "f")
                    write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x24)), True, "c")
                    write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x25)), False, "c")
                    write_memory(game, (cleverglowpointer + (cleverinject * 0x38 + 0x26)), False, "c")


def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX <  -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
 
    return viewAngleX, viewAngleY


def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True


def nanchecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True


def calc_distance(current_x, current_y, new_x, new_y):

    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex

    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey

    return distancex, distancey








def aimthread():
    oldoffpunchx = 0.0
    oldoffpunchy = 0.0
    while switch:
        if test:
            time.sleep(0.01)
            aimlocalplayer = read_memory(game,(off_clientdll + off_localplayer), "i")

            aimteam = read_memory(game,(aimlocalplayer + off_teamnum), "i")
            enginepointer = read_memory(game,(off_enginedll + off_clientstate), "i")
            #print viewanglex
            #print viewangley


            for y in range(1, 64):
              
                aimplayer =  read_memory(game,(off_clientdll + off_entitylist +  ((y -1) * 0x10)), "i")

                

                aimplayerteam = read_memory(game,(aimplayer + off_teamnum), "i")
                aimplayerhealth = read_memory(game,(aimplayer + off_health), "i")             

                if aimplayerteam != aimteam and aimplayerhealth > 0:
                    vecorigin = read_memory(game,(aimlocalplayer + off_vecorigin), "i")
                    localpos1 = read_memory(game,(aimlocalplayer + off_vecorigin), "f") + read_memory(game,(vecorigin + off_vecviewoffset + 0x104), "f")
                    localpos2 = read_memory(game,(aimlocalplayer + off_vecorigin + 0x4), "f") + read_memory(game,(vecorigin + off_vecviewoffset + 0x108), "f")
                    localpos3 = read_memory(game,(aimlocalplayer + off_vecorigin + 0x8), "f") + read_memory(game,(aimlocalplayer + 0x10C), "f")
                    
                    
                    
                    vecorigin = read_memory(game,(aimplayer + off_vecorigin), "i")
                    aimplayerbones = read_memory(game,(aimplayer + off_bonematrix), "i")
                    enemypos1 = read_memory(game,(aimplayerbones + 0x30 * aimbone + 0x0C), "f")
                    enemypos2 = read_memory(game,(aimplayerbones + 0x30 * aimbone + 0x1C), "f")
                    enemypos3 = read_memory(game,(aimplayerbones + 0x30 * aimbone + 0x2C), "f")
                    targetline1 = enemypos1 - localpos1
                    targetline2 = enemypos2 - localpos2
                    targetline3 = enemypos3 - localpos3

                    viewanglex = read_memory(game,(enginepointer + off_dwviewangle), "f")
                    viewangley = read_memory(game,(enginepointer + off_dwviewangle + 0x4), "f")
                    offpunchx = read_memory(game,(aimlocalplayer +  off_aimpunch), "f")
                    offpunchy = read_memory(game,(aimlocalplayer +  off_aimpunch + 0x4), "f")

                    if targetline2 == 0 and targetline1 == 0:
                        yaw = 0
                        if targetline3 > 0:
                            pitch = 270
                        else:
                            pitch = 90
                    else:
                        yaw = (math.atan2(targetline2, targetline1) * 180 / math.pi )  - (offpunchy * 2)
                        if yaw < 0:
                            yaw += 360
                        hypotenuse = math.sqrt((targetline1*targetline1) + (targetline2*targetline2) + (targetline3*targetline3))
                        pitch = (math.atan2(-targetline3, hypotenuse) * 180 / math.pi) - (offpunchx * 2)
                        if pitch < 0:
                            pitch += 360
                    

                    pitch, yaw = normalizeAngles(pitch, yaw)
                    if checkangles(pitch, yaw):


                        distance_x, distance_y = calc_distance(viewanglex, viewangley, pitch, yaw)


                        if (distance_x < aimfov and distance_y < aimfov and win32api.GetAsyncKeyState(0x14)):
 
                            if nanchecker(pitch, yaw):

                                write_memory(game,(enginepointer + off_dwviewangle), pitch, "f")
                                write_memory(game,(enginepointer + (off_dwviewangle + 0x4)), yaw, "f")



                        elif (distance_x < aimfov and distance_y < aimfov and read_memory(game,(aimlocalplayer + off_shotsfired), "i") >= 1 and aimonoff) and aimonoff:

                            if nanchecker(pitch, yaw):

                                write_memory(game,(enginepointer + off_dwviewangle), pitch, "f")
                                write_memory(game,(enginepointer + (off_dwviewangle + 0x4)), yaw, "f")










                                  
                    
def recoilsystem():
    oldpunchx = 0.0
    oldpunchy = 0.0
    while switch:
        time.sleep(0.01)
        if rcsonoff:
            
            rcslocalplayer = read_memory(game,(off_clientdll +off_localplayer), "i")
            rcsengine = read_memory(game,(off_enginedll + off_clientstate), "i")
            if read_memory(game,(rcslocalplayer + off_shotsfired), "i") > 2: 

                rcs_x = read_memory(game,(rcsengine + off_dwviewangle), "f")
                rcs_y = read_memory(game,(rcsengine + off_dwviewangle + 0x4), "f")
                
                punchx = read_memory(game,(rcslocalplayer +  off_aimpunch), "f")
                punchy = read_memory(game,(rcslocalplayer + off_aimpunch + 0x4), "f")
               
                newrcsx = rcs_x - (punchx - oldpunchx) * 2.0
                newrcsy = rcs_y - (punchy - oldpunchy) * 2.0
                newrcs, newrcy = normalizeAngles(newrcsx, newrcsy)




                oldpunchx = punchx
                oldpunchy = punchy



                if nanchecker(newrcsx, newrcsy) and checkangles(newrcsx, newrcsy):

                    write_memory(game,(rcsengine + off_dwviewangle), newrcsx, "f")
                    write_memory(game,(rcsengine + off_dwviewangle + 0x4), newrcsy, "f")

                

            else:
                oldpunchx = 0.0
                oldpunchy = 0.0
                newrcsx = 0.0
                newrcsy = 0.0



def skinchanger():
    while switch:
        time.sleep(0.01)
        if win32api.GetAsyncKeyState(0x2D):
            knifeengine = read_memory(game,(off_enginedll + off_clientstate), "i")
            knifeplayer = read_memory(game, (off_clientdll + off_localplayer), "i")
            current_weapon = read_memory(game, (knifeplayer + off_activeweapon), "i")
            current_weapon &= 0xFFF
            weapon_entity = read_memory(game, (off_clientdll + off_entitylist + (current_weapon -1) * 0x10), "i")
            currentweapon = read_memory(game, (weapon_entity + off_weaponid), "i")
            currentskinid = read_memory(game, (weapon_entity + off_fallbackpaintkit), "i")

            write_memory(game,(weapon_entity + off_itemidhigh), 0, "i")
            write_memory(game,(weapon_entity + off_itemidlow), -1, "i")
            write_memory(game,(weapon_entity + off_fallbackpaintkit), 474, "i")
            write_memory(game,(weapon_entity + off_fallbackwear), 0.000001, "f")


            if currentskinid != read_memory(game, (weapon_entity + off_fallbackpaintkit), "i"):
                write_memory(game,(knifeengine + 0x16C), -1, "i")





Thread(target = triggerthread, daemon = True).start()
Thread(target = bhopthread, daemon = True).start()
Thread(target = glowthread, daemon = True).start()
Thread(target = cleverglow, daemon = True).start()
Thread(target = aimthread, daemon = True).start()
Thread(target = recoilsystem, daemon = True).start()
#thread.start_new_thread(skinchanger, ())





printer()


while switch:
    if win32api.GetAsyncKeyState(0x37):
        time.sleep(0.2)
        if bhoponoff:
            bhoponoff = False
        else:
            bhoponoff = True

        printer()

    elif win32api.GetAsyncKeyState(0x38):
        time.sleep(0.2)
        if triggeronoff:
            triggeronoff = False
        else:
            triggeronoff = True

        printer()

    elif win32api.GetAsyncKeyState(0x39):
        time.sleep(0.2)
        if glowonoff:
            glowonoff = False
        else:
            glowonoff = True
        if cleverglowonoff:
            cleverglowonoff = False

        printer()


    elif win32api.GetAsyncKeyState(0x36):
        time.sleep(0.2)
        if cleverglowonoff:
            cleverglowonoff = False
        else:
            cleverglowonoff = True
        if glowonoff:
            glowonoff = False

        printer()


    elif win32api.GetAsyncKeyState(0x35):
        time.sleep(0.2)
        if rcsonoff:
            rcsonoff = False
        else:
            rcsonoff = True

        printer()


    elif win32api.GetAsyncKeyState(0x28):
        time.sleep(0.2)
        if aimfov > 1.0:
            aimfov -= 0.5
            printer()


    elif win32api.GetAsyncKeyState(0x26):
        time.sleep(0.2)
        aimfov += 0.5
        printer()


    elif win32api.GetAsyncKeyState(0x21):
        time.sleep(0.2)
        if aimbone == 8:
            aimbone = 6
        else:
            aimbone = 8
        printer()


    elif win32api.GetAsyncKeyState(0x22):
        time.sleep(0.2)
        if aimonoff:
            aimonoff = False
        else:
            aimonoff = True

        printer()


    elif win32api.GetAsyncKeyState(0x2E):
    	quit()