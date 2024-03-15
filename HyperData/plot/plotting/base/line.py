from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from typing import List

def line2d (X, Y, ax: Axes) -> List[Line2D]:

    artist = ax.plot(X, Y)

    return artist

def step2d (X, Y, ax:Axes, where="pre") -> List[Line2D]:

    artist = ax.step(X, Y, where=where)
    
    for i in artist: i.where = where

    return artist