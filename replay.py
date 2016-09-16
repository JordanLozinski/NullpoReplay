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

replays = []
counter = 0
oldCounter = 0

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
		if "goaltype" in gameargs.keys():
			try:
				self.linecount = {0:20,1:40,2:100,3:10}[gameargs["goaltype"]] #Converts the goaltype variable to a useful number (number of lines)
			except Exception:
				print("Invalid goaltype?") #This should never happen. Goaltype is constrained by the client. But a person (or some kind of drive error) could modify a replay.
			self.gametype = self.gamemode + str(self.linecount) + "L" #convert the string to something that be compared to our gui string
			print(self.gametype)
def plot(*args):
	global oldCounter
	global replays
	
	if counter != oldCounter:
		replays = []
		for c in pathlist.get(0, tk.END):
			print(c)
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
				if gamemode in ("LINE RACE", "MARATHON"):
					i = Replay(time, date, gamemode, num_frames, pieces, finesse, pps, filename, kpt, kwargs)
					replays.append(i)
	else:
		print("Detected no filepath change - using cached folders")

	oldCounter = counter

	varswitch = {"PPS" : 1, "Time" : 2, "Finesse" : 3, "Pieces" : 4, "KPT" : 5}[varbox.get()]

	typedreplays = [x for x in replays if x.gametype.lower() == gamemodesbox.get().lower()] #so we only parse the replays of the relevant gamemode :3c

	dates = mdates.date2num([x.datetime for x in typedreplays]) 	
	if varswitch == 1:	
		values = [x.pps for x in typedreplays]
	elif varswitch == 2:
		values = [x.frames/60 for x in typedreplays]
	elif varswitch == 3:
		values = [x.finesse for x in typedreplays]
	elif varswitch == 4:
		values = [x.pieces for x in typedreplays]
	elif varswitch == 5:
		values = [x.kpt for x in typedreplays]
	plt.plot_date(dates, values)

	if maxvar.get(): #plot max
		maxvals = [values[0]]
		maxx = maxvals[0]
		for x in values:
			if x > maxx:
				maxvals.append(x)
				maxx = x
	plt.plot_date(dates, maxvals)

	mb = np.polyfit(dates, values, 10) #returns polynomial coefficients
	poly = np.poly1d(mb)

	maxmb = np.polyfit(dates, maxvals, 10)
	maxpoly = np.poly1d(maxmb)

	xpoints = np.linspace(min(dates),max(dates),100)
	#plt.plot()
	plt.plot(xpoints,poly(xpoints),color="#F09902",linestyle='solid', linewidth=2.0)
	plt.plot(xpoints,maxpoly(xpoints), color="#ff0000", linestyle='solid', linewidth=2.0)
	plt.show()

def fileDialog(*args):
	global counter
	a = filedialog.askdirectory(title="Directory Select")
	print(type(a))
	counter += 1
	pathlist.insert(tk.END, a)

def deletePath(*args):
	global counter
	try:
		pathlist.delete(*pathlist.curselection())
		counter += 1
	except TypeError:
		print("Nothing was selected to delete.")

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
deletebtn = ttk.Button(mainframe, text="X", command=deletePath, width="3").grid(column=2, row=1, sticky=tk.E)

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

pathlist = tk.Listbox(mainframe, width=40, height=5)
pathlist.grid(column=0, row=1, columnspan=3)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5) 	

root.mainloop()
