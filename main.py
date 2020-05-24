
import xmltodict
import functions as fun
from datetime import datetime
import matplotlib.pyplot as plt


(PATH, FILE) = (
        '/home/chipdelmal/Documents/Github/MarioKart8DeluxeSpeedruns/Splits/',
        '03 - Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
    )

with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())

doc['Run']
gameName = doc['Run']['GameName']
segment = doc['Run']['Segments']['Segment']

len(segment)

(tNames, tHists) = ([], [])
for track in range(len(segment)):
    (tName, tHistory) = fun.getTrackHistory(segment[track])
    (tNames.append(tName), tHists.append(tHistory))


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
ax.grid(which='major', alpha=.1)
# Create the boxplot
bp = ax.violinplot(tHists, widths=1)
fig.savefig('./img/violin.png', pad_inches=.1, bbox_inches="tight")
