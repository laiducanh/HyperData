from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt6.QtCore import pyqtSignal
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
def findobj (x):
    return True if x.get_gid() != None else False

class Canvas (FigureCanvasQTAgg):
    sig_text = pyqtSignal(object)
    sig_removeText = pyqtSignal()
    sig_pickedArtist = pyqtSignal(object)
    sig_openMenu = pyqtSignal(object)
    sig_hover = pyqtSignal() # to use in future
    def __init__(self):
        
        self.fig = Figure()
        self.fig.set_dpi(150)
        self.fig.subplots_adjust(left=0.12,right=0.9,top=0.9,bottom=0.12)
        self.annot_box = dict(boxstyle="round",pad=0.3,facecolor='orange',edgecolor='none')

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
    
class Canvas3D (Canvas):
    def __init__(self):
        super().__init__()

    def initAxes(self):
        self.axes = self.fig.add_subplot(projection='3d')  
        self.axesleg = None