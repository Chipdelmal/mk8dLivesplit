
import plot
import xmltodict
import functions as fun
import matplotlib.pylab as pl


(PATH, FILE, OUT) = (
        './dta/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss',
        '/home/chipdelmal/MEGAsync/MK8D/'
    )
# Parse XML ###################################################################
with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())
# Violin ######################################################################
tStats = fun.getSegmentStats(doc)
fig = plot.plotTimings(tStats)
fig.savefig(
        OUT+'violin.png',
        pad_inches=.1, bbox_inches="tight", dpi=250
    )
# Traces ######################################################################
tracesDta = fun.getSegmentTraces(doc, skip=1)
(names, means, fSplit, cTimes, cTimesT, traces) = (
        tracesDta['names'], tracesDta['means'],
        tracesDta['final'], tracesDta['cmTimes'],
        tracesDta['cmTimesT'], tracesDta['deviance']
    )
fig = plot.plotTraces(
        traces, fSplit, cTimes, cTimesT, means, names,
        yRange=1, cmap=pl.cm.Purples
    )
fig.savefig(
        OUT+'times.png',
        pad_inches=.1, bbox_inches="tight", dpi=250
    )
# Timings Table ###############################################################
catDicts = fun.timesForCategories(doc)
