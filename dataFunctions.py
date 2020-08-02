from datetime import datetime
# from datetime import timedelta
from collections import OrderedDict
import statistics


REFT = datetime(1900, 1, 1, 0, 0, 0, 0)


def getSegments(doc):
    return doc['Run']['Segments']['Segment']


def getFinishedRunsId(segment, skip=0):
    endTimesDict = segment[-1]['SegmentHistory']['Time']
    endRunIds = [int(ts['@id']) for ts in endTimesDict]
    return [int(i) for i in endRunIds if (i > skip)]


def getSegmentsNames(seg):
    return [i['Name'] for i in seg]


def tdeltaToSec(tDelta, microSec=1000000):
    tm = (tDelta.seconds) + (tDelta.microseconds / microSec)
    return tm


def tStrToSecs(tStr, refTime=REFT):
    trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
    tDiff = tdeltaToSec(trackTiming - REFT)
    return tDiff


def getRunsDict(seg):
    (nms, tracksDict) = (getSegmentsNames(seg), OrderedDict())
    for (ix, track) in enumerate(seg):
        tHist = track['SegmentHistory']['Time']
        tEntries = {int(i['@id']): tStrToSecs(i['RealTime']) for i in tHist}
        tracksDict.update({nms[ix]: tEntries})
    return tracksDict


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


def getRunsStats(runsHistory):
    (keys, tracksStats) = (list(runsHistory.keys()), OrderedDict())
    for trackName in keys:
        track = runsHistory[trackName]
        tracksStats.update({trackName: getTrackStats(track)})
    return tracksStats
