
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
