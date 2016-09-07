# ReplayMino: data analysis for improvement playing Tetris
ReplayMino is a data analysis tool for the Nullpomino tetris client. Nullpomino saves a replay of every completed game by default, and ReplayMino lets you take advantage of this valuable data source by graphing different data (speed, finesse, time, and pieces) over long periods of time.
ReplayMino is written in Python 3, utilizing Tk for the GUI and matplotlib for plotting the data.
ReplayMino is currently only meant for use with 40 line sprint replays.

# Features

* Graph PPS, finesse, time, or pieces over time
* Graph from multiple sources of replays (i.e, from different Nullpomino clients)
* Graphs a best fit line (in orange) for the data

# Pictures

![Graph](https://github.com/JordanLozinski/ReplayMino/raw/master/demo/graph.png) ![GUI](https://github.com/JordanLozinski/ReplayMino/raw/master/demo/gui.png)

# Planned Features:

* Plotting variance of different variables over time (local variance, not variance irrespective of time)
* Caching source folders for replays, so they don't have to be inputted everytime the tool is used
* Expanding to allow analysis for different gamemodes, like 100L sprint or Marathon.
* A curve describing the max/min of a given variable

# Contact

If you have feedback or a feature request, please just DM me on github. Thank you.
