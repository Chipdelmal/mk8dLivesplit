
import math
import numpy as np
import statistics as stats
import xmltodict
import functions as fun
from datetime import datetime
import matplotlib.pyplot as plt


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

fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
ax.plot(
        [i[0] - i[1] for i in zip(cTimesT, means)],
        linewidth=1.5, marker='x', markersize=7.5,
        color=(.75, .3, .9, .35)
    )
bp = ax.violinplot(
        [i[0] - i[1] for i in zip(cTimesT, means)],
        widths=.75, showmedians=False, showmeans=True, showextrema=False,
        positions=range(0, len(cTimes[0]))
    )
for (i, vElement) in enumerate(bp['bodies']):
    vElement.set_facecolor((0, 0, 1, .5))
    vElement.set_alpha(.1)
    vElement.set_edgecolor((0, 0, 0))
    # vElement.set_edgecolor((0, 0, 0))
    vElement.set_linewidth(1.5)
ax.set_ylim(-1.5, 1.5)
major_ticks = range(0, 48, 1)
minor_ticks = range(0, 48, 4)
ax.set_xticks(range(0, len(means)))
ax.grid(which='both')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=.1)
ax.grid(which='major', alpha=.1)
ax.set_xticklabels(['{:.2f}'.format(i) for i in means], rotation=90)
fig.savefig('./img/times.png', pad_inches=.1, bbox_inches="tight", dpi=400)
