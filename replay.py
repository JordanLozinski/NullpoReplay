#timestamp.time is the time in hours/min/seconds
#timestamp.date is YYYY/MM/DD
#name.mode is the gamemode
#result.time is the number of frames 
#0.statistics.totalPieceLocked is the amount of pieces placed
#0.statistics.pps is global pps
#0.statistics.ppm is global ppm
#0.statistics.finesse is global finesse
#0.statistics.kpt is kpt

#Future ideas: limiting scope of plot for pieces
#things celer.be plots: ppm, time, kpt, finesse, manipulations (rotations, moves) and pieces
#checking that the gamemode was sprint
#	name.mode=LINE RACE
#checking that the options are consistent.. e.g 40L vs 100L
#	linerace.goaltype.-1:{0=20,1=40,2=100,3=10}
#labeling axes

#plotting variance:
#	Checkbox that says variance
#	Calculate variance within a certain timeframe (only present and past) 
#	and weigh the results by recentness (maybe linear but perhaps something more complex)
#	use an anonymous function to describe the weight curve

#making this code easier to modify

"""
GUI element features remaining to be implemented
	More gamemodes
	Max/min value plot
	Variance
"""
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
	def __init__(self, time, date, gamemode, num_frames, pieces, finesse, pps, filename, kpt, **gameargs):
		self.frames = num_frames
		self.pieces = pieces
		self.gamemode = gamemode
		self.finesse = finesse
		self.pps = pps
		self.datetime = datetime.datetime.strptime(date.rstrip("\n")+"/"+"/".join(time.rstrip("\n").split("\:")),'%Y/%m/%d/%H/%M/%S')
		self.filename = filename
		self.kpt = kpt
		if "sprinttype" in gameargs.keys():
			self.lines = {0:20,1:40,2:100,3:10}[gameargs["goaltype"]]			
    
def plot(*args):
	global oldContents
	global replays
	varswitch = {"PPS" : 1, "Time" : 2, "Finesse" : 3, "Pieces" : 4, "KPT" : 5}[varbox.get()]
	modeswitch = {"Line Race 40L" : 1, "Line Race 20L" : 1, "Line Race 10L" : 1, "Line Race 100L": 1, "Marathon" : 2}[gamemodesbox.get()]
	if pathtext.get(1.0, tk.END) != oldContents: #if the filepaths have changed since we last populated the replays thing
		replays = []
		for c in replayFolders:
			for replay in os.listdir(c):
				time = ""
				date = ""
				gamemode = ""
				num_frames = ""
				pieces = ""
				finesse = ""
				timeElapsed = ""
				filename = replay
				kpt = -1
				kwargs = {}
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
					elif line[0] == "name.mode" and gamemode == "":
						gamemode = line[1]
					elif line[0] == "0.statistics.pps":
						pps = float(line[1].strip('\n'))
					elif line[0] == "0.statistics.kpt":
						kpt = float(line[1])
					elif line[0] == "linerace.goaltype.-1":
						gamemode = "LINE RACE"
						kwargs["goaltype"] = int(line[1])
					i = Replay(time, date, gamemode, num_frames, pieces, finesse, pps, filename, kpt, kwargs)
					replays.append(i)
	else:
		print("Detected no filepath change - using cached replayFolders")

	oldContents = pathtext.get(1.0, tk.END)

	dates = mdates.date2num([x.datetime for x in replays]) #if x.gamemode == (grab gamemode from gui)
	if varswitch == 1:	
		values = [x.pps for x in replays]
	elif varswitch == 2:
		values = [x.frames/60 for x in replays]
	elif varswitch == 3:
		values = [x.finesse for x in replays]
	elif varswitch == 4:
		values = [x.pieces for x in replays]
	elif varswitch == 5:
		values = [x.kpt for x in replays]
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

gamevar = tk.StringVar()
gamevar.set("Gamemode")

browsebtn = ttk.Button(mainframe, text="Browse", command=fileDialog).grid(column=0, row=0, columnspan=3)
plotbtn = ttk.Button(mainframe, text="Plot", command=plot).grid(column=1, row=2)

varbox = ttk.Combobox(mainframe, textvariable=varvar, width=12)
varbox.grid(column=0,row=2)
varbox['values'] = ('PPS', 'Time', 'Finesse', 'Pieces', 'KPT')

gamemodesbox = ttk.Combobox(mainframe, textvariable=gamevar, width=12)
gamemodesbox.grid(column=0, row=3)
gamemodesbox['values'] = ('Line Race 40L', 'Line Race 20L', 'Line Race 100L', 'Line Race 10L', 'Marathon')

maxvar = tk.BooleanVar()
maxbutton = ttk.Checkbutton(mainframe, text='Plot max value', variable=maxvar)
maxbutton.grid(column=1, row=3)

minvar = tk.BooleanVar()
minbutton = ttk.Checkbutton(mainframe, text='Plot min value', variable=minvar, width=13)
minbutton.grid(column=2, row=3)

variancevar = tk.BooleanVar()
variancebutton = ttk.Checkbutton(mainframe, text='Plot variance', variable=variancevar, width=13)
variancebutton.grid(column=2, row=2)

pathtext = tk.Text(mainframe, width=40, height=5, wrap="none")
pathtext.grid(column=0, row=1, columnspan=3)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5) 	

root.mainloop()






#plot goals:
#y is pps. x is date every 10 days up to now
