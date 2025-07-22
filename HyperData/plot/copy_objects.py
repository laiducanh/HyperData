from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.image import AxesImage
from matplotlib.legend import Legend
from matplotlib.figure import Figure
from matplotlib import lines, patches, collections, text, legend, artist
from plot.utilis import find_mpl_object, remove_legend, get_legend_anchor
from config.settings import logger
from typing import Union

def update_props(from_obj: artist.Artist, to_obj: artist.Artist) -> None:
    if isinstance(from_obj, lines.Line2D) and isinstance(to_obj, lines.Line2D):
        to_obj.set(
            visible = from_obj.get_visible(),
            alpha = from_obj.get_alpha(),
            color = from_obj.get_color(),
            dash_capstyle = from_obj.get_dash_capstyle(),
            dash_joinstyle = from_obj.get_dash_joinstyle(),
            linestyle = from_obj.get_linestyle(),
            linewidth = from_obj.get_linewidth(),
            marker = from_obj.get_marker(),
            markeredgecolor = from_obj.get_markeredgecolor(),
            markeredgewidth = from_obj.get_markeredgewidth(),
            markerfacecolor = from_obj.get_markerfacecolor(),
            markersize = from_obj.get_markersize(),
            solid_capstyle = from_obj.get_solid_capstyle(),
            solid_joinstyle = from_obj.get_solid_joinstyle(),
            zorder = from_obj.get_zorder(),
            label = from_obj.get_label(),
        )
    elif isinstance(from_obj, collections.Collection) and isinstance(to_obj, collections.Collection):
        to_obj.set(
            visible = from_obj.get_visible(),
            alpha = from_obj.get_alpha(),
            cmap = from_obj.get_cmap(),
            edgecolor = from_obj.get_edgecolor(),
            facecolor = from_obj.get_facecolor(),
            label = from_obj.get_label(),
            linestyle = from_obj.get_linestyle(),
            linewidth = from_obj.get_linewidth(),
            zorder = from_obj.get_zorder()
        )
    elif isinstance(from_obj, patches.Patch) and isinstance(to_obj, patches.Patch):
        to_obj.set(
            visible = from_obj.get_visible(),
            alpha = from_obj.get_alpha(),
            edgecolor = from_obj.get_edgecolor(),
            facecolor = from_obj.get_facecolor(),
            label = from_obj.get_label(),
            linestyle = from_obj.get_linestyle(),
            linewidth = from_obj.get_linewidth(),
            zorder = from_obj.get_zorder()
        )
    elif isinstance(from_obj, AxesImage) and isinstance(to_obj, AxesImage):
        to_obj.set(
            visible = from_obj.get_visible(),
            alpha = from_obj.get_alpha(),
            cmap = from_obj.get_cmap(),
            extent = from_obj.get_extent(),
            filternorm = from_obj.get_filternorm(),
            filterad = from_obj.get_filterrad(),
            interpolation = from_obj.get_interpolation(),
            label = from_obj.get_label(),
            resample = from_obj.get_resample(),
            zorder = from_obj.get_zorder()
        )
    elif isinstance(from_obj, text.Text) and isinstance(to_obj, text.Text):
        to_obj.set(
            visible = from_obj.get_visible(),
            alpha = from_obj.get_alpha(),
            color = from_obj.get_color(),
            fontfamily = from_obj.get_fontfamily(),
            fontproperties = from_obj.get_fontproperties(),
            fontsize = from_obj.get_fontsize(),
            fontstyle = from_obj.get_fontstyle(),
            fontvariant = from_obj.get_fontvariant(),
            fontweight = from_obj.get_fontweight(),
            horizontalalignment = from_obj.get_horizontalalignment(),
            label = from_obj.get_label(),
            math_fontfamily = from_obj.get_math_fontfamily(),
            parse_math = from_obj.get_parse_math(),
            position = from_obj.get_position(),
            rotation = from_obj.get_rotation(),
            rotation_mode = from_obj.get_rotation_mode(),
            verticalalignment = from_obj.get_verticalalignment(),
            wrap = from_obj.get_wrap(),
            zorder = from_obj.get_zorder()
        )
    logger.info(f"Canvas {to_obj.figure.canvas.id}: Update artist properties from {from_obj} to {to_obj}.")

def update_legend(old_legend:Legend, ax:Axes, **kwargs) -> Legend:
    
    legend_title = old_legend.get_title()
    legend_texts = old_legend.get_texts()
    legend_patch = old_legend.legendPatch
    params = {
        "handles": old_legend.legend_handles,
        "numpoints": old_legend.numpoints,
        "scatterpoints": old_legend.scatterpoints,
        "ncols": old_legend._ncols,
        "columnspacing": old_legend.columnspacing,
        "shadow": old_legend.shadow,
        "borderpad": old_legend.borderpad,
        "handlelength": old_legend.handlelength,
        "handleheight": old_legend.handleheight,
        "handletextpad": old_legend.handletextpad,
        "title": old_legend.get_title().get_text()
    }
    params.update(**kwargs)
    anchor_point = get_legend_anchor(old_legend.figure)
    bbox_transform = old_legend.figure.transFigure
    # remove the old legend
    remove_legend(old_legend.figure)
    # draw new legend based on anchor point of the old one.
    legend = ax.legend(
        loc=anchor_point,
        bbox_to_anchor=anchor_point,
        bbox_transform=bbox_transform,
        draggable=True,
        **params
    )
    legend.set_gid('legend')

    update_props(legend_title, legend.get_title())
    for new_text, old_text in zip(legend.get_texts(), legend_texts):
        update_props(old_text, new_text)
    update_props(legend_patch, legend.legendPatch)

    logger.info(f"Canvas {ax.figure.canvas.id}: Update legend.")

    return legend

def copy_Axes(source_ax:Union[Axes,Axes3D], destination_ax:Union[Axes,Axes3D]):
    # Copy Axes properties
    destination_ax.set(
        aspect=source_ax.get_aspect(),
        xscale=source_ax.get_xscale(),
        yscale=source_ax.get_yscale(),
        facecolor=source_ax.get_facecolor(),
        gid=source_ax.get_gid()
    )

    if isinstance(source_ax, Axes3D) and isinstance(destination_ax, Axes3D):
        destination_ax._axis3don = source_ax._axis3don
    else:
        destination_ax.axison = source_ax.axison
    
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
    for obj in source_ax.findobj(
        lambda a: isinstance(a, lines.Line2D) and a.get_gid() \
        and 'spine' in a.get_gid()
    ):
        for new_obj in destination_ax.findobj(
            lambda a: isinstance(a, lines.Line2D) and a.get_gid() \
            and obj.get_gid() == a.get_gid()
        ):
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

    # Recreate only artist whose gid
    for artist in source_ax.findobj(lambda a: a.get_gid()):
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
            ax = destination_ax.figure.findobj(
                lambda a: isinstance(a, (Axes, Axes3D)) and a.get_gid() \
                and a.get_gid() == 'legend axes'
            )[0]
            update_legend(artist, ax)

        if new_artist:
            destination_ax.add_artist(new_artist)
            destination_ax.figure.add_artist(new_artist)
            # Update gid
            new_artist.set_gid(artist.get_gid())
            # Update props
            update_props(artist, new_artist)
            if not isinstance(new_artist, 
                              (collections.PathCollection, text.Text)):
                new_artist.set_transform(destination_ax.transData)  
    logger.info(f'Canvas {destination_ax.figure.canvas.id}: Copy artists from {source_ax.get_gid()} to {destination_ax.get_gid()}.')

def copy_Drawings(source_fig:Figure, destination_fig:Figure):
    for artist in source_fig.findobj(lambda a: a.get_gid() and "drawing" in a.get_gid()):
        new_artist = None
        if isinstance(artist, patches.Rectangle):
            new_artist = patches.Rectangle(
                    artist.xy,
                    artist.get_width(),
                    artist.get_height(),
                )
        elif isinstance(artist, lines.Line2D):
            new_artist = lines.Line2D(
                    artist.get_xdata(),
                    artist.get_ydata(),
                )
        elif isinstance(artist, patches.Ellipse):
            new_artist = patches.Ellipse(
                artist.get_center(),
                artist.get_width(),
                artist.get_height()
            )
        elif isinstance(artist, text.Text):
            new_artist = text.Text(
                artist.get_position()[0],
                artist.get_position()[1],
                artist.get_text(),
            )
        if new_artist:
            # add to figure
            destination_fig.add_artist(new_artist)
            # Update gid
            new_artist.set_gid(artist.get_gid())
            # Update props
            update_props(artist, new_artist)

def copy_Figure(source_fig:Figure, destination_fig:Figure):

    copy_Drawings(source_fig, destination_fig)

    for source_ax, destination_ax in zip(source_fig.axes, destination_fig.axes):
        copy_Axes(source_ax, destination_ax)