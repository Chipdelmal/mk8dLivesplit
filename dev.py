
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
ylim = (-.6, .6)
vStyle = {
        'color': '#888888', 'alpha': .05, 'width': .65,
        'lw': 3, 'lc': (0, 0, 0)
    }
bgStyle = {
        'bandSize': 4,
        'bandColorA': 'blue', 'bandAlphaA': 0.025,
        'bandColorB': 'white', 'bandAlphaB': 0.025,
        'gridColor': (.3, .3, .3), 'gridAlpha': .05,
        'xtickSize': 22.5, 'ytickSize': 22.5, 'labelsSize': 75
    }
meanStyle = {'color': (.3, .3, .3), 'alpha': .65, 'width': .8}
medianStyle = {'color': (.3, .3, .3), 'alpha': .85, 'width': 3}
# Preprocess ------------------------------------------------------------------
tNames = list(fshdRunHistoryCml.keys())
tNum = len(tNames)
runsNum = len(fshdRunHistoryCml.get(tNames[0]))
runsIDs = list(fshdRunHistoryCml.get(tNames[0]).keys())
lastKey = list(fshdRunHistoryCml.keys())[-1]
# Calculate traces ------------------------------------------------------------
central = [fshdRunsStatsCml.get(track)[center] for track in tNames]
traces = []
for (i, id) in enumerate(runsIDs):
    trace = list(fun.getRunFromID(fshdRunHistoryCml, id).values())
    traceDiff = [(i[1] - i[0])/60 for i in zip(central, trace)]
    traceDiff = aux.prependValue(traceDiff)
    traces.append(traceDiff)
tracesT = list(map(list, zip(*traces)))
# Min and max traces ----------------------------------------------------------
minRID = fun.getRunIDWithTime(fshdRunHistoryCml, lastKey, op=min)
minRun = fun.getRunFromID(fshdRunHistoryCml, minRID)
minTrace = [(i[1] - i[0])/60 for i in zip(central, list(minRun.values()))]
minTrace = aux.prependValue(minTrace)
maxRID = fun.getRunIDWithTime(fshdRunHistoryCml, lastKey, op=max)
maxRun = fun.getRunFromID(fshdRunHistoryCml, maxRID)
maxTrace = [(i[1] - i[0])/60 for i in zip(central, list(maxRun.values()))]
# Setup figure and axes -------------------------------------------------------
fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
colors = cmap(np.linspace(.05, 1, 1+runsNum))
# Plot traces -----------------------------------------------------------------
for (i, trace) in enumerate(traces):
    ax.plot(
            trace,
            linewidth=2.5, marker='.', markersize=0,
            color=colors[i], alpha=.5
        )
ax.plot(
        minTrace,
        linewidth=2.5, marker='.', markersize=0,
        color='#e239e6', alpha=.5
    )
# Plot violins ----------------------------------------------------------------
bp = ax.violinplot(
        tracesT,
        widths=vStyle['width'],
        showmedians=True, showmeans=True, showextrema=False,
        positions=range(0, len(tracesT))
    )
for (i, vElement) in enumerate(bp['bodies']):
    vElement.set_facecolor(vStyle['color'])
    vElement.set_alpha(vStyle['alpha'])
    vElement.set_edgecolor(vStyle['lc'])
    vElement.set_linewidth(vStyle['lw'])
# Medians and Means style -------------------------------------------------
vp = bp['cmedians']
vp.set_edgecolor(medianStyle['color'])
vp.set_linewidth(medianStyle['width'])
vp.set_alpha(medianStyle['alpha'])
vp = bp['cmeans']
vp.set_edgecolor(meanStyle['color'])
vp.set_linewidth(meanStyle['width'])
vp.set_alpha(meanStyle['alpha'])
# Grids -------------------------------------------------------------------
ax.grid(which='both')
major_ticks = range(1, tNum+1, 1)
ax.set_xticks(major_ticks)
ax.grid(
        which='major', zorder=0,
        color=bgStyle['gridColor'], alpha=bgStyle['gridAlpha']
    )
delta = bgStyle['bandSize']
for i in range(0, tNum, delta):
    if i % (2 * delta) == 0:
        (clr, alp) = (bgStyle['bandColorA'], bgStyle['bandAlphaA'])
    else:
        (clr, alp) = (bgStyle['bandColorB'], bgStyle['bandAlphaB'])
    ax.axvspan(i+0.5, i+delta+0.5, zorder=0, color=clr, alpha=alp)
# Labels ------------------------------------------------------------------
plt.xticks(fontsize=bgStyle['xtickSize'])
plt.yticks(fontsize=bgStyle['ytickSize'], rotation=0)
ax.set_xticklabels(tNames, rotation=90)
plt.ylabel('Duration (seconds)', fontsize=bgStyle['labelsSize'] * .75)
plt.title('Split Time Distributions', fontsize=bgStyle['labelsSize'])
# Ranges ------------------------------------------------------------------
ax.set_ylim(ylim[0], ylim[1])
ax.set_xlim(0, tNum+4)
# Save --------------------------------------------------------------------
aux.saveFig(fig, '{}plotTraces.{}'.format(OUT, TYP))
