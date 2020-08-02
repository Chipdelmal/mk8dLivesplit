from datetime import datetime
# from datetime import timedelta
from collections import OrderedDict
import statistics


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


###############################################################################
# Runs
###############################################################################
def getSegments(doc):
    return doc['Run']['Segments']['Segment']


def getRunsDict(seg):
    (nms, tracksDict) = (getSegmentsNames(seg), OrderedDict())
    for (ix, track) in enumerate(seg):
        tHist = track['SegmentHistory']['Time']
        tEntries = {int(i['@id']): tStrToSecs(i['RealTime']) for i in tHist}
        tracksDict.update({nms[ix]: tEntries})
    return tracksDict


def filterRunsDict(runsHistory, filterIDs):
    (keys, fltrHist) = (list(runsHistory.keys()), OrderedDict())
    for trkName in keys:
        track = runsHistory[trkName]
        ftrdTimes = {i: track.get(i) for i in filterIDs}
        fltrHist.update({trkName: ftrdTimes})
    return fltrHist


def getRunFromID(runsHistory, id):
    (keys, trace) = (list(runsHistory.keys()), OrderedDict())
    for trkName in keys:
        track = runsHistory[trkName]
        trace.update({trkName: track.get(id)})
    return trace


def getRunsStats(runsHistory):
    (keys, tracksStats) = (list(runsHistory.keys()), OrderedDict())
    for trackName in keys:
        track = runsHistory[trackName]
        tracksStats.update({trackName: getTrackStats(track)})
    return tracksStats


###############################################################################
# Statistics
###############################################################################
def getTrackStats(track):
    trackTimes = list(track.values())
    trackStats = {
            'Min': min(trackTimes),
            'Max': max(trackTimes),
            'Mean': statistics.mean(trackTimes),
            'Median': statistics.median(trackTimes),
            'SD': statistics.stdev(trackTimes),
            'Variance': statistics.variance(trackTimes)
        }
    return trackStats


###############################################################################
# Auxiliary
###############################################################################
def getFinishedRunsId(segment, skip=0):
    endTimesDict = segment[-1]['SegmentHistory']['Time']
    endRunIds = [int(ts['@id']) for ts in endTimesDict]
    return set([int(i) for i in endRunIds if (i > skip)])


def getSegmentsNames(seg):
    return [i['Name'] for i in seg]
