from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, PathPatch, Ellipse
from matplotlib.lines import Line2D
from matplotlib.collections import PolyCollection, LineCollection, EventCollection, QuadMesh, PathCollection
from plot.utilis import complementary_color
import numpy as np
import matplotlib
from pandas.plotting._matplotlib.style import get_standard_colors
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

def pareto(X, Y, ax:Axes, gid:str, width=0.8, bottom=0, align="center", *args, **kwargs) -> tuple[list[Union[Rectangle, Line2D]], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = range(3)
        Y = [40, 25, 10]
    
    X = np.asarray(X)
    Y = np.asarray(Y)
    Y_cum = np.cumsum(Y-bottom)/np.sum(Y-bottom)*100
    
    artist = list()
    props = {
        "width": width,
        "bottom": bottom,
        "align": align
    }

    bars = ax.bar(X, Y, gid=f"{gid}/bar", width=width, bottom=bottom, align=align, *args, **kwargs)
    artist += bars.patches

    line = ax.figure.canvas.axesy2.plot(X, Y_cum, gid=f"{gid}/line", 
                                        c=complementary_color(bars.patches[0].get_facecolor()))
    artist += line

    return artist, props

def _andrews_helper(amplitudes):
    def f(t):
        x1 = amplitudes[0]
        result = x1 / np.sqrt(2.0)

        # Take the rest of the coefficients and resize them
        # appropriately. Take a copy of amplitudes as otherwise numpy
        # deletes the element from amplitudes itself.
        coeffs = np.delete(np.copy(amplitudes), 0)
        coeffs = np.resize(coeffs, (int((coeffs.size + 1) / 2), 2))

        # Generate the harmonics and arguments for the sin and cos
        # functions.
        harmonics = np.arange(0, coeffs.shape[0]) + 1
        trig_args = np.outer(harmonics, t)

        result += np.sum(
            coeffs[:, 0, np.newaxis] * np.sin(trig_args)
            + coeffs[:, 1, np.newaxis] * np.cos(trig_args),
            axis=0,
        )
        return result

    return f

def andrews(X, Y, ax:Axes, gid:str, samples=200, *args, **kwargs) -> tuple[list[Line2D], dict]:

    if DEBUG or GLOBAL_DEBUG:
        from sklearn.datasets import load_iris
        iris = load_iris()
        X = iris.data
        Y = iris.target_names[iris.target]
    
    X = np.asarray(X)
    Y = np.asarray(Y)
    artist = list()
    props = {
        "samples": samples,
    }

    n = len(X)
    classes = np.unique(Y)
    t = np.linspace(-np.pi, np.pi, samples)
    color_values = get_standard_colors(
        num_colors=len(classes), colormap=None, color_type="default", color=None
    )
    colors = dict(zip(classes, color_values))
    for i in range(n):
        f = _andrews_helper(X[i])
        y = f(t)
        kls = Y[i]
        line = ax.plot(
            t, y, 
            color=colors[kls],
            marker='none', 
            lw=1, 
            label=kls,
            gid=f'{gid}.{np.where(classes==kls)[0][0]+1}'
            )
        artist += line
    
    return artist, props

def cov_ellipse(X, Y, ax:Axes, gid:str, n_std=2, sizes=1, *args, **kwargs) -> tuple[list[Union[PathCollection, Ellipse]], dict]:

    if DEBUG or GLOBAL_DEBUG:
        data = np.random.multivariate_normal([0, 0], [[3, 1], [1, 2]], size=300)
        X = data[:, 0]
        Y = data[:, 1]
    
    data = np.column_stack((X, Y))
    mean = np.mean(data, axis=0)
    cov = np.cov(data, rowvar=False)
    artist = list()
    props = {
        "n_std": n_std,
        "sizes": sizes
    }

    # Eigen decomposition
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]

    # Compute angle and ellipse width/height
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    width, height = 2 * n_std * np.sqrt(vals)

    # Draw scatter for raw data
    sct = ax.scatter(
        X, Y, 
        s=matplotlib.rcParams["lines.markersize"]**2*sizes,
        gid=f'{gid}/scatter'
    )
    artist.append(sct)

    # Draw ellipse
    ellipse = Ellipse(
        xy=mean, 
        width=width, 
        height=height, 
        angle=theta,
        edgecolor=complementary_color(sct.get_facecolor()),
        facecolor='none',
        lw=2,
        gid=f'{gid}/ellipse'
    )
    ax.add_patch(ellipse)
    artist.append(ellipse)
    
    

    return artist, props