from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtCore import Signal
import matplotlib, pickle, os
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D
from plot.copy_objects import copy_Axes
from config.settings import config, logger

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
                    "axis": matplotlib.rcParams['axes.grid.axis'],
                    "alpha": matplotlib.rcParams['grid.alpha'],
                    "linewidth": matplotlib.rcParams['grid.linewidth'],
                    "linestyle": matplotlib.rcParams['grid.linestyle'],
                    "color": matplotlib.rcParams['grid.color']
                }
            }
        self.figure = Figure()
        self.figure.set_dpi(100)
        # self.fig.subplots_adjust(*self._config['margin'])
        self.initAxes()
        
        super().__init__(self.figure)
    
    def initAxes (self):
        self.axes = self.figure.add_subplot()
        self.axesy2 = self.axes.twinx()
        self.axesx2 = self.axes.twiny()
        self.axespie = self.figure.add_subplot()
        self.axespolar = self.figure.add_subplot(projection='polar')
        self.axesleg = self.figure.add_subplot(gid='legend axes')

        self.axespie.set_axis_off()
        self.axespolar.set_axis_off()
        self.axesleg.set_axis_off()

        self.axes.xaxis.set_gid("bottom")
        self.axes.yaxis.set_gid("left")
        self.axesy2.yaxis.set_gid("right")
        self.axesx2.xaxis.set_gid("top")
        
        for _ax in [self.axes, self.axesy2, self.axesx2]:     
            _ax.spines["bottom"].set_gid("spine bottom")
            _ax.plot(1, 0, marker=",", 
                     color=matplotlib.colors.rgb2hex(_ax.spines["bottom"].get_edgecolor()),
                     transform=_ax.transAxes,
                     clip_on=False,
                     gid="spine bottom"
            )
            _ax.spines["top"].set_gid("spine top")
            _ax.plot(1, 1, marker=",", 
                     color=matplotlib.colors.rgb2hex(_ax.spines["top"].get_edgecolor()),
                     transform=_ax.transAxes,
                     clip_on=False,
                     gid="spine top"
            )
            _ax.spines["left"].set_gid("spine left")
            _ax.plot(0, 1, marker=",", 
                     color=matplotlib.colors.rgb2hex(_ax.spines["left"].get_edgecolor()),
                     transform=_ax.transAxes,
                     clip_on=False,
                     gid="spine left"
            )
            _ax.spines["right"].set_gid("spine right")
            _ax.plot(1, 1, marker=",", 
                     color=matplotlib.colors.rgb2hex(_ax.spines["right"].get_edgecolor()),
                     transform=_ax.transAxes,
                     clip_on=False,
                     gid="spine right"
            )
            
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

            for source_ax, destination_ax in zip(loaded_fig.axes, self.figure.axes):
                copy_Axes(source_ax, destination_ax)
            
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

    def initAxes(self):
        self.axes = self.figure.add_subplot()
        self.axesy2 = self.axes.twinx()
        self.axesx2 = self.axes.twiny()

        self.axes.xaxis.set_gid("bottom")
        self.axes.yaxis.set_gid("left")
        self.axesy2.yaxis.set_gid("right")
        self.axesx2.xaxis.set_gid("top")

        for ax in self.figure.axes:
            # Turn off spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            # Turn off ticks
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')

            # Turn off tick labels
            ax.set_xticklabels([])
            ax.set_yticklabels([])

