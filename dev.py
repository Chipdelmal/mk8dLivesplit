
import dataFunctions as fun
import matplotlib.pylab as pl
import matplotlib.pyplot as plt

(PATH, OUT, FILE) = (
        './dta/', '/home/chipdelmal/MEGAsync/MK8D/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss'

    )
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
fshdRunsCmlStats = fun.getRunsStats(fshdRunHistoryCml)
# Filter runs -----------------------------------------------------------------
trace = fun.getRunFromID(fshdRunHistoryCml, 66)
###############################################################################
# Plot Data
###############################################################################
# IN --------------------------------------------------------------------------
# runsHistory
# runsStats
ylim = (70, 150)
meanStyle = {'color': (.3, .3, .3), 'alpha': .8, 'width': .8}
medianStyle = {'color': (.3, .3, .3), 'alpha': .75, 'width': .75}
# Preprocess ------------------------------------------------------------------
tNames = list(runsHistory.keys())
tNum = len(tNames)
tTimes = [list(runsHistory[track].values()) for track in tNames]
# Setup figure and axes -------------------------------------------------------
fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_ylim(ylim[0], ylim[1])
ax.set_xlim(-1, tNum + 2)
# Violin plot -----------------------------------------------------------------
bp = ax.violinplot(
        tTimes, widths=.9,
        showmedians=True, showmeans=True, showextrema=False
    )
# Medians and Means style -----------------------------------------------------
vp = bp['cmedians']
vp.set_edgecolor(medianStyle['color'])
vp.set_linewidth(medianStyle['width'])
vp.set_alpha(medianStyle['alpha'])
vp = bp['cmeans']
vp.set_edgecolor(meanStyle['color'])
vp.set_linewidth(meanStyle['width'])
vp.set_alpha(meanStyle['alpha'])
# Grids -----------------------------------------------------------------------
ax.grid(which='both')
major_ticks = range(1, tNum+1, 1)
ax.set_xticks(major_ticks)
ax.set_xticklabels(tNames, rotation=90)
