
import numpy as np
import plotViolin as pv
import plotTraces as pt
import auxFunctions as aux
import dataFunctions as fun
import matplotlib.pyplot as plt

(PATH, OUT, FILE) = (
        './dta/', '/home/chipdelmal/MEGAsync/MK8D/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss'

    )
(DPI, PAD, TYP) = (250, .1, 'png')
###############################################################################
# Read File
###############################################################################
seg = fun.getSegmentsFromFile(PATH+FILE)
###############################################################################
# Shape Runs Data
###############################################################################
# Runs history and stats ------------------------------------------------------
runsHistory = fun.getRunsDict(seg)
runsStats = fun.getRunsStats(runsHistory)
# Filter to finished runs -----------------------------------------------------
fshdRunID = fun.getFinishedRunsId(seg)
fshdRunHistory = fun.filterRunsDict(runsHistory, fshdRunID)
fshdRunsStats = fun.getRunsStats(fshdRunHistory)
# Cumulative history ----------------------------------------------------------
fshdRunHistoryCml = fun.calcRunsCumulative(fshdRunHistory)
fshdRunsStatsCml = fun.getRunsStats(fshdRunHistoryCml)
# Filter runs -----------------------------------------------------------------
trace = fun.getRunFromID(fshdRunHistoryCml, 66)
minTimes = fun.getRunFromOp(runsHistory, op=min)
###############################################################################
# Plot Data
###############################################################################
# Violin ----------------------------------------------------------------------
(fig, ax) = pv.plotSegmentViolins(runsHistory, runsStats, ylim=(78, 142))
aux.saveFig(fig, '{}plotViolin.{}'.format(OUT, TYP))
plt.close(fig)
# Traces ----------------------------------------------------------------------
(fig, ax) = pt.plotSegmentTraces(
        runsHistory, fshdRunHistoryCml, fshdRunsStatsCml, ylim=(-.65, .65)
    )
aux.saveFig(fig, '{}plotTraces.{}'.format(OUT, TYP))
plt.close(fig)



import matplotlib.pylab as pl
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
# Heatmap ---------------------------------------------------------------------
cmap = pl.cm.Purples
tNames = list(fshdRunHistoryCml.keys())
runsNum = len(fshdRunHistoryCml.get(tNames[0]))

track = []
for trackName in tNames:
    track.append(list(fshdRunHistory[trackName].values()))
timesArrays = np.array(track)

nTimesArrays = np.empty(timesArrays.shape)
for (i, row) in enumerate(timesArrays):
    nTimesArrays[i] = NormalizeData(row)

fig, ax = plt.subplots()
im = ax.imshow(nTimesArrays.T, cmap=cmap)

# We want to show all ticks...
ax.set_yticks(np.arange(runsNum))
ax.set_xticks(np.arange(len(tNames)))
# ... and label them with the respective list entries
ax.set_yticklabels(range(runsNum), fontsize=5)
ax.set_xticklabels(tNames, fontsize=7)

# Rotate the tick labels and set their alignment.
plt.setp(
        ax.get_xticklabels(), rotation_mode="anchor",
        rotation=90, ha="right", va="center"
    )
for i in range(len(tNames)):
    plt.axvline(i+.5, color='k', linestyle='solid', lw=.5)
# Loop over data dimensions and create text annotations.
for i in np.arange(len(tNames)):
    for j in np.arange(runsNum):
        text = ax.text(
                i, j, round(timesArrays[i, j], 2),
                ha="center", va="center", color="k",
                fontsize=2
            )

ax.set_title("Tracks Timing")
fig.tight_layout()
aux.saveFig(fig, '{}plotHeat.{}'.format(OUT, TYP), dpi=500)
