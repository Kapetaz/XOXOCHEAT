
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