
import numpy as np
import functions as fun
import matplotlib.pylab as pl
from datetime import timedelta
import matplotlib.pyplot as plt


def plotTimings(tStats, bc=(0, .3, .75), ylim=(80, 150)):
    (tHists, tDevs, tNames) = (
            tStats['hist'], tStats['sd'], tStats['names']
        )
    entries = len(tNames)
    colors = [(fun.scaleDevs(dev, tDevs)/1.25, bc[1], bc[2], .5) for dev in tDevs]
    # Create a figure instance
    fig = plt.figure(figsize=(24, 12))
    # Create an axes instance
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xticks(range(1, len(tNames) + 1))
    ax.set_xticklabels(tNames, rotation=90)
    major_ticks = range(1, entries+1, 1)
    minor_ticks = range(1, entries+1, 4)
    ax.grid(which='both')
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.grid(which='minor', alpha=1)
    ax.grid(which='major', alpha=.5)
    # plt.ylabel('Seconds')
    plt.xticks(fontsize=22.5)
    plt.yticks(fontsize=22.5, rotation=0)
    plt.ylabel('Duration (seconds)', fontsize=50)
    plt.title('Split Time Distributions', fontsize=75)

    # Create the boxplot
    bp = ax.violinplot(
            tHists, widths=.9, showmedians=True, showmeans=False,
            showextrema=False
        )
    for (i, vElement) in enumerate(bp['bodies']):
        vElement.set_facecolor(colors[i])
        vElement.set_alpha(.25)
        # vElement.set_edgecolor((0, 0, 0))
        vElement.set_linewidth(3)
    vp = bp['cmedians']
    vp.set_edgecolor((.3, .3, .3))
    vp.set_linewidth(3)
    vp.set_alpha(.8)
    label = "Total: [Min: {:.2f}, Mean: {:.2f}, Median: {:.2f}, Max: {:.2f}]".format(
            tStats['min'], tStats['mean'], tStats['median'], tStats['max']
        )
    plt.text(
            .5, .975, label, fontsize=25,
            horizontalalignment='center', verticalalignment='center',
            transform=ax.transAxes
        )
    return fig


def plotTraces(traces, fSplit, cTimes, cTimesT, means, names):
    fig = plt.figure(figsize=(24, 12))
    ax = fig.add_axes([0, 0, 1, 1])
    colors = pl.cm.Purples(np.linspace(.05, .95, 1 + len(traces[0])))
    yRange = fun.ceilFloat(max(abs(traces[-1])))
    # Plot traces -------------------------------------------------------------
    for (i, trace) in enumerate(list(zip(*traces))):
        ax.plot(
                trace,
                linewidth=1.5, marker='.', markersize=0,
                color=colors[i], alpha=.75
            )
    # Plot violins ------------------------------------------------------------
    bp = ax.violinplot(
            [i[0] - i[1] for i in zip(cTimesT, means)],
            widths=.75, showmedians=True, showmeans=False, showextrema=False,
            positions=range(0, len(cTimes[0])+1)
        )
    for (i, vElement) in enumerate(bp['bodies']):
        vElement.set_facecolor((0, 0, 1, .5))
        vElement.set_alpha(.05)
        vElement.set_linewidth(1.5)
    vp = bp['cmedians']
    vp.set_edgecolor((.3, .3, .3))
    vp.set_linewidth(3)
    vp.set_alpha(.8)
    # Grids and labels --------------------------------------------------------
    major_ticks = range(0, len(means), 1)
    ax.grid(which='both')
    ax.set_xticks(major_ticks)
    ax.set_yticks([.5 * i for i in range(-4, 4, 1)])
    ax.grid(which='major', alpha=.5)
    ax.set_xticklabels(
            ['{} [{}]'.format(i[1], '%05.2f' % i[0]) for i in zip(means, names)],
            rotation=90
        )
    ax.set_ylim(-yRange, yRange)
    plt.xticks(fontsize=22.5)
    plt.yticks(fontsize=22.5, rotation=0)
    plt.ylabel('Deviation from Mean (minutes)', fontsize=50)
    plt.title('Run Time Distributions', fontsize=75)
    for (i, y) in enumerate(list(traces[-1])):
        x = len(means) - .6
        if i % 2 == 1:
            x = x + 0
        plt.text(
                x, round(y, 4), str(timedelta(minutes=fSplit[i]))[:-4],
                fontsize=9,
                horizontalalignment='left', verticalalignment='center',
                color=colors[i], rotation=0
            )
