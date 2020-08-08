
from matplotlib import colors
import matplotlib.pylab as pl
import matplotlib.pyplot as plt


###############################################################################
# Constants
###############################################################################
ylim = (50, 150)
vStyle = {
        'color': pl.cm.Purples_r, 'alpha': .4, 'width': .65,
        'lw': 3, 'lc': (0, 0, 0)
    }
bgStyle = {
        'bandSize': 4,
        'bandColorA': 'blue', 'bandAlphaA': 0.025,
        'bandColorB': 'white', 'bandAlphaB': 0.025,
        'gridColor': (.3, .3, .3), 'gridAlpha': .05,
        'xtickSize': 22.5, 'ytickSize': 22.5, 'labelsSize': 75
    }
meanStyle = {'color': (.3, .3, .3), 'alpha': .65, 'width': .8}
medianStyle = {'color': (.3, .3, .3), 'alpha': .85, 'width': 3}


###############################################################################
# Violin
###############################################################################
def plotSegmentViolins(
            runsHistory, runsStats,
            ylim=ylim, vStyle=vStyle, bgStyle=bgStyle,
            meanStyle=meanStyle, medianStyle=medianStyle
        ):
    # Preprocess --------------------------------------------------------------
    tNames = list(runsHistory.keys())
    tNum = len(tNames)
    tTimes = [list(runsHistory.get(track).values()) for track in tNames]
    tSDs = [runsStats.get(track).get('SD') for track in tNames]
    # Setup figure and axes ---------------------------------------------------
    fig = plt.figure(figsize=(24, 12))
    ax = fig.add_axes([0, 0, 1, 1])
    # Violin plot -------------------------------------------------------------
    bp = ax.violinplot(
            tTimes, widths=vStyle['width'],
            showmedians=True, showmeans=True, showextrema=False
        )
    # Medians and Means style -------------------------------------------------
    vp = bp['cmedians']
    vp.set_edgecolor(medianStyle['color'])
    vp.set_linewidth(medianStyle['width'])
    vp.set_alpha(medianStyle['alpha'])
    vp = bp['cmeans']
    vp.set_edgecolor(meanStyle['color'])
    vp.set_linewidth(meanStyle['width'])
    vp.set_alpha(meanStyle['alpha'])
    # Grids -------------------------------------------------------------------
    ax.grid(which='both')
    major_ticks = range(1, tNum+1, 1)
    ax.set_xticks(major_ticks)
    ax.grid(
            which='major', zorder=0,
            color=bgStyle['gridColor'], alpha=bgStyle['gridAlpha']
        )
    delta = bgStyle['bandSize']
    for i in range(0, tNum, delta):
        if i % (2 * delta) == 0:
            (clr, alp) = (bgStyle['bandColorA'], bgStyle['bandAlphaA'])
        else:
            (clr, alp) = (bgStyle['bandColorB'], bgStyle['bandAlphaB'])
        ax.axvspan(i+0.5, i+delta+0.5, zorder=0, color=clr, alpha=alp)
    # Colors ------------------------------------------------------------------
    (cmap, norm) = (vStyle['color'], colors.Normalize(vmin=0, vmax=max(tSDs)))
    vColors = cmap(norm(tSDs))
    for (i, vElement) in enumerate(bp['bodies']):
        vElement.set_facecolor(vColors[i])
        vElement.set_alpha(vStyle['alpha'])
        vElement.set_edgecolor(vStyle['lc'])
        vElement.set_linewidth(vStyle['lw'])
    # Labels ------------------------------------------------------------------
    plt.xticks(fontsize=bgStyle['xtickSize'])
    plt.yticks(fontsize=bgStyle['ytickSize'], rotation=0)
    ax.set_xticklabels(tNames, rotation=90)
    plt.ylabel('Duration (seconds)', fontsize=bgStyle['labelsSize'] * .75)
    plt.title('Split Time Distributions', fontsize=bgStyle['labelsSize'])
    # Ranges ------------------------------------------------------------------
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlim(.25, tNum+.75)
    return (fig, ax)
