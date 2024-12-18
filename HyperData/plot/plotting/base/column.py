from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import colors
from typing import List
import matplotlib.pyplot
import pandas as pd
import numpy as np
import squarify, matplotlib

def column2d (X, Y, ax:Axes, gid, orientation="vertical", 
              width=0.8, bottom=0, align="center", *args, **kwargs) -> List[Rectangle]:
    
    if orientation == "vertical":
        artist = ax.bar(X, Y, gid=gid, width=width, bottom=bottom, align=align, *args, **kwargs)
    elif orientation == "horizontal":
        artist = ax.barh(X, Y, gid=gid, height=width, left=bottom, align=align, *args, **kwargs)
  
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = bottom
        art.align = align
        art.width = width
        art.Xdata = X[ind]
        art.Ydata = Y[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = Y[ind]

    return artist

def column3d (X, Y, Z, ax:Axes3D, gid, Dx=0.5, Dy=0.5, bottom=0, color = None,
              orientation="z", zsort="average", shade=True, *args, **kwargs) -> List[Poly3DCollection]:

    match orientation:
        case "x":   x, y, z, dx, dy, dz = bottom, X, Y, Z, Dx, Dy
        case "y":   x, y, z, dx, dy, dz = X, bottom, Y, Dx, Z, Dy
        case "z":   x, y, z, dx, dy, dz = X, Y, bottom, Dx, Dy, Z
   
    artist = ax.bar3d(x, y, z, dx, dy, dz, gid=gid,
                      zsort=zsort, shade=shade, color=color, *args, **kwargs)
    
    artist.Dx = Dx
    artist.Dy = Dy
    artist.bottom = bottom
    artist.orientation = orientation
    artist.zsort = zsort
    artist.shade = shade
    artist.color = color

    return [artist]

def clusteredcolumn2d (X, Y, ax:Axes, gid, orientation="vertical",
                       width=0.8, bottom=0, align="center", distance=1, *args, **kwargs) -> List[Rectangle]:

    multiplier = 0
    artist = list()
    df = (pd.DataFrame(Y)).transpose()

    for index, values in df.items():
        offset = width*multiplier
        multiplier += distance
        
        if orientation == "vertical":
            bars = ax.bar([a+offset for a in X], values, gid = f"{gid}.{index+1}",
                          width=width, bottom=bottom, align=align, *args, **kwargs)
        elif orientation == "horizontal":
            bars = ax.barh([a+offset for a in X], values, gid = f"{gid}.{index+1}",
                           height=width, left=bottom, align=align, *args, **kwargs)

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = bottom
        art.align = align
        art.width = width
        art.distance = distance
        art.Xdata = np.asarray(X*len(Y))[ind]
        art.Ydata = np.asarray(Y).flatten()[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = np.asarray(Y).flatten()[ind]

    return artist

def stackedcolumn2d (X, Y, ax:Axes, gid, orientation="vertical",
                     width=0.8, bottom=0, align="center", *args, **kwargs) -> List[Rectangle]:

    df = (pd.DataFrame(Y)).transpose()
    artist = list()
    _bottom = bottom
    
    for index, values in df.items():

        if orientation == "vertical":
            bars = ax.bar(X, values, gid=f"{gid}.{index+1}", 
                          bottom=bottom, width=width, align=align, *args, **kwargs)
        elif orientation == "horizontal":
            bars = ax.barh(X, values,gid=f"{gid}.{index+1}", 
                           left=bottom, height=width, align=align, *args, **kwargs)
        
        bottom += values

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = _bottom
        art.align = align
        art.width = width
        art.Xdata = np.asarray(X*len(Y))[ind]
        art.Ydata = np.asarray(Y).flatten()[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = art.get_center()[1]

    return artist

def stackedcolumn2d100 (X, Y, ax:Axes, gid, orientation="vertical",
                        width=0.8, bottom=0, align="center", *args, **kwargs) -> List[Rectangle]:

    df = pd.DataFrame(Y)
    df = (df.divide(df.sum())).transpose()
    artist = list()
    _bottom = bottom

    for index, values in df.items():   
        if orientation == "vertical":
            bars = ax.bar(X, values, gid=f"{gid}.{index+1}", 
                          bottom=bottom, width=width, align=align, *args, **kwargs)
        elif orientation == "horizontal":
            bars = ax.barh(X, values,gid=f"{gid}.{index+1}", 
                           left=bottom, height=width, align=align, *args, **kwargs)
        
        bottom += values

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = _bottom
        art.align = align
        art.width = width
        art.Xdata = np.asarray(X*len(Y))[ind]
        art.Ydata = np.asarray(Y).flatten()[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = art.get_center()[1]
   
    return artist

def marimekko (X, ax:Axes, gid, orientation="vertical", *args, **kwargs) -> List[Rectangle]:
    
    df = pd.DataFrame(X)
    df = (df.divide(df.sum())).transpose()
    max_x = [sum(a) for a in np.array(X).transpose()]
    width = [a/max(max_x) for a in max_x]
    bottom = 0
    artist = list()

    pos = [sum(width[:n])+width[n]/2 for n,_ in enumerate(width)] 
    
    for index, values in df.items():
        if orientation == "vertical":
            bars = ax.bar(pos,values,width=width,bottom=bottom,gid=f"{gid}.{index+1}", *args, **kwargs)
        elif orientation == "horizontal":
            bars = ax.barh(pos,values,height=width,left=bottom,gid=f"{gid}.{index+1}", *args, **kwargs)

        bottom += values

        artist += bars.patches
    
    for ind, art in enumerate(artist):
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
        art.orientation = orientation
        art.Xdata = np.asarray(X).flatten()[ind]
        art.Ydata = None
        art.Xshow = art.get_center()[0]
        art.Yshow = art.get_center()[1]

    ax.set_xlim(pos[0]-width[0]/2,pos[-1]+width[-1]/2)
    ax.set_ylim(0,1)
    ax.set_axis_on()

    return artist

def treemap (X, ax:Axes, gid, pad=0, cmap="tab10", alpha=1, *args, **kwargs) -> List[Rectangle]:
    
    # descending sort
    _X = -np.sort(-np.array(X))

    values = squarify.normalize_sizes(_X, 100, 100)

    rects = squarify.squarify(values, 0, 0, 100, 100)
    
    colors = matplotlib.colormaps[cmap](np.linspace(0,1,len(_X)))
    # colors = matplotlib.pyplot.get_cmap(cmap)

    artist = list()
    for ind, _rect in enumerate(rects):
        
        if _rect["dx"] > 2*pad:
            _rect["x"] += pad
            _rect["dx"] -= 2*pad
        if _rect["dy"] > 2*pad:
            _rect["y"] += pad
            _rect["dy"] -= 2*pad

        rect = Rectangle(
            xy      = (_rect['x'], _rect['y']),
            width   = _rect['dx'],
            height  = _rect['dy'],
            color   = colors[ind],
            alpha   = alpha,
            gid     = f"{gid}.{ind+1}"
            )
        
        rect.pad = pad
        rect.cmap = cmap
        rect.Xdata = X[ind]
        rect.Ydata = None
        rect.Xshow = rect.get_center()[0]
        rect.Yshow = rect.get_center()[1]

        ax.add_artist(rect)
        artist.append(rect)
    
    
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    ax.set_aspect('auto')
        
    return artist