from plot.plotting.base.line import *
from plot.plotting.base.column import *
from plot.plotting.base.scatter import *
from plot.plotting.base.pie import *
from plot.plotting.base.stats import *
from plot.plotting.base.mesh import *
from config.settings import GLOBAL_DEBUG, logger
from plot.utilis import find_mpl_object, remove_artist, get_legend, remove_legend, rescale_plot, grid
from plot.copy_objects import update_props, update_legend
from plot.canvas import Canvas3D, MultiFigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.artist import Artist

DEBUG = False

def set_legend(figure:Figure, *args, **kwargs):
    try:   
        # Find list of graphs
        graphs = figure.findobj(
            lambda a: a.get_gid() and "graph" in a.get_gid()
        )
        plot_list = set([s.get_gid().split('/')[0] for s in graphs])
        
        # Find labels and handles corresponding to visible graphs
        labels, handles = list(), list()
        for gid in plot_list:
            arts = figure.findobj(
                lambda a: a.get_gid() and gid in a.get_gid()
            )
            for art in arts:
                if art.get_visible() and art.get_label() and not art.get_label().startswith('_'):
                    labels.append(arts[0].get_label())
                    handles.append(arts[0])
                    break # only one visible artist with valid label is used for legend  
        
        # Find axes for legend
        ax = figure.findobj(
            lambda a: isinstance(a, (Axes, Axes3D)) and a.get_gid() \
            and a.get_gid() == 'legend axes'
        )[0]


        if handles != []:            
            if get_legend(figure): 
                update_legend(
                    get_legend(figure), ax,
                    handles=handles, labels=labels
                )
            else:
                legend = ax.legend(
                    handles=handles, labels=labels, 
                    draggable=True,
                    *args, *kwargs
                )
                legend.set_gid('legend')
                logger.info("Create legend.")
        else:
            remove_legend(ax.figure)
        
    except Exception as e:
        logger.exception(e)  

def plotting(X, Y, Z, T, ax:Axes, gid:str=None, plot_type:str=None, *args, **kwargs) -> tuple[list[Artist], dict]:

    # remove selected rectangles:
    for rect in find_mpl_object(ax.figure, gid='_selected', rule='exact'):
        ax.figure.patches.remove(rect)
   
    # get old artist that will be replaced
    # but its properties will apply to the new ones  
    artist_old = remove_artist(ax.figure, gid)
    
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
    elif plot_type == "radar":                   artist, props = radar(X, ax, gid, *args, **kwargs)
    elif plot_type == "histogram":               artist, props = histogram(X, ax, gid, *args, **kwargs)
    elif plot_type == "stacked histogram":       artist, props = stacked_histogram(X, ax, gid, *args, **kwargs)
    elif plot_type == "boxplot":                 artist, props = boxplot(X, ax, gid, *args, **kwargs)
    elif plot_type == "violinplot":              artist, props = violinplot(X, ax, gid, *args, **kwargs)
    elif plot_type == "eventplot":               artist, props = eventplot(X, ax, gid, *args, **kwargs)
    elif plot_type == "hist2d":                  artist, props = hist2d(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "error bar":               artist, props = errorbar(X, Y, Z, T, ax, gid, *args, **kwargs)
    elif plot_type == "pareto":                  artist, props = pareto(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "andrews plot":            artist, props = andrews(X, Y, ax, gid, *args, **kwargs)
    elif plot_type == "covariance ellipse":      artist, props = cov_ellipse(X, Y, ax, gid, *args, **kwargs)
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
    set_legend(ax.figure)
    
    # ax.figure.canvas.draw_idle()
    ax.redraw_in_frame()

    # add artist from the drawing axes into figure globally
    # in order to have better control in zorder
    for art in artist:
        # remove artist from current Axes 
        if art._remove_method:
            art.remove() 
        # then add to Figure
        ax.figure.add_artist(art) 
    
    # adjust grid when plotting
    if not isinstance(ax.figure.canvas, (Canvas3D, MultiFigureCanvas)): 
        grid(ax.figure)
    
    ax.figure.canvas.draw_idle()

    return artist, props