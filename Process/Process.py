
import win32api
import psutil
import struct

from ctypes import *

## Structures

class Vector3(Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]

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


## Shorting

Module32First = windll.kernel32.Module32First
Module32First.argtypes = [ c_void_p , POINTER(MODULEENTRY32) ]
Module32First.rettype = c_int

Module32Next = windll.kernel32.Module32Next
Module32Next.argtypes = [ c_void_p , POINTER(MODULEENTRY32) ]
Module32Next.rettype = c_int

Thread32First = windll.kernel32.Thread32First
Thread32First.argtypes = [ c_void_p , POINTER(THREADENTRY32) ]
Thread32First.rettype = c_int

Thread32Next = windll.kernel32.Thread32Next
Thread32Next.argtypes = [ c_void_p , POINTER(THREADENTRY32) ]
Thread32Next.rettype = c_int

SetLastError = windll.kernel32.SetLastError
SetLastError.rettype = c_void_p

GetLastError = windll.kernel32.GetLastError
GetLastError.rettype = c_long

RPM = windll.kernel32.ReadProcessMemory
WPM = windll.kernel32.WriteProcessMemory


## Utils

def getSnapshot(flag, pid):

	FLAGS = {

		"TH32CS_INHERIT"		: 0x80000000,
		"TH32CS_SNAPHEAPLIST"	: 0x00000001,
		"TH32CS_SNAPMODULE"		: 0x00000008,
		"TH32CS_SNAPMODULE32"	: 0x00000010,
		"TH32CS_SNAPPROCESS"	: 0x00000002,
		"TH32CS_SNAPTHREAD"		: 0x00000004,

		"TH32CS_SNAPALL"		: 0x00000001 | 0x00000008 | 0x00000002 | 0x00000004

	}

	if not flag in FLAGS: raise Exception("Error on Process::getSnapshot(): Invalid flag")

	handler = windll.kernel32.CreateToolhelp32Snapshot(FLAGS[flag], pid)

	return handler


typesStr = {
	
	c_int 	: 'i',
	c_float : 'f',
	c_char	: 'c',
	Vector3	: "3f"

}

cvtType = {
	
	"Vec3"	:	Vector3

}


## Main

class Process():

	@staticmethod
	def getPID(targetName):

		if targetName[::-1][0:4] == "exe.": targetName = targetName[0:-4]

		for proc in psutil.process_iter():

			try:	name = proc.name()

			except Exception as error:
				print(f"Error on Process.py::Process::getPID: {error}")
				continue

			if name == f"{targetName}.exe": return proc.pid

		raise Exception("Process not found.")

	def getModuleBase(self):

		snap = getSnapshot("TH32CS_SNAPMODULE", self.pid)

		moduleEntry = MODULEENTRY32()
		moduleEntry.dwSize = sizeof(MODULEENTRY32)

		Module32First( snap, byref(moduleEntry) )

		modules = {}

		while True:

			mName = moduleEntry.szModule.decode("utf-8").upper()
			modules[mName] = moduleEntry.modBaseAddr


			if not Module32Next(snap, byref(moduleEntry)): break


		windll.kernel32.CloseHandle(snap)

		return modules

	def RPM(self, address, type):

		if type in cvtType:	type = cvtType[type]

		buffer = (c_byte * sizeof(type))() # Bytes array
		
		bytesRead = c_ulonglong(0)
		readSize = sizeof(type)
		
		RPM(self.procHandler, address, buffer, readSize, byref(bytesRead))

		bytes = struct.unpack(typesStr[type], buffer)

		if len(bytes) == 1:
			return bytes[0]

		return bytes

	def WPM(self, address, data, type):

		size = sizeof(type)
		count = c_ulong(0)

		buffer = struct.pack(typesStr[type], data)

		WPM(self.procHandler, address, buffer, size, byref(count))


	def __init__(self, procName):
		
		self.name = procName
		self.pid = self.getPID(self.name)
		SetLastError(0)

		# Modules
		self.modules = self.getModuleBase()

		# Game
		self.procHandler = windll.kernel32.OpenProcess(0x1F0FFF, 0, self.pid)


