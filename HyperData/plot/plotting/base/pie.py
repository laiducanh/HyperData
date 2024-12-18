from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Wedge, Rectangle
from typing import List
import math
import numpy as np

def pie (X, ax: Axes, gid, explode=None, labels=None, startangle=0,
         radius=1, counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> List[Wedge]:

    if explode != None and len(explode) != len(X):
        explode = None
    
    if labels != None and len(labels) != len(X):
        labels = None
    
    if not normalize and sum(X) > 1:
        X = [float(i)/sum(X) for i in X]

    artist = ax.pie(X, explode=explode, labels=labels, startangle=startangle,
                    radius=radius, counterclock=counterclock, rotatelabels=rotatelabels,
                    normalize=normalize, frame=True, *args, **kwargs)

    # artist has type of [[wedges],[text],[autotexts]]
    for ind, obj in enumerate(artist[0]):
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

        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)
    
    for ind, obj in enumerate(artist[1]):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist[0]

def doughnut (X, ax:Axes, gid, width=0.3, explode=None, labels=None, startangle=0,
              radius=1, counterclock=True, rotatelabels=True, normalize=True, *args, **kwargs) -> List[Wedge]:

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

        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist