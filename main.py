# import tkinter as tk
from traceback import print_exc
from numba.typed import List
from numba import njit, vectorize
from selenium import webdriver
import selenium.common.exceptions as selexcept
import warnings as warn
from UpdaterExceptions import *
import threading
# import tqdm

warn.simplefilter('always')

@njit
def getConf():
	try:
		conffile = open("updaterConf.conf", "r")
		confstr = conffile.read()
		return confstr
	except FileNotFoundError:
		warn.warn("Configuration file not found.", ResourceWarning)
		return "fileserver=https://susite.ga/resources/ExampleFile.txt checkver=true verstring=https://susite.ga/api/InvCrtlastVersion uimode=console filename=ExampleFile.txt"

@njit
def extractConf(confstr):
	confstr = confstr.split()

	fileserver = confstr[0]
	fileserver = fileserver.split("=")
	fileserver = fileserver[1]

	checkver = confstr[1]
	checkver = checkver.split("=")
	checkver = checkver[1]

	verstring = confstr[2]
	verstring = verstring.split("=")
	verstring = verstring[1]

	uimode = confstr[3]
	uimode = uimode.split("=")
	uimode = uimode[1]

	filename = confstr[4]
	filename = filename.split("=")
	filename = filename[1]

	returnList = List()
	returnList.extend(fileserver, checkver, verstring, uimode, filename)
	print(returnList)

	del fileserver
	del checkver
	del verstring
	del uimode
	del filename

	return returnList

@njit
def checkURL(url, uimode='gui'):
	if (url.startswith("http://") == False):
		if (url.startswith("https://") == False):
			if (url.startswith("ftp://") == False):
				if (url.startswith("ftps://") == False):
					if(url.startswith("sftp://") == False):
						if uimode == 'gui':
							messagebox.showerror("Error", "Unknown or unsupported file protocol. Please contact software developer.")
						elif uimode == 'console':
							print("Unknown or unsupported file protocol. Please contact software developer.")
						else:
							raise ConfigError("Unknown UI Mode.")
						raise ProtocalError

confstr = getConf()
conflist = extractConf(confstr)
checkURL(fileserver, uimode=conflist[3])

@njit
def chkupdate(conflist):
	if conflist[3] == 'gui':
		from tkinter import messagebox
		import tkinter as tk
		import tkinter.ttk as ttk
		chkUpdateWindows_Exists = False

		@njit
		def NotUpToDate(noinf=False):
			if noinf == False:
				answer = messagebox.askquestion("Update", "Your program is NOT up to date. Do you want to update now?")
				if answer == 'yes':
					if chkUpdateWindows_Exists == True:
						prgUpdateWindow.destroy()
					prgUpdateWindow = tk.Tk()
					prgUpdateWindow.title("Getting an update...")
					tk.Label(prgUpdateWindow, text="Getting an update...").pack()
					prgUpdateBar = ttk.Progressbar(prgUpdateBar, orient=tk.HORIZONTAL, length=100, mode='determinate')
					prgUpdateBar.pack()
					tsleep(3)
					prgUpdateWindow.mainloop()
					prgUpdateBar['value'] = 10

					#Download required file
					req = reget(conflist[0], allow_redirects=True)
					prgUpdateBar['value'] = 30
					open(conflist[4], 'wb').write(req.content)
					prgUpdateBar['value'] = 50
					process = Popen([conflist[4]])
					prgUpdateBar['value'] = 80
					process.wait()
					prgUpdateBar['value'] = 100
					try:
						sys.exit()
					except Exception as e:
						messagebox.showerror("Unexpected Error", "An Unexpected error occurred while exiting this program.\n{e}")
						quit()
			else:
				#Download required file
				req = reget(conflist[0], allow_redirects=True)
				prgUpdateBar['value'] = 30
				open(conflist[4], 'wb').write(req.content)
				prgUpdateBar['value'] = 50
				process = Popen([conflist[4]])
				prgUpdateBar['value'] = 80
				process.wait()
				prgUpdateBar['value'] = 100
				try:
					sys.exit()
				except Exception:
					print_exc()
					quit()

		chkUpdateWindows_Exists = True
		class PrgWindow(threading.Thread):
			def __init__(self):
				self.isDestroyThread = False
				self.isAlreadyCreateWindow = False
				self.root = None
				self.prgUpdateBar = None
				threading.Thread.__init__(self)
				self.start()

			def callback(self):
				self.root.quit()

			def run(self):
				if self.isAlreadyCreateWindow == False:
					self.root = tk.Tk()
					self.root.protocol("WM_DELETE_WINDOW", self.callback)
					self.root.title("Check for Updates")
					tk.Label(self.root, text="Checking for Updates...").pack()
					self.prgUpdateBar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=100, mode='determinate')
					self.prgUpdateBar.pack()
					self.root.mainloop()
					self.isAlreadyCreateWindow = True

			def setPrgBarValueByInput(self, input):
				self.prgUpdateBar['value'] += input

			def destroyWindow(self):
				self.root.destroy()
				self.join()
			
		#End of PrgWindow Class
		prgWindowObj = PrgWindow()

		tsleep(3)

		if conflist[1] == 'true':
			wdriver = webdriver.PhantomJS()
			prgWindowObj.setPrgBarValueByInput(15)
			wdriver.get(conflist[2])
			prgWindowObj.setPrgBarValueByInput(25)
			pageContent = None
			try:
				pageContent = wdriver.find_element_by_id(id_="content")
			except selexcept.NoSuchElementException:
				tsleep(1)
				messagebox.showinfo("Unexpected Error", "Unable to load Version Number properly. Please try again.")
				prgWindowObj.destroyWindow()
				return
			prgWindowObj.setPrgBarValueByInput(35)
			versionNum = pageContent.text
			versionNum = versionNum.split()
			versionNum = versionNum[1].split(",")
			prgWindowObj.setPrgBarValueByInput(45)

			if(int(versionNum[0]) == CURRENT_VERSION[0]):
				prgWindowObj.setPrgBarValueByInput(55)
				if(int(versionNum[1]) == CURRENT_VERSION[1]):
					prgWindowObj.setPrgBarValueByInput(65)
					if(int(versionNum[2]) == CURRENT_VERSION[2]):
						prgWindowObj.setPrgBarValueByInput(75)
						if(int(versionNum[3]) == CURRENT_VERSION[3]):
							prgWindowObj.setPrgBarValueByInput(85)
							messagebox.showinfo("Update", "This program is Up to Date.")
							prgWindowObj.setPrgBarValueByInput(95)
							del wdriver
							tsleep(1)
							prgWindowObj.setPrgBarValueByInput(100)
							messagebox.showinfo("Info", "The program will now restarting. Please wait.")
							try:
								sys.exit()
							except Exception:
								print_exc()
								quit()
							prgWindowObj.destroyWindow()
						else:
							NotUpToDate()
					else:
						NotUpToDate()
				else:
					NotUpToDate()
			else:
				NotUpToDate()
		elif conflist[1] == 'false':
			NotUpToDate(noinf=True)
		else:
			raise ConfigError
	else:
		# Console mode
		@njit
		def NotUpToDate(noinf=False):
			if noinf == False:
				#Download required file
				req = reget(conflist[0], allow_redirects=True)
				prgUpdateBar['value'] = 30
				open(conflist[4], 'wb').write(req.content)
				prgUpdateBar['value'] = 50
				process = Popen([conflist[4]])
				prgUpdateBar['value'] = 80
				process.wait()
				prgUpdateBar['value'] = 100
				try:
					sys.exit()
				except Exception as e:
					messagebox.showerror("Unexpected Error", "An Unexpected error occurred while exiting this program.\n{e}")
					quit()
			else:
				#Download required file
				req = reget(conflist[0], allow_redirects=True) 
				open(conflist[4], 'wb').write(req.content)
				process = Popen([conflist[4]])
				process.wait()
				try:
					sys.exit()
				except Exception:
					print_exc()
					quit()

		if conflist[1] == 'true':
			wdriver = webdriver.PhantomJS()
			wdriver.get(conflist[2])
			pageContent = None
			try:
				pageContent = wdriver.find_element_by_id(id_="content")
			except selexcept.NoSuchElementException:
				tsleep(1)

				return
			versionNum = pageContent.text
			versionNum = versionNum.split()
			versionNum = versionNum[1].split(",")

			if(int(versionNum[0]) == CURRENT_VERSION[0]):
				if(int(versionNum[1]) == CURRENT_VERSION[1]):
					if(int(versionNum[2]) == CURRENT_VERSION[2]):
						if(int(versionNum[3]) == CURRENT_VERSION[3]):
							print("The program is Up to date")
							del wdriver
							tsleep(1)
							prgWindowObj.destroyWindow()
						else:
							NotUpToDate()
					else:
						NotUpToDate()
				else:
					NotUpToDate()
			else:
				NotUpToDate()
		elif conflist[1] == 'false':
			NotUpToDate()
		else:
			raise ConfigError

"""Configuration List: fileserver [0],
checkver [1], verstring [2], uimode [3], filename [4]"""