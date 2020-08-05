
import plot
import xmltodict
import functions as fun
import matplotlib.pylab as pl
from datetime import timedelta

(PATH, OUT, FILE) = (
        './dta/', '/home/chipdelmal/MEGAsync/MK8D/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss'
    )
(DPI, PAD, TYP) = (250, .1, 'png')
# Parse XML ###################################################################
with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())
# Violin ######################################################################
tStats = fun.getSegmentStats(doc)
fig = plot.plotTimings(
        tStats, vNames=None,  # 'cups'
        ylim=(70, 140)
        # vNames=['Rainbow Road', 'N64 Rainbow Road', 'Big Blue']
    )
fig.savefig(
        '{}plotViolin.{}'.format(OUT, TYP),
        pad_inches=PAD, bbox_inches="tight", dpi=DPI
    )
# Traces ######################################################################
tracesDta = fun.getSegmentTraces(doc, skip=0)
(names, means, fSplit, cTimes, cTimesT, traces) = (
        tracesDta['names'], tracesDta['means'],
        tracesDta['final'], tracesDta['cmTimes'],
        tracesDta['cmTimesT'], tracesDta['deviance']
    )
fig = plot.plotTraces(
        traces, fSplit, cTimes, cTimesT, means, names, tStats, env=False,
        yRange=(-.75, .75), cmap=pl.cm.Purples,
        vNames=None  # ['Rainbow Road', 'N64 Rainbow Road', 'Big Blue']
    )
fig.savefig(
        '{}plotTimes.{}'.format(OUT, TYP),
        pad_inches=PAD, bbox_inches="tight", dpi=DPI
    )
# Timings Table ###############################################################
catDict = fun.timesForCategories(doc)
catPD = fun.getTimesTableForCategories(catDict)
mixLst = fun.getTableMinTimes(catDict)
fig = plot.renderTable(catPD, minPos=mixLst, col_width=1.75)
fig.savefig(
        '{}tableRun.{}'.format(OUT, TYP),
        pad_inches=PAD, bbox_inches="tight", dpi=DPI
    )
# Tracks Table ################################################################
(tTable, tDict) = fun.getTimesForTracks(doc)
mixLstT = fun.getTrackTableMinTimes(tDict)
catPDT = fun.getTimesTableForTracks(tTable)
fig = plot.renderTable(catPDT, col_width=3.5, minPos=mixLstT)
fig.savefig(
        '{}tableTrack.{}'.format(OUT, TYP),
        pad_inches=PAD, bbox_inches="tight", dpi=DPI
    )
# Video Summary ###############################################################
catNames = list(catPD.columns)
lastIx = catPD.shape[0]
finalRun = catPD[catPD['Run'] == lastIx]
catSummary = ['{}: \t{}'.format(i, list(finalRun.get(i))[0]) for i in catNames]
runNum = len(catDict.get('48 Tracks'))
timeRun = list(finalRun.get('48 Tracks'))[0]
videoTitle = '[{}] MK8D {} (200cc, 48 tracks, no items, digital)'.format(
        str(runNum).zfill(2), timeRun
    )
speedrunHandle = 'https://www.speedrun.com/user/chipdelmal'
cmmnt = '200cc, 48 tracks, No items, Digital'
tags = [
        'mk8d', 'mario kart', 'speedrun', 'speed run', 'gaming', '48',
        '200cc', 'no item', 'switch'
    ]
','.join(tags)
txtOut = '{}\n{}\n{}\n{}\n{}'.format(
        videoTitle, '\n'.join(catSummary[1:]),
        speedrunHandle,
        cmmnt, ', '.join(tags)
    )

with open(OUT+'youtubeSummary.txt', "w") as text_file:
    text_file.write(txtOut)
# Timestaps ###################################################################
(ix, videoOffset) = (-1, 27)
sTimes = [i[ix]+videoOffset/60 for i in cTimesT]
sTimesFmt = [str(timedelta(minutes=time))[:7] for time in sTimes]
tStamps = ['{}: {}'.format(i[0], i[1]) for i in zip(names[1:], sTimesFmt[:-1])]
with open(OUT+'youtubeTimestamps.txt', "w") as text_file:
    text_file.write('\n'.join(tStamps))
