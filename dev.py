
import auxFunctions as aux
import dataFunctions as fun
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
from matplotlib import colors

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
fshdRunsCmlStats = fun.getRunsStats(fshdRunHistoryCml)
# Filter runs -----------------------------------------------------------------
trace = fun.getRunFromID(fshdRunHistoryCml, 66)
###############################################################################
# Plot Data
###############################################################################
# IN --------------------------------------------------------------------------
# runsHistory
# runsStats
ylim = (78, 142)
violinStyle = {
        'color': pl.cm.Purples, 'alpha': .4, 'width': .65,
        'lw': 3, 'lc': (0, 0, 0),
        'bandSize': 4,
        'bandColorA': 'blue', 'bandAlphaA': 0.025,
        'bandColorB': 'white', 'bandAlphaB': 0.025
    }
meanStyle = {'color': (.3, .3, .3), 'alpha': .65, 'width': .8}
medianStyle = {'color': (.3, .3, .3), 'alpha': .85, 'width': 3}
# Preprocess ------------------------------------------------------------------
tNames = list(runsHistory.keys())
tNum = len(tNames)
tTimes = [list(runsHistory.get(track).values()) for track in tNames]
tSDs = [runsStats.get(track).get('SD') for track in tNames]
aux.scaleDevs(2, tSDs)
# Setup figure and axes -------------------------------------------------------
fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_ylim(ylim[0], ylim[1])
ax.set_xlim(0.5, tNum + 0.5)
# Violin plot -----------------------------------------------------------------
bp = ax.violinplot(
        tTimes, widths=violinStyle['width'],
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
ax.grid(which='major', alpha=0)
delta = violinStyle['bandSize']
for i in range(0, tNum, delta):
    if i % (2 * delta) == 0:
        (clr, alp) = (violinStyle['bandColorA'], violinStyle['bandAlphaA'])
    else:
        (clr, alp) = (violinStyle['bandColorB'], violinStyle['bandAlphaB'])
    ax.axvspan(i+0.5, i+delta+0.5, zorder=0, color=clr, alpha=alp)
# Colors ----------------------------------------------------------------------
(cmap, norm) = (violinStyle['color'], colors.Normalize(vmin=0, vmax=max(tSDs)))
vColors = cmap(norm(tSDs))
for (i, vElement) in enumerate(bp['bodies']):
    vElement.set_facecolor(vColors[i])
    vElement.set_alpha(violinStyle['alpha'])
    vElement.set_edgecolor(violinStyle['lc'])
    vElement.set_linewidth(violinStyle['lw'])
# Labels ----------------------------------------------------------------------
plt.xticks(fontsize=22.5)
plt.yticks(fontsize=22.5, rotation=0)
plt.ylabel('Duration (seconds)', fontsize=50)
plt.title('Split Time Distributions', fontsize=75)
# Export ----------------------------------------------------------------------
fig.savefig(
        '{}plotViolin.{}'.format(OUT, TYP),
        pad_inches=PAD, bbox_inches="tight", dpi=DPI
    )
