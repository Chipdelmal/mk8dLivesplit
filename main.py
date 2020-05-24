
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
fig = plt.figure()
# Create an axes instance
ax = fig.add_axes([0, 0, 1, 1])
ax.set_ylim(80, 150)
ax.set_xticks(range(1, len(tNames) + 1))
ax.set_xticklabels(tNames, rotation=90)
# Create the boxplot
bp = ax.violinplot(tHists)
plt.show()
