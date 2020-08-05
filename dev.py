
import auxFunctions as aux
import dataFunctions as fun
import plotFunctions as plot
import numpy as np
import matplotlib.pylab as pl
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
###############################################################################
# Plot Data
###############################################################################
# Violin ----------------------------------------------------------------------
(fig, ax) = plot.plotSegmentViolins(runsHistory, runsStats, ylim=(78, 142))
aux.saveFig(fig, '{}plotViolin.{}'.format(OUT, TYP))
# Traces ----------------------------------------------------------------------

###############################################################################
# Dev
###############################################################################
# In --------------------------------------------------------------------------
# fshdRunHistoryCml
# fshdRunsStatsCml
cmap = pl.cm.Purples
center = 'Mean'
yRange = (-1, 1)
# Preprocess ------------------------------------------------------------------
tNames = list(fshdRunHistoryCml.keys())
runsNum = len(fshdRunHistoryCml.get(tNames[0]))
runsIDs = list(fshdRunHistoryCml.get(tNames[0]).keys())
# Setup figure and axes -------------------------------------------------------
fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
colors = cmap(np.linspace(.05, 1, 1+runsNum))
# Calculate traces ------------------------------------------------------------
central = [fshdRunsStatsCml.get(track)[center] for track in tNames]
traces = []
for (i, id) in enumerate(runsIDs):
    padTrace = [0]
    trace = list(fun.getRunFromID(fshdRunHistoryCml, id).values())
    traceDiff = [(i[1] - i[0])/60 for i in zip(central, trace)]
    padTrace.extend(traceDiff)
    traces.append(padTrace)
tracesT = list(map(list, zip(*traces)))
# Plot traces -----------------------------------------------------------------
ax.plot(
        tracesT,
        linewidth=1.5, marker='.', markersize=0,
        color=colors[i], alpha=.5
    )
# Plot violins ----------------------------------------------------------------
bp = ax.violinplot(
        tracesT,
        widths=.75, showmedians=True, showmeans=True, showextrema=False,
        positions=range(0, len(tracesT))
    )
fig
