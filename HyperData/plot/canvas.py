from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtCore import Signal
import matplotlib, pickle, os
from matplotlib.figure import Figure
from plot.multifigure.utilis import copy_objects

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
        
        self.fig = Figure()
        self.id = id(self)
        self._config = {
            'dpi': 150,
            'margin': (0.12, 0.12, 0.9, 0.9),
            'plot_type': '2d line',
            'data_input': [str(), str(), str(), str()],
            'plot_props': dict(),
        }
        self.fig.set_dpi(self._config['dpi'])
        self.fig.subplots_adjust(*self._config['margin'])

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
        # figure = dict()
        # for i in vars(self.fig).keys(): figure[i] = str(vars(self.fig)[i])
        # axes = dict(ax = {}, axy2 = {}, axx2 = {})
        # axes['ax'] = {
        #     "_visible": self.axes.get_visible()
        # }
        # # for i in vars(self.axes).keys(): 
        # #     axes['ax'][i] = (vars(self.axes)[i])

        # for i in vars(self.axesy2).keys(): axes['axy2'][i] = str(vars(self.axesy2)[i])
        # for i in vars(self.axesx2).keys(): axes['axx2'][i] = str(vars(self.axesx2)[i])

        # graph = dict()
        # for obj in self.fig.findobj():
        #     if obj._gid != None and "graph" in obj._gid:
        #         graph[str(obj)] = dict()
        #         for i in vars(obj).keys():
        #             graph[str(obj)][str(i)] = str(vars(obj)[i])            

        with open(f'canvas_{self.id}.pickle', 'wb') as file: 
            pickle.dump(self.fig, file)
                
        return {"id": self.id,
                "pickle": f'canvas_{self.id}.pickle',
                'config': self._config}
    

    def deserialize(self, data, hashmap={}):

        self.id = data['id']
        hashmap[data['id']] = self
        self._config = data['config']

        with open(f'canvas_{self.id}.pickle','rb') as file:
            loaded_fig = pickle.load(file)
        
        self.fig.clear()
        self.initAxes()

        for source_ax, destination_ax in zip(loaded_fig.axes, self.fig.axes):
            copy_objects(source_ax, destination_ax)
            
        self.fig.canvas.draw_idle()

class ExplorerCanvas(FigureCanvasQTAgg):
    def __init__(self):
        
        self.fig = Figure()
        self.fig.set_dpi(150)
        self.fig.subplots_adjust(left=0.12,right=0.9,top=0.9,bottom=0.12)
        self.id = id(self)

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

class MultiFigureCanvas(Canvas):
    def __init__(self):
        super().__init__()

    def initAxes(self):
        self.axes = self.fig.add_subplot()
        self.axesy2 = self.axes.twinx()
        self.axesx2 = self.axes.twiny()

        self.axes.xaxis.set_gid("bottom")
        self.axes.yaxis.set_gid("left")
        self.axesy2.yaxis.set_gid("right")
        self.axesx2.xaxis.set_gid("top")

        for ax in self.fig.axes:
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

