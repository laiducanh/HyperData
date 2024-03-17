from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import PathCollection
from typing import List

def scatter2d (X, Y, ax:Axes, gid) -> List[PathCollection]:

    artist = ax.scatter(X, Y, gid=gid)
    
    return [artist]

def bubble (X, Y, Z, ax:Axes, gid) -> List[PathCollection]:

    artist = ax.scatter(X, Y, Z, gid=gid)

    return [artist]