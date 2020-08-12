from matplotlib.colors import LinearSegmentedColormap

cdict2 = {
    'red':   ((0.0, 0.3, 0.3), (1.0, 0.175, 0.175)),
    'green': ((0.0, 0.5, 0.5), (1.0, 0.175, 0.175)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, .6, .6)),
}
LightBlue = LinearSegmentedColormap('LightBlue', cdict2)

cdict3 = {
    'red':   ((0.0, 0.5, 0.5), (1.0, 237/250, 237/250)),
    'green': ((0.0, 0.0, 0.0), (1.0, 40/250, 40/250)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 90/250, 90/250)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, .75, .75)),
}
purple1 = LinearSegmentedColormap('Purple1', cdict3)
