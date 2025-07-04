from matplotlib.axes import Axes
from matplotlib.patches import Wedge, Polygon
from matplotlib.lines import Line2D
from plot.utilis import complementary_color
import math
import numpy as np
from config.settings import GLOBAL_DEBUG, logger
from typing import Union

DEBUG = False

def pie (X, ax: Axes, gid, explode=None, labels=None, startangle=0,
         radius=1, counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> tuple[list[Wedge], dict]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.asarray([1,4])

    props = {
        "explode": explode,
        "labels": labels,
        "startangle": startangle,
        "radius": radius,
        "counterclock": counterclock,
        "rotatelabels": rotatelabels,
        "normalize": normalize
    }
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
        obj.Xdata = X[ind]
        obj.Ydata = None
        thetam = np.pi * (obj.theta2 + obj.theta1)/360
        obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
        obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)
        obj.set_gid(f"{gid}.{ind+1}")
        
    for ind, obj in enumerate(artist[1]):
        obj.set_gid(f"{gid}.{ind+1}")

    return artist[0], props

def coxcomb(X, ax:Axes, gid, explode=None, labels=None, startangle=0,
            radius=1, counterclock=True, rotatelabels=True, *args, **kwargs) -> tuple[list[Wedge], dict]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.array([10,8,15])
    
    X = np.asarray(X)
    X = (X/np.sum(X))/np.max(X/np.sum(X))

    props = {
        "explode": explode,
        "labels": labels,
        "startangle": startangle,
        "radius": radius,
        "counterclock": counterclock,
        "rotatelabels": rotatelabels
    }

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
        obj.Xdata = X[ind]
        obj.Ydata = None
        thetam = np.pi * (obj.theta2 + obj.theta1)/360
        obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
        obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)

        obj.set_gid(f"{gid}.{ind+1}")
        
    for ind, obj in enumerate(artist[1]):
        obj.set_gid(f"{gid}.{ind+1}")

    return artist[0], props

def doughnut (X, ax:Axes, gid, width=0.3, explode=None, labels=None, startangle=0,
              radius=1, counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> tuple[list[Wedge], dict]:
    
    if DEBUG or GLOBAL_DEBUG:
        X = np.asarray([1,4])
    
    props = {
        "width": width,
        "explode": explode,
        "labels": labels,
        "startangle": startangle,
        "radius": radius,
        "counterclock": counterclock,
        "rotatelabels": rotatelabels,
        "normalize": normalize
    }

    artist = ax.pie(X, wedgeprops=dict(width=width), explode=explode, labels=labels, startangle=startangle,
                    radius=radius, counterclock=counterclock, rotatelabels=rotatelabels, normalize=normalize, *args, **kwargs)

    artist = artist[0]

    for ind, obj in enumerate(artist):
        obj.Xdata = X[ind]
        obj.Ydata = None
        thetam = np.pi * (obj.theta2 + obj.theta1)/360
        obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
        obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)

        obj.set_gid(f"{gid}.{ind+1}")


    return artist, props

def multilevel_doughnut(X, ax:Axes, gid, width=0.25, explode=None, labels=None, startangle=0, pad=0.03, 
                        radius=1, counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> tuple[list[Wedge], dict]:
    if DEBUG or GLOBAL_DEBUG:
        X = np.array([[[20, 40], [18, 22]], [[10,12], [8,15]], [[15,14], [2,8]]])
    
    props = {
        "width": width,
        "explode": explode,
        "labels": labels,
        "startangle": startangle,
        "pad": pad,
        "radius": radius,
        "counterclock": counterclock,
        "rotatelabels": rotatelabels,
        "normalize": normalize
    }
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

    return artist, props

def semicircle_doughnut(X, ax:Axes, gid, width=0.3, explode=None, labels=None, startangle=0, radius=1, 
                        counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> tuple[list[Wedge], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = np.array([2,3])
    
    X = np.asarray(X)

    props = {
        "width": width,
        "explode": explode,
        "labels": labels,
        "startangle": startangle,
        "radius": radius,
        "counterclock": counterclock,
        "rotatelabels": rotatelabels,
        "normalize": normalize
    }

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
        obj.Xdata = X[ind]
        obj.Ydata = None
        thetam = np.pi * (obj.theta2 + obj.theta1)/360
        obj.Xshow = obj.center[0] + obj.r * math.cos(thetam)
        obj.Yshow = obj.center[1] + obj.r * math.sin(thetam)

        obj.set_gid(f"{gid}.{ind+1}")
    
    return artist, props

def radar(X, ax:Axes, gid:str, labels=None, startangle=0, *args, **kwargs) -> tuple[list[Union[Line2D, Polygon]], dict]:

    if DEBUG or GLOBAL_DEBUG:
        X = [4, 3, 5, 4, 2]
    
    X = np.asarray(X)
    X = np.append(X, X[0]) # Repeat the first value to close the circle

    artist = list()
    props = {
        "labels": labels,
        "startangle": startangle
    }

    startangle = np.radians(startangle)
    num_vars = len(X)-1

    # Compute angle for each axis
    angles = np.linspace(startangle, startangle + 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fill = ax.fill(angles, X, alpha=0.25, label='_child', gid=f'{gid}/fill')
    artist += fill
    line = ax.plot(
        angles, X, 
        color=complementary_color(fill[0].get_facecolor()),
        linewidth=2,
        gid=f'{gid}/line'
    )
    artist += line

    # Set labels
    ax.set_xticks(angles[:-1])
    if labels: ax.set_xticklabels(labels)

    # Adjust range
    ax.set_xlim(0, 2 * np.pi)
    # ax.set_ylim(0, np.max(X))

    return artist, props
    

    