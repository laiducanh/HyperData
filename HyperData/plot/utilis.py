from matplotlib.lines import Line2D
from matplotlib.collections import Collection, PathCollection, PolyCollection, LineCollection
from matplotlib.patches import Patch
from matplotlib.colors import to_hex
from matplotlib.artist import Artist
from matplotlib.figure import Figure
from typing import List
import numpy as np

def get_color(artist:Artist):
    """ get color of a matplotlib artist"""
    
    if isinstance(artist, Line2D):
        return to_hex(artist.get_color())
    
    elif isinstance(artist, PolyCollection): 
        return to_hex(artist.get_facecolor()[0])
    
    elif isinstance(artist, PathCollection):
        return to_hex(np.max(artist.get_facecolor(), axis=0))
    
    elif isinstance(artist, LineCollection):
        return to_hex(artist.get_edgecolor()[0])

    elif isinstance(artist, Patch):
        return to_hex(artist.get_facecolor())

    return "white"

def find_mpl_object(figure:Figure, match=list([Line2D,Collection,Patch]), gid:str=None) -> List[Artist]:

    """ This function is used to find artist plot (having gid) in matplotlib,
        for other objects such as text, use matplotlib function findobj() instead """

    obj_found = list()
    for artist_class in match:
        _found: list[Artist] = figure.findobj(match=artist_class)
        for artist in _found:
            if artist.get_gid():
                if gid:
                    if gid == artist.get_gid():
                        obj_found.append(artist)
                else: obj_found.append(artist)
        #obj_found += [artist for artist in _found if artist.get_gid() != None]
    return obj_found