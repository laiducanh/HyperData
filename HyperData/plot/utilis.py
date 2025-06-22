from matplotlib.colors import to_hex
from matplotlib.artist import Artist
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import lines, patches, collections, text, legend
from mpl_toolkits.mplot3d.axes3d import Axes3D
from typing import Literal, Union
import numpy as np
from config.settings import GLOBAL_DEBUG, logger

def get_color(artist:Artist):
    """ get color of a matplotlib artist"""
    
    if isinstance(artist, lines.Line2D):
        return to_hex(artist.get_color())
    
    elif isinstance(artist, (collections.PolyCollection, collections.QuadMesh)): 
        return to_hex(artist.get_facecolor()[0])
    
    elif isinstance(artist, collections.PathCollection):
        return to_hex(np.max(artist.get_facecolor(), axis=0))
    
    elif isinstance(artist, collections.LineCollection):
        return to_hex(artist.get_edgecolor()[0])

    elif isinstance(artist, (patches.Patch, patches.Rectangle)):
        return to_hex(artist.get_facecolor())

    return "white"

def find_mpl_object(source:Union[Figure,Axes,Axes3D], match:list=None, gid:str=None, rule:Literal["exact","contain"]="contain") -> list[Artist]:

    """ This function is used to find artist plot (having gid) in matplotlib,
        for other objects such as text, use matplotlib function findobj() instead """

    obj_found = list()
    if not match:
        match = [lines.Line2D,collections.Collection,patches.Patch,AxesImage,legend.Legend,text.Text]
    
    for artist_class in match:
        _found: list[Artist] = source.findobj(match=artist_class)
        for artist in _found:
            if artist.get_gid():
                if gid:
                    if rule == "contain" and gid in artist.get_gid():
                        obj_found.append(artist)
                    elif rule == "exact" and gid == artist.get_gid():
                        obj_found.append(artist)
                else: obj_found.append(artist)
        #obj_found += [artist for artist in _found if artist.get_gid() != None]
    return obj_found

def update_props (from_obj: Artist, to_obj: Artist) -> None:  
    try:      
        #print("update props")
        #print(to_obj, from_obj)
        to_obj_props = to_obj.properties()
        from_obj_props = from_obj.properties()

        if type(from_obj) == type(to_obj):
            to_obj.update_from(from_obj)

        to_obj.update(dict(label=from_obj.get_label()))
        
    except Exception as e:
        logger.exception(e)

def copy_Axes(source_ax:Union[Axes,Axes3D], destination_ax:Union[Axes,Axes3D]):
    # Copy Axes properties
    destination_ax.set(
        aspect=source_ax.get_aspect(),
        xscale=source_ax.get_xscale(),
        yscale=source_ax.get_yscale(),
        facecolor=source_ax.get_facecolor(),
    )
    
    destination_ax.title.set(
        text=source_ax.get_title(),
        fontname=source_ax.title.get_fontname(),
        fontsize=source_ax.title.get_fontsize(),
        color=source_ax.title.get_color(),
        alpha=source_ax.title.get_alpha(),
        fontstyle=source_ax.title.get_fontstyle(),
        fontweight=source_ax.title.get_fontweight()
    )

    # Copy tick locations
    destination_ax.set_xticks(source_ax.get_xticks(), minor=False)
    destination_ax.set_xticks(source_ax.get_xticks(minor=True), minor=True)
    destination_ax.set_yticks(source_ax.get_yticks(), minor=False)
    destination_ax.set_yticks(source_ax.get_yticks(minor=True), minor=True)
    
    # Copy tick labels
    destination_ax.set_xticklabels([label.get_text() for label in source_ax.get_xticklabels(minor=False)], minor=False)
    destination_ax.set_xticklabels([label.get_text() for label in source_ax.get_xticklabels(minor=True)], minor=True)
    destination_ax.set_yticklabels([label.get_text() for label in source_ax.get_yticklabels(minor=False)], minor=False)
    destination_ax.set_yticklabels([label.get_text() for label in source_ax.get_yticklabels(minor=True)], minor=True)

    destination_ax.xaxis.set(
        visible = source_ax.xaxis.get_visible(),
        label_text = source_ax.xaxis.get_label_text()
    )
    destination_ax.xaxis.label.set(
        fontname = source_ax.xaxis.label.get_fontname(),
        fontsize = source_ax.xaxis.label.get_fontsize(),
        color = source_ax.xaxis.label.get_color(),
        alpha = source_ax.xaxis.label.get_alpha(),
        fontstyle=source_ax.xaxis.label.get_fontstyle(),
        fontweight=source_ax.xaxis.label.get_fontweight()
    )

    destination_ax.yaxis.set(
        visible = source_ax.yaxis.get_visible(),
        label_text = source_ax.yaxis.get_label_text()
    )
    destination_ax.yaxis.label.set(
        fontname = source_ax.yaxis.label.get_fontname(),
        fontsize = source_ax.yaxis.label.get_fontsize(),
        color = source_ax.yaxis.label.get_color(),
        alpha = source_ax.yaxis.label.get_alpha(),
        fontstyle=source_ax.yaxis.label.get_fontstyle(),
        fontweight=source_ax.yaxis.label.get_fontweight()
    )

    # Copy tick parameters
    for which in ["major","minor"]:
        destination_ax.xaxis.set_tick_params(which=which, **source_ax.xaxis.get_tick_params(which=which))
        destination_ax.yaxis.set_tick_params(which=which, **source_ax.yaxis.get_tick_params(which=which))

    # Copy Axes limits
    destination_ax.set_xlim(source_ax.get_xlim())
    destination_ax.set_ylim(source_ax.get_ylim())
    if isinstance(destination_ax, Axes3D):
        destination_ax.set_zlim(source_ax.get_zlim())
    
    # Spines
    for name, spine in source_ax.spines.items():
        destination_ax.spines[name].set(
            visible=spine.get_visible(),
            alpha=spine.get_alpha(),
            linestyle=spine.get_linestyle(),
            linewidth=spine.get_linewidth(),
            color=spine.get_edgecolor(),
            gid=spine.get_gid()
        )
    for obj in find_mpl_object(source_ax, match=[lines.Line2D], gid="spine"):
        for new_obj in find_mpl_object(destination_ax, match=[lines.Line2D], gid=obj.get_gid()):
            new_obj.set(
                marker=obj.get_marker(),
                markerfacecolor=obj.get_markerfacecolor(),
                transform=destination_ax.transAxes,
                clip_on=obj.get_clip_on(),
            )

    # Pane
    destination_ax.patch.set(
        visible = source_ax.patch.get_visible(),
        color = source_ax.patch.get_facecolor(),
        alpha = source_ax.patch.get_alpha(),
    )
    destination_ax.figure.set_facecolor(source_ax.figure.get_facecolor())

    # Margins
    destination_ax.figure.subplots_adjust(
        left=source_ax.figure.subplotpars.left,
        right=source_ax.figure.subplotpars.right,
        bottom=source_ax.figure.subplotpars.bottom,
        top=source_ax.figure.subplotpars.top,
        wspace=source_ax.figure.subplotpars.wspace,
        hspace=source_ax.figure.subplotpars.hspace
    )

    # Recreate artist
    for artist in find_mpl_object(source_ax):
        new_artist = None
        if "graph" in artist.get_gid():
            if isinstance(artist, lines.Line2D):
                new_artist = lines.Line2D(
                    artist.get_xdata(),
                    artist.get_ydata(),
                )
            elif isinstance(artist, patches.Wedge):
                new_artist = patches.Wedge(
                    artist.center,
                    artist.r,
                    artist.theta1,
                    artist.theta2
                )
                destination_ax.set_aspect("equal", adjustable="box")
            elif isinstance(artist, patches.Rectangle):
                new_artist = patches.Rectangle(
                    artist.xy,
                    artist.get_width(),
                    artist.get_height(),
                )
            elif isinstance(artist, patches.PathPatch):
                new_artist = patches.PathPatch(
                    artist.get_path()
                )
            elif isinstance(artist, patches.FancyBboxPatch):
                new_artist = patches.FancyBboxPatch(
                    (artist.get_x(), artist.get_y()),
                    artist.get_width(),
                    artist.get_height()
                )
            elif isinstance(artist, patches.PathPatch):
                new_artist = patches.PathPatch(
                    artist.get_path()
                )
            elif isinstance(artist, collections.PolyCollection):
                new_artist = collections.PolyCollection(
                    [artist.get_paths()[0].vertices]
                )
            elif isinstance(artist, collections.PathCollection):
                new_artist = collections.PathCollection(
                    paths=[artist.get_paths()[0]],
                    sizes=artist.get_sizes(),
                    offsets=artist.get_offsets(),
                    offset_transform=destination_ax.transData,
                )
            elif isinstance(artist, collections.EventCollection):
                new_artist = collections.EventCollection(
                    positions=artist.get_positions(),
                    lineoffset=artist.get_lineoffset()
                )
            elif isinstance(artist, collections.LineCollection):
                new_artist = collections.LineCollection(
                    [path.vertices for path in artist.get_paths()]
                )
            elif isinstance(artist, collections.QuadMesh):
                new_artist = collections.QuadMesh(
                    artist.get_coordinates()
                )
        elif isinstance(artist, text.Text):
            new_artist = text.Text(
                artist.get_position()[0],
                artist.get_position()[1],
                artist.get_text(),
                transform=destination_ax.transAxes
            )
        elif isinstance(artist, legend.Legend):
            new_artist = legend.Legend(
                destination_ax,
                artist.legend_handles,
                [i.get_label() for i in artist.legend_handles],
                title=artist.get_title().get_text()
            )
            title_transform = new_artist.get_title().get_transform()
            new_artist.get_title().update_from(artist.get_title())
            new_artist.get_title().set_transform(title_transform)
            bbox = source_ax.transAxes.inverted().transform((
                artist.get_tightbbox().x0,
                artist.get_tightbbox().y0
            ))
            new_artist.set_bbox_to_anchor(bbox, destination_ax.transAxes)
            new_artist.set_loc("lower left") # because bbox is computed from (x0, y0)
            #TO-DO: the legend box actually shifts up and right a little bit

        if new_artist:
            # Update gid
            new_artist.set_gid(artist.get_gid())
            # Update props
            update_props(artist, new_artist)
            if not isinstance(new_artist, 
                              (collections.PathCollection, text.Text)):
                new_artist.set_transform(destination_ax.transData)  
            destination_ax.add_artist(new_artist)

    
