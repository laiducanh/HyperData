from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import PolyCollection
from typing import List
import pandas as pd

def line2d (X, Y, ax: Axes, gid) -> List[Line2D]:

    artist = ax.plot(X, Y)

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def step2d (X, Y, ax:Axes, gid, where="pre") -> List[Line2D]:

    artist = ax.step(X, Y, where=where)
    
    for i in artist: i.where = where

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def fill_between (X, Y, Z, ax:Axes, gid, step=None) -> List[PolyCollection]:

    artist = ax.fill_between(X, Y, Z, step=step)
    
    if step == None:
        artist.step = 'none' 
    else: artist.step = step

    artist = [artist]

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def stackedarea (X, Y, ax:Axes, gid) -> List[PolyCollection]:

    artist = ax.stackplot(X, Y)

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def stackedarea100 (X, Y, ax:Axes, gid) -> List[PolyCollection]:

    artist = ax.stackplot(X, pd.DataFrame(Y).divide(pd.DataFrame(Y).sum()))

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist