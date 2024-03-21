from plot.plotting.base.line import *
from plot.plotting.base.column import *
from plot.plotting.base.scatter import *
from plot.plotting.base.pie import *
from matplotlib.axes import Axes
from matplotlib.artist import Artist
from typing import List, Union
from plot.canvas import Canvas


def remove_artist (ax:Axes, gid:str) -> List[Artist]:
    #print('remove artist')
    old_artist = list()
    for obj in ax.figure.findobj():
        if obj._gid != None and gid in obj._gid:
            old_artist.append(obj)
            obj.remove()
            #print("remove", obj, obj._gid)

    return old_artist

def update_props (from_obj: Union[Line2D], to_obj: Union[Line2D]):        
    #print("update props")
    exclude = ["xdata","ydata","xydata","data","transform","paths","height","width","offsets",
               "offset_transform","sizes","x","y","xy"]

    for _prop in from_obj.properties().keys():
        if _prop not in exclude:
            try:
                to_obj.update({_prop:from_obj.properties()[_prop]})
                #print("update", _prop, "value", from_obj.properties()[_prop])
            except Exception as e:
                pass
                #print('cannot update property', _prop, 'because of', repr(e))
   

def plotting(X, Y, Z, T, ax:Axes, gid:str=None, plot_type:str=None, update=True, **kwargs) -> List[str]:
    
    old_artist = remove_artist(ax, gid)

    # rescale all axes while remove old artists and add new artists
    for _ax in ax.figure.axes:
        _ax.relim()
        _ax.autoscale_view()
    
    gidlist = list()    

    if plot_type == "treemap":
        # treemap cannot update props from old artists
        artist = treemap(X, ax, gid, **kwargs)

    else:

        if plot_type == "2d line":
            artist = line2d(X, Y, ax, gid, **kwargs)
        elif plot_type == "2d step":
            artist = step2d(X, Y, ax, gid, **kwargs)
        elif plot_type == "2d area":
            artist = fill_between(X, Y, 0, ax, gid, **kwargs)
        elif plot_type == "fill between":
            artist = fill_between(X, Y, Z, ax, gid, **kwargs)
        elif plot_type == "2d stacked area":
            artist = stackedarea(X, Y, ax, gid, **kwargs)
        elif plot_type == "2d 100% stacked area":
            artist = stackedarea100(X, Y, ax, gid, **kwargs)
        elif plot_type == "2d column":
            artist = column2d(X, Y, ax, gid, **kwargs)
        elif plot_type == "2d clustered column":
            artist = clusteredcolumn2d(X, Y, ax, gid, **kwargs)
        elif plot_type == "2d stacked column":
            artist = stackedcolumn2d(X, Y, ax, gid, **kwargs)
        elif plot_type == "2d 100% stacked column":
            artist = stackedcolumn2d100(X, Y, ax, gid, **kwargs)
        elif plot_type == "marimekko":
            artist = marimekko(X, ax, gid, **kwargs)
        elif plot_type == "2d scatter":
            artist = scatter2d(X, Y, ax, gid, **kwargs)
        elif plot_type == "bubble":
            artist = bubble(X, Y, Z, ax, gid, **kwargs)
        elif plot_type == "pie":
            artist = pie(X, ax, gid, **kwargs)
        elif plot_type == "doughnut":
            artist = doughnut(X, ax, gid, **kwargs)
        
        #print("draw artist", artist)
        
        for ind, obj in enumerate(artist):
            if update:
                try:update_props(old_artist[ind],obj)
                except Exception as e:print(e)
    
    
    for ind, obj in enumerate(artist):

        obj.plot_type = plot_type
        gidlist.append(obj._gid)

    # remove duplicates in gidlist
    gidlist = list(set(gidlist))
    #print("finish plotting", gidlist)
    
    ax.figure.canvas.draw()

    return gidlist