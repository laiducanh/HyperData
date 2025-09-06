from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtCore import Signal
import matplotlib, pickle, os
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.lines import Line2D
from matplotlib.colorbar import Colorbar
from matplotlib.cm import ScalarMappable
from mpl_toolkits.mplot3d.axes3d import Axes3D
from plot.copy_objects import copy_Figure
from config.settings import config, logger
from typing import Literal
import numpy as np

matplotlib.use("QtAgg")
#matplotlib.style.use('bmh')
#matplotlib.pyplot.rcParams['text.usetex'] = True
#plt.rcParams['mathtext.fontset'] = 'cm'
#plt.rcParams['mathtext.default'] = 'regular'

#matplotlib.rcParams['figure.figsize'] = [20,20]

class Canvas (FigureCanvasQTAgg):
    sig_text = Signal(object)
    sig_removeText = Signal()
    sig_pickedArtist = Signal(object)
    sig_openMenu = Signal(object)
    sig_hover = Signal() # to use in future
    sig_serialize = Signal()
    def __init__(self):
        self.id = id(self)
        self._config = {
                # 'margin': (0.12, 0.12, 0.9, 0.9),
                "grid": {
                    "visible": False,
                    "which": matplotlib.rcParams['axes.grid.which'],
                    "xaxis": matplotlib.rcParams['axes.grid.axis'] in ['x','both'],
                    "yaxis": matplotlib.rcParams['axes.grid.axis'] in ['y','both'],                  
                    "coord": "bottom-left",
                }, 
                "cbar": {
                    "visible": True,
                    "size": 0.05,
                    "pad": 0.05,
                    "loc": "right"
                }
            }
        self.figure = Figure()
        self.figure.set_dpi(100)
        self.figure.suptitle('')
        # self.fig.subplots_adjust(*self._config['margin'])
        self.initAxes()

        super().__init__(self.figure)
    
    def initAxes (self):

        # Bottom-Left Axes
        self.axes = self.figure.add_subplot()
        self.axes.spines[:].set_visible(False)

        # Bottom-Right Axes
        self.axesy2 = self.axes.twinx()
        self.axesy2.spines[:].set_visible(False)

        # Top-Left Axes
        self.axesx2 = self.axes.twiny()
        self.axesx2.spines[:].set_visible(False)

        # Axes for Pie-like plots
        self.axespie = self.figure.add_subplot()
        self.axespie.set_axis_off()

        # Axes for plots using polar coordinate system
        self.axespolar = self.figure.add_subplot(projection='polar')
        self.axespolar.set_axis_off()

        # Axes for colorbar
        self.cax = self.figure.add_subplot()
        self.cax.set_axis_off()

        # set gid to axis for tick and labels on axes
        self.axes.xaxis.set_gid("bottom")
        self.axes.yaxis.set_gid("left")
        self.axesy2.yaxis.set_gid("right")
        self.axesx2.xaxis.set_gid("top")

        # Init spines
        self.spines()
    
    def spines(self):
        self.spine_bottom = Line2D(
            [1, 0], [0, 0], 
            marker='none',
            markevery=2,
            color=matplotlib.rcParams['axes.edgecolor'],
            linewidth=1.0,
            transform=self.axes.transAxes,
            clip_on=False,
            gid='spine bottom'
        )
        self.figure.add_artist(self.spine_bottom)
        self.spine_left = Line2D(
            [0, 0], [1, 0],
            marker='none',
            markevery=2,
            color=matplotlib.rcParams['axes.edgecolor'],
            linewidth=1.0,
            transform=self.axes.transAxes,
            clip_on=False,
            gid='spine left'
        )
        self.figure.add_artist(self.spine_left)
        self.spine_top = Line2D(
            [1, 0], [1, 1],
            marker='none',
            markevery=2,
            color=matplotlib.rcParams['axes.edgecolor'],
            linewidth=1.0,
            transform=self.axes.transAxes,
            clip_on=False,
            gid='spine top'
        )
        self.figure.add_artist(self.spine_top)
        self.spine_right = Line2D(
            [1, 1], [1, 0],
            marker='none',
            markevery=2,
            color=matplotlib.rcParams['axes.edgecolor'],
            linewidth=1.0,
            transform=self.axes.transAxes,
            clip_on=False,
            gid='spine right'
        )
        self.figure.add_artist(self.spine_right)
    
    def colorbar(self, *args, **kwargs):

        loc = self._config["cbar"]["loc"]
        size = self._config["cbar"]["size"]
        pad = self._config["cbar"]["pad"]
        visible = self._config["cbar"]["visible"]

        self.cax.cla()

        if visible:
            renderer = self.get_renderer()
            transform = self.figure.transFigure.inverted()
            
            xmargins, ymargins = [], []
            for ax in [self.axes, self.axesx2, self.axesy2]:
                ax: Axes
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                for text in ax.get_xticklabels() + ax.get_yticklabels():
                    bbox = text.get_window_extent(renderer).transformed(transform)
                    if bbox.width > 0 and bbox.height > 0: # skip empty labels
                        if xlim[0] <= text.get_position()[0] <= xlim[1] and \
                        ylim[0] <= text.get_position()[1] <= ylim[1]:
                            xmargins += [bbox.x0, bbox.x1]
                            ymargins += [bbox.y0, bbox.y1]
                for text in [ax.xaxis.get_label(), ax.yaxis.get_label()]:
                    bbox = text.get_window_extent(renderer).transformed(transform)
                    if bbox.width > 0 and bbox.height > 0: # skip empty labels
                        xmargins += [bbox.x0, bbox.x1]
                        ymargins += [bbox.y0, bbox.y1]  
                        
            # Compute extent of the ticks and labels from spine locations
            spine_margins = [
                self.spine_bottom.get_tightbbox(renderer).transformed(transform).y0,
                self.spine_top.get_tightbbox(renderer).transformed(transform).y1,
                self.spine_left.get_tightbbox(renderer).transformed(transform).x0,
                self.spine_right.get_tightbbox(renderer).transformed(transform).x1
            ]
            
            lb_margins = [
                abs(min(ymargins) - spine_margins[0]), # bottom
                abs(max(ymargins) - spine_margins[1]), # top
                abs(min(xmargins) - spine_margins[2]), # left
                abs(max(xmargins) - spine_margins[3]), # right
            ]

            self.cax.set_axis_on()
            fig_margins = self.figure.subplotpars

            if loc == 'bottom':
                self.axes.set_position([
                    fig_margins.left,
                    fig_margins.bottom + size + pad + lb_margins[0],
                    fig_margins.right - fig_margins.left,
                    fig_margins.top - fig_margins.bottom - size - pad - lb_margins[0]
                ])
                self.cax.set_position([
                    fig_margins.left,
                    fig_margins.bottom,
                    fig_margins.right - fig_margins.left,
                    size
                ])
            elif loc == 'right':
                self.axes.set_position([
                    fig_margins.left,
                    fig_margins.bottom,
                    fig_margins.right - fig_margins.left - size - pad - lb_margins[3],
                    fig_margins.top - fig_margins.bottom
                ])
                self.cax.set_position([
                    fig_margins.right - size,
                    fig_margins.bottom,
                    size,
                    fig_margins.top - fig_margins.bottom
                ])
            elif loc == 'left':
                self.axes.set_position([
                    fig_margins.left + size + pad + lb_margins[2],
                    fig_margins.bottom,
                    fig_margins.right - fig_margins.left - size - pad - lb_margins[2],
                    fig_margins.top - fig_margins.bottom
                ])
                self.cax.set_position([
                    fig_margins.left,
                    fig_margins.bottom,
                    size,
                    fig_margins.top - fig_margins.bottom
                ])
            
            mappable = self.figure.findobj(
                lambda a: isinstance(a, ScalarMappable) and \
                a.get_gid() and "graph" in a.get_gid()
            )
            if mappable != []:
                mappable = mappable[0]
            else:
                mappable = None
            
            Colorbar(self.cax, mappable, location=loc, *args, **kwargs)
        
        else:
            fig_margins = self.figure.subplotpars
            self.axes.set_position([
                fig_margins.left,
                fig_margins.bottom,
                fig_margins.right - fig_margins.left,
                fig_margins.top - fig_margins.bottom
            ])   
            self.cax.set_axis_off()
        
        self.draw_idle()

    def grid(self):
        " Only use for 2D Figure "

        # Default grid properties, adapted from rcParams
        props = {
            'color':'#b0b0b0',
            'linewidth':0.8,
            'linestyle':'solid',
            'alpha':1,
            'zorder':2
        }
        for obj in self.figure.findobj(
            lambda a: isinstance(a, Line2D) and a.get_gid() \
            and a.get_gid() == "_grid" 
        ):
            obj.remove()
            props = obj.properties()

        xaxis: Axis = self.figure.findobj(
            lambda a: isinstance(a, Axis) and a.get_gid() \
            and a.get_gid() == self._config['grid']['coord'].split('-')[0]
        )[0]
        yaxis: Axis = self.figure.findobj(
            lambda a: isinstance(a, Axis) and a.get_gid() \
            and a.get_gid() == self._config['grid']['coord'].split('-')[1]
        )[0]
        
        if self._config['grid']['which'] == 'major':
            xticks = xaxis.get_major_ticks()
            yticks = yaxis.get_major_ticks()
        elif self._config['grid']['which'] == 'minor':
            xticks = xaxis.get_minor_ticks()
            yticks = yaxis.get_minor_ticks()
        elif self._config['grid']['which'] == 'both':
            xticks = xaxis.get_major_ticks() + xaxis.get_minor_ticks()
            yticks = yaxis.get_major_ticks() + yaxis.get_minor_ticks()
        
        xlim = xaxis.axes.get_xlim()
        ylim = yaxis.axes.get_ylim()
        gridlines: list[Line2D] = [] # only contains visible gridlines
        if self._config['grid']['xaxis']:
            for tick in xticks:
                if xlim[0] <= tick.gridline.get_xdata()[0] <= xlim[1]:
                    gridlines.append(tick.gridline)
        if self._config['grid']['yaxis']:
            for tick in yticks:
                if ylim[0] <= tick.gridline.get_ydata()[0] <= ylim[1]:
                    gridlines.append(tick.gridline)

        for line in gridlines:
            line.set(visible = False)
            # Get the path in display (pixel) coordinates
            path = line.get_path().transformed(line.get_transform())        
            # Convert display coords to figure coordinates
            fig_coords = self.figure.transFigure.inverted().transform(path.vertices)
            # Clone the gridline and add to Figure
            figline = Line2D(
                xdata=fig_coords[:, 0],
                ydata=fig_coords[:, 1],
                transform=self.figure.transFigure,
                visible=self._config['grid']['visible'],
                color=props['color'],
                linewidth=props["linewidth"],
                linestyle=props["linestyle"],
                alpha=props["alpha"],
                zorder=props["zorder"],
                marker='none',
                gid = '_grid',
            )
            self.figure.add_artist(figline)      

    def serialize(self):
        
        if config['save_path'] != "":
            with open(os.path.join(config['save_path'], f'canvas_{self.id}.pickle'), 'wb') as file:
                pickle.dump(self.figure, file)

        return {"id": self.id,
                'config': self._config}
        
    def deserialize(self, data, hashmap={}):

        self.id = data['id']
        hashmap[data['id']] = self
        self._config = data['config']
        try:
            if config['save_path'] != "":
                with open(os.path.join(config['save_path'], f'canvas_{self.id}.pickle'),'rb') as file:
                    loaded_fig = pickle.load(file)

            copy_Figure(loaded_fig, self.figure)
            self.draw_idle()
            
        except Exception as e:
            logger.exception(e)
            
class ExplorerCanvas(FigureCanvasQTAgg):
    def __init__(self):
        
        self.figure = Figure()
        self.figure.set_dpi(100)
        self.figure.subplots_adjust(left=0.12,right=0.9,top=0.9,bottom=0.12)
        self.id = id(self)

        super().__init__(self.figure)
        
class Canvas3D (Canvas):
    def __init__(self):
        super().__init__()

    def initAxes(self):
        self.axes: Axes3D = self.figure.add_subplot(projection='3d', gid='legend axes')  

        self.axes.xaxis.set_gid("x3d")
        self.axes.yaxis.set_gid("y3d")
        self.axes.zaxis.set_gid("z3d")

class MultiFigureCanvas(Canvas):
    def __init__(self):
        super().__init__()

        self.figure.set_layout_engine(layout='constrained')
        self.figure.suptitle('')
        self.figure.supxlabel('')
        self.figure.supylabel('')

    def initAxes(self):
        pass

