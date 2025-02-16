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
from matplotlib.patches import Rectangle, Wedge, PathPatch, FancyBboxPatch
from matplotlib.legend import Legend, DraggableLegend
from matplotlib.font_manager import FontProperties
from matplotlib.backend_bases import MouseEvent
from typing import List, Union, Literal

DEBUG = False

bbox = None
legend_picked = False

def remove_artist (ax:Axes, gid:str) -> list[Artist]:
    artist_removed = list()
    
    for artist in find_mpl_object(source=ax.figure,match=[Artist],gid=gid,rule="contain"):
        artist_removed.append(artist)
        artist.remove()
        if GLOBAL_DEBUG or DEBUG:
            pass
    return artist_removed

def update_props (from_obj: Artist, to_obj: Artist) -> None:  
    try:      
        #print("update props")
        #print(to_obj, from_obj)
        to_obj_props = to_obj.properties()
        from_obj_props = from_obj.properties()

        if type(from_obj) == type(to_obj):
            to_obj.update_from(from_obj)

            # for step plots
            if isinstance(to_obj, Line2D):
                to_obj.set(drawstyle=to_obj_props.get("drawstyle"))

        to_obj.update(dict(label=from_obj.get_label()))
        
    except Exception as e:
        logger.exception(e)

def get_legend(canvas: Canvas) -> Legend:
    try: return canvas.axesleg.get_legend()
    except: canvas.axes.get_legend()

def legend_onRelease(event:MouseEvent, canvas:Canvas):
    global legend_picked, _legend
    legend_picked = False
    canvas.draw_idle() # draw asap to fix legend's position
    return legend_picked

def legend_onPress(event:MouseEvent, canvas:Canvas):
    global legend_picked
    if get_legend(canvas) and _legend.contains(event)[0]:
        legend_picked = True
    return legend_picked

def legend_onMove(event:MouseEvent, canvas:Canvas):
    global legend_picked, bbox
    if get_legend(canvas) and legend_picked:
        bbox = canvas.axesleg.transAxes.inverted().transform((event.x, event.y))
        _legend.set_bbox_to_anchor(bbox, canvas.axesleg.transAxes)
        #_legend.set_loc('center')
        canvas.axesleg.draw_artist(_legend)
    return legend_picked
    
def set_legend(canvas: Canvas, *args, **kwargs):
    try:   
        _handles: list[Artist] = find_mpl_object(
            canvas.fig,
            match=[Artist],
            gid="graph "
        )
        plot_list = set([s.get_gid() for s in _handles])
        _labels, _handles = list(), list()
        for gid in plot_list:
            arts = find_mpl_object(
                canvas.fig,
                match=[Artist],
                gid=gid,
                rule="exact"
            )

            if arts[0].get_label() and not arts[0].get_label().startswith("_"):
                _labels.append(arts[0].get_label())
                _handles.append(arts[0])
        
        old_title = None
        global bbox, legend_picked
        legend_picked = False
        
        # if not get_legend(canvas): 
        #     mpl_background = canvas.copy_from_bbox(canvas.fig.bbox)

        # if get_legend(canvas): 
        #     old_title = get_legend(canvas).get_title()
        #     get_legend(canvas).remove()

        if _handles != []:
            global _legend
            _legend = canvas.axesleg.legend(_handles, _labels, 
                                            *args, *kwargs)
            #if bbox: _legend.set_loc('center')
            _legend.set_bbox_to_anchor(bbox, canvas.axesleg.transAxes)
            
            _legend.set_gid("legend")
            
            # for _handle, _leghandle, _legtext \
            # in zip(_handles, _legend.legend_handles, _legend.get_texts()):
            #     print("awpoic", _handle.get_gid())
            #     _leghandle.set_gid(f"{_handle.get_gid()}")
            #     _legtext.set_gid(f"{_handle.get_gid()}")     

            # if old_title: 
            #     _legend.set_title(old_title.get_text())
            #     _legend.get_title().update_from(old_title)
            #canvas.draw()
            # canvas.restore_region(mpl_background)
            # canvas.axesleg.draw_artist(_legend)
            # canvas.blit(canvas.fig.bbox)
            
            
    except Exception as e:
        logger.exception(e)

def remove_legend(canvas: Canvas):
    _legend = get_legend(canvas)
    if _legend:
        _legend.remove()
  

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

def plotting(X, Y, Z, T, ax:Axes, gid:str=None, plot_type:str=None, *args, **kwargs) -> List[Artist]:
   
    # get old artist that will be replaced
    # but its properties will apply to the new ones
    artist_old = find_mpl_object(
        ax.figure,
        match=[Line2D,Collection,Rectangle,Wedge,PathPatch,FancyBboxPatch],
        gid=gid)
   
    remove_artist(ax, gid)
    remove_legend(ax.figure.canvas)
    
    # rescale all axes while remove old artists and add new artists
    rescale_plot(ax.figure)
    
    match plot_type:
        case "2d line":                 artist = line2d(X, Y, ax, gid, *args, **kwargs)
        case "2d step":                 artist = step2d(X, Y, ax, gid, *args, **kwargs)
        case "2d stem":                 artist = stem2d(X, Y, ax, gid, *args, **kwargs)
        case "2d area":                 artist = fill_between(X, Y, 0, ax, gid, *args, **kwargs)
        case "fill between":            artist = fill_between(X, Y, Z, ax, gid, *args, **kwargs)
        case "2d stacked area":         artist = stackedarea(X, Y, ax, gid, *args, **kwargs)
        case "2d 100% stacked area":    artist = stackedarea100(X, Y, ax, gid, *args, **kwargs)
        case "2d column":               artist = column2d(X, Y, ax, gid, *args, **kwargs)
        case "dot":                     artist = dot(X, Y, ax, gid, *args, **kwargs)
        case "dumbbell":                artist = dumbbell(X, Y, Z, ax, gid, *args, **kwargs)
        case "2d clustered column":     artist = clusteredcolumn2d(X, Y, ax, gid, *args, **kwargs)
        case "clustered dot":           artist = clustereddot(X, Y, ax, gid, *args, **kwargs)
        case "2d stacked column":       artist = stackedcolumn2d(X, Y, ax, gid, *args, **kwargs)
        case "stacked dot":             artist = stackeddot(X, Y, ax, gid, *args, **kwargs)
        case "2d 100% stacked column":  artist = stackedcolumn2d100(X, Y, ax, gid, *args, **kwargs)
        case "2d waterfall column":     artist = waterfall_bar(X, Y, ax,gid, *args, **kwargs)
        case "marimekko":               artist = marimekko(X, ax, gid, *args, **kwargs)
        case "treemap":                 artist = treemap(X, ax, gid, artist_old, *args, **kwargs)
        case "2d scatter":              artist = scatter2d(X, Y, ax, gid, *args, **kwargs)
        case "2d bubble":               artist = bubble2d(X, Y, Z, ax, gid, *args, **kwargs)
        case "pie":                     artist = pie(X, ax, gid, *args, **kwargs)
        case "coxcomb":                 artist = coxcomb(X, ax, gid, *args, **kwargs)
        case "doughnut":                artist = doughnut(X, ax, gid, *args, **kwargs)
        case "multilevel doughnut":     artist = multilevel_doughnut(X, ax, gid, *args, **kwargs)
        case "semicircle doughnut":     artist = semicircle_doughnut(X, ax, gid, *args, **kwargs)
        case "histogram":               artist = histogram(X, ax, gid, *args, **kwargs)
        case "stacked histogram":       artist = stacked_histogram(X, ax, gid, *args, **kwargs)
        case "boxplot":                 artist = boxplot(X, ax, gid, *args, **kwargs)
        case "violinplot":              artist = violinplot(X, ax, gid, *args, **kwargs)
        case "eventplot":               artist = eventplot(X, ax, gid, *args, **kwargs)
        case "hist2d":                  artist = hist2d(X, Y, ax, gid, *args, **kwargs)

        case "3d line":                 artist = line3d(X, Y, Z, ax, gid, *args, **kwargs)
        case "3d step":                 artist = step3d(X, Y, Z, ax, gid, *args, **kwargs)
        case "3d stem":                 artist = stem3d(X, Y, Z, ax, gid, *args, **kwargs)
        case "3d column":               artist = column3d(X, Y, Z, ax, gid, *args, **kwargs)
        case "3d scatter":              artist = scatter3d(X, Y, Z, ax, gid, *args, **kwargs)
        case "3d bubble":               artist = bubble3d(X, Y, Z, T, ax, gid, *args, **kwargs)
  
    # some plot types cannot generally update props from old artists
    if plot_type not in ["treemap"]:
        if artist_old != []:
            for art in artist:
                for art_old in artist_old:
                    if art.get_gid() == art_old.get_gid():
                        update_props(art_old, art)
   
    # update legend if necessary
    set_legend(ax.figure.canvas)
    
    ax.figure.canvas.draw_idle()
    if DEBUG or GLOBAL_DEBUG: print("plotting")
    return artist