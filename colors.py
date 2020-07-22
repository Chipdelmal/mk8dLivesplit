from matplotlib.colors import LinearSegmentedColormap

cdict2 = {
    'red':   ((0.0, 0.3, 0.3), (1.0, 0.3, 0.3)),
    'green': ((0.0, 0.5, 0.5), (1.0, 0.5, 0.5)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),
}
light_blue1 = LinearSegmentedColormap('LightBlue1', cdict2)

cdict3 = {
    'red':   ((0.0, 0.5, 0.5), (1.0, 0.5, 0.5)),
    'green': ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),
}
purple1 = LinearSegmentedColormap('Purple1', cdict3)
