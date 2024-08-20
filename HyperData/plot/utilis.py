from matplotlib.lines import Line2D
from matplotlib.collections import Collection
from matplotlib.patches import Rectangle
from matplotlib.colors import to_hex
from matplotlib.artist import Artist

def get_color(artist:Artist):
    """ get color of a matplotlib artist"""

    if isinstance(artist, Line2D):
        return artist.get_color()
    
    elif isinstance(artist, Collection): 
        return to_hex(artist.get_facecolor()[0])
    
    elif isinstance(artist, Rectangle):
        return to_hex(artist.get_facecolor())

    return "white"