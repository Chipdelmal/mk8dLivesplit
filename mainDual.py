
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
# Read Files
###############################################################################
print('* Reading file...')
(segD, segC) = [fun.getSegmentsFromFile(i) for i in (FILE_D, FILE_C)]
###############################################################################
# Shape Runs Data
###############################################################################
print('* Calculating stats...')
runsHS = [fun.getRunHistStats(i) for i in (segC, segD)]
runsDF = fun.getRunsDataframe(runsHS)
###############################################################################
# Plot Data
###############################################################################
# Plot ------------------------------------------------------------------------
# fig = plt.figure(figsize=(24, 12))
# ax = sns.violinplot(
#     x="Time", y="Track", hue="Version",
#     data=df, palette="Set2", split=True,
#     inner="stick"
# )
# aux.saveFig(fig, '{}violinSplits.{}'.format(OUT, TYP), dpi=500)
# Web Violin ------------------------------------------------------------------
df = runsDF
ver = ('Digital', 'Cartridge')
tracks = df['Track'].unique()
fig = go.Figure()
fig.add_trace(go.Violin(
    x=df['Track'][df['Version']== ver[0]],
    y=df['Time'][df['Version']==ver[0]],
    legendgroup=ver[0], line={'width': .75},
    scalegroup=ver[0], name=ver[0], side='negative',
    line_color='blue', points=False, spanmode='hard'
))
fig.add_trace(go.Violin(
    x=df['Track'][df['Version']==ver[1]],
    y=df['Time'][df['Version']==ver[1]],
    legendgroup=ver[1], line={'width': .75},
    scalegroup=ver[1], name=ver[1], side='positive',
    line_color='purple', points=False, spanmode='hard'
))
fig.update_traces(
    orientation='v', meanline_visible=True, width=1, points=False
)
fig.update_layout(
    violingap=0, violinmode='overlay', hovermode="x",
    autosize=True, width=1250, height=600,
    margin=go.layout.Margin(l=1, r=1, b=1, t=1, pad=0),
    legend=dict(
        yanchor="top", y=0.99,
        xanchor="left", x=0.01
    ),
    hoverlabel=dict(font_size=12)
)
fig.update_xaxes(range=[-.5, len(tracks)-.5])
# fig.show()
fig.write_html('{}violins.html'.format(OUT))
# Web Traces ------------------------------------------------------------------
versions = ['Digital', 'Cartridge']
verIx = versions[0]
# Version loop ----------------------------------------------------------------
fshdIDs = fun.getFinishedRunsIDs(runsDF, finalTrack='Big Blue', version=verIx)
dfOut = pd.DataFrame(columns=['Track', 'ID', 'Time', 'Version'])
tracks = list(runsDF['Track'].unique()) 
# Tracks loop -----------------------------------------------------------------
tracks 
track = tracks[0]
fltr = zip(
    runsDF['Track'] == track, 
    runsDF['Version'] == 'Digital', 
    [runsDF['ID'].iloc[i] in set(fshdIDs) for i in range(df.shape[0])]
)
print(runsDF[[all(i) for i in fltr]])
dfOut = df.append(runsDF[[all(i) for i in fltr]])


