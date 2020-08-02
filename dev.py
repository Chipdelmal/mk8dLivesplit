
from xmltodict import parse
import dataFunctions as fun


(PATH, FILE, OUT) = (
        './dta/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss',
        '/home/chipdelmal/MEGAsync/MK8D/'
    )
(DPI, PAD, TYP) = (250, .1, 'png')
# Parse XML ###################################################################
with open(PATH+FILE) as fd:
    doc = parse(fd.read())

# Dev #########################################################################
seg = fun.getSegments(doc)
fshdRunID = fun.getFinishedRunsId(seg)
runsHistory = fun.getRunsDict(seg)
runsStats = fun.getRunsStats(runsHistory)
runsStats
