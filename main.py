
import xmltodict
import functions as fun
from datetime import datetime


(PATH, FILE) = (
        '/home/chipdelmal/Documents/Github/MarioKart8DeluxeSpeedruns/Splits/',
        '03 - Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
    )

with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())

doc['Run']
gameName = doc['Run']['GameName']
segment = doc['Run']['Segments']['Segment']


track = 47
(tName, timesHistory) = (segment[track]['Name'], [])
for hist in segment[track]['SegmentHistory']['Time']:
    if len(hist) > 1:
        tStr = hist['RealTime']
        trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
        tDiff = fun.tdToSec(trackTiming - fun.REFT)
        timesHistory.append(tDiff)

timesHistory
