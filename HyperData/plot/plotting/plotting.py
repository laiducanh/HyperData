from plot.plotting.base.line import *
from plot.plotting.base.column import *
from plot.plotting.base.scatter import *
from plot.plotting.base.pie import *
from plot.plotting.base.stats import *
from config.settings import GLOBAL_DEBUG, logger
from plot.utilis import find_mpl_object
from plot.canvas import Canvas
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.collections import Collection
from matplotlib.patches import Rectangle, Wedge, PathPatch
from matplotlib.legend import Legend
from matplotlib.font_manager import FontProperties
from typing import List, Union, Literal

DEBUG = True

def remove_artist (ax:Axes, gid:str) -> List[Artist]:
    artist_removed = list()
    for artist in find_mpl_object(figure=ax.figure,match=[Artist],gid=gid):
        artist.remove()
        if GLOBAL_DEBUG or DEBUG:
            pass
    return artist_removed

def update_props (from_obj: Artist, to_obj: Artist, 
                  include=list(), exclude:Literal["default",None]="default") -> None:  
    try:      
        #print("update props")
        print(to_obj, from_obj)
        to_obj_props = to_obj.properties()
        from_obj_props = from_obj.properties()

        to_obj.update_from(from_obj)

        # for step plots
        if isinstance(to_obj, Line2D):
            to_obj.set(drawstyle=to_obj_props.get("drawstyle"))
        
    except Exception as e:
        logger.exception(e)

def get_legend(canvas: Canvas) -> Legend:
    return canvas.axesleg.get_legend()

def set_legend(canvas: Canvas, *args, **kwargs):
    try:
        _handles = canvas.axes.get_legend_handles_labels()[0]   + \
                canvas.axesx2.get_legend_handles_labels()[0] + \
                canvas.axesy2.get_legend_handles_labels()[0] + \
                canvas.axespie.get_legend_handles_labels()[0]
        _labels = canvas.axes.get_legend_handles_labels()[1]   + \
                canvas.axesx2.get_legend_handles_labels()[1] + \
                canvas.axesy2.get_legend_handles_labels()[1] + \
                canvas.axespie.get_legend_handles_labels()[1]
        old_title = None

        if get_legend(canvas): 
            old_title = get_legend(canvas).get_title()
            get_legend(canvas).remove()
        if _handles != []:
            _legend = canvas.axesleg.legend(_handles, _labels, draggable=True, *args, *kwargs)
            if old_title: 
                _legend.set_title(old_title.get_text())
                _legend.get_title().update_from(old_title)
            canvas.draw()
    except Exception as e:
        logger.exception(e)

def _set_legend(ax:Axes):
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
    
    if ax_leg: 
        ax_leg.get_legend().remove()
        if _artist != []:
            ax_leg.legend(handles=_artist,draggable=True)

def rescale_plot(figure:Figure) -> None:
    for _ax in figure.axes:
        _ax.relim()
        _ax.autoscale()    

def plotting(X, Y, Z, T, ax:Axes, gid:str=None, plot_type:str=None, **kwargs) -> List[Artist]:
    
    # get old artist that will be replaced
    # but its properties will apply to the new ones
    artist_old = find_mpl_object(ax.figure,
                                 match=[Line2D,Collection,Rectangle,Wedge,PathPatch],
                                 gid=gid)
    
    remove_artist(ax, gid)
    
    # rescale all axes while remove old artists and add new artists
    rescale_plot(ax.figure)
    
    match plot_type:
        case "2d line":                 artist = line2d(X, Y, ax, gid, **kwargs)
        case "2d step":                 artist = step2d(X, Y, ax, gid, **kwargs)
        case "2d stem":                 artist = stem2d(X, Y, ax, gid, **kwargs)
        case "2d area":                 artist = fill_between(X, Y, 0, ax, gid, **kwargs)
        case "fill between":            artist = fill_between(X, Y, Z, ax, gid, **kwargs)
        case "2d stacked area":         artist = stackedarea(X, Y, ax, gid, **kwargs)
        case "2d 100% stacked area":    artist = stackedarea100(X, Y, ax, gid, **kwargs)
        case "2d column":               artist = column2d(X, Y, ax, gid, **kwargs)
        case "2d clustered column":     artist = clusteredcolumn2d(X, Y, ax, gid, **kwargs)
        case "2d stacked column":       artist = stackedcolumn2d(X, Y, ax, gid, **kwargs)
        case "2d 100% stacked column":  artist = stackedcolumn2d100(X, Y, ax, gid, **kwargs)
        case "marimekko":               artist = marimekko(X, ax, gid, **kwargs)
        case "treemap":                 artist = treemap(X, ax, gid, **kwargs)
        case "2d scatter":              artist = scatter2d(X, Y, ax, gid, **kwargs)
        case "2d bubble":               artist = bubble2d(X, Y, Z, ax, gid, **kwargs)
        case "pie":                     artist = pie(X, ax, gid, **kwargs)
        case "doughnut":                artist = doughnut(X, ax, gid, **kwargs)
        case "histogram":               artist = histogram(X, ax, gid, **kwargs)
        case "stacked histogram":       artist = stacked_histogram(X, ax, gid, **kwargs)
        case "boxplot":                 artist = boxplot(X, ax, gid, **kwargs)
        case "violinplot":              artist = violinplot(X, ax, gid, **kwargs)
        case "eventplot":               artist = eventplot(X, ax, gid, **kwargs)
        case "hist2d":                  artist = hist2d(X, Y, ax, gid, **kwargs)

        case "3d line":                 artist = line3d(X, Y, Z, ax, gid, **kwargs)
        case "3d step":                 artist = step3d(X, Y, Z, ax, gid, **kwargs)
        case "3d stem":                 artist = stem3d(X, Y, Z, ax, gid, **kwargs)
        case "3d column":               artist = column3d(X, Y, Z, ax, gid, **kwargs)
        case "3d scatter":              artist = scatter3d(X, Y, Z, ax, gid, **kwargs)
        case "3d bubble":               artist = bubble3d(X, Y, Z, T, ax, gid, **kwargs)
    
    # some plot types cannot update props from old artists
    if plot_type not in ["treemap"]:
        if artist_old != []:
            for art in artist:
                for art_old in artist_old:
                    if art.get_gid() == art_old.get_gid():
                        update_props(art_old, art)
    # update legend if necessary
    set_legend(ax.figure.canvas)

    ax.figure.canvas.draw()
    print("plotting")
    return artist