

import numpy as np
import auxFunctions as aux
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def plotSplitsHeatmap(
            fshdRunHistory, cmap=pl.cm.Purples, fontsize=2.5, rnd=2,
            fontColor='k', lineColor='k', lineWidth=.5
        ):
    tNames = list(fshdRunHistory.keys())
    runsNum = len(fshdRunHistory.get(tNames[0]))
    rIds = list(fshdRunHistory[tNames[0]].keys())

    track = []
    for trackName in tNames:
        track.append(list(fshdRunHistory[trackName].values()))
    timesArrays = np.array(track)

    nTimesArrays = np.empty(timesArrays.shape)
    for (i, row) in enumerate(timesArrays):
        nTimesArrays[i] = aux.NormalizeData(row)

    fig, ax = plt.subplots()
    ax.matshow(nTimesArrays.T, cmap=cmap, norm=LogNorm(vmin=0.05, vmax=1))
    # We want to show all ticks...
    ax.set_yticks(np.arange(runsNum))
    ax.set_xticks(np.arange(len(tNames)))
    # ... and label them with the respective list entries
    ax.set_yticklabels(rIds, fontsize=5)
    ax.set_xticklabels(tNames, fontsize=7)
    # Rotate the tick labels and set their alignment.
    ax.xaxis.set_ticks_position('bottom')
    plt.setp(
            ax.get_xticklabels(), rotation_mode="anchor",
            rotation=90, ha="right", va="center"
        )
    for i in range(len(tNames)):
        plt.axvline(i+.5, color=lineColor, linestyle='solid', lw=lineWidth)
    # Loop over data dimensions and create text annotations.
    for i in np.arange(len(tNames)):
        for j in np.arange(runsNum):
            ax.text(
                    i, j, round(timesArrays[i, j], rnd),
                    ha="center", va="center", color=fontColor,
                    fontsize=fontsize, rotation=45
                )
    ax.set_title("Tracks Timing")
    fig.tight_layout()
    return (fig, ax)
