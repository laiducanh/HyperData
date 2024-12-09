from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import PolyCollection
from typing import List
import pandas as pd
import numpy as np

def line2d (X, Y, ax: Axes, gid) -> List[Line2D]:

    artist = ax.plot(X, Y)

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def line3d (X, Y, Z, ax:Axes, gid:str) -> List[Line2D]:

    artist = ax.plot(X, Y, Z, gid=gid)

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def step2d (X, Y, ax:Axes, gid, where="pre") -> List[Line2D]:

    artist = ax.step(X, Y, where=where)
    
    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)
        
        obj.where = where

    return artist

def step3d (X, Y, Z, ax:Axes, gid, where="pre") -> List[Line2D]:

    artist = ax.step(X, Y, Z, where=where)
    
    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)
        
        obj.where = where

    return artist

def stem2d (X, Y, ax:Axes, gid, orientation="vertical",bottom=0) -> List[Line2D]:

    artist = list()
    markerline, stemlines, baseline = ax.stem(X, Y, orientation=orientation,bottom=bottom)

    markerline.set_gid(f"{gid}/markerline")
    stemlines.set_gid(f"{gid}/stemlines")
    baseline.set_gid(f"{gid}/baseline")

    artist.append(markerline)
    artist.append(baseline)
    artist.append(stemlines)

    for art in artist:        
        art.orientation = orientation
        art.bottom = bottom
    
    return artist

def stem3d (X, Y, Z, ax:Axes, gid, orientation="z",bottom=0) -> List[Line2D]:
    X = np.linspace(0.1, 2 * np.pi, 41)
    Y = np.exp(np.sin(X))
    Z = np.linspace(0,1,41)

    artist = list()
    markerline, stemlines, baseline = ax.stem(X, Y, Z, orientation=orientation,bottom=bottom)

    markerline.set_gid(f"{gid}/markerline")
    stemlines.set_gid(f"{gid}/stemlines")
    baseline.set_gid(f"{gid}/baseline")

    artist.append(markerline)
    artist.append(baseline)
    artist.append(stemlines)

    for art in artist:        
        art.orientation = orientation
        art.bottom = bottom
    
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

def stackedarea (X, Y, ax:Axes, gid, step=None, baseline="zero") -> List[PolyCollection]:
    
    artist = ax.stackplot(X, Y, step=step, baseline=baseline)
    
    for ind, obj in enumerate(artist):
        obj.baseline = baseline
        if step == None: obj.step = 'none'
        else: obj.step = step

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