from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
from matplotlib import colors
from typing import List
import pandas as pd
import numpy as np

def column2d (X, Y, ax:Axes, gid, orientation="vertical", 
              width=0.8, bottom=0, align="center") -> List[Rectangle]:
    
    if orientation == "vertical":
        artist = ax.bar(X, Y, gid=gid, width=width, bottom=bottom, align=align)
    elif orientation == "horizontal":
        artist = ax.barh(X, Y, gid=gid, height=width, left=bottom, align=align)

    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for art in artist:
        art.orientation = orientation
        art.bottom = bottom
        art.align = align
        art.width = width
    
    return artist

def clusteredcolumn2d (X, Y, ax:Axes, gid, orientation="vertical",
                       width=0.8, bottom=0, align="center", distance=1) -> List[Rectangle]:

    multiplier = 0
    artist = list()
    df = (pd.DataFrame(Y)).transpose()

    for index, values in df.items():
        offset = width*multiplier
        multiplier += distance
        
        if orientation == "vertical":
            bars = ax.bar([a+offset for a in X], values, gid = f"{gid}.{index+1}",
                          width=width, bottom=bottom, align=align)
        elif orientation == "horizontal":
            bars = ax.barh([a+offset for a in X], values, gid = f"{gid}.{index+1}",
                           height=width, left=bottom, align=align)

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for art in artist:
        art.orientation = orientation
        art.bottom = bottom
        art.align = align
        art.width = width
        art.distance = distance

    return artist

def stackedcolumn2d (X, Y, ax:Axes, gid, orientation="vertical",
                     width=0.8, bottom=0, align="center") -> List[Rectangle]:

    df = (pd.DataFrame(Y)).transpose()
    artist = list()
    _bottom = bottom
    
    for index, values in df.items():

        if orientation == "vertical":
            bars = ax.bar(X, values, gid=f"{gid}.{index+1}", 
                          bottom=bottom, width=width, align=align)
        elif orientation == "horizontal":
            bars = ax.barh(X, values,gid=f"{gid}.{index+1}", 
                           left=bottom, height=width, align=align)
        
        bottom += values

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for art in artist:
        art.orientation = orientation
        art.bottom = _bottom
        art.align = align
        art.width = width
    return artist

def stackedcolumn2d100 (X, Y, ax:Axes, gid, orientation="vertical",
                        width=0.8, bottom=0, align="center") -> List[Rectangle]:

    df = (pd.DataFrame(Y))
    df = (df.divide(df.sum())).transpose()
    artist = list()
    _bottom = bottom

    for index, values in df.items():   
        if orientation == "vertical":
            bars = ax.bar(X, values, gid=f"{gid}.{index+1}", 
                          bottom=bottom, width=width, align=align)
        elif orientation == "horizontal":
            bars = ax.barh(X, values,gid=f"{gid}.{index+1}", 
                           left=bottom, height=width, align=align)
        
        bottom += values

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for art in artist:
        art.orientation = orientation
        art.bottom = _bottom
        art.align = align
        art.width = width
   
    return artist

def marimekko (X, ax:Axes, gid, orientation="vertical") -> List[Rectangle]:

    df = (pd.DataFrame(X))
    df = (df.divide(df.sum())).transpose()
    max_x = [sum(a) for a in np.array(X).transpose()]
    width = [a/max(max_x) for a in max_x]
    bottom = 0
    artist = list()

    pos = [sum(width[:n])+width[n]/2 for n,_ in enumerate(width)] 

    for index, values in df.items():
        if orientation == "vertical":
            bars = ax.bar(pos,values,width=width,bottom=bottom,gid=f"{gid}.{index+1}")
        elif orientation == "horizontal":
            bars = ax.barh(pos,values,height=width,left=bottom,gid=f"{gid}.{index+1}")

        bottom += values

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for art in artist:
        art.orientation = orientation
    
    return artist