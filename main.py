
import plot
import xmltodict
import functions as fun
import matplotlib.pylab as pl


(PATH, OUT, FILE) = (
        './dta/', '/home/chipdelmal/MEGAsync/MK8D/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
    )
(DPI, PAD, TYP) = (250, .1, 'png')
# Parse XML ###################################################################
with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())
# Violin ######################################################################
tStats = fun.getSegmentStats(doc)
fig = plot.plotTimings(tStats)
fig.savefig(
        '{}violin.{}'.format(OUT, TYP),
        pad_inches=PAD, bbox_inches="tight", dpi=DPI
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
        '{}times.{}'.format(OUT, TYP),
        pad_inches=PAD, bbox_inches="tight", dpi=DPI
    )
# Timings Table ###############################################################
catDict = fun.timesForCategories(doc)
catPD = fun.getTimesTableForCategories(catDict)
fig = plot.renderTable(catPD)
fig.savefig(
        '{}table.{}'.format(OUT, TYP),
        pad_inches=PAD, bbox_inches="tight", dpi=DPI
    )
