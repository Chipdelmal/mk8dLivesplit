
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

plt.plot(list(zip(*cTimes)))
