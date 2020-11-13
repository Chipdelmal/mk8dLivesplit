from matplotlib.colors import LinearSegmentedColormap

cdict1 = {
    'red':   ((0.0, 0.5, 0.5), (1.0,0.38671875, 0.38671875)),
    'green': ((0.0, 0.5, 0.5), (1.0, 0.27734375, 0.27734375)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 0.99609375, 0.99609375)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, .6, .6)),
}
LightBlue = LinearSegmentedColormap('LightBlue', cdict1)


cdict2 = {
    'red':   ((0.0, 0.1, 0.5), (1.0, 0.92578125, 0.92578125)),
    'green': ((0.0, 0.5, 0.5), (1.0, 0.08984375, 0.08984375)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 0.292968750, 0.29296875)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, .75, .75)),
}
LightRed = LinearSegmentedColormap('LightRed', cdict2)


cdict3 = {
    'red':   ((0.0, 1.00, 1.00), (1.0, 50/255, 50/255)),
    'green': ((0.0, 1.00, 1.00), (1.0, 5/255, 5/255)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 150/255, 150/255)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, .525, .525)),
}
Purple = LinearSegmentedColormap('Purple', cdict3)


cdict4 = {
    'red':   ((0.0, 1, 1), (1.0, 19/250, 19/250)),
    'green': ((0.0, 1, 1), (1.0, 68/250, 68/250)),
    'blue':  ((0.0, 1, 1), (1.0, 184/250, 184/250)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, .75, .75)),
}
Navy = LinearSegmentedColormap('Navy', cdict4)


[i/256 for i in (237, 23, 75)]