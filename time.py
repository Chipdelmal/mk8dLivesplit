
import math
import numpy as np
import statistics as stats
import xmltodict
import functions as fun
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.pylab as pl


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
means = [np.median(i) for i in cTimesT]
names = fun.getSegmentStats(doc)['names']


fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
traces = [i[0] - i[1] for i in zip(cTimesT, means)]
colors = pl.cm.Purples(np.linspace(.05, .95, 1 + len(traces[0])))

for (i, trace) in enumerate(list(zip(*traces))):
    ax.plot(
            trace,
            linewidth=1.5, marker='.', markersize=5,
            color=colors[i], alpha=.5
        )
bp = ax.violinplot(
        [i[0] - i[1] for i in zip(cTimesT, means)],
        widths=.75, showmedians=False, showmeans=True, showextrema=False,
        positions=range(0, len(cTimes[0]))
    )
for (i, vElement) in enumerate(bp['bodies']):
    vElement.set_facecolor((0, 0, 1, .5))
    vElement.set_alpha(.05)
    vElement.set_edgecolor((0, 0, 0))
    # vElement.set_edgecolor((0, 0, 0))
    vElement.set_linewidth(1.5)
major_ticks = range(0, 48, 1)
ax.set_ylim(-1.5, 1.5)
ax.grid(which='both')
ax.set_xticks(major_ticks)
ax.grid(which='major', alpha=.1)
ax.set_xticklabels(['{} [{}]'.format(i[1], '%05.2f' % i[0]) for i in zip(means, names)], rotation=90)
plt.xticks(fontsize=22.5)
plt.yticks(fontsize=22.5, rotation=0)
plt.title('Run Time Distributions', fontsize=50)
# axR = ax.twiny()
# axR.set_xticks(major_ticks)
# axR.grid(which='major', alpha=.1)
# axR.tick_params(direction = 'out')
# axR.set_xticklabels(['{}: {:2.2f}'.format(i[1], i[0]) for i in zip(means, names)], rotation=90)
fig.savefig('./img/times.png', pad_inches=.1, bbox_inches="tight", dpi=400)
