from matplotlib.colors import to_hex, to_rgb
from matplotlib.artist import Artist
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import lines, patches, collections, text, legend
from typing import Literal, Union, Type, TypeVar
import numpy as np
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

T = TypeVar('T', bound=Artist)

def get_color(artist:Artist):
    """ get color of a matplotlib artist"""
    
    if isinstance(artist, lines.Line2D):
        return to_hex(artist.get_color())
    
    elif isinstance(artist, (collections.PolyCollection, collections.QuadMesh)): 
        return to_hex(artist.get_facecolor()[0])
    
    elif isinstance(artist, collections.PathCollection):
        return to_hex(np.max(artist.get_facecolor(), axis=0))
    
    elif isinstance(artist, collections.LineCollection):
        return to_hex(artist.get_edgecolor()[0])

    elif isinstance(artist, (patches.Patch, patches.Rectangle)):
        return to_hex(artist.get_facecolor())

    return "white"

def complementary_color(color):
    """
    Returns the complementary color of a given color.
    Supports color names, hex, or RGB tuples.
    """
    # Convert to RGB (0–1)
    rgb = to_rgb(color)
    
    # Complement: 1 - R, G, B
    comp_rgb = tuple(1.0 - c for c in rgb)
    
    # Convert back to hex
    comp_hex = to_hex(comp_rgb)
    
    return comp_hex

def find_mpl_object(figure:Figure, match:list[Type[T]]=None, 
                    gid:str=None, rule:Literal["exact","contain","index"]="index") -> list[T]:

    """ This function is used to find artist plot (having gid) in figure,
        for general uses, use matplotlib function findobj() instead """

    
    if not match:
        match = [lines.Line2D,collections.Collection,patches.Patch,AxesImage,legend.Legend,text.Text]

    if not gid:
        return [x for x in figure.artists if isinstance(x, tuple(match))]
        
    if rule == 'exact':
        return [x for x in figure.artists if isinstance(x, tuple(match)) \
                and x.get_gid() and x.get_gid() == gid]
            
    elif rule == 'contain':
        return [x for x in figure.artists if isinstance(x, tuple(match)) \
                and x.get_gid() and gid in x.get_gid()]

    elif rule == 'index':
        return [x for x in figure.artists if isinstance(x, tuple(match)) \
                and x.get_gid() \
                and gid.split()[0] in x.get_gid().split('/')[0] \
                and gid.split()[-1] == x.get_gid().split('/')[0].split()[-1]]

def remove_artist(figure:Figure, gid:str) -> list[Artist]:
    """
    Remove artist which contains gid from Axes
    
    """
    artist_removed = list()

    for ax in figure.axes:
        artists = ax.findobj(
            lambda a: isinstance(a, Artist) and a.get_gid() \
            and gid.split()[0] in a.get_gid().split('/')[0] \
            and gid.split()[-1] == a.get_gid().split('/')[0].split()[-1]
        )
        if artists:
            ax._children = [x for x in ax._children if x not in artists]
            figure.artists = [x for x in figure.artists if x not in artists]
            artist_removed += artists
            logger.info(f'Canvas {figure.canvas.id}: remove_artist {artists}.')
                        
    return artist_removed

def get_legend(figure: Figure) -> Union[legend.Legend, None]:
    found = figure.findobj(
        lambda a: isinstance(a, legend.Legend) and a.get_gid() \
        and a.get_gid() == 'legend'
    )
    if found: return found[0]
    return

def get_legend_anchor(figure: Figure):
    legend = get_legend(figure)
    # get legend bbox in display coords (pixels)
    bbox = legend.get_window_extent()
    # convert to figure coordinates
    inv_fig = figure.transFigure.inverted()
    # get lower-left corner of bbox
    anchor_point = inv_fig.transform(bbox)[0]
    return anchor_point

def remove_legend(figure: Figure):
    legend = get_legend(figure)
    if legend: legend.remove()

def rescale_plot(figure:Figure) -> None:
    for _ax in figure.axes:
        _ax.relim()
        _ax.autoscale()  

def normalize_zorder(figure:Figure):
    zorders = [artist.zorder for artist in figure.artists]
    zorders_map = {z : i+1 for i, z in enumerate(sorted(set(zorders)))}
    for artist in figure.artists:
        artist.set_zorder(zorders_map[artist.zorder])

def set_zorder(figure:Figure, gid:str, 
               action:Literal['Send to Back','Bring to Front',
                              'Bring Forward','Send Backward']):

    artists = figure.artists
    zorders = [a.get_zorder() for a in artists]
    zorders.insert(0, min(zorders) - 1e-3)
    zorders.append(max(zorders) + 1e-3)
    for obj in artists:
        try:
            if obj.get_gid() == gid:
                if action == 'Send to Back':
                    obj.set_zorder(min(zorders))
                elif action == 'Bring to Front':
                    obj.set_zorder(max(zorders))
                elif action == 'Bring Forward':
                    sorted_unique_zorders = sorted(set(zorders))
                    index = sorted_unique_zorders.index(obj.zorder)
                    if index < len(sorted_unique_zorders)-1:
                        obj.set_zorder((
                            sorted_unique_zorders[index+1]+ \
                            sorted_unique_zorders[index+2]) / 2
                        )
                    else:
                        obj.set_zorder((
                            sorted_unique_zorders[index+1]+ \
                            sorted_unique_zorders[index]) / 2
                        )
                elif action == 'Send Backward':
                    sorted_unique_zorders = sorted(set(zorders))
                    index = sorted_unique_zorders.index(obj.zorder)
                    if index > 1:
                        obj.set_zorder((
                            sorted_unique_zorders[index-1]+ \
                            sorted_unique_zorders[index-2]) / 2
                        )
                    else:
                        obj.set_zorder((
                            sorted_unique_zorders[index-1]+ \
                            sorted_unique_zorders[index]) / 2
                        )
        except Exception as e: pass
    normalize_zorder(figure)

def grid(figure: Figure):
    " Only use for 2D Figure "

    for obj in find_mpl_object(
        figure, [lines.Line2D],
        gid='_grid', rule='exact'
    ):
        figure.artists.remove(obj)

    xaxis: Axis = figure.findobj(
        lambda a: isinstance(a, Axis) and a.get_gid() \
        and a.get_gid() == figure.canvas._config['grid']['coord'].split('-')[0]
    )[0]
    yaxis: Axis = figure.findobj(
        lambda a: isinstance(a, Axis) and a.get_gid() \
        and a.get_gid() == figure.canvas._config['grid']['coord'].split('-')[1]
    )[0]
    
    if figure.canvas._config['grid']['which'] == 'major':
        xticks = xaxis.get_major_ticks()
        yticks = yaxis.get_major_ticks()
    elif figure.canvas._config['grid']['which'] == 'minor':
        xticks = xaxis.get_minor_ticks()
        yticks = yaxis.get_minor_ticks()
    elif figure.canvas._config['grid']['which'] == 'both':
        xticks = xaxis.get_major_ticks() + xaxis.get_minor_ticks()
        yticks = yaxis.get_major_ticks() + yaxis.get_minor_ticks()
    
    if figure.canvas._config['grid']['axis'] == 'x':
        gridlines = [tick.gridline for tick in xticks]
    elif figure.canvas._config['grid']['axis'] == 'y':
        gridlines = [tick.gridline for tick in yticks]
    elif figure.canvas._config['grid']['axis'] == 'both':
        gridlines = [tick.gridline for tick in xticks + yticks]

    for line in gridlines:
        line.set(
            visible = figure.canvas._config['grid']['visible'],
            gid = '_grid'
        )
        figure.add_artist(line)