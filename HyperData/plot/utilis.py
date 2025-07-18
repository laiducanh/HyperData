from matplotlib.colors import to_hex, to_rgb
from matplotlib.artist import Artist
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.axes import Axes
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

def find_mpl_object(source:Union[Figure,Axes,Axes3D], match:list[Type[T]]=None, 
                    gid:str=None, rule:Literal["exact","contain"]="contain") -> list[T]:

    """ This function is used to find artist plot (having gid) in matplotlib,
        for general uses, use matplotlib function findobj() instead """

    
    if not match:
        match = [lines.Line2D,collections.Collection,patches.Patch,AxesImage,legend.Legend,text.Text]

    if not gid:
        return source.findobj(
            lambda a: isinstance(a, tuple(match))
        )    
    if rule == 'exact':
        return source.findobj(
            lambda a: isinstance(a, tuple(match)) and a.get_gid() == gid
        )
            
    elif rule == 'contain':
        return source.findobj(
            lambda a: isinstance(a, tuple(match)) and a.get_gid() and gid in a.get_gid()
        )

def remove_artist (figure: Figure, gid:str) -> list[Artist]:
    """
    Remove artist which contains gid from figure
    
    """
    artist_removed = list()
    
    for artist in find_mpl_object(source=figure,match=[Artist],gid=gid,rule="contain"):
        artist_removed.append(artist)
        artist.remove()
        logger.info(f'Canvas {figure.canvas.id}: remove_artist {artist}.')
    return artist_removed

def get_legend(figure: Figure) -> Union[legend.Legend, None]:
    found = find_mpl_object(source=figure, match=[legend.Legend], gid='legend', rule='exact')
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