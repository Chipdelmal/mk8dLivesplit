
import math
import numpy as np
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

segment = doc['Run']['Segments']['Segment']
fTimes = fun.finishedRunsTimes(segment)
cTimes = [np.cumsum(i)/60 for i in fTimes]

fig = plt.figure(figsize=(24, 12))
ax = fig.add_axes([0, 0, 1, 1])
ax.plot(
        list(zip(*cTimes)),
        linewidth=.1
    )
ax.violinplot(
        (list(zip(*cTimes))),
        widths=1, showmedians=True, showmeans=False, showextrema=False,
        positions=range(0, len(cTimes[0]))
    )
fig.savefig('./img/times.png', pad_inches=.1, bbox_inches="tight", dpi=250)
