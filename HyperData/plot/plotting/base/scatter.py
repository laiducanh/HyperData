from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import PathCollection
from typing import List
import matplotlib

def scatter2d (X, Y, ax:Axes, gid, sizes=1) -> List[PathCollection]:

    artist = ax.scatter(X, Y, gid=gid, s=matplotlib.rcParams["lines.markersize"]**2*sizes)

    artist.sizes = sizes
    
    return [artist]

def bubble (X, Y, Z, ax:Axes, gid, sizes=1) -> List[PathCollection]:

    artist = ax.scatter(X, Y, s=Z*sizes, gid=gid)

    artist.sizes = sizes

    return [artist]