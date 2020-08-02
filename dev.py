
import pandas as pd
from xmltodict import parse
import functions as fun
from datetime import datetime
from datetime import timedelta


(PATH, FILE, OUT) = (
        './dta/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss',
        '/home/chipdelmal/MEGAsync/MK8D/'
    )
(DPI, PAD, TYP) = (250, .1, 'png')
# Parse XML ###################################################################
with open(PATH+FILE) as fd:
    doc = parse(fd.read())


# Functions ###################################################################
REFT = datetime(1900, 1, 1, 0, 0, 0, 0)


def getSegments(doc):
    return doc['Run']['Segments']['Segment']


def getFinishedRunsId(segment, skip=0):
    endTimesDict = segment[-1]['SegmentHistory']['Time']
    endRunIds = [int(ts['@id']) for ts in endTimesDict]
    return [i for i in endRunIds if (i > skip)]


def getSegmentsNames(seg):
    return [i['Name'] for i in seg]


def tdeltaToSec(tDelta, microSec=1000000):
    tm = (tDelta.seconds) + (tDelta.microseconds / microSec)
    return tm


def tStrToSecs(tStr, refTime=REFT):
    trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
    tDiff = tdeltaToSec(trackTiming - REFT)
    return tDiff


def getTracksDict(seg):
    (nms, tracksDict) = (getSegmentsNames(seg), {})
    for (ix, track) in enumerate(seg):
        tHist = track['SegmentHistory']['Time']
        tEntries = [(i['@id'], tStrToSecs(i['RealTime'])) for i in tHist]
        tracksDict.update({nms[ix]: tEntries})
    return tracksDict


# Dev #########################################################################
seg = getSegments(doc)
fshdID = getFinishedRunsId(seg)
segRuns = getTracksDict(seg)
segRuns
