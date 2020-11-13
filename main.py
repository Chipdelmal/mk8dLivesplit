
import sys
import colors as cl
import plotViolin as pv
import plotTraces as pt
import plotHeatmap as hea
import auxFunctions as aux
import dataFunctions as fun
import plotCategories as cap
import matplotlib.pylab as pl
import matplotlib.pyplot as plt


# (FILE, OUT, VOFF) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (DPI, PAD, TYP, VOFF) = (250, .1, 'png', 30)
TYP = 'png'
(FILE, OUT, VOFF) = (
        './dta/Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss',
        '/home/chipdelmal/Documents/MK8D/Livesplit/', 30
    )
###############################################################################
# Read File
###############################################################################
print('* Reading file...')
seg = fun.getSegmentsFromFile(FILE)
###############################################################################
# Shape Runs Data
###############################################################################
print('* Calculating stats...')
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
# Categories history ----------------------------------------------------------
catHistory = fun.getCategoriesTimes(fshdRunHistoryCml, fshdRunID)
catStats = fun.getRunsStats(catHistory)
# Filter runs -----------------------------------------------------------------
# trace = fun.getRunFromID(fshdRunHistoryCml, 66)
# minTimes = fun.getRunFromStatsOp(runsStats, op='Min')
###############################################################################
# Plot Data
###############################################################################
# Violin ----------------------------------------------------------------------
print('* Plotting violins...')
(fig, ax) = pv.plotSegmentViolins(
        runsHistory, runsStats, ylim=(78, 142),
        vStyle={
                'color': pl.cm.Purples.reversed(), 'alpha': .4,
                'width': .65, 'lw': 3, 'lc': (0, 0, 0)
            }
    )
aux.saveFig(fig, '{}plotViolin.{}'.format(OUT, TYP))
plt.close(fig)
# Traces ----------------------------------------------------------------------
print('* Plotting traces...')
(fig, ax) = pt.plotSegmentTraces(
        fshdRunHistoryCml, runsStats, fshdRunsStatsCml, ylim=(-.65, .65),
        traceStyle={
                'alpha': .5, 'lw': 1.5,
                'lcm': pl.cm.Purples, 'tcl': '#888888'
            }
    )
aux.saveFig(fig, '{}plotTraces.{}'.format(OUT, TYP))
plt.close(fig)
# Heatmap ---------------------------------------------------------------------
print('* Plotting heatmap...')
(fig, ax) = hea.plotSplitsHeatmap(fshdRunHistory, cmap=pl.cm.Purples)
aux.saveFig(fig, '{}plotHeat.{}'.format(OUT, TYP), dpi=500)
plt.close(fig)
# MK8D Categories  ------------------------------------------------------------
print('* Parsing category times...')
(fig, ax) = cap.plotCategoryHeatmap(
        fshdRunHistoryCml, fshdRunID, cmap=pl.cm.Purples
    )
aux.saveFig(fig, '{}plotCategories.{}'.format(OUT, TYP), dpi=500)
plt.close(fig)
###############################################################################
# Text Data
###############################################################################
# Timestaps -------------------------------------------------------------------
print('* Parsing timestamps...')
timpestamps = aux.getTracksTimestamps(
        fshdRunHistoryCml, vOff=VOFF, ix=fshdRunID[-1]
    )
aux.exportTxt('\n'.join(timpestamps), OUT+'youtubeTimestamps.txt')
# Video Summary ---------------------------------------------------------------
print('* Parsing summaries...')
summary = fun.getYoutubeSummary(fshdRunHistoryCml, fshdRunID)
aux.exportTxt('\n'.join(summary), OUT+'youtubeInfo.txt')
