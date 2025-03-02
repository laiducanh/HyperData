from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.lines import Line2D
from matplotlib.collections import PolyCollection, LineCollection, EventCollection, QuadMesh
import numpy as np
from config.settings import logger, GLOBAL_DEBUG
from typing import Union

DEBUG = True

def histogram(X, ax:Axes, gid:str, bins=10, density=False, cumulative=False,
              bottom=0, histtype="bar", align="mid", orientation="vertical",
              rwidth=None, log=False, *args, **kwargs) -> list[Rectangle]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(1000, 3)
    
    X = np.asarray(X)

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
            art.bins = bins
            art.density = density
            art.cumulative = cumulative
            art.bottom = bottom
            art.histtype = histtype
            art.align = align
            art.orientation = orientation
            art.rwidth = rwidth
            art.log = log
            art.Xdata = x
            art.Ydata = y
            art.Xshow = art.get_center()[0]
            art.Yshow = y
            artist.append(art)
    elif np.ndim(_artist[0]) > 1:
        for idx in range(len(_artist[0])):
            for y, x, art in zip(_artist[0][idx],_artist[1],_artist[2][idx]):
                art.set_gid(gid=f"{gid}.{idx+1}")
                art.bins = bins
                art.density = density
                art.cumulative = cumulative
                art.bottom = bottom
                art.histtype = histtype
                art.align = align
                art.orientation = orientation
                art.rwidth = rwidth
                art.log = log
                art.Xdata = x
                art.Ydata = y
                art.Xshow = art.get_center()[0]
                art.Yshow = y
                artist.append(art)

    ax.set_axis_on()
    
    return artist

def stacked_histogram(X, ax:Axes, gid:str, bins=10, density=False, cumulative=False,
                      bottom=0, histtype="bar", align="mid", orientation="vertical",
                      rwidth=None, log=False, *args, **kwargs) -> list[Rectangle]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(1000, 3)
    
    X = np.asarray(X)
    
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
            art.bins = bins
            art.density = density
            art.cumulative = cumulative
            art.bottom = bottom
            art.histtype = histtype
            art.align = align
            art.orientation = orientation
            art.rwidth = rwidth
            art.log = log
            art.Xdata = x
            art.Ydata = y
            art.Xshow = art.get_center()[0]
            art.Yshow = y
            artist.append(art)
    elif np.ndim(_artist[0]) > 1:
        for idx in range(len(_artist[0])):
            for y, x, art in zip(_artist[0][idx],_artist[1],_artist[2][idx]):
                art.set_gid(gid=f"{gid}.{idx+1}")
                art.bins = bins
                art.density = density
                art.cumulative = cumulative
                art.bottom = bottom
                art.histtype = histtype
                art.align = align
                art.orientation = orientation
                art.rwidth = rwidth
                art.log = log
                art.Xdata = x
                art.Ydata = y
                art.Xshow = art.get_center()[0]
                art.Yshow = y
                artist.append(art)
        
    ax.set_axis_on()
    
    return artist

def boxplot(X, ax:Axes, gid:str, showbox = True, notch = False,
            vert = True, widths = 0.5, whis = 1.5, autorange = False,
            showcaps = True, capwidths = 0, showfliers = True,
            bootstrap = 1000, showmeans = False, meanline = False, *args, **kwargs) -> list[Union[Line2D,PathPatch]]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(1000, 1)

    X = np.asarray(X)

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
        art.set_gid(gid=f"{gid}/medians")
    for art in _artist.get("whiskers"):
        artist.append(art)
        art.set_gid(gid=f"{gid}/whiskers")
    for art in _artist.get("caps"):
        artist.append(art)
        art.set_gid(gid=f"{gid}/caps")
    for art in _artist.get("fliers"):
        artist.append(art)
        art.set_gid(gid=f"{gid}/fliers")
    for art in _artist.get("means"):
        artist.append(art)
        art.set_gid(gid=f"{gid}/means")

    for art in artist:
       # print("abc", art, art.get_gid())
        art.showbox = showbox
        art.notch = notch
        art.vert = vert
        art.widths = widths
        art.whis = whis
        art.autorange = autorange
        art.showcaps = showcaps
        art.capwidths = capwidths
        art.showfliers = showfliers
        art.bootstrap = bootstrap
        art.showmeans = showmeans
        art.meanline = meanline
    
    ax.set_axis_on()
   
    return artist

def violinplot(X, ax:Axes, gid:str, orientation='vertical', widths=0.5,
               showmeans=False, showextrema=True, showmedians=False,
               points=100, bw_method="scott", quantiles=None, *args, **kwargs) -> list[Union[PolyCollection, LineCollection]]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(1000, 3)
    
    X = np.asarray(X)

    artist = list()
    _artist = ax.violinplot(
        X, 
        orientation=orientation, 
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
        cmeans.set_gid(gid=f"{gid}/cmeans")
    if cmins: 
        artist.append(cmins)
        cmins.set_gid(gid=f"{gid}/cmins")
    if cmaxes: 
        artist.append(cmaxes)
        cmaxes.set_gid(gid=f"{gid}/cmaxes")
    if cbars: 
        artist.append(cbars)
        cbars.set_gid(gid=f"{gid}/cbars")
    if cmedians: 
        artist.append(cmedians)
        cmedians.set_gid(gid=f"{gid}/cmedians")
    if cquantiles: 
        artist.append(cquantiles)
        cquantiles.set_gid(gid=f"{gid}/cquantiles")
    
    for art in artist:
        art.orientation = orientation
        art.widths = widths
        art.showmeans = showmeans
        art.showextrema = showextrema
        art.showmedians = showmedians
        art.quantiles = quantiles
        art.points = points
        art.bw_method = bw_method
        art.Xdata = None
        art.Ydata = None
        p = np.array(art.get_paths()[0].vertices).mean(axis=0)
        art.Xshow = p[0]
        art.Yshow = p[1]

    ax.set_axis_on()

    return artist

def eventplot(X, ax:Axes, gid:str, orientation="horizontal",
              lineoffsets=1, linelengths=1, *args, **kwargs) -> list[EventCollection]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.random.gamma(4, size=(3, 50))

    X = np.asarray(X)

    artist = ax.eventplot(
        X, 
        gid=gid, 
        orientation=orientation,
        lineoffsets=lineoffsets,
        linelengths=linelengths,
        *args, **kwargs
    )
    
    for art in artist:
        art.orientation = orientation
        art.lineoffsets = lineoffsets
        art.linelengths = linelengths
        art.Xdata = None
        art.Ydata = None
        p = np.array(art.get_paths()[0].vertices).mean(axis=0)
        art.Xshow = p[0]
        art.Yshow = p[1]
    
    ax.set_axis_on()

    return artist

def hist2d(X, Y, ax:Axes, gid:str, binx=10, biny=10, density=False, *args, **kwargs) -> list[QuadMesh]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.random.randn(5000)
        Y = 1.2 * X + np.random.randn(5000) / 3

    X = np.asarray(X)
    Y = np.asarray(Y)

    _, _, _, artist = ax.hist2d(X, Y, gid=gid, bins=(binx, biny), density=density, *args, **kwargs)

    artist.binx = binx
    artist.biny = biny
    artist.density = density

    return [artist]

