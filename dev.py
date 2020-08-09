
import plotViolin as pv
import plotTraces as pt
import plotHeatmap as hea
import auxFunctions as aux
import dataFunctions as fun
import matplotlib.pylab as pl
import matplotlib.pyplot as plt

(PATH, OUT, FILE) = (
        './dta/', '/home/chipdelmal/MEGAsync/MK8D/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss'
    )
(DPI, PAD, TYP, VOFF) = (250, .1, 'png', 25)
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
minTimes = fun.getRunFromStatsOp(runsStats, op='Min')
###############################################################################
# Plot Data
###############################################################################
# Violin ----------------------------------------------------------------------
(fig, ax) = pv.plotSegmentViolins(runsHistory, runsStats, ylim=(78, 142))
aux.saveFig(fig, '{}plotViolin.{}'.format(OUT, TYP))
plt.close(fig)
# Traces ----------------------------------------------------------------------
(fig, ax) = pt.plotSegmentTraces(
        fshdRunHistoryCml, runsStats, fshdRunsStatsCml, ylim=(-.65, .65)
    )
aux.saveFig(fig, '{}plotTraces.{}'.format(OUT, TYP))
plt.close(fig)
# Heatmap ---------------------------------------------------------------------
(fig, ax) = hea.plotSplitsHeatmap(fshdRunHistory, cmap=pl.cm.Purples)
aux.saveFig(fig, '{}plotHeat.{}'.format(OUT, TYP), dpi=500)
plt.close(fig)
###############################################################################
# Text Data
###############################################################################
# Timestaps -------------------------------------------------------------------
timpestamps = aux.getTracksTimestamps(
        fshdRunHistoryCml, vOff=VOFF, ix=fshdRunID[-1]
    )
aux.exportTxt('\n'.join(timpestamps), OUT+'youtubeTimestamps.txt')
