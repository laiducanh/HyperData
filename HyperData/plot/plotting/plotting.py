from plot.plotting.base.line import *
from plot.plotting.base.column import *
from plot.plotting.base.scatter import *
from plot.plotting.base.pie import *
from plot.plotting.base.stats import *
from plot.plotting.base.mesh import *
from config.settings import GLOBAL_DEBUG, logger
from plot.utilis import find_mpl_object, update_props
from plot.canvas import Canvas
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.artist import Artist
from matplotlib.legend import Legend
from matplotlib.backend_bases import MouseEvent

DEBUG = False

bbox = None
legend_picked = False

def remove_artist (figure: Figure, gid:str) -> list[Artist]:
    """
    Remove artist which contains gid from figure
    
    """
    artist_removed = list()
    
    for artist in find_mpl_object(source=figure,match=[Artist],gid=gid,rule="contain"):
        artist_removed.append(artist)
        artist.remove()
        if GLOBAL_DEBUG or DEBUG:
            print('remove_artist::',artist)
    return artist_removed

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
        # _legend.set_loc("center")
        canvas.axesleg.draw_artist(_legend)
    return legend_picked

def get_legend_anchor(canvas: Canvas):
    legend = get_legend(canvas)
    # get legend bbox in display coords (pixels)
    bbox = legend.get_window_extent()
    # convert to figure coordinates
    inv_fig = canvas.figure.transFigure.inverted()
    # get lower-left corner of bbox
    anchor_point = inv_fig.transform(bbox)[0]
    return anchor_point

def set_legend(canvas: Canvas, *args, **kwargs):
    try:   
        handles = find_mpl_object(
            canvas.figure,
            match=[Artist],
            gid="graph "
        )
        plot_list = set([s.get_gid().split('/')[0] for s in handles])
        labels, handles = list(), list()
        for gid in plot_list:
            arts = find_mpl_object(
                canvas.figure,
                match=[Artist],
                gid=gid,
            )

            for art in arts:
                if art.get_visible() and art.get_label() and not art.get_label().startswith('_'):
                    labels.append(arts[0].get_label())
                    handles.append(arts[0])
                    break # only one visible artist with valid label is used for legend                

        if handles != []:            
            if get_legend(canvas): 
                update_legend(canvas, handles=handles, labels=labels)
            else:
                legend = canvas.axesleg.legend(
                    handles=handles, labels=labels, 
                    *args, *kwargs
                )
                legend.set_draggable(True, update='bbox')
                legend.set_gid("legend")
        
    except Exception as e:
        logger.exception(e)

def update_legend(canvas: Canvas, **kwargs):
    old_legend = get_legend(canvas)
    legend_title = old_legend.get_title()
    legend_texts = old_legend.get_texts()
    params = {
        "handles": old_legend.legend_handles,
        "numpoints": old_legend.numpoints,
        "scatterpoints": old_legend.scatterpoints,
        "ncols": old_legend._ncols,
        "columnspacing": old_legend.columnspacing,
        "frameon": old_legend.get_frame_on(),
        "shadow": old_legend.shadow,
        "facecolor": old_legend.legendPatch.get_facecolor(),
        "edgecolor": old_legend.legendPatch.get_edgecolor(),
        "framealpha": old_legend.legendPatch.get_alpha(),
        "borderpad": old_legend.borderpad,
        "handlelength": old_legend.handlelength,
        "handleheight": old_legend.handleheight,
        "handletextpad": old_legend.handletextpad,
        "title": old_legend.get_title().get_text()
    }
    params.update(**kwargs)
    anchor_point = get_legend_anchor(canvas)
    # remove the old legend
    remove_legend(canvas)
    # draw new legend based on anchor point of the old one.
    legend = canvas.axesleg.legend(
        loc=anchor_point,
        bbox_to_anchor=anchor_point,
        bbox_transform=canvas.figure.transFigure,
        **params
    )
    legend.set_draggable(True, update='bbox')
    legend.set_gid(old_legend.get_gid())

    update_props(legend_title, legend.get_title())
    for new_text, old_text in zip(legend.get_texts(), legend_texts):
        update_props(old_text, new_text)

    

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

def plotting(X, Y, Z, T, ax:Axes, gid:str=None, plot_type:str=None, *args, **kwargs) -> tuple[list[Artist], dict]:
   
    # get old artist that will be replaced
    # but its properties will apply to the new ones  
    artist_old = remove_artist(ax.figure, gid)

    remove_legend(ax.figure.canvas)
    
    # rescale all axes while remove old artists and add new artists
    rescale_plot(ax.figure)
    
    if   plot_type == "2d line":                 artist, props = line2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d step":                 artist, props = step2d(X, Y, ax, gid, artist_old, *args, **kwargs)
    elif plot_type == "2d stem":                 artist, props = stem2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d spline":               artist, props = spline2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d area":                 artist, props = fill_between(X, Y, 0, ax, gid, *args, **kwargs)
    elif plot_type == "fill between":            artist, props = fill_between(X, Y, Z, ax, gid, *args, **kwargs)
    elif plot_type == "2d stacked area":         artist, props = stackedarea(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d 100% stacked area":    artist, props = stackedarea100(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d column":               artist, props = column2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "dot":                     artist, props = dot(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "dumbbell":                artist, props = dumbbell(X, Y, Z, ax, gid, *args, **kwargs)
    elif plot_type == "2d clustered column":     artist, props = clusteredcolumn2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "clustered dot":           artist, props = clustereddot(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d stacked column":       artist, props = stackedcolumn2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "stacked dot":             artist, props = stackeddot(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d 100% stacked column":  artist, props = stackedcolumn2d100(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d waterfall column":     artist, props = waterfall_bar(X, Y, ax,gid, *args, **kwargs)
    elif plot_type == "marimekko":               artist, props = marimekko(X, ax, gid, *args, **kwargs)
    elif plot_type == "treemap":                 artist, props = treemap(X, ax, gid, artist_old, *args, **kwargs)
    elif plot_type == "2d scatter":              artist, props = scatter2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "2d bubble":               artist, props = bubble2d(X, Y, Z, ax, gid, *args, **kwargs)
    elif plot_type == "pie":                     artist, props = pie(X, ax, gid, *args, **kwargs)
    elif plot_type == "coxcomb":                 artist, props = coxcomb(X, ax, gid, *args, **kwargs)
    elif plot_type == "doughnut":                artist, props = doughnut(X, ax, gid, *args, **kwargs)
    elif plot_type == "multilevel doughnut":     artist, props = multilevel_doughnut(X, ax, gid, *args, **kwargs)
    elif plot_type == "semicircle doughnut":     artist, props = semicircle_doughnut(X, ax, gid, *args, **kwargs)
    elif plot_type == "histogram":               artist, props = histogram(X, ax, gid, *args, **kwargs)
    elif plot_type == "stacked histogram":       artist, props = stacked_histogram(X, ax, gid, *args, **kwargs)
    elif plot_type == "boxplot":                 artist, props = boxplot(X, ax, gid, *args, **kwargs)
    elif plot_type == "violinplot":              artist, props = violinplot(X, ax, gid, *args, **kwargs)
    elif plot_type == "eventplot":               artist, props = eventplot(X, ax, gid, *args, **kwargs)
    elif plot_type == "hist2d":                  artist, props = hist2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "error bar":               artist, props = errorbar(X, Y, Z, T, ax, gid, *args, **kwargs)
    elif plot_type == "heatmap":                 artist, props = heatmap(X, ax, gid, *args, **kwargs)
    elif plot_type == "contour":                 artist, props = contour(X, ax, gid, *args, **kwargs)

    elif plot_type == "3d line":                 artist, props = line3d(X, Y, Z, ax, gid, *args, **kwargs)
    elif plot_type == "3d step":                 artist, props = step3d(X, Y, Z, ax, gid, *args, **kwargs)
    elif plot_type == "3d stem":                 artist, props = stem3d(X, Y, Z, ax, gid, *args, **kwargs)
    elif plot_type == "3d column":               artist, props = column3d(X, Y, Z, ax, gid, *args, **kwargs)
    elif plot_type == "3d scatter":              artist, props = scatter3d(X, Y, Z, ax, gid, *args, **kwargs)
    elif plot_type == "3d bubble":               artist, props = bubble3d(X, Y, Z, T, ax, gid, *args, **kwargs)
  
    # some plot types cannot generally update props from old artists
    if plot_type not in ["treemap","contour"]:
        if artist_old != []:
            for art in artist:
                for art_old in artist_old:
                    if art.get_gid() == art_old.get_gid():
                        update_props(art_old, art)
   
    # update legend if necessary
    set_legend(ax.figure.canvas)

    ax.figure.canvas.draw_idle()
    if DEBUG or GLOBAL_DEBUG: print("plotting")
    return artist, props