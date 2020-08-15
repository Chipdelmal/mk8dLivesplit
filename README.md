# mk8dLivesplit

This code generates split time distribution, traces and heatmaps plots for Mario Kart 8 Deluxe speedruns saved with [LiveSplit](https://one.livesplit.org/) (**.lss** format).


## Example and Output

To run the script, install the [required dependencies](#dependencies) and call the following command from the terminal:

```bash
python main.py\
    dataFile\
    outputDirectory\
    videoOffset\
```

where:
* *dataFile* is the path to the **lss** file
* *outputDirectory* is path where the output files should be exported
* *videoOffset* is the offset to the beginning of the run (set to 0 if timestamps are not needed)

An example on how to call the script would be:

```bash
python main.py\
    './dta/Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss'\
    ./img/\
    32\
```

### Splits Violins

This plot shows the distributions of each one of the splits. Median is highlighted in a thick rectangle, whilst the mean is shown in a thin line. Splits with widest spread have more variation (meaning they need more practice).

<img src="https://chipdelmal.github.io/blog/uploads/mk_plotViolin.png" style="width:100%;">

### Runs Time Series (traces)

Shows the cumulative times of the finished splits in one plot.
Darker lines are more recent runs (using the standard **cmap** palette provided), and the plot is centered around the mean, showing the deviation from the average time at that point in the run. Median is highlighted in each violin, and the final runtime is also shown (with the sum of best segments shown at the bottom, and sum of worst at the top). Personal best is highlighted in magenta by default.

<img src="https://chipdelmal.github.io/blog/uploads/mk_plotTraces.png" style="width:100%;">

### Splits Heatmap

This heatmap shows the timing for each track (column) split per run (rows). The color of the cell is mapped to its difference to the best split (white is the best split in the standard palette provided, whilst blue is the worst).

<img src="https://chipdelmal.github.io/blog/uploads/mk_plotHeat.png"
 style="width:100%;">

### Categories Heatmap

Same as with splits heatmap, but this one calculates the information for the current categories on the [speedrun.com leaderboards](https://www.speedrun.com/mk8dx).

Warning: This routine assumes it's a 48 track run, and backtracks the categories from a "finished run". Non-48 track runs are omitted (this needs fixing in future versions).

<img src="https://chipdelmal.github.io/blog/uploads/mk_plotCategories.png"
 style="width:100%;">

### Timestamps

Given a video start offset (the point where the first track, "Mario Kart Stadium" begins), it calculates and exports the timestamps for all the other tracks to a **txt** file so that it can be used in Youtube videos.

```
Mario Kart Stadium: 0:30:00
Water Park: 0:02:06
Sweet Sweet Canyon: 0:03:47
Thwomp Ruins: 0:05:43
Mario Circuit: 0:07:35
...
Animal Crossing: 1:22:38
3DS Neo Bowser City: 1:24:28
GBA Ribbon Road: 1:26:31
Super Bell Subway: 1:28:32
Big Blue: 1:30:22
```


### Youtube Summary

This one's just a helper function mostly developed for myself as it exports the title, timings, tags and other things I post in [my MK8D youtube videos](https://www.youtube.com/playlist?list=PLRzY6w7pvIWoMQRecwt-pJD5bU9jwbdRN).

```
[10] MK8D 1:31:29.88 (200cc, 48 tracks, no items, digital)
48 Tracks - 1:31:29.88
32 Tracks - 1:01:35.56
Nitro Tracks - 0:31:30.77
Retro Tracks - 0:30:04.78
Bonus Tracks - 0:29:54.31
https://www.speedrun.com/user/chipdelmal
mk8d, mario kart, speedrun, speed run, gaming, 48, 200cc, no item, switch
```

##  Dependencies

The required dependencies are [numpy](https://numpy.org/), [matplotlib](https://matplotlib.org/) and [xmltodict](https://github.com/martinblech/xmltodict). To install them, run:

```bash
pip install numpy
pip install matplotlib
pip install xmltodict
```

##  Documentation, Extensions and Known Issues



#  Author

For more information, read my [blogpost](https://chipdelmal.github.io/blog/).

<img src="https://raw.githubusercontent.com/Chipdelmal/WaveArt/master/media/pusheen.jpg" height="130px" align="middle"><br>

[Héctor M. Sánchez C.](https://chipdelmal.github.io/blog/)
