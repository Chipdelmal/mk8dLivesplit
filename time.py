
import numpy as np
import xmltodict
import functions as fun
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
fSplit = list(zip(*cTimes))[-1]

fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
traces = [i[0] - i[1] for i in zip(cTimesT, means)]
colors = pl.cm.Purples(np.linspace(.05, .95, 1 + len(traces[0])))

for (i, trace) in enumerate(list(zip(*traces))):
    ax.plot(
            trace,
            linewidth=1.5, marker='.', markersize=0,
            color=colors[i], alpha=.75
        )
bp = ax.violinplot(
        [i[0] - i[1] for i in zip(cTimesT, means)],
        widths=.75, showmedians=False, showmeans=True, showextrema=False,
        positions=range(0, len(cTimes[0]))
    )
for (i, vElement) in enumerate(bp['bodies']):
    vElement.set_facecolor((0, 0, 1, .5))
    vElement.set_alpha(.05)
    vElement.set_linewidth(1.5)
vp = bp['cmeans']
vp.set_edgecolor((.3, .3, .3))
vp.set_linewidth(3)
vp.set_alpha(.8)
major_ticks = range(0, 48, 1)
ax.set_ylim(-1.5, 1.5)
ax.grid(which='both')
ax.set_xticks(major_ticks)
ax.grid(which='major', alpha=.5)
ax.set_xticklabels(['{} [{}]'.format(i[1], '%05.2f' % i[0])
                   for i in zip(means, names)], rotation=90)
plt.xticks(fontsize=22.5)
plt.yticks(fontsize=22.5, rotation=0)
plt.title('Run Time Distributions', fontsize=50)
for (i, y) in enumerate(list(traces[-1])):
    x = 47.25
    if i % 2 == 1:
        x = 47.25
    plt.text(
            x, y, '%05.2f' % fSplit[i], fontsize=6.5,
            horizontalalignment='left', verticalalignment='center',
            color=colors[i], rotation=25
        )
fig.savefig('./img/times.png', pad_inches=.1, bbox_inches="tight", dpi=400)
#
# zero=[np.zeros(len(traces[0]))]
# zero.extend(traces)
# zero
