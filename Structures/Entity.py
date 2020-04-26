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
