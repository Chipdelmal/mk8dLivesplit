
import plot
import xmltodict
import functions as fun


(PATH, FILE) = (
        './dta/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
    )
# Parse XML ###################################################################
with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())
# Violin ######################################################################
tStats = fun.getSegmentStats(doc)
fig = plot.plotTimings(tStats)
fig.savefig('./img/violin.png', pad_inches=.1, bbox_inches="tight", dpi=250)
# Traces ######################################################################
tracesDta = fun.getSegmentTraces(doc)
(names, means, fSplit, cTimes, cTimesT, traces) = (
        tracesDta['names'], tracesDta['means'],
        tracesDta['final'], tracesDta['cumTimes'],
        tracesDta['cumTimesT'], tracesDta['deviance']
    )
fig = plot.plotTraces(traces, fSplit, cTimes, cTimesT, means, names, yRange=1)
fig.savefig('./img/times.png', pad_inches=.1, bbox_inches="tight", dpi=250)
