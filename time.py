
import numpy as np
import xmltodict
import functions as fun
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from datetime import timedelta
import plot

(PATH, FILE) = (
        './dta/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
    )

with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())

segment = doc['Run']['Segments']['Segment']
fTimes = fun.finishedRunsTimes(segment)
cTimes = [np.cumsum(i)/60 for i in fTimes]
cTimesT = list(zip(*cTimes))
means = [np.mean(i) for i in cTimesT]
names = fun.getSegmentStats(doc)['names']
fSplit = list(zip(*cTimes))[-1]
traces = [i[0] - i[1] for i in zip(cTimesT, means)]
zero = np.zeros(len(traces[0]))
traces.insert(0, zero)
means.insert(0, 0)
cTimesT.insert(0, zero)
names.insert(0, 'Start')


tracesDta = fun.getSegmentTraces(doc)
(names, means, fSplit, cTimes, cTimesT, traces) = (
        tracesDta['names'], tracesDta['means'],
        tracesDta['final'], tracesDta['cumTimes'],
        tracesDta['cumTimesT'], tracesDta['deviance']
    )
plot.plotTraces(traces, fSplit, cTimes, cTimesT, means, names)



fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
colors = pl.cm.Purples(np.linspace(.05, .95, 1 + len(traces[0])))
yRange = fun.ceilFloat(max(abs(traces[-1])))
# Plot traces -----------------------------------------------------------------
for (i, trace) in enumerate(list(zip(*traces))):
    ax.plot(
            trace,
            linewidth=1.5, marker='.', markersize=0,
            color=colors[i], alpha=.75
        )
# Plot violins ----------------------------------------------------------------
bp = ax.violinplot(
        [i[0] - i[1] for i in zip(cTimesT, means)],
        widths=.75, showmedians=True, showmeans=False, showextrema=False,
        positions=range(0, len(cTimes[0])+1)
    )
for (i, vElement) in enumerate(bp['bodies']):
    vElement.set_facecolor((0, 0, 1, .5))
    vElement.set_alpha(.05)
    vElement.set_linewidth(1.5)
vp = bp['cmedians']
vp.set_edgecolor((.3, .3, .3))
vp.set_linewidth(3)
vp.set_alpha(.8)
# Grids and labels ------------------------------------------------------------
major_ticks = range(0, len(means), 1)
ax.grid(which='both')
ax.set_xticks(major_ticks)
ax.set_yticks([.5 * i for i in range(-round(yRange) * 2, round(yRange) * 2, 1)])
ax.grid(which='major', alpha=.5)
ax.set_xticklabels(
        ['{} [{}]'.format(i[1], '%05.2f' % i[0]) for i in zip(means, names)],
        rotation=90
    )
plt.xticks(fontsize=22.5)
plt.yticks(fontsize=22.5, rotation=0)
plt.ylabel('Deviation from Mean (minutes)', fontsize=50)
plt.title('Run Time Distributions', fontsize=75)
ax.set_ylim(-yRange, yRange)
for (i, y) in enumerate(list(traces[-1])):
    x = len(means) - .6
    if i % 2 == 1:
        x = x + 0
    plt.text(
            x, round(y, 4), str(timedelta(minutes=fSplit[i]))[:-4],
            fontsize=9,
            horizontalalignment='left', verticalalignment='center',
            color=colors[i], rotation=0
        )
fig.savefig('./img/times.png', pad_inches=.1, bbox_inches="tight", dpi=250)
