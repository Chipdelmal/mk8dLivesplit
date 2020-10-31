
import numpy as np
import dataFunctions as fun
from datetime import datetime
from datetime import timedelta

###############################################################################
# Timing
###############################################################################
REFT = datetime(1900, 1, 1, 0, 0, 0, 0)


def tdeltaToSec(tDelta, microSec=1000000):
    tm = (tDelta.seconds) + (tDelta.microseconds / microSec)
    return tm


def tStrToSecs(tStr, refTime=REFT):
    trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
    tDiff = tdeltaToSec(trackTiming - REFT)
    return tDiff


def secToMin(sec, prec=-4):
    return str(timedelta(seconds=sec))[2:prec]


def minsToHr(mins, prec=-4):
    return str(timedelta(minutes=mins))[:prec]


def scaleDevs(x, tDevs):
    return (x - min(tDevs)) / (max(tDevs) - min(tDevs))


###############################################################################
# Save figure
###############################################################################
def saveFig(fig, path, pad=.1, bbox='tight', dpi=250):
    fig.savefig(path, pad_inches=pad, bbox_inches=bbox, dpi=dpi)


###############################################################################
# Youtube
###############################################################################
def getTracksTimestamps(fshdRunHistoryCml, vOff=0, ix=-1):
    lastRun = fun.getRunFromID(fshdRunHistoryCml, ix)
    names = ["Start"]
    tNames = list(fshdRunHistoryCml.keys())
    names.extend(tNames)
    splits = [vOff]
    mins = [(vOff+float(lastRun[i]))/60 for i in tNames]
    splits.extend(mins)
    sTimesFmt = [str(timedelta(minutes=time))[:7] for time in splits]
    itr = zip(names[1:], sTimesFmt[:-1])
    tStamps = ['{}: {}'.format(i[0], i[1]) for i in itr]
    return tStamps


###############################################################################
# Other
###############################################################################
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key


def prependValue(inList, value=0):
    pad = [0]
    pad.extend(inList)
    return pad


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


###############################################################################
# Write
###############################################################################
def exportTxt(textData, outPath):
    with open(outPath, "w") as text_file:
        text_file.write(textData)
