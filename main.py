
import plot
import xmltodict
import functions as fun


(PATH, FILE) = (
        './dta/',
        'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
    )

with open(PATH+FILE) as fd:
    doc = xmltodict.parse(fd.read())
tStats = fun.getSegmentStats(doc)
fig = plot.plotTimings(tStats)
fig.savefig('./img/violin.png', pad_inches=.1, bbox_inches="tight", dpi=250)
