#timestamp.time is the time in hours/min/seconds
#timestamp.date is YYYY/MM/DD
#name.mode is the gamemode
#result.time is the number of frames 
#0.statistics.totalPieceLocked is the amount of pieces placed
#0.statistics.pps is global pps
#0.statistics.ppm is global ppm
#0.statistics.finesse is global finesse 
#Future ideas: limiting scope of plot for pieces, plotting ekpt/kpt
#things celer.be plots: ppm, time, kpt, finesse, manipulations (rotations, moves) and pieces
#checking that the gamemode was sprint, labeling axes
import os, datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sys import argv

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

replayFolders = []
replays = []
counter = 0
oldContents = ""

class Replay(object): #essentially used as a struct
	def __init__(self, time, date, num_frames, pieces, finesse, pps, filename):
		self.frames = num_frames
		self.pieces = pieces
		self.finesse = finesse
		self.pps = pps
		self.datetime = datetime.datetime.strptime(date.rstrip("\n")+"/"+"/".join(time.rstrip("\n").split("\:")),'%Y/%m/%d/%H/%M/%S')
		self.filename = filename

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
    
def plot(*args):
	global oldContents
	varb = varbox.get()
	while varb not in (1,2,3,4):
		break
		#send a mean error dialog
	switch = {"PPS" : 1, "Time" : 2, "Finesse" : 3, "Pieces" : 4}[varb]
	if pathtext.get(1.0, tk.END) != oldContents: #if the filepaths have changed since we last populated the replays thing
		replays = []
		for c in replayFolders:
			for replay in os.listdir(c):
				time = ""
				date = ""
				sprint = False
				num_frames = ""
				pieces = ""
				finesse = ""
				timeElapsed = ""
				filename = replay
				replay = open(c+"\\"+replay)
				for line in replay:
					line = line.split("=")
					if line[0] == "timestamp.time":
						time = line[1]
					elif line[0] == "timestamp.date":
						date = line[1]
					elif line[0] == "result.time":
						num_frames = int(line[1])
					elif line[0] == "0.statistics.totalPieceLocked":
						pieces = int(line[1])
					elif line[0] == "0.statistics.finesse":
						finesse = int(line[1])
					elif line[0] == "name.mode" and line[1] == "LINE RACE\n":
						sprint = True
					elif line[0] == "0.statistics.pps":
						pps = float(line[1].strip('\n'))
				if sprint and pieces > 100:
					i = Replay(time, date, num_frames, pieces, finesse, pps, filename)
					replays.append(i)
	else:
		print("Detected no filepath change - using cached replayFolders")

	oldContents = pathtext.get(1.0, tk.END)

	dates = mdates.date2num([x.datetime for x in replays])
	if switch == 1:	
		values = [x.pps for x in replays]
	elif switch == 2:
		values = [x.frames/60 for x in replays]
	elif switch == 3:
		values = [x.finesse for x in replays]
	elif switch == 4:
		values = [x.pieces for x in replays]
	plt.plot_date(dates, values)

	mb = np.polyfit(dates, values, 10) #returns polynomial coefficients
	poly = np.poly1d(mb)

	xpoints = np.linspace(min(dates),max(dates),100)
	plt.plot()
	plt.plot(xpoints,poly(xpoints),color="#F09902",linestyle='solid', linewidth=2.0)
	plt.show()

def fileDialog(*args):
	a = filedialog.askdirectory(title="Directory Select")
	replayFolders.append(a)
	pathtext.insert(tk.END, a+"\n")


root = tk.Tk()
root.title("Replaymino")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

varvar = tk.StringVar()
varvar.set("Variable")

browsebtn = ttk.Button(mainframe, text="Browse", command=fileDialog).grid(column=0, row=0, columnspan=2)
plotbtn = ttk.Button(mainframe, text="Plot", command=plot).grid(column=1, row=2)
varbox = ttk.Combobox(mainframe, textvariable=varvar)
varbox.grid(column=0,row=2)
varbox['values'] = ('PPS', 'Time', 'Finesse', 'Pieces')
pathtext = tk.Text(mainframe, width=20, height=5, wrap="none")
pathtext.grid(column=0, row=1, columnspan=2)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5) 	
root.bind('<Return>', calculate)

root.mainloop()






#plot goals:
#y is pps. x is date every 10 days up to now



