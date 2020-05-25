from datetime import datetime

REFT = datetime(1900, 1, 1, 0, 0, 0, 0)


def tdToSec(tDelta):
    micro = 1000000
    tm = (tDelta.seconds) + (tDelta.microseconds / micro)
    return tm


def getTrackHistory(segmentTrack):
    (tName, timesHistory) = (segmentTrack['Name'], [])
    for hist in segmentTrack['SegmentHistory']['Time']:
        if len(hist) > 1:
            tStr = hist['RealTime']
            trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
            tDiff = tdToSec(trackTiming - REFT)
            timesHistory.append(tDiff)
    return (tName, timesHistory)


def scaleDevs(x, tDevs):
    return (x - min(tDevs)) / (max(tDevs) - min(tDevs))
