from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
from typing import List
import pandas as pd
import numpy as np

def column2d (X, Y, ax:Axes, gid, orientation="horizontal") -> List[Rectangle]:

    if orientation == "vertical":
        artist = ax.bar(X, Y, gid=gid)
    elif orientation == "horizontal":
        artist = ax.barh(X, Y, gid=gid)
    
    return artist

def clusteredcolumn2d (X, Y, ax:Axes, gid, orientation="horizontal") -> List[Rectangle]:

    multiplier = 0
    bar_width = 0.25
    distance = 0.25
    artist = list()
    df = (pd.DataFrame(Y)).transpose()

    for index, values in df.items():
        offset = bar_width*multiplier
        multiplier += distance
        
        if orientation == "vertical":
            bars = ax.bar([a+offset for a in X], values, gid = f"{gid}.{index+1}")
        elif orientation == "horizontal":
            bars = ax.barh([a+offset for a in X], values, gid = f"{gid}.{index+1}")

        artist += bars.patches

    return artist

def stackedcolumn2d (X, Y, ax:Axes, gid, orientation="horizontal") -> List[Rectangle]:

    df = (pd.DataFrame(Y)).transpose()
    bottom = 0
    artist = list()
    
    for index, values in df.items():

        if orientation == "vertical":
            bars = ax.bar(X, values, gid=f"{gid}.{index+1}", bottom=bottom)
        elif orientation == "horizontal":
            bars = ax.barh(X, values,gid=f"{gid}.{index+1}", left=bottom)
        
        bottom += values

        artist += bars.patches

    return artist

def stackedcolumn2d100 (X, Y, ax:Axes, gid, orientation="horizontal") -> List[Rectangle]:

    df = (pd.DataFrame(Y))
    df = (df.divide(df.sum())).transpose()
    bottom = 0
    artist = list()

    for index, values in df.items():   
        if orientation == "vertical":
            bars = ax.bar(X, values, gid=f"{gid}.{index+1}", bottom=bottom)
        elif orientation == "horizontal":
            bars = ax.barh(X, values,gid=f"{gid}.{index+1}", left=bottom)
        
        bottom += values

        artist += bars.patches
   
    return artist

def marimekko (X, ax:Axes, gid, orientation="horizontal") -> List[Rectangle]:

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
    
    return artist