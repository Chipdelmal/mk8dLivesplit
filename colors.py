from matplotlib.colors import LinearSegmentedColormap

cdict1 = {
    'red':   ((0.0, 0.5, 0.5), (1.0, 0.175, 0.175)),
    'green': ((0.0, 0.5, 0.5), (1.0, 0.175, 0.175)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, .6, .6)),
}
LightBlue = LinearSegmentedColormap('LightBlue', cdict1)


cdict2 = {
    'red':   ((0.0, 0.5, 0.5), (1.0, 237/250, 237/250)),
    'green': ((0.0, 0.5, 0.5), (1.0, 23/250, 23/250)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 75/250, 75/250)),
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
    'red':   ((0.0, 0.5, 0.5), (1.0, 19/250, 19/250)),
    'green': ((0.0, 0.5, 0.5), (1.0, 68/250, 68/250)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 184/250, 184/250)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, .6, .6)),
}
Navy = LinearSegmentedColormap('Navy', cdict4)
