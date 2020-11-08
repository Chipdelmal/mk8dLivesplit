
import sys
import pandas as pd
import colors as cl
import seaborn as sns
import plotViolin as pv
import plotTraces as pt
import plotHeatmap as hea
import auxFunctions as aux
import dataFunctions as fun
import plotCategories as cap
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import plotly.graph_objects as go



# (FILE, OUT, VOFF) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (DPI, PAD, TYP, VOFF) = (250, .1, 'png', 30)
TYP = 'png'
(FILE_D, FILE_C, OUT, VOFF) = (
        './dta/Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss',
        './dta/Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss',
        '/home/chipdelmal/Documents/MK8D/Livesplit/', 35
    )
###############################################################################
# Read File
###############################################################################
print('* Reading file...')
(segD, segC) = [fun.getSegmentsFromFile(i) for i in (FILE_D, FILE_C)]
###############################################################################
# Shape Runs Data
###############################################################################
print('* Calculating stats...')
runsHS = [fun.getRunHistStats(i) for i in (segD, segC)]
###############################################################################
# Plot Data
###############################################################################
# Empty dataframe -------------------------------------------------------------
columns = ['Track', 'Time', 'Version']
ver = ['Digital', 'Cartridge']
df = pd.DataFrame(columns=columns)
# Populate dataframe ----------------------------------------------------------
for hist in range(len(runsHS)):
    tracksHist = runsHS[hist][0]
    tracks = list(tracksHist.keys())
    # Append entries ----------------------------------------------------------
    for track in tracks:
        times = list(tracksHist[track].values())
        for time in times:
            df = df.append(
                {
                    'Track': track, 
                    'Time': time, 
                    'Version': ver[hist]
                }, 
                ignore_index=True
            )
# Plot ------------------------------------------------------------------------
# fig = plt.figure(figsize=(24, 12))
# ax = sns.violinplot(
#     x="Time", y="Track", hue="Version",
#     data=df, palette="Set2", split=True,
#     inner="stick"
# )
# aux.saveFig(fig, '{}violinSplits.{}'.format(OUT, TYP), dpi=500)
# Plot ------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Violin(x=df['Track'][ df['Version'] == 'Digital' ],
                        y=df['Time'][ df['Version'] == 'Digital' ],
                        legendgroup='Yes', scalegroup='Yes', name='Yes',
                        side='negative',
                        line_color='blue')
             )
fig.add_trace(go.Violin(x=df['Track'][ df['Version'] == 'Cartridge' ],
                        y=df['Time'][ df['Version'] == 'Cartridge' ],
                        legendgroup='No', scalegroup='No', name='No',
                        side='positive',
                        line_color='orange')
             )