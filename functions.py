
import statistics as stats
from datetime import datetime
import matplotlib.pyplot as plt

REFT = datetime(1900, 1, 1, 0, 0, 0, 0)


def tdToSec(tDelta):
    micro = 1000000
    tm = (tDelta.seconds) + (tDelta.microseconds / micro)
    return tm


def getTrackHistory(segmentTrack):
    (tName, timesHistory) = (segmentTrack['Name'], [])
    for hist in segmentTrack['SegmentHistory']['Time']:
        if len(hist) > 1:
            tStr = hist['RealTime']
            tDiff = timeToSecs(tStr, refTime=REFT)
            timesHistory.append(tDiff)
    return (tName, timesHistory)


def scaleDevs(x, tDevs):
    return (x - min(tDevs)) / (max(tDevs) - min(tDevs))


def getEndRunIds(segment):
    endTimesDict = segment[-1]['SegmentHistory']['Time']
    endRunIds = [ts['@id'] for ts in endTimesDict]
    return set(endRunIds)


def timeToSecs(tStr, refTime=REFT):
    trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
    tDiff = tdToSec(trackTiming - REFT)
    return tDiff


def filterFinishedSegments(track, endRId, reft=REFT):
    trackSplits = []
    segHist = track['SegmentHistory']['Time']
    for rHist in segHist:
        if rHist['@id'] in endRId:
            splitTime = timeToSecs(rHist['RealTime'])
            trackSplits.append(splitTime)
    return trackSplits


def finishedRunsTimes(segment):
    endRId = getEndRunIds(segment)
    fRun = []
    for segmentTrack in segment:
        fTime = filterFinishedSegments(segmentTrack, endRId, reft=REFT)
        fRun.append(fTime)
    return (list(zip(*fRun)))


def getSegmentStats(doc):
    segment = doc['Run']['Segments']['Segment']
    (tNames, tHists, tDevs, tMin, tMedian, tMean, tMax) = (
            [], [], [], [], [], [], []
        )
    for track in range(len(segment)):
        (tName, tHistory) = getTrackHistory(segment[track])
        tNames.append(tName)
        tHists.append(tHistory)
        tDevs.append(stats.stdev(tHistory))
        tMin.append(min(tHistory))
        tMean.append(stats.mean(tHistory))
        tMedian.append(stats.median(tHistory))
        tMax.append(max(tHistory))
    tStats = {
            'min': sum(tMin)/60, 'median': sum(tMedian)/60,
            'max': sum(tMax)/60, 'mean': sum(tMean)/60,
            'sd': tDevs, 'hist': tHists, 'names': tNames
        }
    return tStats


def plotTimings(tStats, bc=(0, .3, .75), ylim=(80, 150)):
    (tHists, tDevs, tNames) = (
            tStats['hist'], tStats['sd'], tStats['names']
        )
    entries = len(tNames)
    colors = [(scaleDevs(dev, tDevs)/1.25, bc[1], bc[2], .5) for dev in tDevs]
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
            tHists, widths=1, showmedians=True, showmeans=False,
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
