from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import colors
import matplotlib.pyplot
import pandas as pd
import numpy as np
import squarify, matplotlib, fractions
from config.settings import logger, GLOBAL_DEBUG, color_cycle

DEBUG = True

def column2d (X, Y, ax:Axes, gid, orientation="vertical", 
              width=0.8, bottom=0, align="center", *args, **kwargs) -> list[Rectangle]:
    
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
              orientation="z", zsort="average", shade=True, *args, **kwargs) -> list[Poly3DCollection]:

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

def _dotstep(arr) -> float|int:
    """ thif function auto calculates the step between dots to draw on Canvas,  
        the step will be computed from the greatest division in the array
        of the greatest division of the closest denominator of each element in array
    """
    Y = np.asarray(arr).flatten()
    try: 
        step = np.gcd.reduce(Y)
    except: # if the input if float
        _Y = np.zeros(Y.size, dtype=np.int32)
        for idx, y in enumerate(Y):
            _Y[idx] = fractions.Fraction(y).limit_denominator().denominator
        fac = np.prod(_Y)/np.gcd(*_Y)
        step = (1/fac) * np.gcd.reduce(np.asarray(Y*fac, dtype=np.int32))
    return step

def dot(X, Y, ax:Axes, gid, orientation='vertical', bottom=0, *args, **kwargs) -> list[Line2D]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(0,10)
        Y = np.array([2.2,3.4])

    X = np.asarray(X)
    Y = np.asarray(Y)
    
    step = _dotstep(Y)
    artist = list()

    for _x, _y in zip(X, Y):
        if orientation == "vertical":
            x = np.repeat(_x, int(_y*(1/step)))
            y = np.linspace(bottom+step, _y+bottom, num=int(_y*(1/step)), endpoint=True, dtype=np.float16)
        else:
            x = np.linspace(bottom+step, _y+bottom, num=int(_y*(1/step)), endpoint=True, dtype=np.float16)
            y = np.repeat(_x, int(_y*(1/step)))

        _line = ax.plot(
            x, y,
            gid=gid,
            marker=".",
            linewidth=0,
            color="black",
            markersize=14,
            *args, **kwargs
        )
        artist += _line
        
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = bottom
    
    return artist

def clusteredcolumn2d (X, Y, ax:Axes, gid, orientation="vertical",
                       width=0.8, bottom=0, distance=1, *args, **kwargs) -> list[Rectangle]:

    multiplier = 0
    artist = list()
    df = (pd.DataFrame(Y)).transpose()

    for index, values in df.items():
        offset = width*multiplier
        multiplier += distance
        
        if orientation == "vertical":
            bars = ax.bar([a+offset for a in X], values, gid = f"{gid}.{index+1}",
                          width=width, bottom=bottom, *args, **kwargs)
        elif orientation == "horizontal":
            bars = ax.barh([a+offset for a in X], values, gid = f"{gid}.{index+1}",
                           height=width, left=bottom, *args, **kwargs)

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = bottom
        art.width = width
        art.distance = distance
        art.Xdata = np.asarray(X*len(Y))[ind]
        art.Ydata = np.asarray(Y).flatten()[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = np.asarray(Y).flatten()[ind]

    return artist

def clustereddot(X, Y, ax:Axes, gid, orientation='vertical', bottom=0, 
                 distance=0.2, *args, **kwargs) -> list[Line2D]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(3)
        Y = np.array([[2,4,7],[1,5,3]])

    X = np.asarray(X)
    Y = np.asarray(Y)
    multiplier = 0
    step = _dotstep(Y)
    artist = list()

    for idx, _Y in enumerate(Y):
        offset = multiplier
        multiplier += distance
        color = next(color_cycle)
        for _x, _y in zip(X, _Y):
            if orientation == "vertical":
                x = np.repeat(_x+offset, int(_y*(1/step)))
                y = np.linspace(bottom+step, _y+bottom, num=int(_y*(1/step)), endpoint=True, dtype=np.float16)
            else:
                x = np.linspace(bottom+step, _y+bottom, num=int(_y*(1/step)), endpoint=True, dtype=np.float16)
                y = np.repeat(_x+offset, int(_y*(1/step))+1)
            _lines = ax.plot(
                x, y,
                gid = f"{gid}.{idx+1}",
                color = color,
                marker=".",
                linewidth=0,
                markersize=14,
                *args, **kwargs
            )
            artist += _lines

    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = bottom
        art.distance = distance
    
    return artist

def stackedcolumn2d (X, Y, ax:Axes, gid, orientation="vertical",
                     width=0.8, bottom=0, *args, **kwargs) -> list[Rectangle]:

    df = (pd.DataFrame(Y)).transpose()
    artist = list()
    _bottom = bottom
    
    for index, values in df.items():

        if orientation == "vertical":
            bars = ax.bar(X, values, gid=f"{gid}.{index+1}", 
                          bottom=bottom, width=width, *args, **kwargs)
        elif orientation == "horizontal":
            bars = ax.barh(X, values,gid=f"{gid}.{index+1}", 
                           left=bottom, height=width, *args, **kwargs)
        
        bottom += values

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = _bottom
        art.width = width
        art.Xdata = np.asarray(X*len(Y))[ind]
        art.Ydata = np.asarray(Y).flatten()[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = art.get_center()[1]

    return artist

def stackeddot(X, Y, ax:Axes, gid, orientation="vertical", bottom=0, *args, **kwargs) -> list[Line2D]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(3)
        Y = np.array([[2,4,7],[1,5,3]])
    
    X = np.asarray(X)
    Y = np.asarray(Y)
    step = _dotstep(Y)
    artist = list()
    _bottom = bottom
    bottom = np.repeat([bottom], X.size)

    for idx, _Y in enumerate(Y):
        color = next(color_cycle)
        bottom_idx = 0
        for _x, _y in zip(X, _Y):
            b = bottom[bottom_idx]
            if orientation == "vertical":
                x = np.repeat(_x, int(_y*(1/step)))
                y = np.linspace(b+step, _y+b, num=int(_y*(1/step)), endpoint=True, dtype=np.float16)
            else:
                x = np.linspace(b+step, _y+b, num=int(_y*(1/step)), endpoint=True, dtype=np.float16)
                y = np.repeat(_x, int(_y*(1/step)))
            _lines = ax.plot(
                x, y,
                gid = f"{gid}.{idx+1}",
                color = color,
                marker=".",
                linewidth=0,
                markersize=14,
                *args, **kwargs
            )
            artist += _lines
            bottom_idx += 1
        bottom += _Y
        
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = bottom
        
    return artist

def stackedcolumn2d100 (X, Y, ax:Axes, gid, orientation="vertical",
                        width=0.8, bottom=0, align="center", *args, **kwargs) -> list[Rectangle]:

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

def marimekko (X, ax:Axes, gid, orientation="vertical", *args, **kwargs) -> list[Rectangle]:
    
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

def treemap (X, ax:Axes, gid, pad=0.0, cmap="tab10", alpha=1, rounded=False, *args, **kwargs) -> list[Rectangle]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.array([1,2,6])

    # descending sort
    _X = -np.sort(-np.asarray(X))

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
        
        if rounded:
            rect = FancyBboxPatch(
                xy      = (_rect['x'], _rect['y']),
                width   = _rect['dx'],
                height  = _rect['dy'],
                color   = colors[ind],
                alpha   = alpha,
                gid     = f"{gid}.{ind+1}",
                boxstyle=f"round,pad={pad*0.5}",
            )

        else:
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
        rect.rounded = rounded
        rect.Xdata = X[ind]
        rect.Ydata = None
        x, y, w, h = rect.get_bbox().bounds
        rect.Xshow = x + w / 2
        rect.Yshow = y + h / 2

        ax.add_artist(rect)
        artist.append(rect)
    
    
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    ax.set_aspect('auto')
        
    return artist