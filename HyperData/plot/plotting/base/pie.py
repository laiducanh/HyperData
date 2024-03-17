from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Wedge
from typing import List

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