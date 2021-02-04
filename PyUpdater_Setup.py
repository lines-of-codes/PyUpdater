# Config Maker
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
import setupsettings as settings

TitlePageList = ["Welcome to PyUpdater Setup!", "PyUpdater UI Mode", "PyUpdater Version Checking", "File Information", "Version Checking", "Setup Finished!"]
SInfoMessageList = ["This setup will help you Configuring PyUpdater.\nTo continue, Click the \"Next\" button.\nOr click the \"Cancel\" button to cancel.",
	"PyUpdater has GUI (Graphical User Interface) and CLI (Command Line Interface) mode.\nClick \"Settings\" button to change the setting.",
	"Do you want PyUpdater to check version of the program version before update?\nIf choose No, PyUpdater will skip to download the program.\nNote: If select \"No\" a file called \"PhantomJS.exe\" is not required.",
	"Please set the file information. I recommended If your software contains multiple files, This file should be the setup file. (Click on \"Settings\" button.)",
	"PyUpdater required where to check for what is the lastest version. This is not required,\nIf you don't want to check for version before update. Check \"https://github.com/lines-of-codes/PyUpdater/wiki/Version-Settings\"",
	"Congratulation! You have completed setting up PyUpdater! You can now use it with your software."
]

setupVar = settings.SetupVariable()

def NextMessage():
	setupVar.nextIndex()
	currentSetupIndex = setupVar.getIndex()
	MenuLabelStrVar.set(TitlePageList[currentSetupIndex])
	SetupInfoMessageStrVar.set(SInfoMessageList[currentSetupIndex])
	if currentSetupIndex >= 1:
		SettingsButton["state"] = "normal"
	if currentSetupIndex == (len(TitlePageList) - 1):
		NextButton["state"] = "disabled"
		CancelButtonStrVar.set("Finish")
		setupVar.setNoQuitConfirm(True)
		SettingsButton["state"] = "disabled"

def PreviousMessage():
	setupVar.previousIndex()
	currentSetupIndex = setupVar.getIndex()
	MenuLabelStrVar.set(TitlePageList[currentSetupIndex])
	SetupInfoMessageStrVar.set(SInfoMessageList[currentSetupIndex])
	if currentSetupIndex <= 0:
		SettingsButton["state"] = "disabled"
	if currentSetupIndex < (len(TitlePageList) - 1):
		NextButton["state"] = "normal"
		if not currentSetupIndex <= 0:
			SettingsButton["state"] = "normal"
		CancelButtonStrVar.set("Cancel")
		setupVar.setNoQuitConfirm(False)

def SettingsMenu():
	currentSetupIndex = setupVar.getIndex()
	settings.OpenSettings(setupVar, currentSetupIndex)

def CancelSetup():
	if setupVar.getNoQuitConfirm() == False:
		confirm = messagebox.askquestion("Confirmation", "Do you want to cancel the setup?")
		if confirm == 'yes':
			mw.destroy()
	else:
		mw.destroy()

mw = tk.Tk()
mw.title("PyUpdater - Setup")
mw.geometry("450x150")

MenuLabelStrVar = tk.StringVar()
SetupInfoMessageStrVar = tk.StringVar()
CancelButtonStrVar = tk.StringVar()

tk.Label(mw, textvariable=MenuLabelStrVar).pack()
tk.Message(mw, textvariable=SetupInfoMessageStrVar, width=400).pack()
SettingsButton = tk.Button(mw, text="Settings", command=SettingsMenu)

MenuLabelStrVar.set(TitlePageList[0])
SetupInfoMessageStrVar.set(SInfoMessageList[0])

NextButton = tk.Button(mw, text="Next", command=NextMessage)
BackButton = tk.Button(mw, text='Back', command=PreviousMessage)
CancelButton = tk.Button(mw, textvariable=CancelButtonStrVar, command=CancelSetup)
CancelButtonStrVar.set("Cancel")

SettingsButton.pack()
CancelButton.pack(side=tk.RIGHT, padx=5)
BackButton.pack(side=tk.RIGHT, padx=5)
NextButton.pack(side=tk.RIGHT, padx=5)

SettingsButton["state"] = "disabled"

mw.mainloop()
f = open("updaterConf.conf", "w")
f.write("fileserver=" + setupVar.ConfigDict['fileserver'] + " ")
f.close()
f = open("updaterConf.conf", "a")
f.write("checkver=" + setupVar.ConfigDict['checkver'] + " ")
f.write("verstring=" + setupVar.ConfigDict['verstring'] + " ")
f.write("uimode=" + setupVar.ConfigDict['uimode'] + " ")
f.write("filename=" + setupVar.ConfigDict['filename'])
f.close()