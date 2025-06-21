from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.collections import PathCollection
import matplotlib
from config.settings import GLOBAL_DEBUG

DEBUG = True

def scatter2d (X, Y, ax:Axes, gid, sizes=1, *args, **kwargs) -> tuple[list[PathCollection], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = [1,2]
        Y = [2,5]
    props = {"sizes": sizes}
    artist = ax.scatter(X, Y, gid=gid, s=matplotlib.rcParams["lines.markersize"]**2*sizes, *args, **kwargs)

    artist.Xdata = X
    artist.Ydata = Y
    artist.Xshow = artist.Xdata
    artist.Yshow = artist.Ydata
    
    return [artist], props

def scatter3d(X, Y, Z, ax:Axes3D, gid, sizes=1, depthshade=True, *args, **kwargs) -> tuple[list[PathCollection], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = [1,2]
        Y = [2,5]
        Z = [3,6]
    props = {
        "sizes": sizes,
        "depthshade": depthshade
    }
    artist = ax.scatter(X, Y, Z, gid=gid, depthshade=depthshade,
                        s=matplotlib.rcParams["lines.markersize"]**2*sizes, *args, **kwargs)

    return [artist], props

def bubble2d (X, Y, Z, ax:Axes, gid, sizes=1, *args, **kwargs) -> tuple[list[PathCollection], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = [1,2]
        Y = [2,5]
        Z = [10,15]
    props = {"sizes": sizes}

    artist = ax.scatter(X, Y, s=Z*sizes, gid=gid, *args, **kwargs)

    artist.Xdata = X
    artist.Ydata = Y
    artist.Xshow = artist.Xdata
    artist.Yshow = artist.Ydata

    return [artist], props

def bubble3d (X, Y, Z, T, ax:Axes3D, gid, sizes=1, depthshade=True, *args, **kwargs) -> tuple[list[PathCollection], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = [1,2]
        Y = [2,5]
        Z = [3,6]
        T = [10,15]
    props = {
        "sizes": sizes,
        "depthshade": depthshade
    }
        
    artist = ax.scatter(X, Y, Z, s=T*sizes, gid=gid, depthshade=depthshade, *args, **kwargs)

    return [artist], props