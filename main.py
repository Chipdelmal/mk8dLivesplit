
import math
import statistics as stats
import xmltodict
import functions as fun
from datetime import datetime
import matplotlib.pyplot as plt


(PATH, FILE) = (
        '/home/chipdelmal/Documents/Github/MarioKart8DeluxeSpeedruns/Splits/',
        '07 - Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
    )

with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())

doc['Run']
gameName = doc['Run']['GameName']
segment = doc['Run']['Segments']['Segment']

len(segment)

(tNames, tHists, tDevs, tMin, tMedian, tMean, tMax) = ([], [], [], [], [], [], [])
for track in range(len(segment)):
    (tName, tHistory) = fun.getTrackHistory(segment[track])
    tNames.append(tName)
    tHists.append(tHistory)
    tDevs.append(stats.stdev(tHistory))
    tMin.append(min(tHistory))
    tMean.append(stats.mean(tHistory))
    tMedian.append(stats.median(tHistory))
    tMax.append(max(tHistory))
tStats = [sum(tMin)/60, sum(tMedian)/60, sum(tMax)/60, sum(tMean)/60]


baseColor = (0, .3, .75)
colors = [(fun.scaleDevs(dev, tDevs)/1.25, baseColor[1], baseColor[2], .5) for dev in tDevs]

# Create a figure instance
fig = plt.figure(figsize=(24, 12))
# Create an axes instance
ax = fig.add_axes([0, 0, 1, 1])
ax.set_ylim(80, 150)
ax.set_xticks(range(1, len(tNames) + 1))
ax.set_xticklabels(tNames, rotation=90)
major_ticks = range(1, 48+1, 1)
minor_ticks = range(1, 48+1, 4)
ax.grid(which='both')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=1)
ax.grid(which='major', alpha=.5)
# plt.ylabel('Seconds')
plt.xticks(fontsize=25)
plt.yticks(fontsize=25, rotation=0)
plt.title('Time Distributions', fontsize=50)

# Create the boxplot
bp = ax.violinplot(tHists, widths=1, showmedians=True, showmeans=False, showextrema=False)
for (i, vElement) in enumerate(bp['bodies']):
    vElement.set_facecolor(colors[i])
    vElement.set_alpha(.25)
    # vElement.set_edgecolor((0, 0, 0))
    vElement.set_linewidth(3)
vp = bp['cmedians']
vp.set_edgecolor((.3, .3, .3))
vp.set_linewidth(3)
vp.set_alpha(.8)
label = "[Min: {:.2f}, Mean: {:.2f}, Median: {:.2f}, Max: {:.2f}]".format(tStats[0], tStats[3], tStats[1], tStats[2])
plt.text(
        .5, .975, label, fontsize=25,
        horizontalalignment='center', verticalalignment='center',
        transform=ax.transAxes
    )

fig.savefig('./img/violin.png', pad_inches=.1, bbox_inches="tight", dpi=250)
