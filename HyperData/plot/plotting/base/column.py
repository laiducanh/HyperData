from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from typing import List

def column2d (X, Y, ax:Axes, gid) -> BarContainer:

    artist = ax.bar(X, Y, gid=gid)
    
    return artist