
from xmltodict import parse
import dataFunctions as fun
from collections import OrderedDict

(PATH, FILE, OUT) = (
        './dta/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss',
        '/home/chipdelmal/MEGAsync/MK8D/'
    )
(DPI, PAD, TYP) = (250, .1, 'png')
# Parse XML ###################################################################
with open(PATH+FILE) as fd:
    doc = parse(fd.read())
seg = fun.getSegments(doc)

# Runs history and stats ######################################################
runsHistory = fun.getRunsDict(seg)
runsStats = fun.getRunsStats(runsHistory)
# Filter to finished runs #####################################################
fshdRunID = fun.getFinishedRunsId(seg)
fshdRunHistory = fun.filterRunsDict(runsHistory, fshdRunID)
fshdRunsStats = fun.getRunsStats(fshdRunHistory)
# Filter runs #################################################################
trace = fun.getRunFromID(runsHistory, 66)
trace
