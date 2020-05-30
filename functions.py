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
            tDiff = timeToSecs(tStr, refTime=REFT)
            timesHistory.append(tDiff)
    return (tName, timesHistory)


def scaleDevs(x, tDevs):
    return (x - min(tDevs)) / (max(tDevs) - min(tDevs))


def getEndRunIds(segment):
    endTimesDict = segment[-1]['SegmentHistory']['Time']
    endRunIds = [ts['@id'] for ts in endTimesDict]
    return set(endRunIds)


def timeToSecs(tStr, refTime=REFT):
    trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
    tDiff = tdToSec(trackTiming - REFT)
    return tDiff


def filterFinishedSegments(track, endRId, reft=REFT):
    trackSplits = []
    segHist = track['SegmentHistory']['Time']
    for rHist in segHist:
        if rHist['@id'] in endRId:
            splitTime = timeToSecs(rHist['RealTime'])
            trackSplits.append(splitTime)
    return trackSplits


def finishedRunsTimes(segment):
    endRId = getEndRunIds(segment)
    fRun = []
    for segmentTrack in segment:
        fTime = filterFinishedSegments(segmentTrack, endRId, reft=REFT)
        fRun.append(fTime)
    return (list(zip(*fRun)))
