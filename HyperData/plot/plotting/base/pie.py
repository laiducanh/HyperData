from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Wedge, Rectangle
from typing import List
import squarify, matplotlib, numpy

def pie (X, ax: Axes, gid) -> List[Wedge]:

    artist = ax.pie(X)

    # artist has type of [[wedges],[text],[autotexts]] -> take the first elements to return a list of wedges
    artist = artist[0]

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def doughnut (X, ax:Axes, gid, width=0.3) -> List[Wedge]:

    artist = ax.pie(X, wedgeprops=dict(width=width))

    artist = artist[0]

    for ind, obj in enumerate(artist):
        if len(artist) > 1:
            obj.set_gid(f"{gid}.{ind+1}")
        else:
            obj.set_gid(gid)

    return artist

def treemap (X, ax:Axes, gid) -> List[Rectangle]:

    X.sort(reverse=True)
    values = squarify.normalize_sizes(X,1,1)
    rects = squarify.squarify(values,0,0,1,1)

    colors = matplotlib.colormaps["tab10"](numpy.linspace(0,1,len(X)))

    artist = list()
    for _ind_face, _rect in enumerate(rects):

        rect = Rectangle((_rect['x'],_rect['y']),_rect['dx'],_rect['dy'],
                            color=colors[_ind_face],gid=f"{gid}.{_ind_face+1}"
                                        )
        ax.add_artist(rect)
        artist.append(rect)
    
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    
    return artist