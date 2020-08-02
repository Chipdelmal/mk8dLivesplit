
import dataFunctions as fun
from collections import OrderedDict

(PATH, OUT, FILE) = (
        './dta/', '/home/chipdelmal/MEGAsync/MK8D/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss'

    )
# Parse XML ###################################################################
seg = fun.getSegmentsFromFile(PATH+FILE)
# Runs history and stats ######################################################
runsHistory = fun.getRunsDict(seg)
runsStats = fun.getRunsStats(runsHistory)
# Filter to finished runs #####################################################
fshdRunID = fun.getFinishedRunsId(seg)
fshdRunHistory = fun.filterRunsDict(runsHistory, fshdRunID)
fshdRunsStats = fun.getRunsStats(fshdRunHistory)
# Cumulative history ##########################################################
fshdRunHistoryCml = fun.calcRunsCumulative(fshdRunHistory)
# Filter runs #################################################################
trace = fun.getRunFromID(fshdRunHistoryCml, 66)
