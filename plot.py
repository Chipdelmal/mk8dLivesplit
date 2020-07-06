
import six
import numpy as np
import pandas as pd
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
    # ax.set_xlim(-1, len(tNames) + 2)
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
            tHists, widths=.9, showmedians=True, showmeans=True,
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
    vp = bp['cmeans']
    vp.set_edgecolor((.3, .3, .3))
    vp.set_linewidth(.75)
    vp.set_alpha(.75)
    # tSts = (tStats['min'], tStats['mean'], tStats['median'], tStats['max'])
    # tms = [fun.minsToHr(i, prec=-7) for i in tSts]
    # label = "Total: [Min: {}, Mean: {}, Median: {}, Max: {}]".format(
    #         tms[0], tms[1], tms[2], tms[3]
    #     )
    # plt.text(
    #         .5, .975, label, fontsize=40,
    #         horizontalalignment='center', verticalalignment='center',
    #         transform=ax.transAxes, color=(0, 0, 0, .25)
    #     )
    return fig


def plotTraces(
            traces, fSplit, cTimes, cTimesT, means, names, yRange=1,
            vNames=None,
            cmap=pl.cm.Purples
        ):
    # Stats ...................................................................
    tSts = (
            np.min(fSplit), np.mean(fSplit),
            np.median(fSplit), np.max(fSplit)
        )
    tms = [fun.minsToHr(i, prec=-4) for i in tSts]
    labelMean = "{}".format(tms[1])
    labelMedian = "{}".format(tms[2])
    # Fig ---------------------------------------------------------------------
    fig = plt.figure(figsize=(24, 12))
    ax = fig.add_axes([0, 0, 1, 1])
    colors = cmap(np.linspace(.05, 1, 1 + len(traces[0])))
    # yRange = fun.ceilFloat(max(abs(traces[-1])))
    # Plot traces -------------------------------------------------------------
    for (i, trace) in enumerate(list(zip(*traces))):
        ax.plot(
                trace,
                linewidth=1.5, marker='.', markersize=0,
                color=colors[i], alpha=.5
            )
    # Plot violins ------------------------------------------------------------
    bp = ax.violinplot(
            [i[0] - i[1] for i in zip(cTimesT, means)],
            widths=.75, showmedians=True, showmeans=True, showextrema=False,
            positions=range(0, len(cTimes[0])+1)
        )
    for (i, vElement) in enumerate(bp['bodies']):
        vElement.set_facecolor((0, 0, 1, .5))
        vElement.set_alpha(.035)
        vElement.set_linewidth(1.5)
    vp = bp['cmedians']
    vp.set_edgecolor((.3, .3, .3))
    vp.set_linewidth(3)
    vp.set_alpha(.8)
    vp = bp['cmeans']
    vp.set_edgecolor((.3, .3, .3))
    vp.set_linewidth(1.25)
    vp.set_alpha(.75)
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
    ax.set_xlim(-2, len(cTimesT) + 2)
    plt.xticks(fontsize=22.5)
    plt.yticks(fontsize=22.5, rotation=0)
    plt.ylabel('Deviation from Mean (minutes)', fontsize=50)
    plt.title('Run Time', fontsize=75)
    for (i, y) in enumerate(list(traces[-1])):
        x = len(means) - .6
        if i % 2 == 1:
            x = x + 0
        plt.text(
                x, round(y, 4), str(timedelta(minutes=fSplit[i]))[:-4],
                fontsize=13,
                horizontalalignment='left', verticalalignment='center',
                color=colors[i], rotation=0
            )
    plt.text(
            x, 0, labelMean, fontsize=13,
            horizontalalignment='left', verticalalignment='center',
            color=(0, 0, 0, .25)
        )
    plt.text(
            x, tSts[2]-tSts[1], labelMedian, fontsize=13,
            horizontalalignment='left', verticalalignment='center',
            color=(0, 0, 0, .5)
        )
    # VLines ------------------------------------------------------------------
    if vNames is not None:
        vLinesLst = [names.index(name) for name in vNames]
        vLinesLst.extend([0])
        for vlin in vLinesLst:
            plt.vlines(
                    vlin, -yRange, yRange, linestyles="dashed",
                    colors=(.5, 0, 0, .4)
                )
    return fig


def renderTable(
            data, minPos=None, col_width=3.0, row_height=0.625, font_size=14,
            header_color='#40466e', row_colors=['#f1f1f2', 'w'],
            edge_color='w', bbox=[0, 0, 1, 1], header_columns=0,
            ax=None, **kwargs
        ):
    # #########################################################################
    # https://stackoverflow.com/questions/26678467/export-a-pandas-dataframe-as-a-table-image
    # #########################################################################
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(
            cellText=data.values, bbox=bbox, colLabels=data.columns,
            cellLoc='center', **kwargs
        )
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    if minPos is not None:
        for ix in minPos:
            mpl_table[ix].set_facecolor("#56b5fd50")
    return fig
