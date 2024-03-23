from plot.plotting.base.line import *
from plot.plotting.base.column import *
from plot.plotting.base.scatter import *
from plot.plotting.base.pie import *
from matplotlib.axes import Axes
from matplotlib.artist import Artist
from typing import List, Union, Literal
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

def update_props (from_obj: Union[Line2D], to_obj: Union[Line2D], 
                  include=list(), exclude:Literal["default",None]="default"):        
    #print("update props")
    if exclude == None:
        exclude = from_obj.properties().keys()
    else:
        exclude = ["xdata","ydata","xydata","data","transform","paths","height","width","offsets",
               "offset_transform","sizes","x","y","xy","gid"]

    for _prop in from_obj.properties().keys():
        if _prop not in exclude or _prop in include:
            try:
                to_obj.update({_prop:from_obj.properties()[_prop]})
                #print("update", _prop, "value", from_obj.properties()[_prop])
            except Exception as e:
                pass
                #print('cannot update property', _prop, 'because of', repr(e))

def set_legend(ax:Axes):
    _artist = list()
    _gid = list()
    _label = list()
    
    for obj in ax.figure.findobj(match=Artist):
        if obj._gid != None and "graph" in obj._gid and obj._gid not in _gid:
            _gid.append(obj._gid)
            _artist.append(obj)
            _label.append(obj._label)
    for ind, val in enumerate(_label):
        if val.startswith("_"):
            _label.pop(ind)
            _artist.pop(ind)

    ax_leg = None
    for _ax in ax.figure.axes:
        if _ax.get_legend():
           ax_leg = _ax # get the axis for legend
           break
    
    if ax_leg != None: ax_leg.get_legend().remove()
    if _artist != []:
        ax_leg.legend(handles=_artist,draggable=True)

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
            update_props(old_artist[ind], obj, include=["label"], exclude=None)
            if update:
                update_props(old_artist[ind],obj,exclude="default")
    
    # update legend if necessary
    set_legend(ax)

    for ind, obj in enumerate(artist):

        obj.plot_type = plot_type
        gidlist.append(obj._gid)

    # remove duplicates in gidlist
    gidlist = list(set(gidlist))
    #print("finish plotting", gidlist)
    
    ax.figure.canvas.draw()

    return gidlist