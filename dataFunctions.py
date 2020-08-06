
import statistics
import auxFunctions as aux
from xmltodict import parse
from collections import OrderedDict


###############################################################################
# Runs
###############################################################################
def getSegments(doc):
    return doc['Run']['Segments']['Segment']


def getRunsDict(seg):
    (nms, tracksDict) = (getSegmentsNames(seg), OrderedDict())
    for (ix, track) in enumerate(seg):
        tHist = track['SegmentHistory']['Time']
        tEntry = {int(i['@id']): aux.tStrToSecs(i['RealTime']) for i in tHist}
        tracksDict.update({nms[ix]: tEntry})
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


def calcRunsCumulative(finishedRunsHistory):
    (keys, runHistCml) = (list(finishedRunsHistory.keys()), OrderedDict())
    fshdRunID = list(finishedRunsHistory.get(keys[0]).keys())
    # Prime the dictionary with first track
    runHistCml.update({keys[0]: finishedRunsHistory.get(keys[0])})
    # Iterate through the rest of the tracks
    for tIx in range(1, len(keys)):
        trackDict = {}
        (tKeyC, tKeyP) = (keys[tIx], keys[tIx-1])
        for rID in fshdRunID:
            (tC, tP) = (
                    finishedRunsHistory[tKeyC].get(rID),
                    runHistCml[tKeyP].get(rID)
                )
            trackDict.update({rID: tC + tP})
        runHistCml.update({keys[tIx]: trackDict})
    return runHistCml


def getRunIDWithTime(finishedRunsHistoryCum, trackName, op=min):
    lastSplit = finishedRunsHistoryCum[trackName]
    minTime = op(list(lastSplit.values()))
    runID = aux.get_key(minTime, lastSplit)
    return runID

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
    return sorted(list([int(i) for i in endRunIds if (i > skip)]))


def getSegmentsNames(seg):
    return [i['Name'] for i in seg]


def getSegmentsFromFile(filePath):
    with open(filePath) as fd:
        doc = parse(fd.read())
    seg = getSegments(doc)
    return seg
