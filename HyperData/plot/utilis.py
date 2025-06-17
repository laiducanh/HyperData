from matplotlib.lines import Line2D
from matplotlib.collections import Collection, PathCollection, PolyCollection, LineCollection
from matplotlib.patches import Patch, Rectangle, Wedge, PathPatch, FancyBboxPatch
from matplotlib.colors import to_hex
from matplotlib.artist import Artist
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.text import Text
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from mpl_toolkits.mplot3d.axes3d import Axes3D
from PySide6.QtCore import QSize
from typing import Literal, Union
import numpy as np
from config.settings import GLOBAL_DEBUG, logger

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

    elif isinstance(artist, (Patch, Rectangle)):
        return to_hex(artist.get_facecolor())

    return "white"

def find_mpl_object(source:Union[Figure,Axes,Axes3D], match:list=None, gid:str=None, rule:Literal["exact","contain"]="contain") -> list[Artist]:

    """ This function is used to find artist plot (having gid) in matplotlib,
        for other objects such as text, use matplotlib function findobj() instead """

    obj_found = list()
    if not match:
        match = [Line2D,Collection,Patch,AxesImage,Legend,Text]
    
    for artist_class in match:
        _found: list[Artist] = source.findobj(match=artist_class)
        for artist in _found:
            if artist.get_gid():
                if gid:
                    if rule == "contain" and gid in artist.get_gid():
                        obj_found.append(artist)
                    elif rule == "exact" and gid == artist.get_gid():
                        obj_found.append(artist)
                else: obj_found.append(artist)
        #obj_found += [artist for artist in _found if artist.get_gid() != None]
    return obj_found

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