from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtCore import Signal
import matplotlib, pickle, os
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D
from plot.copy_objects import copy_Figure
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
                    "coord": "bottom-left",
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

        # Axes to hold legend, this axes will be on top
        self.axesleg = self.figure.add_subplot(gid='legend axes')
        self.axesleg.set_xticks([])
        self.axesleg.set_yticks([])
        self.axesleg.spines["bottom"].set_gid("spine bottom")
        self.axesleg.plot(1, 0, marker="none", 
            color=matplotlib.colors.rgb2hex(self.axesleg.spines["bottom"].get_edgecolor()),
            transform=self.axesleg.transAxes,
            clip_on=False,
            gid="spine bottom"
        )
        self.axesleg.spines["top"].set_gid("spine top")
        self.axesleg.plot(1, 1, marker="none", 
            color=matplotlib.colors.rgb2hex(self.axesleg.spines["top"].get_edgecolor()),
            transform=self.axesleg.transAxes,
            clip_on=False,
            gid="spine top"
        )
        self.axesleg.spines["left"].set_gid("spine left")
        self.axesleg.plot(0, 1, marker="none", 
            color=matplotlib.colors.rgb2hex(self.axesleg.spines["left"].get_edgecolor()),
            transform=self.axesleg.transAxes,
            clip_on=False,
            gid="spine left"
        )
        self.axesleg.spines["right"].set_gid("spine right")
        self.axesleg.plot(1, 1, marker="none", 
            color=matplotlib.colors.rgb2hex(self.axesleg.spines["right"].get_edgecolor()),
            transform=self.axesleg.transAxes,
            clip_on=False,
            gid="spine right"
        )

        # set gid to axis for tick and labels on axes
        self.axes.xaxis.set_gid("bottom")
        self.axes.yaxis.set_gid("left")
        self.axesy2.yaxis.set_gid("right")
        self.axesx2.xaxis.set_gid("top")
        
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

