from plot.plotting.base.line import *
from matplotlib.axes import Axes
from matplotlib.artist import Artist
from typing import List, Union
from plot.canvas import Canvas


def remove_artist (ax:Axes, gid:str) -> List[Artist]:
    old_artist = list()
    for obj in ax.figure.findobj():
        if obj._gid != None and gid in obj._gid:
            old_artist.append(obj)
            obj.remove()
            print("remove", obj)

    return old_artist

def update_props (from_obj: Union[Line2D], to_obj: Union[Line2D]):        

    exclude = ["xdata","ydata","xydata","data","transform"]

    for _prop in from_obj.properties().keys():
        if _prop not in exclude:
            try:
                to_obj.update({_prop:from_obj.properties()[_prop]})
            except Exception as e:
                pass
                #print('cannot update property', _prop, 'because of', repr(e))
   

def plotting(X, Y, Z, T, ax:Axes, gid:str=None, plot_type:str=None, update=True) -> List[str]:
    
    old_artist = remove_artist(ax, gid)

    # rescale all axes while remove old artist
    for _ax in ax.figure.axes:
        _ax.relim()
        _ax.autoscale_view()
    
    gidlist = list()    

    if plot_type == "2d line":
        artist = line2d(X, Y, ax)
    elif plot_type == "2d step":
        artist = step2d(X, Y, ax)

    
    for ind, obj in enumerate(artist):

        if update:
            try:update_props(old_artist[ind],obj)
            except Exception as e:print(e)

        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

        obj.plot_type = plot_type
        gidlist.append(obj._gid)

        
    
    
    ax.figure.canvas.draw()

    return gidlist