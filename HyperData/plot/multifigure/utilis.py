from matplotlib.artist import Artist
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import lines, patches, collections, text, legend
from plot.plotting.plotting import update_props, find_mpl_object

def copy_objects(source_ax:Axes|Axes3D, destination_ax:Axes|Axes3D):
    
    for artist in find_mpl_object(source_ax):
        #print(artist, artist.get_gid())
        new_artist = None
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
                [artist.get_paths()[0].vertices]
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
            update_props(artist, new_artist)
            if not isinstance(new_artist, 
                              (collections.PathCollection, text.Text)):
                new_artist.set_transform(destination_ax.transData)  
            destination_ax.add_artist(new_artist)

    destination_ax.set_xlim(source_ax.get_xlim())
    destination_ax.set_ylim(source_ax.get_ylim())
    if isinstance(destination_ax, Axes3D):
        destination_ax.set_zlim(source_ax.get_zlim())
