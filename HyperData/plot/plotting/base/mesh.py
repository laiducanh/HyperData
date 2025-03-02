from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import QuadMesh
from matplotlib.contour import QuadContourSet
import numpy as np
import matplotlib
from skimage import measure
from config.settings import logger, GLOBAL_DEBUG
from typing import Union

DEBUG = True

""" Data input X in these function are 2D arrays """

def heatmap(X, ax:Axes, gid, *args, **kwargs) -> list[QuadMesh]:
    if DEBUG or GLOBAL_DEBUG:
        X = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                    [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])
    
    artist = ax.pcolormesh(
        X,
        gid=gid,
    )
    return [artist]

def contour(X, ax:Axes, gid, fill=False, cmap=matplotlib.rcParams["image.cmap"], 
            norm="linear", *args, **kwargs) -> list[Union[QuadMesh, Line2D]]:
    
    if DEBUG or GLOBAL_DEBUG:
        X, Y = np.meshgrid(np.linspace(-3, 3, 256), np.linspace(-3, 3, 256))
        X = (1 - X/2 + X**5 + Y**3) * np.exp(-X**2 - Y**2)
   
    artist = list()
    contours = QuadContourSet(ax, X, cmap=cmap, norm=norm)
    
    if fill: 
        art = ax.pcolormesh(
            X,
            gid=f"{gid}/mesh",
            cmap=cmap,
            norm=norm
        )
        artist.append(art)
        
    idx = 0
    for level, color in zip(contours.levels, contours._mapped_colors):
        conts = measure.find_contours(X, level=level)
        for cont in conts:
            line = ax.plot(
                cont[:, 1], 
                cont[:, 0],
                gid=f"{gid}/{idx}",
                color=color
            )
            idx += 1
            artist += line

    contours.remove()
    ax.set_axis_on()

    for art in artist:
        art.norm_ = norm
        art.fill = fill
       
    #print(artist)
    return artist
        
        