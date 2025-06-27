from plot.plotting.base.line import *
from plot.plotting.base.column import *
from plot.plotting.base.scatter import *
from plot.plotting.base.pie import *
from plot.plotting.base.stats import *
from plot.plotting.base.mesh import *
from config.settings import GLOBAL_DEBUG, logger
from plot.utilis import find_mpl_object, remove_artist, get_legend, remove_legend, rescale_plot
from plot.copy_objects import update_props, update_legend
from plot.canvas import Canvas
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.figure import Figure
from matplotlib.artist import Artist

DEBUG = False

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
        ax = find_mpl_object(canvas.figure, match=[Axes, Axes3D], gid='legend axes', rule='exact')[0]
        if handles != []:            
            if get_legend(canvas.figure): 
                update_legend(
                    get_legend(canvas.figure), ax,
                    handles=handles, labels=labels
                )
            else:
                legend = ax.legend(
                    handles=handles, labels=labels, 
                    draggable=True,
                    *args, *kwargs
                )
                legend.set_gid('legend')
        
    except Exception as e:
        logger.exception(e)  

def plotting(X, Y, Z, T, ax:Axes, gid:str=None, plot_type:str=None, *args, **kwargs) -> tuple[list[Artist], dict]:
   
    # get old artist that will be replaced
    # but its properties will apply to the new ones  
    artist_old = remove_artist(ax.figure, gid)

    remove_legend(ax.figure)
    
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