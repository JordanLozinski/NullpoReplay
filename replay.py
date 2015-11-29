#timestamp.time is the time in hours/min/seconds
#timestamp.date is YYYY/MM/DD
#name.mode is the gamemode
#result.time is the number of frames 
#0.statistics.totalPieceLocked is the amount of pieces placed
#0.statistics.pps is global pps
#0.statistics.ppm is global ppm
#0.statistics.finesse is global finesse 
import os, datetime
from sys import argv
class Replay(object): #essentially used as a struct
	def __init__(self, time, date, num_frames, pieces, finesse):
		self.hours, self.minutes, self.seconds = time.split("\:")
		self.year, self.month, self.day = date.split("/")
		self.frames = int(num_frames)
		self.pieces = int(pieces)
		self.finesse = int(finesse)
		#self.datetime = datetime.datetime.strptime(date+"/"+"/".join(time.split("\:")),'%Y/%m/%d/%H/%M/%S')


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
			num_frames = line[1]
			if int(line[1]) < 2520 and int(line[1]) > 2460:
				print(filename + " " + line[1])
		elif line[0] == "0.statistics.totalPieceLocked":
			pieces = line[1]
		elif line[0] == "0.statistics.finesse":
			finesse = line[1]
		elif line[0] == "name.mode":
			sprint = True
	if sprint:
		i=Replay(time, date, num_frames, pieces, finesse)
		replays.append(i)
		counter += 1

print(counter)




