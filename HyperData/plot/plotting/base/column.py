from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D
from matplotlib.collections import PathCollection, LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import colors
import matplotlib.pyplot
import numpy as np
import squarify, matplotlib, fractions, math
from config.settings import logger, GLOBAL_DEBUG
from typing import Union

DEBUG = True

def column2d (X, Y, ax:Axes, gid, orientation="vertical", width=0.8, bottom=0, align="center", *args, **kwargs) -> list[Union[Rectangle, LineCollection]]:
    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(3)
        Y = np.array([2,4,7])

    segments = list()
    artist = list()

    if orientation == "vertical":
        bars = ax.bar(X, Y, gid=gid, width=width, bottom=bottom, align=align, *args, **kwargs)
        for idx in range(len(bars.patches)):
            if idx < len(bars.patches)-1:
                rect1 = bars.patches[idx]
                rect2 = bars.patches[idx+1]
                segments.append([
                    (rect1.get_x()+rect1.get_width(), rect1.get_y()+rect1.get_height()),
                    (rect2.get_x(), rect2.get_y()+rect2.get_height())
                ])
    elif orientation == "horizontal":
        bars = ax.barh(X, Y, gid=gid, height=width, left=bottom, align=align, *args, **kwargs)
        for idx in range(len(bars.patches)):
            if idx < len(bars.patches)-1:
                rect1 = bars.patches[idx]
                rect2 = bars.patches[idx+1]
                segments.append([
                    (rect1.get_x()+rect1.get_width(), rect1.get_y()+rect1.get_height()),
                    (rect2.get_x()+rect2.get_width(), rect2.get_y())
                ])
    artist += bars.patches
  
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
        art.Yshow = art.get_center()[1]
    
    art = LineCollection(
        segments, 
        gid=f"_{gid}",
        color='black',
    )
    art.set_visible(False)
    ax.add_artist(art)
    artist.append(art)
    art.Xdata = None
    art.Ydata = None
    art.Xshow = None
    art.Yshow = None

    return artist

def column3d (X, Y, Z, ax:Axes3D, gid, Dx=0.5, Dy=0.5, bottom=0, color = None,
              orientation="z", zsort="average", shade=True, *args, **kwargs) -> list[Poly3DCollection]:

    if orientation == "x": x, y, z, dx, dy, dz = bottom, X, Y, Z, Dx, Dy
    elif orientation == "y":   x, y, z, dx, dy, dz = X, bottom, Y, Dx, Z, Dy
    elif orientation == "z":   x, y, z, dx, dy, dz = X, Y, bottom, Dx, Dy, Z
   
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

def _dotstep(arr) -> Union[float,int]:
    """ thif function auto calculates the step between dots to draw on Canvas,  
        the step will be computed from the greatest division in the array
        of the greatest division of the closest denominator of each element in array
        the step is considered as the amount of data each dot represents
    """
    Y = np.asarray(arr).flatten()
    try: 
        step = np.gcd.reduce(Y)
    except: # if the input if float
        _Y = np.zeros(Y.size, dtype=np.int32)
        for idx, y in enumerate(Y):
            _Y[idx] = fractions.Fraction(y).limit_denominator().denominator
        fac = np.prod(_Y)/np.gcd.reduce(_Y)
        step = (1/fac) * np.gcd.reduce(np.asarray(Y*fac, dtype=np.int32))
    return step

def dot(X, Y, ax:Axes, gid, orientation='vertical', bottom=0, *args, **kwargs) -> list[Line2D]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(0,10)
        Y = np.array([2.2,3.2])

    X = np.asarray(X)
    Y = np.asarray(Y)
    
    step = _dotstep(Y)
    artist = list()
    for _x, _y in zip(X, Y):
        if orientation == "vertical":
            x = np.repeat(_x, int(_y*(1/step)*0.5))
            y = np.linspace(bottom+step, _y+bottom, num=int(_y*(1/step)), endpoint=True, dtype=np.float16)
        else:
            x = np.linspace(bottom+step, _y+bottom, num=int(_y*(1/step)), endpoint=True, dtype=np.float16)
            y = np.repeat(_x, int(_y*(1/step)))
        
        _line = ax.plot(
            x, y,
            gid=gid,
            marker=".",
            linewidth=0,
            markersize=14,
            *args, **kwargs
        )
        artist += _line
        
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = bottom
    
    return artist

def _waffle(X, Y, ax:Axes, gid, orientation='vertical', bottom=0, cols=3, rows=20,
           sizes=0.1, distance=0.05, *args, **kwargs) -> list[PathCollection]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(0,10)
        Y = np.array([2.2,3.5])
    
    X = np.asarray(X)
    Y = np.asarray(Y)
    
    step = _dotstep(Y)
    artist = list()
    max_npoints = math.ceil(np.max(Y)*(1/step)*(1/cols))
    max_npoints = max_npoints if max_npoints > rows else rows

    for _x, _y in zip(X, Y):
        if orientation == 'vertical':
            x = np.linspace(_x+bottom, _x+bottom+cols*sizes+distance, cols)
            x = np.tile(x, max_npoints)
            y = np.linspace(step, np.max(Y), max_npoints)
            y = np.repeat(y, cols)
        else:
            y = np.linspace(_x+bottom, _x+bottom+cols*sizes+distance, cols)
            y = np.tile(y, max_npoints)
            x = np.linspace(step, np.max(Y), max_npoints)
            x = np.repeat(x, cols)
        colors = np.repeat('lightgray', cols*max_npoints)
        print(x, y)
        for _xx, _yy in zip(x, y):
            print(_xx, _yy)
            r = Rectangle((_xx, _yy), sizes, sizes,
                transform = ax.transAxes)
            ax.add_artist(r)
        ax.set_xlim(x[0],x[-1])
        ax.set_ylim(y[0], y[-1])
    #     _scatter = ax.scatter(
    #         x, y, 
    #         marker='s', 
    #         s=matplotlib.rcParams["lines.markersize"]**2*sizes/max_npoints,
    #         linewidths=0, 
    #         color=colors,
    #         gid=gid
    #     )
        
        artist.append(r)
    
    for art in artist:
        art.sizes = sizes
        art.orientation = orientation
        art.bottom = bottom
        art.distance = distance
        art.Xdata = X
        art.Ydata = Y
        art.Xshow = art.Xdata
        art.Yshow = art.Ydata
    
    return artist

def dumbbell(X, Y, Z, ax:Axes, gid, orientation='vertical', *args, **kwargs) -> list[Union[Line2D,PathCollection]]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(3)
        Y = np.array([1,3,5])
        Z = np.array([2,4,7])

    X = np.asarray(X)
    Y = np.asarray(Y)
    Z = np.asarray(Z)
    artist = list()

    if orientation == "vertical":
        # connecting lines
        for idx, x in enumerate(X):
            line = ax.plot(
                np.repeat(x, 2),
                (Y[idx], Z[idx]),
                color='black',
                linewidth=1,
                solid_capstyle="round",
                gid=f"{gid}.0",
            )
            artist += line

        # draw two heads
        p1 = ax.plot(
            X, Y, 
            marker='o', 
            gid=f"{gid}.1", 
            linestyle="none",
            zorder=line[0].get_zorder()+1
        )
        p2 = ax.plot(
            X, Z, 
            marker='o', 
            gid=f"{gid}.2", 
            linestyle="none",
            zorder=line[0].get_zorder()+1
        )
        artist += p1
        artist += p2

    else:
         # connecting lines
        for idx, x in enumerate(X):
            line = ax.plot(
                (Y[idx], Z[idx]),
                np.repeat(x, 2),
                color='black',
                linewidth=1,
                solid_capstyle="round",
                gid=f"{gid}.0",
            )
            artist += line

        # draw two heads
        p1 = ax.plot(
            Y, X, 
            marker='o', 
            gid=f"{gid}.1", 
            linestyle="none",
            zorder=line[0].get_zorder()+1
        )
        p2 = ax.scatter(
            Z, X, 
            marker='o', 
            gid=f"{gid}.2", 
            linestyle="none",
            zorder=line[0].get_zorder()+1
        )
        artist += p1
        artist += p2
    
    for art in artist:
        art.orientation = orientation

    return artist


def clusteredcolumn2d (X, Y, ax:Axes, gid, orientation="vertical",
                       width=0.8, bottom=0, distance=1, *args, **kwargs) -> list[Rectangle]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(3)
        Y = np.array([[2,4,7],[1,5,3]])

    X = np.asarray(X)
    Y = np.asarray(Y)

    multiplier = 0
    artist = list()

    for idx, y in enumerate(Y):
        offset = width*multiplier
        multiplier += distance
        
        if orientation == "vertical":
            bars = ax.bar([a+offset for a in X], y, gid = f"{gid}.{idx+1}",
                          width=width, bottom=bottom, *args, **kwargs)
        elif orientation == "horizontal":
            bars = ax.barh([a+offset for a in X], y, gid = f"{gid}.{idx+1}",
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
        art.Xdata = np.repeat(X, len(Y))[ind]
        art.Ydata = np.asarray(Y).flatten()[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = art.get_center()[1]

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

def stackedcolumn2d (X, Y, ax:Axes, gid, orientation="vertical", width=0.8, 
                     bottom=0, *args, **kwargs) -> list[Union[Rectangle, LineCollection]]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(3)
        Y = np.array([[2,4,7],[1,5,3]])

    X = np.asarray(X)
    Y = np.asarray(Y)

    artist = list()
    _bottom = bottom
    segments = list()
    
    for idx, y in enumerate(Y):
        if orientation == "vertical":
            bars = ax.bar(X, y, gid=f"{gid}.{idx+1}", 
                          bottom=bottom, width=width, *args, **kwargs)
            for idx in range(len(bars.patches)):
                if idx < len(bars.patches)-1:
                    rect1 = bars.patches[idx]
                    rect2 = bars.patches[idx+1]
                    segments.append([
                        (rect1.get_x()+rect1.get_width(), rect1.get_y()+rect1.get_height()),
                        (rect2.get_x(), rect2.get_y()+rect2.get_height())
                    ])
        elif orientation == "horizontal":
            bars = ax.barh(X, y,gid=f"{gid}.{idx+1}", 
                           left=bottom, height=width, *args, **kwargs)
            for idx in range(len(bars.patches)):
                if idx < len(bars.patches)-1:
                    rect1 = bars.patches[idx]
                    rect2 = bars.patches[idx+1]
                    segments.append([
                        (rect1.get_x()+rect1.get_width(), rect1.get_y()+rect1.get_height()),
                        (rect2.get_x()+rect2.get_width(), rect2.get_y())
                    ])
        
        bottom += y
        artist += bars.patches
        
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = _bottom
        art.width = width
        art.Xdata = np.repeat(X, len(Y))[ind]
        art.Ydata = np.asarray(Y).flatten()[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = art.get_center()[1]
    
    art = LineCollection(
        segments, 
        gid=f"_{gid}",
        color='black',
    )
    art.set_visible(False)
    ax.add_artist(art)
    artist.append(art)
    art.Xdata = None
    art.Ydata = None
    art.Xshow = None
    art.Yshow = None

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
        art.bottom = _bottom
        
    return artist

def stackedcolumn2d100 (X, Y, ax:Axes, gid, orientation="vertical", width=0.8, bottom=0, *args, **kwargs) -> list[Union[Rectangle, LineCollection]]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(3)
        Y = np.array([[2,4,7],[1,5,3]])

    X = np.asarray(X)
    Y = np.asarray(Y)
    Y = Y/np.sum(Y, axis=0)

    artist = list()
    _bottom = bottom
    segments = list()

    for idx, y in enumerate(Y):
    #for index, values in df.items():   
        if orientation == "vertical":
            bars = ax.bar(X, y, gid=f"{gid}.{idx+1}", 
                          bottom=bottom, width=width, *args, **kwargs)
            for idx in range(len(bars.patches)):
                if idx < len(bars.patches)-1:
                    rect1 = bars.patches[idx]
                    rect2 = bars.patches[idx+1]
                    segments.append([
                        (rect1.get_x()+rect1.get_width(), rect1.get_y()+rect1.get_height()),
                        (rect2.get_x(), rect2.get_y()+rect2.get_height())
                    ])
        elif orientation == "horizontal":
            bars = ax.barh(X, y,gid=f"{gid}.{idx+1}", 
                           left=bottom, height=width, *args, **kwargs)
            for idx in range(len(bars.patches)):
                if idx < len(bars.patches)-1:
                    rect1 = bars.patches[idx]
                    rect2 = bars.patches[idx+1]
                    segments.append([
                        (rect1.get_x()+rect1.get_width(), rect1.get_y()+rect1.get_height()),
                        (rect2.get_x()+rect2.get_width(), rect2.get_y())
                    ])
        
        bottom += y

        artist += bars.patches
    
    # set edge_color
    for art in artist:
        art.set_edgecolor(colors.to_hex(art.get_edgecolor()))
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = _bottom
        art.width = width
        art.Xdata = np.repeat(X, len(Y))[ind]
        art.Ydata = np.asarray(Y).flatten()[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = art.get_center()[1]
    
    art = LineCollection(
        segments, 
        gid=f"_{gid}",
        color='black',
    )
    art.set_visible(False)
    ax.add_artist(art)
    artist.append(art)
    art.Xdata = None
    art.Ydata = None
    art.Xshow = None
    art.Yshow = None

    return artist

def marimekko (X, ax:Axes, gid, orientation="vertical", *args, **kwargs) -> list[Rectangle]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.array([[2,4,7],[1,5,3]])

    X = np.asarray(X)
    max_x = np.sum(X, axis=0)
    width = max_x/np.max(max_x)
    pos = np.cumsum(width) - width*0.5
    X = X/max_x

   
    bottom = 0
    artist = list()

   
    for idx, x in enumerate(X):
        if orientation == "vertical":
            bars = ax.bar(pos,x,width=width,bottom=bottom,gid=f"{gid}.{idx+1}", *args, **kwargs)
        elif orientation == "horizontal":
            bars = ax.barh(pos,x,height=width,left=bottom,gid=f"{gid}.{idx+1}", *args, **kwargs)

        bottom += x

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

def treemap (X, ax:Axes, gid, artist_old:list[FancyBboxPatch], pad=0.0, cmap_on=True, cmap="tab10", alpha=1, rounded=0, *args, **kwargs) -> list[FancyBboxPatch]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.array([1,2,6])

    # descending sort
    _X = -np.sort(-np.asarray(X))

    values = squarify.normalize_sizes(_X, 100, 100)

    rects = squarify.squarify(values, 0, 0, 100, 100)

    if cmap_on:
        colors = matplotlib.colormaps[cmap](np.linspace(0,1,len(_X)))
    else: colors = np.repeat([None], len(_X))

    # colors = matplotlib.pyplot.get_cmap(cmap)
    #print(pad, cmap, rounded)
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
                boxstyle=f"round,pad=0,rounding_size={rounded}",
            )

        else:
            rect = FancyBboxPatch(
                xy      = (_rect['x'], _rect['y']),
                width   = _rect['dx'],
                height  = _rect['dy'],
                color   = colors[ind],
                alpha   = alpha,
                gid     = f"{gid}.{ind+1}",
                boxstyle="square,pad=0",
            )
        
        
        rect.pad = pad
        rect.cmap_on = cmap_on
        rect.cmap = cmap
        rect.rounded = rounded
        rect.Xdata = X[ind]
        rect.Ydata = None
        x, y, w, h = rect.get_bbox().bounds
        rect.Xshow = x + w / 2
        rect.Yshow = y + h / 2
        
        for rect_old in artist_old:
            if rect.get_gid() == rect_old.get_gid():
                rect.set(
                    edgecolor=rect_old.get_edgecolor(),
                    linewidth=rect_old.get_linewidth(),
                    linestyle=rect_old.get_linestyle(),
                    alpha=rect_old.get_alpha(),
                )
                if not cmap_on:
                    rect.set(
                        facecolor=rect_old.get_facecolor()
                    )

        ax.add_artist(rect)
        artist.append(rect)
    
    
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    ax.set_aspect('auto')
        
    return artist

def waterfall_bar(X, Y, ax:Axes, gid, orientation="vertical", width=0.8, bottom=0, *args, **kwargs) -> list[Union[Rectangle, LineCollection]]:
    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(5)
        Y = np.array([3,-1,2,-3,5])
    
    artist = list()
    _bottom = bottom
    segments = list() # for linecollection plot
    idx = 0

    if orientation == "vertical":
        for x, y in zip(X, Y):
            if _bottom+y < _bottom: # draw negative bars
                rect = Rectangle(
                    xy=(x-width/2,_bottom+y),
                    width=width,
                    height=abs(y),
                    color='red',
                    gid=f"{gid}/negative",
                )
            else: # draw positive bars
                rect = Rectangle(
                    xy=(x-width/2,_bottom),
                    width=width,
                    height=y,
                    color='blue',
                    gid=f"{gid}/positive",
                )
            _bottom += y
            if idx < len(X)-1:
                segments.append([(X[idx]-width/2,_bottom),(X[idx+1]+width/2,_bottom)])
            idx += 1
            ax.add_artist(rect)
            artist.append(rect)
    
    elif orientation == "horizontal":
        for x, y in zip(X, Y):
            if _bottom+y < _bottom:
                rect = Rectangle(
                    xy=(_bottom+y,x-width/2),
                    width=abs(y),
                    height=width,
                    color='red',
                    gid=f"{gid}/negative",
                )
            else:
                rect = Rectangle(
                    xy=(_bottom,x-width/2),
                    width=y,
                    height=width,
                    color='blue',
                    gid=f"{gid}/positive",
                )
            _bottom += y
            if idx < len(X)-1:
                segments.append([(_bottom,X[idx]-width/2),(_bottom,X[idx+1]+width/2)])
            idx += 1
            ax.add_artist(rect)
            artist.append(rect)
    
    for ind, art in enumerate(artist):
        art.orientation = orientation
        art.bottom = bottom
        art.width = width
        art.Xdata = X[ind]
        art.Ydata = Y[ind]
        art.Xshow = art.get_center()[0]
        art.Yshow = art.get_center()[1]

    lines = LineCollection(
        segments,
        gid=f"{gid}/line",
    )
    lines.Xdata = None
    lines.Ydata = None
    lines.Xshow = None
    lines.Yshow = None

    ax.add_artist(lines)
    artist.append(lines)
    
    ax.relim()
    
    #print(artist)
    return artist