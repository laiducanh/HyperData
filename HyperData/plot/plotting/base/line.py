from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import PolyCollection
from typing import List
import pandas as pd
import numpy as np
from config.settings import color_cycle

def line2d (X, Y, ax: Axes, gid, *args, **kwargs) -> List[Line2D]:

    _X = np.asarray(X)
    _Y = np.asarray(Y)
    artist = list()
    
    if _Y.ndim > 1:
        for ind, y in enumerate(_Y):
            _line = ax.plot(_X, y, color=next(color_cycle), 
                            gid=f"{gid}.{ind+1}", *args, **kwargs)
            artist += _line
    else:
        _line = ax.plot(_X, _Y, color=next(color_cycle),
                        gid=gid, *args, **kwargs)
        artist += _line

    return artist

def line3d (X, Y, Z, ax:Axes, gid:str, *args, **kwargs) -> List[Line2D]:

    artist = ax.plot(X, Y, Z, gid=gid, *args, **kwargs)

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def step2d (X, Y, ax:Axes, gid, where="pre", *args, **kwargs) -> List[Line2D]:

    _X = np.asarray(X)
    _Y = np.asarray(Y)
    artist = list()

    if _Y.ndim > 1:
        for ind, y in enumerate(_Y):
            _step = ax.step(_X, y, where=where, color=next(color_cycle),
                            gid=f"{gid}.{ind+1}", *args, **kwargs)
            artist += _step
    else:
        _step = ax.step(_X, _Y, where=where, color=next(color_cycle),
                        gid=gid, *args, **kwargs)
        artist += _step
    
    for art in artist:
        art.where = where
            
    return artist

def step3d (X, Y, Z, ax:Axes, gid, where="pre", *args, **kwargs) -> List[Line2D]:

    artist = ax.step(X, Y, Z, where=where, *args, **kwargs)
    
    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)
        
        obj.where = where

    return artist

def stem2d (X, Y, ax:Axes, gid, orientation="vertical",bottom=0, *args, **kwargs) -> List[Line2D]:

    _X = np.asarray(X)
    _Y = np.asarray(Y)
    artist = list()
    markerline, stemlines, baseline = ax.stem(_X, _Y, orientation=orientation,
                                              bottom=bottom, *args, **kwargs)

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

def stem3d (X, Y, Z, ax:Axes, gid, orientation="z",bottom=0, *args, **kwargs) -> List[Line2D]:
    X = np.linspace(0.1, 2 * np.pi, 41)
    Y = np.exp(np.sin(X))
    Z = np.linspace(0,1,41)

    artist = list()
    markerline, stemlines, baseline = ax.stem(X, Y, Z, orientation=orientation,bottom=bottom, *args, **kwargs)

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

def fill_between (X, Y, Z, ax:Axes, gid, step=None, orientation='vertical', *args, **kwargs) -> List[PolyCollection]:

    _X = np.asarray(X)
    _Y = np.asarray(Y)
    _Z = np.asarray(Z)

    if orientation == "vertical":
        artist = ax.fill_between(_X, _Y, _Z, step=step, gid=gid, *args, **kwargs)
    elif orientation == "horizontal":
        artist = ax.fill_betweenx(_X, _Y, _Z, step=step, gid=gid, *args, **kwargs)
        # swap X and Y
        _X = np.asarray(Y).copy()
        _Y = np.asarray(X).copy()

    if Z: 
        # for fill_between plot
        artist.Xdata = np.repeat(_X, 2)
        artist.Ydata = np.concatenate((_Y, _Z))
        artist.Xshow = artist.Xdata.copy()
        artist.Yshow = artist.Ydata.copy()
    else: 
        # for 2d area plot
        artist.Xdata = np.asarray(X).copy()
        artist.Ydata = np.asarray(Y).copy()
        artist.Xshow = _X.copy()
        artist.Yshow = _Y.copy()
    
    artist.orientation = orientation
    if step == None:
        artist.step = 'none' 
    else: artist.step = step

    return [artist]

def stackedarea (X, Y, ax:Axes, gid, step=None, baseline="zero", *args, **kwargs) -> List[PolyCollection]:
    
    _X = np.asarray(X)
    _Y = np.asarray(Y)
    stack = np.cumsum(_Y, axis=0)
    
    artist = ax.stackplot(_X, _Y, baseline=baseline, step=step, *args, **kwargs)

    for ind, art in enumerate(artist):
        art.baseline = baseline
        art.Xdata = _X.copy()
        art.Ydata = stack[ind, :].copy()
        art.Xshow = art.Xdata.copy()
        art.Yshow = art.Ydata.copy()
    
        if step: art.step = step
        else: art.step = 'none'  

        if len(artist) > 1:
            art.set_gid(f"{gid}.{ind+1}")
        else:
            art.set_gid(gid)  
        
    return artist

def stackedarea100 (X, Y, ax:Axes, gid, *args, **kwargs) -> List[PolyCollection]:

    _X = np.asarray(X)
    _Y = np.asarray(Y)
    _Y = _Y/np.sum(_Y, axis=0)
    stack = np.cumsum(_Y, axis=0)

    artist = ax.stackplot(_X, _Y, *args, **kwargs)

    for ind, art in enumerate(artist):
        art.Xdata = _X.copy()
        art.Ydata = np.asarray(Y)[ind, :].copy()
        art.Xshow = _X.copy()
        art.Yshow = stack[ind, :].copy()
        if len(artist) > 1:
            art.set_gid(f"{gid}.{ind+1}")
        else:
            art.set_gid(gid)  
    
    return artist