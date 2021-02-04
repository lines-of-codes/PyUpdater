import tkinter as tk
from tkinter import messagebox
from subprocess import Popen
from easygui import enterbox
"""from numba.experimental import jitclass
from numba import njit, int8, boolean, types, typeof, jit
from numba.typed import Dict

params_default = Dict.empty(
    key_type=typeof('str'),
    value_type=typeof('str')
)

sVClassSpec = [
	('currentSetupIndex', int8),
	('NoQuitConfirm', boolean),
	('ConfigDict', types.DictType(typeof('str'), typeof('str')))
]

@jitclass(sVClassSpec)"""
class SetupVariable():
	def __init__(self):
		self.currentSetupIndex = 0
		self.NoQuitConfirm = False
		self.ConfigDict = {
			'fileserver': None,
			'checkver': None,
			'verstring': None,
			'uimode': None,
			'filename': None
		}

	def getIndex(self):
		return self.currentSetupIndex

	def nextIndex(self):
		self.currentSetupIndex += 1

	def previousIndex(self):
		if not self.currentSetupIndex <= 0:
			self.currentSetupIndex -= 1

	def getNoQuitConfirm(self):
		return self.NoQuitConfirm

	def setNoQuitConfirm(self, value):
		self.NoQuitConfirm = value

	def getConfigDict(self):
		return self.ConfigDict

	def setConfigDict(self, key, value):
		self.ConfigDict[key] = value

#@njit
def OpenSettings(setupVar, currentSetupIndex):
	if currentSetupIndex == 1:
		Choice("UI Mode", "UI Mode settings", setupVar, ['console', "Console mode", 'gui', "GUI mode"], 'uimode')
	elif currentSetupIndex == 2:
		Choice("Settings", "Do you want PyUpdater to check for new version?", setupVar, ['true', 'Yes', 'false', 'No'], 'checkver')
	elif currentSetupIndex == 3:
		prc = Popen(['WebUrlInputBox.exe'])
		prc.wait()
		f = open("filedata.txt", "r")
		cont = f.read()
		f.close()
		cont = cont.split()
		setupVar.setConfigDict('fileserver', cont[0])
		setupVar.setConfigDict('filename', cont[1])
	elif currentSetupIndex == 4:
		uinput = enterbox("Please enter webpage URL.")
		if uinput != None or uinput == '':
			if (uinput.startswith("http://") == False):
				if (uinput.startswith("https://") == False):
					messagebox.showerror("Error", "Unknown or unsupported file protocol. Please contact software developer.")
					return
		else:
			messagebox.showerror("Error", "URL Can't be empty")
			return
		setupVar.setConfigDict('verstring', uinput)

#@njit
def Choice(Title, Message, confdct, cl, key):
	# cl : [value1, text1, value2, text2]
	def Apply(IntValue):
		val = None
		if IntValue == 0:
			val = cl[0]
		elif IntValue == 1:
			val = cl[2]
		confdct.setConfigDict(key, val)
		settingsMenu.destroy()
	settingsMenu = tk.Tk()
	settingsMenu.title(Title)
	tk.Label(settingsMenu, text=Message).pack()
	tk.Button(settingsMenu, text=cl[1], command=lambda: Apply (0)).pack(pady=5)
	tk.Button(settingsMenu, text=cl[3], command=lambda: Apply (1)).pack(pady=5)
	settingsMenu.mainloop()
