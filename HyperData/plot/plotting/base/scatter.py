from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.lines import Line2D
from matplotlib.collections import PathCollection
from typing import List
import matplotlib
import numpy as np

def scatter2d (X, Y, ax:Axes, gid, sizes=1) -> List[PathCollection]:
    
    artist = ax.scatter(X, Y, gid=gid, s=matplotlib.rcParams["lines.markersize"]**2*sizes)

    artist.sizes = sizes
    
    return [artist]

def scatter3d(X, Y, Z, ax:Axes3D, gid, sizes=1, depthshade=True) -> List[PathCollection]:
    
    artist = ax.scatter(X, Y, Z, gid=gid, depthshade=depthshade,
                        s=matplotlib.rcParams["lines.markersize"]**2*sizes)

    artist.sizes = sizes
    artist.depthshade = depthshade

    return [artist]

def bubble2d (X, Y, Z, ax:Axes, gid, sizes=1) -> List[PathCollection]:

    artist = ax.scatter(X, Y, s=Z*sizes, gid=gid)

    artist.sizes = sizes

    return [artist]

def bubble3d (X, Y, Z, T, ax:Axes3D, gid, sizes=1, depthshade=True) -> List[PathCollection]:

    artist = ax.scatter(X, Y, Z, s=T*sizes, gid=gid, depthshade=depthshade)

    artist.sizes = sizes
    artist.depthshade = depthshade

    return [artist]