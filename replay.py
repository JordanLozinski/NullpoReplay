#timestamp.time is the time in hours/min/seconds
#timestamp.date is YYYY/MM/DD
#name.mode is the gamemode
#result.time is the number of frames 
#0.statistics.totalPieceLocked is the amount of pieces placed
#0.statistics.pps is global pps
#0.statistics.ppm is global ppm
#0.statistics.finesse is global finesse 
import os, datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sys import argv

class Replay(object): #essentially used as a struct
	def __init__(self, time, date, num_frames, pieces, finesse, pps, filename):
		self.frames = num_frames
		self.pieces = pieces
		self.finesse = finesse
		self.pps = pps
		self.datetime = datetime.datetime.strptime(date.rstrip("\n")+"/"+"/".join(time.rstrip("\n").split("\:")),'%Y/%m/%d/%H/%M/%S')
		self.filename = filename

replays = []
counter = 0

for replay in os.listdir(argv[1]):
	time = ""
	date = ""
	sprint = False
	num_frames = ""
	pieces = ""
	finesse = ""
	timeElapsed = ""
	filename = replay
	replay = open(argv[1]+"\\"+replay)
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
print(len(replays))

dates = mdates.date2num([x.datetime for x in replays])
values = [x.frames/60 for x in replays]
plt.plot_date(dates, values)

print(np.polyfit(dates, values, 3))
plt.plot(m, b)
plt.show()

#plot goals:
#y is pps. x is date every 10 days up to now



