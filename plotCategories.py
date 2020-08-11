
import numpy as np
import auxFunctions as aux
import dataFunctions as fun
import matplotlib.pylab as pl
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def plotCategoryHeatmap(
            fshdRunHistoryCml, fshdRunID, cmap=pl.cm.Purples,
            fontsize=12, rnd=2,
            fontColor='k', lineColor='k', lineWidth=.5
        ):
    catTimes = [fun.getMK8DCategories(fshdRunHistoryCml, i) for i in fshdRunID]
    cat = list(catTimes[0].keys())
    timesGrid = np.array([[run[c] for run in catTimes] for c in cat])
    runsNum = len(timesGrid[0])
    # Empty array for the data
    nTimesArrays = np.empty(timesGrid.shape)
    for (i, row) in enumerate(timesGrid):
        nTimesArrays[i] = aux.NormalizeData(row)
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.matshow(
            nTimesArrays.T, cmap=cmap,
            norm=LogNorm(vmin=0.05, vmax=1), aspect="auto"
        )
    # We want to show all ticks...
    ax.set_yticks(np.arange(runsNum))
    ax.set_xticks(np.arange(len(cat)))
    # ... and label them with the respective list entries
    runsNumStr = [str(i+1).zfill(2) for i in range(runsNum)]
    ylab = ['[{} id:{}]'.format(i[1], i[0]) for i in zip(fshdRunID, runsNumStr)]
    ax.set_yticklabels(ylab, fontsize=10)
    ax.set_xticklabels(cat, fontsize=12)
    ax.set_title("Categories Timing", fontsize=30)
    ax.xaxis.set_ticks_position('bottom')
    for j in range(runsNum):
        plt.axhline(j+.5, color='w', linestyle='solid', lw=lineWidth)
    for i in range(len(cat)):
        plt.axvline(i+.5, color=lineColor, linestyle='solid', lw=lineWidth)
    for i in np.arange(len(cat)):
        for j in np.arange(runsNum):
            ax.text(
                    i, j, str(timedelta(seconds=timesGrid[i, j]))[2:-4],
                    ha="center", va="center", color=fontColor,
                    fontsize=fontsize, rotation=0
                )
    return (fig, ax)
