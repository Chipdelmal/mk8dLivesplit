
import statistics
import pandas as pd
import auxFunctions as aux
import dataFunctions as fun
from xmltodict import parse
from datetime import timedelta
from collections import OrderedDict


###############################################################################
# Runs
###############################################################################
def getRunHistStats(segments):
    runsHistory = fun.getRunsDict(segments)
    runsStats = fun.getRunsStats(runsHistory)
    return (runsHistory, runsStats)


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


def getRunFromOp(runsHistory, op=min):
    tNames = list(runsHistory.keys())
    opDict = OrderedDict()
    for track in tNames:
        times = list(runsHistory[track].values())
        opDict.update({track: {'0': op(times)}})
    return opDict


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


def getRunFromStatsOp(runsStats, op='Min'):
    tNames = list(runsStats.keys())
    oDict = OrderedDict()
    for tName in tNames:
        oDict.update({tName: {'0': runsStats[tName][op]}})
    return oDict


def timeBetweenTracks(fshdRunDta, tracksInterval):
    if tracksInterval[0] is None:
        tInt = fshdRunDta[tracksInterval[1]]
    else:
        tInt = (fshdRunDta[tracksInterval[1]] - fshdRunDta[tracksInterval[0]])
    return tInt


def mk8dCategoriesSplits(fshdRun):
    tFortyEight = timeBetweenTracks(fshdRun, (None, 'Big Blue'))
    tThirtyTwo = timeBetweenTracks(fshdRun, (None, 'N64 Rainbow Road'))
    tNitro = timeBetweenTracks(fshdRun, (None, 'Rainbow Road'))
    tRetro = timeBetweenTracks(fshdRun, ('Rainbow Road', 'N64 Rainbow Road'))
    tBonus = timeBetweenTracks(fshdRun, ('N64 Rainbow Road', 'Big Blue'))
    catDict = {
            '48 Tracks': tFortyEight, '32 Tracks': tThirtyTwo,
            'Nitro Tracks': tNitro, 'Retro Tracks': tRetro,
            'Bonus Tracks': tBonus
        }
    return catDict


def getMK8DCategories(fshdRunHistoryCml, id):
    catNames = [
            '48 Tracks', '32 Tracks', 'Nitro Tracks',
            'Retro Tracks', 'Bonus Tracks'
        ]
    fshdRun = getRunFromID(fshdRunHistoryCml, id)
    catTimes = mk8dCategoriesSplits(fshdRun)
    catStrg = {i: catTimes[i] for i in catNames}
    return catStrg


def getYoutubeSummary(
            fshdRunHistoryCml, fshdRunID,
            usr='https://www.speedrun.com/user/chipdelmal'
        ):
    (runID, runNum) = (fshdRunID[-1], str(len(fshdRunID)).zfill(2))
    finishTime = fshdRunHistoryCml.get('Big Blue').get(runID)
    label = '(200cc, 48 tracks, no items, digital)'
    timeString = str(timedelta(seconds=finishTime))[:-4]
    title = '[{}] MK8D {} {}'.format(runNum, timeString, label)
    catTimes = fun.getMK8DCategories(fshdRunHistoryCml, runID)
    cStr = [cat+' - '+str(timedelta(seconds=catTimes[cat]))[:-4] for cat in catTimes]
    categories = '\n'.join(cStr)
    tags = 'mk8d, mario kart, speedrun, speed run, gaming, 48, 200cc, no item, switch'
    full = [title, categories, usr, tags]
    return full


def getCategoriesTimes(fshdRunHistoryCml, fshdRunID):
    fshdHist = [
            fun.getMK8DCategories(fshdRunHistoryCml, id) for id in fshdRunID
        ]
    catNames = [
            '48 Tracks', '32 Tracks', 'Nitro Tracks',
            'Retro Tracks', 'Bonus Tracks'
        ]
    dictTracks = {}
    for track in list(catNames):
        t = {fshdRunID[j]: run[track]/60 for (j, run) in enumerate(fshdHist)}
        dictTracks.update({track: t})
    return dictTracks


# #############################################################################
# Dataframe structured functions
# #############################################################################
def getRunsDataframe(
    runsHS, 
    versions=('Cartridge', 'Digital')
):
    columns = ['Track', 'ID', 'Time', 'Version']
    df = pd.DataFrame(columns=columns)
    # Populate dataframe ----------------
    for hist in range(len(runsHS)):
        tracksHist = runsHS[hist][0]
        tracks = list(tracksHist.keys())
        # Append entries ----------------------------------------------------------
        for track in tracks:
            ids = list(tracksHist[track].keys())
            times = list(tracksHist[track].values())
            for (key, time) in zip(ids, times):
                df = df.append(
                    {
                        'Track': track,
                        'ID': int(key),
                        'Time': time, 
                        'Version': versions[hist]
                    }, ignore_index=True
                )
    return df


def getFinishedRunsIDs(
    runsDF, 
    finalTrack='Big Blue', 
    version='Digital'
):
    fltr = zip(
        runsDF['Track'] == finalTrack, 
        runsDF['Version'] == version
    ) 
    fshdID = list(runsDF[[all(i) for i in fltr]].get('ID'))
    return set(fshdID)


TRACKS = [
    'Mario Kart Stadium', 'Water Park', 'Sweet Sweet Canyon', 'Thwomp Ruins',
    'Mario Circuit', 'Toad Harbor', 'Twisted Mansion', 'Shy Guy Falls',
    'Sunshine Airport', 'Dolphin Shoals', 'Electrodrome', 'Mount Wario',
    'Cloudtop Cruise', 'Bone-Dry Dunes', "Bowser's Castle", 'Rainbow Road',
    'Wii Moo Moo Meadows', 'GBA Mario Circuit', 'DS Cheep Cheep Beach', "N64 Toad's Turnpike",
    'GCN Dry Dry Desert', 'SNES Donut Plains 3', 'N64 Royal Raceway', '3DS DK Jungle',
    'DS Wario Stadium', 'GCN Sherbet Land', '3DS Music Park', 'N64 Yoshi Valley',
    'DS Tick-Tock Clock', '3DS Piranha Plant Slide', 'Wii Grumble Volcano', 'N64 Rainbow Road',
    'GCN Yoshi Circuit', 'Excitebike Arena', 'Dragon Driftway', 'Mute City',
    "Wii Wario's Gold Mine", 'SNES Rainbow Road', 'Ice Ice Outpost', 'Hyrule Circuit',
    'GCN Baby Park', 'GBA Cheese Land', 'Wild Woods', 'Animal Crossing',
    '3DS Neo Bowser City', 'GBA Ribbon Road', 'Super Bell Subway','Big Blue'
]