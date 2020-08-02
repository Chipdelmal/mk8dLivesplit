
import pandas as pd
from xmltodict import parse
import functions as fun

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
def getSegments(doc):
    return doc['Run']['Segments']['Segment']


def getFinishedRunsId(segment, skip=0):
    endTimesDict = segment[-1]['SegmentHistory']['Time']
    endRunIds = [int(ts['@id']) for ts in endTimesDict]
    return [i for i in endRunIds if (i > skip)]


def getSegmentsNames(seg):
    return [i['Name'] for i in seg]


# Dev #########################################################################
seg = getSegments(doc)
fshdID = getFinishedRunsId(seg)
nms = getSegmentsNames(seg)

nms
