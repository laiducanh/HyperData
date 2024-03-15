from plot.plotting.base.line import *
from matplotlib.axes import Axes
from typing import List

def plotting(X=list(), Y=list(), Z=list(), T=list(), ax:Axes=None, gid:str=None, plot_type:str=None) -> List[str]:
    
    old_artist = list()
    for obj in ax.figure.findobj():
        if obj._gid != None and gid in obj._gid:
            old_artist.append(obj)
            obj.remove()

    gidlist = list()    

    if plot_type == "2d line":
        artist = line2d(X, Y, ax)
    elif plot_type == "2d step":
        artist = step2d(X, Y, ax)

    
    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)
        obj.plot_type = plot_type
        gidlist.append(obj._gid)
        try:obj.update_from(old_artist[ind])
        except:pass
    
    ax.relim()
    ax.autoscale() # use autoscale_view if the axis lim is set before
    ax.figure.canvas.draw()

    return gidlist