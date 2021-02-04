import tkinter as tk

# Compile this as a Seperate File

settingsMenu = tk.Tk()
fileserver = tk.StringVar()
filename = tk.StringVar()
def Apply():
	fs = fileserver.get()
	fn = filename.get()
	if fn == '':
		fn = 'setup.exe'
	f = open("filedata.txt", "w")
	f.write(fs)
	f.close()
	f = open("filedata.txt", "a")
	f.write(" " + fn)
	f.close()
	settingsMenu.destroy()
tk.Label(settingsMenu, text="Web File Location").pack()
fsre = tk.Entry(settingsMenu, textvariable=fileserver, validate="focusout", width=100).pack()
tk.Label(settingsMenu, text="File name (Leave blank for setup.exe)").pack()
fnee = tk.Entry(settingsMenu, textvariable=filename, validate="focusout", width=100).pack()
abtn = tk.Button(settingsMenu, text='Apply', command=Apply)
abtn.pack()
settingsMenu.mainloop()