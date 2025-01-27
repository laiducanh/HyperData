from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Wedge, Rectangle
from matplotlib.pyplot import colormaps
from matplotlib import cm
import math
import numpy as np
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

def pie (X, ax: Axes, gid, explode=None, labels=None, startangle=0,
         radius=1, counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> list[Wedge]:

    if explode != None and len(explode) != len(X):
        explode = None
    
    if labels != None and len(labels) != len(X):
        labels = None
    
    if not normalize and sum(X) > 1:
        X = [float(i)/sum(X) for i in X]
    
    artist = ax.pie(X, explode=explode, labels=labels, startangle=startangle,
                    radius=radius, counterclock=counterclock, rotatelabels=rotatelabels,
                    normalize=normalize, *args, **kwargs)

    # artist has type of [[wedges],[text],[autotexts]]
    for ind, obj in enumerate(artist[0]):
        obj.explode = explode
        obj.labels = labels
        obj.startangle = startangle
        obj.counterclock = counterclock
        obj.rotatelabels = rotatelabels
        obj.normalize = normalize
        obj.Xdata = X[ind]
        obj.Ydata = None
        thetam = np.pi * (obj.theta2 + obj.theta1)/360
        obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
        obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)
        obj.set_gid(f"{gid}.{ind+1}")
        
    for ind, obj in enumerate(artist[1]):
        obj.set_gid(f"{gid}.{ind+1}")

    return artist[0]

def coxcomb(X, ax:Axes, gid, explode=None, labels=None, startangle=0,
            radius=1, counterclock=True, rotatelabels=True, *args, **kwargs) -> list[Wedge]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.array([10,8,15])
    
    X = np.asarray(X)
    X = (X/np.sum(X))/np.max(X/np.sum(X))

    artist = ax.pie(
        np.repeat([1], len(X)), 
        explode=explode, 
        labels=labels, 
        startangle=startangle,
        radius=radius, 
        counterclock=counterclock, 
        rotatelabels=rotatelabels,
        *args, **kwargs
    )

    for ind, obj in enumerate(artist[0]):
        obj.set_radius(X[ind] * radius)

        obj.explode = explode
        obj.labels = labels
        obj.startangle = startangle
        obj.radius = radius
        obj.counterclock = counterclock
        obj.rotatelabels = rotatelabels
        obj.Xdata = X[ind]
        obj.Ydata = None
        thetam = np.pi * (obj.theta2 + obj.theta1)/360
        obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
        obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)

        obj.set_gid(f"{gid}.{ind+1}")
        
    for ind, obj in enumerate(artist[1]):
        obj.set_gid(f"{gid}.{ind+1}")

    return artist[0]

def doughnut (X, ax:Axes, gid, width=0.3, explode=None, labels=None, startangle=0,
              radius=1, counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> list[Wedge]:

    artist = ax.pie(X, wedgeprops=dict(width=width), explode=explode, labels=labels, startangle=startangle,
                    radius=radius, counterclock=counterclock, rotatelabels=rotatelabels, normalize=normalize, *args, **kwargs)

    artist = artist[0]

    for ind, obj in enumerate(artist):
        obj.width = width
        obj.explode = explode
        obj.labels = labels
        obj.startangle = startangle
        obj.radius = radius
        obj.counterclock = counterclock
        obj.rotatelabels = rotatelabels
        obj.normalize = normalize
        obj.Xdata = X[ind]
        obj.Ydata = None
        thetam = np.pi * (obj.theta2 + obj.theta1)/360
        obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
        obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)

        obj.set_gid(f"{gid}.{ind+1}")


    return artist

def multilevel_doughnut(X, ax:Axes, gid, width=0.25, explode=None, labels=None, startangle=0, pad=0.03, 
                        radius=1, counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> list[Wedge]:
    if DEBUG or GLOBAL_DEBUG:
        X = np.array([[[20, 40], [18, 22]], [[10,12], [8,15]], [[15,14], [2,8]]])
        
    X = np.asarray(X)
    artist: list[Wedge] = list()
    cumshape = np.cumprod(X.shape)
    
    gid_list = list()
    color_list = list()

    for dim in range(X.ndim):
        _x = X.reshape(cumshape[dim], -1)
        c = np.linspace(dim, cumshape.sum()-dim, cumshape[dim])
        c = c/cumshape.sum()
        art = ax.pie(
            _x.sum(axis=1), 
            radius=radius-dim*(width+pad),
            wedgeprops=dict(width=width),
            explode=explode, 
            labels=labels, 
            startangle=startangle,
            counterclock=counterclock, 
            rotatelabels=rotatelabels, 
            normalize=normalize,
            *args, **kwargs
        )

        if dim:
            gid_list = np.repeat(gid_list, X.shape[dim])
            color_list = np.repeat(color_list, X.shape[dim],axis=0)
        
        for ind, obj in enumerate(art[0]):
            obj.width = width
            obj.explode = explode
            obj.labels = labels
            obj.startangle = startangle
            obj.radius = radius
            obj.counterclock = counterclock
            obj.rotatelabels = rotatelabels
            obj.normalize = normalize
            obj.pad = pad
            obj.Xdata = _x.sum(axis=1)[ind]
            obj.Ydata = None
            thetam = np.pi * (obj.theta2 + obj.theta1)/360
            obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
            obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)
            
            if not dim:
                obj.set_gid(f"{gid}.{ind+1}")
                gid_list.append(f"{gid}.{ind+1}")
                color_list.append(obj.get_facecolor())
            else:
                obj.set_gid(f"{gid_list[ind]}")
                obj.set_color(color_list[ind])

        artist += art[0]
    
    for _gid in set(gid_list):
        i = 1
        for obj in artist:
            if obj.get_gid() == _gid:
                c = np.array([obj.get_facecolor()])
                color = (1-1/i)*(1-c) + c
                obj.set_facecolor(color)
                i += 1/np.sum(X.shape)

    return artist

def semicircle_doughnut(X, ax:Axes, gid, width=0.3, explode=None, labels=None, startangle=0, radius=1, 
                        counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> list[Wedge]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.array([2,3])
    
    X = np.asarray(X)

    artist = ax.pie(
        X/(2*np.sum(X)), 
        wedgeprops=dict(width=width), 
        explode=explode, 
        labels=labels, 
        startangle=startangle,
        radius=radius, 
        counterclock=counterclock, 
        rotatelabels=rotatelabels, 
        normalize=False, 
        *args, **kwargs
    )
    
    artist = artist[0]

    for ind, obj in enumerate(artist):
        obj.width = width
        obj.explode = explode
        obj.labels = labels
        obj.startangle = startangle
        obj.radius = radius
        obj.counterclock = counterclock
        obj.rotatelabels = rotatelabels
        obj.normalize = normalize
        obj.Xdata = X[ind]
        obj.Ydata = None
        thetam = np.pi * (obj.theta2 + obj.theta1)/360
        obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
        obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)

        obj.set_gid(f"{gid}.{ind+1}")
    
    return artist