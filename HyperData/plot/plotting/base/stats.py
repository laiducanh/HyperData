from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.lines import Line2D
from matplotlib.collections import PolyCollection, LineCollection, EventCollection, QuadMesh
import numpy as np
from config.settings import logger, GLOBAL_DEBUG
from typing import Union

DEBUG = False

def histogram(X, ax:Axes, gid:str, bins=10, density=False, cumulative=False,
              bottom=0, histtype="bar", align="mid", orientation="vertical",
              rwidth=None, log=False, *args, **kwargs) -> tuple[list[Rectangle], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(1000, 3)
    
    X = np.asarray(X)

    props = {
        "bins": bins,
        "density": density,
        "cumulative": cumulative,
        "bottom": bottom,
        "histtype": histtype,
        "align": align,
        "orientation": orientation,
        "rwidth": rwidth,
        "log": log
    }

    _artist = ax.hist(
        X, 
        bins=bins, 
        density=density,
        cumulative=cumulative,
        bottom=bottom, 
        histtype=histtype, 
        align=align, 
        orientation=orientation, 
        rwidth=rwidth, 
        log=log, 
        stacked=False,
        *args, **kwargs
    )
    # return as tuple(n, bins, patches)
    artist = list()

    if np.ndim(_artist[0]) == 1:
        for y, x, art in zip(*_artist):
            art.set_gid(gid=gid)
            art.Xdata = x
            art.Ydata = y
            art.Xshow = art.get_center()[0]
            art.Yshow = y
            artist.append(art)
    elif np.ndim(_artist[0]) > 1:
        for idx in range(len(_artist[0])):
            for y, x, art in zip(_artist[0][idx],_artist[1],_artist[2][idx]):
                art.set_gid(gid=f"{gid}.{idx+1}")
                art.Xdata = x
                art.Ydata = y
                art.Xshow = art.get_center()[0]
                art.Yshow = y
                artist.append(art)

    ax.set_axis_on()
    
    return artist, props

def stacked_histogram(X, ax:Axes, gid:str, bins=10, density=False, cumulative=False,
                      bottom=0, histtype="bar", align="mid", orientation="vertical",
                      rwidth=None, log=False, *args, **kwargs) -> tuple[list[Rectangle], dict]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(1000, 3)
    
    X = np.asarray(X)

    props = {
        "bins": bins,
        "density": density,
        "cumulative": cumulative,
        "bottom": bottom,
        "histtype": histtype,
        "align": align,
        "orientation": orientation,
        "rwidth": rwidth,
        "log": log
    }
    
    _artist = ax.hist(
        X, 
        bins=bins, 
        density=density,
        cumulative=cumulative,
        bottom=bottom, 
        histtype=histtype, 
        align=align, 
        orientation=orientation, 
        rwidth=rwidth, 
        log=log,
        stacked=True, 
        *args, **kwargs
    )
    # return as tuple(n, bins, patches)
    artist = list()

    if np.ndim(_artist[0]) == 1:
        for y, x, art in zip(*_artist):
            art.set_gid(gid=gid)
            art.Xdata = x
            art.Ydata = y
            art.Xshow = art.get_center()[0]
            art.Yshow = y
            artist.append(art)
    elif np.ndim(_artist[0]) > 1:
        for idx in range(len(_artist[0])):
            for y, x, art in zip(_artist[0][idx],_artist[1],_artist[2][idx]):
                art.set_gid(gid=f"{gid}.{idx+1}")
                art.Xdata = x
                art.Ydata = y
                art.Xshow = art.get_center()[0]
                art.Yshow = y
                artist.append(art)
        
    ax.set_axis_on()
    
    return artist, props

def boxplot(X, ax:Axes, gid:str, showbox = True, notch = False,
            vert = True, widths = 0.5, whis = 1.5, autorange = False,
            showcaps = True, capwidths = 0, showfliers = True,
            bootstrap = 1000, showmeans = False, meanline = False, *args, **kwargs) -> tuple[list[Union[Line2D,PathPatch]], dict]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(1000, 1)

    X = np.asarray(X)

    props = {
        "showbox": showbox,
        "notch": notch,
        "vert": vert,
        "widths": widths,
        "whis": whis,
        "autorange": autorange,
        "showcaps": showcaps,
        "capwidths": capwidths,
        "showfliers": showfliers,
        "bootstrap": bootstrap,
        "showmeans": showmeans,
        "meanline": meanline,
    }

    artist = list()
    _artist = ax.boxplot(
        X, 
        patch_artist=True, 
        showbox=showbox,
        notch=notch,
        vert=vert,
        widths=widths,
        whis=whis,
        autorange=autorange,
        showcaps=showcaps,
        capwidths=capwidths,
        showfliers=showfliers,
        bootstrap=bootstrap,
        showmeans=showmeans,
        meanline=meanline, 
        *args, **kwargs
    )
    
    for art in _artist.get("boxes"):
        artist.append(art)
        art.set_gid(gid=f"{gid}/boxes")
        art.Xdata = None
        art.Ydata = None
        p = np.array(art.get_path().vertices).mean(axis=0)
        art.Xshow = p[0]
        art.Yshow = p[1]
    for art in _artist.get("medians"):
        artist.append(art)
        art.set_gid(gid=f"_{gid}/medians")
    for art in _artist.get("whiskers"):
        artist.append(art)
        art.set_gid(gid=f"_{gid}/whiskers")
    for art in _artist.get("caps"):
        artist.append(art)
        art.set_gid(gid=f"_{gid}/caps")
    for art in _artist.get("fliers"):
        artist.append(art)
        art.set_gid(gid=f"_{gid}/fliers")
    for art in _artist.get("means"):
        artist.append(art)
        art.set_gid(gid=f"_{gid}/means")
    
    ax.set_axis_on()
   
    return artist, props

def violinplot(X, ax:Axes, gid:str, orientation='vertical', widths=0.5,
               showmeans=False, showextrema=True, showmedians=False,
               points=100, bw_method="scott", quantiles=None, *args, **kwargs) -> tuple[list[Union[PolyCollection, LineCollection]], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(1000, 3)
    
    X = np.asarray(X)

    props = {
        "orientation": orientation,
        "widths": widths,
        "showmeans": showmeans,
        "showextrema": showextrema,
        "showmedians": showmedians,
        "points": points,
        "bw_method": bw_method,
        "quantiles": quantiles
    }

    artist = list()
    _artist = ax.violinplot(
        X, 
        vert=orientation, 
        widths=widths,
        showextrema=showextrema, 
        showmeans=showmeans,
        showmedians=showmedians, 
        points=points,
        bw_method=bw_method, 
        quantiles=quantiles, 
        *args, **kwargs
    )

    bodies = _artist.get("bodies")
    cmeans = _artist.get("cmeans")
    cmins = _artist.get("cmins")
    cmaxes = _artist.get("cmaxes")
    cbars = _artist.get("cbars")
    cmedians = _artist.get("cmedians")
    cquantiles = _artist.get("cquantiles")

    
    if bodies != []:
        for art in bodies:
            artist.append(art)
            art.set_gid(gid=f"{gid}/bodies")
    if cmeans: 
        artist.append(cmeans)
        cmeans.set_gid(gid=f"_{gid}/cmeans")
    if cmins: 
        artist.append(cmins)
        cmins.set_gid(gid=f"_{gid}/cmins")
    if cmaxes: 
        artist.append(cmaxes)
        cmaxes.set_gid(gid=f"_{gid}/cmaxes")
    if cbars: 
        artist.append(cbars)
        cbars.set_gid(gid=f"_{gid}/cbars")
    if cmedians: 
        artist.append(cmedians)
        cmedians.set_gid(gid=f"_{gid}/cmedians")
    if cquantiles: 
        artist.append(cquantiles)
        cquantiles.set_gid(gid=f"_{gid}/cquantiles")
    
    for art in artist:
        art.Xdata = None
        art.Ydata = None
        p = np.array(art.get_paths()[0].vertices).mean(axis=0)
        art.Xshow = p[0]
        art.Yshow = p[1]

    ax.set_axis_on()

    return artist, props

def eventplot(X, ax:Axes, gid:str, orientation="horizontal",
              lineoffsets=1, linelengths=1, *args, **kwargs) -> tuple[list[EventCollection], dict]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.random.gamma(4, size=(3, 50))

    X = np.asarray(X)

    props = {
        "orientation": orientation,
        "lineoffsets": lineoffsets,
        "linelengths": linelengths
    }

    artist = ax.eventplot(
        X, 
        gid=gid, 
        orientation=orientation,
        lineoffsets=lineoffsets,
        linelengths=linelengths,
        *args, **kwargs
    )
    
    for art in artist:
        art.Xdata = None
        art.Ydata = None
        p = np.array(art.get_paths()[0].vertices).mean(axis=0)
        art.Xshow = p[0]
        art.Yshow = p[1]
    
    ax.set_axis_on()

    return artist, props

def hist2d(X, Y, ax:Axes, gid:str, binx=10, biny=10, density=False, *args, **kwargs) -> tuple[list[QuadMesh], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(5000)
        Y = 1.2 * X + np.random.randn(5000) / 3

    X = np.asarray(X)
    Y = np.asarray(Y)

    props = {
        "binx": binx,
        "biny": biny,
        "density": density
    }

    _, _, _, artist = ax.hist2d(X, Y, gid=gid, bins=(binx, biny), density=density, *args, **kwargs)

    return [artist], props

def errorbar(X, Y, Yerr, Xerr, ax:Axes, gid:str, capsize=10, errorevery=1, *args, **kwargs) -> tuple[list[Line2D], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.arange(0.1, 4, 0.5)
        Y = np.exp(-X)
        Yerr = 0.1 + 0.2 * X
        Xerr = [0.4 * Yerr, Yerr]
    
    X = np.asarray(X)
    Y = np.asarray(Y)
    Yerr = np.asarray(Yerr)
    Xerr = np.asarray(Xerr)
    artist = list()
    props = {
        "capsize": capsize,
        "errorevery": errorevery
    }

    art = ax.errorbar(
        X, Y, Yerr, Xerr, 
        capsize=capsize, 
        errorevery=errorevery,
        *args, **kwargs
    )
    
    data_line = art.lines[0]
    artist.append(data_line)
    data_line.set_gid(f'{gid}/dataline')

    for cap in art.lines[1]:
        artist.append(cap)
        cap.set_gid(f'_{gid}/err')
    for err in art.lines[2]:
        artist.append(err)
        err.set_gid(f'_{gid}/err')

    return artist, props