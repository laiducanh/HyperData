from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.markers
from PySide6.QtCore import Signal
import matplotlib
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.text import Annotation, Text
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.backend_bases import PickEvent, cursors
from matplotlib.widgets import TextBox, Cursor
import pandas as pd
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
    def __init__(self):
        
        self.fig = Figure()
        self.fig.set_dpi(150)
        self.fig.subplots_adjust(left=0.12,right=0.9,top=0.9,bottom=0.12)

        self.initAxes()
        super().__init__(self.fig)
    
    def initAxes (self):
        self.axes = self.fig.add_subplot()
        self.axesy2 = self.axes.twinx()
        self.axesx2 = self.axes.twiny()
        self.axespie = self.fig.add_subplot()
        self.axesleg = self.fig.add_subplot()

        self.axespie.set_axis_off()
        self.axesleg.set_axis_off()

        self.axes.xaxis.set_gid("bottom")
        self.axes.yaxis.set_gid("left")
        self.axesy2.yaxis.set_gid("right")
        self.axesx2.xaxis.set_gid("top")
        
        for _ax in self.fig.axes:     
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
        figure = dict()
        for i in vars(self.fig).keys(): figure[i] = str(vars(self.fig)[i])
        axes = dict(ax = {}, axy2 = {}, axx2 = {})
        for i in vars(self.axes).keys(): axes['ax'][i] = str(vars(self.axes)[i])
        for i in vars(self.axesy2).keys(): axes['axy2'][i] = str(vars(self.axesy2)[i])
        for i in vars(self.axesx2).keys(): axes['axx2'][i] = str(vars(self.axesx2)[i])

        graph = dict()
        for obj in self.fig.findobj():
            if obj._gid != None and "graph" in obj._gid:
                graph[str(obj)] = dict()
                for i in vars(obj).keys():
                    graph[str(obj)][str(i)] = str(vars(obj)[i])
            
        
        return {"figure":figure,
                "label":dict(),
                "axis":axes,
                "grid":dict(),
                "plot":graph,}
    

    def deserialize(self, data, hashmap={}):
        pass

class ExplorerCanvas(FigureCanvasQTAgg):
    def __init__(self):
        
        self.fig = Figure()
        self.fig.set_dpi(150)
        self.fig.subplots_adjust(left=0.12,right=0.9,top=0.9,bottom=0.12)

        super().__init__(self.fig)
        
class Canvas3D (Canvas):
    def __init__(self):
        super().__init__()

    def initAxes(self):
        self.axes = self.fig.add_subplot(projection='3d')  
        self.axesleg = None

        self.axes.xaxis.set_gid("x3d")
        self.axes.yaxis.set_gid("y3d")
        self.axes.zaxis.set_gid("z3d")