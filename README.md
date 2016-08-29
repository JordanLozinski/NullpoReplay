# ReplayMino: data analysis for improvement playing Tetris
ReplayMino is a data analysis tool for the Nullpomino tetris client. Nullpomino saves a replay of every completed game by default, and ReplayMino lets you take advantage of this valuable data source by graphing different data (speed, finesse, time, and pieces) over long periods of time.
ReplayMino is written in Python 3, utilizing Tk for the GUI and matplotlib for plotting the data.

# Features

* Graph PPS, finesse, time, or pieces over time
* Graph from multilple sources of replays (i.e, from different Nullpomino clients)
* Graphs a best fit line (in orange) for the data

# Pictures

![GUI](https://github.com/JordanLozinski/ReplayMino/demo/GUI.png) ![Graph](https://github.com/JordanLozinski/ReplayMino/demo/graph.png)

# Planned Features:

* Plotting variance of different variables over time (local variance, not variance irrespective of time)
* Plotting kpt/ekpt
* Caching source folders for replays, so they don't have to be inputted everytime the tool is used

# Contact

If you have feedback or a feature request, please just DM me on github. Thank you.
