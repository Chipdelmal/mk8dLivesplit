
import numpy as np
import statistics as stats
from datetime import datetime
from datetime import timedelta

REFT = datetime(1900, 1, 1, 0, 0, 0, 0)


def minsToHr(mins, prec=-4):
    return str(timedelta(minutes=mins))[:prec]


def ceilFloat(x, prec=2, base=.5):
    return round(base * round(float(x)/base), prec) + base


def tdToSec(tDelta):
    micro = 1000000
    tm = (tDelta.seconds) + (tDelta.microseconds / micro)
    return tm


def getTrackHistory(segmentTrack, skip=0):
    (tName, timesHistory) = (segmentTrack['Name'], [])
    for hist in segmentTrack['SegmentHistory']['Time']:
        if (len(hist) > 1) and (int(hist['@id']) > skip):
            tStr = hist['RealTime']
            tDiff = timeToSecs(tStr, refTime=REFT)
            timesHistory.append(tDiff)
    return (tName, timesHistory)


def scaleDevs(x, tDevs):
    return (x - min(tDevs)) / (max(tDevs) - min(tDevs))


def getEndRunIds(segment, skip=0):
    endTimesDict = segment[-1]['SegmentHistory']['Time']
    endRunIds = [int(ts['@id']) for ts in endTimesDict]
    return [i for i in endRunIds if (i > skip)]


def timeToSecs(tStr, refTime=REFT):
    trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
    tDiff = tdToSec(trackTiming - REFT)
    return tDiff


def filterFinishedSegments(track, endRId, reft=REFT):
    trackSplits = []
    segHist = track['SegmentHistory']['Time']
    for rHist in segHist:
        if int(rHist['@id']) in endRId:
            splitTime = timeToSecs(rHist['RealTime'])
            trackSplits.append(splitTime)
    return trackSplits


def finishedRunsTimes(segment, skip=0):
    endRId = getEndRunIds(segment, skip=skip)
    fRun = []
    for segmentTrack in segment:
        fTime = filterFinishedSegments(segmentTrack, endRId, reft=REFT)
        fRun.append(fTime)
    return list(zip(*fRun))


def getSegmentStats(doc, skip=0):
    segment = doc['Run']['Segments']['Segment']
    (tNames, tHists, tDevs, tMin, tMedian, tMean, tMax) = (
            [], [], [], [], [], [], []
        )
    for track in range(len(segment)):
        (tName, tHistory) = getTrackHistory(segment[track], skip=skip)
        tNames.append(tName)
        tHists.append(tHistory)
        tDevs.append(stats.stdev(tHistory))
        tMin.append(min(tHistory))
        tMean.append(stats.mean(tHistory))
        tMedian.append(stats.median(tHistory))
        tMax.append(max(tHistory))
    tStats = {
            'min': sum(tMin)/60, 'median': sum(tMedian)/60,
            'max': sum(tMax)/60, 'mean': sum(tMean)/60,
            'sd': tDevs, 'hist': tHists, 'names': tNames
        }
    return tStats


def getSegmentTraces(doc, skip=0):
    segment = doc['Run']['Segments']['Segment']
    fTimes = finishedRunsTimes(segment, skip=skip)
    cTimes = [np.cumsum(i)/60 for i in fTimes]
    cTimesT = list(zip(*cTimes))
    means = [np.mean(i) for i in cTimesT]
    names = getSegmentStats(doc)['names']
    fSplit = list(zip(*cTimes))[-1]
    traces = [i[0] - i[1] for i in zip(cTimesT, means)]
    zero = np.zeros(len(traces[0]))
    traces.insert(0, zero)
    means.insert(0, 0)
    cTimesT.insert(0, zero)
    names.insert(0, 'Start')
    tDicts = {
            'names': names,
            'means': means,
            'final': fSplit,
            'cmTimes': cTimes,
            'cmTimesT': cTimesT,
            'deviance': traces
        }
    return tDicts


def timeIntervalsFromTrackNames(tNameStart, tNameEnd, cTimes, tNames):
    runsNum = len(cTimes[0])
    # Get Starting track timings
    if tNameStart is None:
        tSrt = [0] * runsNum
    else:
        ixSrt = tNames.index(tNameStart)
        tSrt = [split[ixSrt] for split in cTimes]
    # Get Ending track timings
    ixEnd = tNames.index(tNameEnd)
    tEnd = [split[ixEnd] for split in cTimes]
    # Calculate times
    times = [i[1] - i[0] for i in zip(tSrt, tEnd)]
    return times


def timesForCategories(doc):
    # #########################################################################
    # Get Timings and names
    # #########################################################################
    seg = doc['Run']['Segments']['Segment']
    fTimes = finishedRunsTimes(seg)
    cTimes = [np.cumsum(i)/60 for i in fTimes]
    names = getSegmentStats(doc)['names']
    # #########################################################################
    # Get category timings (https://www.speedrun.com/mk8dx)
    # #########################################################################
    tFortyEight = timeIntervalsFromTrackNames(
            None, 'Big Blue', cTimes, names
        )
    tThirtyTwo = timeIntervalsFromTrackNames(
            None, 'N64 Rainbow Road', cTimes, names
        )
    tNitro = timeIntervalsFromTrackNames(
            None, 'Rainbow Road', cTimes, names
        )
    tRetro = timeIntervalsFromTrackNames(
            'Rainbow Road', 'N64 Rainbow Road', cTimes, names
        )
    tBonus = timeIntervalsFromTrackNames(
            'N64 Rainbow Road', 'Big Blue', cTimes, names
        )
    # #########################################################################
    # Compile dictionary for return
    # #########################################################################
    tSplits = {
            '48 Tracks': tFortyEight, '32 Tracks': tThirtyTwo,
            'Nitro': tNitro, 'Retro': tRetro, 'Bonus': tBonus
        }
    return tSplits
