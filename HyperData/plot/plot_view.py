### Import libraries from Python
import matplotlib

### Import libraries from PyQt6
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QDockWidget,
                             QStackedLayout, QTreeWidgetItem, QApplication)
from PyQt6.QtGui import QKeyEvent, QPaintEvent, QPixmap, QColor, QIcon

### Import self classes
from plot.insert_plot.insert_plot import InsertPlot
from plot.curve.curve import Curve
from plot.axes.axes import Tick, Spine
from plot.plot_graphics_view import GraphicsView
from ui.base_widgets.list import TreeWidget
from ui.base_widgets.button import _TransparentToolButton
from ui.base_widgets.line_edit import _SearchBox
from ui.base_widgets.window import ProgressDialog
from plot.canvas import Canvas
from plot.grid.grid import Grid
from plot.label.graph_title import GraphTitle
from config.settings import config
from node_editor.node_node import Node

DEBUG = False

class PlotView (QMainWindow):
    sig_back_to_grScene = pyqtSignal()
    def __init__(self, node:Node, canvas:Canvas, parent=None):
        super().__init__(parent)
        
        ### 
        #self.data_window = DataView(data,self)

        self.node = node
        self.canvas = canvas
        self.num_plot = 0
        self.current_plot = 0
        self.curvelist = list()
        self.parent = parent

        self.treeview_list = {"Graph":["Manage graph"],
                               "Tick":["Tick bottom","Tick left","Tick top","Tick right"],
                               "Spine":["Spine bottom","Spine left","Spine top","Spine right"],
                               "Figure":["Plot size","Grid"],
                               "Label":["Title","Axis lebel","Legend","Data annotation"],}
        
        self.diag = ProgressDialog("Initializing figure", None, parent)
        self.diag.progressbar._setValue(0)
        self.diag.show()
        QApplication.processEvents()

        ### Initialize UI components
        self.setup_visual()
        self.setup_sidebar()
        
        ###
            
    def setup_visual (self):
        self.plot_visual = GraphicsView(self.canvas,parent=self.parent)
        self.plot_visual.sig_keyPressEvent.connect(lambda s: self.keyPressEvent(s))
        for i in self.canvas.fig.findobj():
            if i._gid != None and "graph" in i._gid:
                self.treeview_list['Graph'].insert(-1,i._gid.title())
                i.set_color('red')
        self.setCentralWidget(self.plot_visual)
    
    def setup_sidebar(self):

        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(0,0,0,0)
        self.sidebar.setLayout(self.sidebar_layout)

        static_layout = QHBoxLayout()
        static_layout.setContentsMargins(10,0,10,15)
        self.sidebar_layout.addLayout(static_layout)

        self.graphicscreen_btn = _TransparentToolButton()
        self.graphicscreen_btn.setIcon("stack.png")
        self.graphicscreen_btn.pressed.connect(self.sig_back_to_grScene.emit)
        static_layout.addWidget(self.graphicscreen_btn)
        self.treeview_btn = _TransparentToolButton()
        self.treeview_btn.setIcon("home.svg")
        self.treeview_btn.pressed.connect(lambda: self.stackedlayout.setCurrentIndex(0))
        static_layout.addWidget(self.treeview_btn)
        self.search_box = _SearchBox(parent=self.parent)
        self.search_box.setPlaceholderText("Type / to search")
        static_layout.addWidget(self.search_box)
        

        self.stackedlayout = QStackedLayout()
        self.sidebar_layout.addLayout(self.stackedlayout)

        self.treeview = TreeWidget()
        self.treeview.itemPressed.connect(self.treeview_func)
        self.treeview.setData(self.treeview_list)
        self.stackedlayout.addWidget(self.treeview)

        self.search_box.set_TreeView(self.treeview)

        self.dock = QDockWidget('Figure')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dock.setWidget(self.sidebar)
        self.dock.setTitleBarWidget(QWidget())
        
        self.diag.progressbar._setValue(10)
        self.diag.setLabelText("Loading plot types")
        QApplication.processEvents()

        self.insertplot = InsertPlot (self.canvas, self.node, self.parent)
        self.insertplot.sig.connect(self.add_plot)
        self.stackedlayout.addWidget(self.insertplot)
        
        self.diag.progressbar._setValue(20)
        self.diag.setLabelText("Loading ticks")
        QApplication.processEvents()
        self.tick = Tick(self.canvas)
        self.stackedlayout.addWidget(self.tick)

        self.diag.progressbar._setValue(60)
        self.diag.setLabelText("Loading spines")
        QApplication.processEvents()
        self.spine = Spine(self.canvas)
        self.stackedlayout.addWidget(self.spine)
        self.diag.progressbar._setValue(70)
        self.diag.setLabelText("Loading grid")
        QApplication.processEvents()
        self.grid = Grid(self.canvas,self.parent)
        self.stackedlayout.addWidget(self.grid)
        self.diag.progressbar._setValue(80)
        self.diag.setLabelText("Loading labels")
        QApplication.processEvents()
        self.title = GraphTitle(self.canvas)
        self.stackedlayout.addWidget(self.title)
        self.diag.progressbar._setValue(100)
        self.diag.close()

    def add_plot (self):
        self.treeview_list["Graph"] = ["Manage graph"]

        for gid in self.insertplot.gidlist:
            self.treeview_list["Graph"].insert(-1,str(gid).title())
        
        self.treeview.setData(self.treeview_list)
        self.update_plot()
        

    def update_plot (self):
        pixmap = QPixmap(12,12)
        for item in self.treeview.findItems("Graph",Qt.MatchFlag.MatchExactly):
            for child in range(item.childCount()):
                name = item.child(child).text(0).lower()
                if "graph " in name:
                    color = 'white' # whenever color changes to white, there is an error!
                    for graph in self.canvas.fig.findobj():
                        if graph._gid != None and name in graph._gid:
                            if isinstance(graph, matplotlib.lines.Line2D):
                                color = graph.get_color()
                            elif isinstance(graph, matplotlib.collections.Collection): 
                                color = matplotlib.colors.to_hex(graph.get_facecolor()[0])
                            elif isinstance(graph, matplotlib.patches.Rectangle):
                                color = matplotlib.colors.to_hex(graph.get_facecolor())
                            break
                    pixmap.fill(QColor(color))
                    item.child(child).setIcon(0,QIcon(pixmap))    

    def treeview_func (self, s:QTreeWidgetItem):
        text = s.text(0).lower()
        if "graph " in text:
            _plot_index = int(text.split(".")[0].split()[-1])-1
            _plot = self.insertplot.plotlist[_plot_index]
            curve = Curve(text, self.plot_visual.canvas, _plot, self.parent)
            curve.sig.connect(self.update_plot)
            self.stackedlayout.addWidget(curve)
            self.stackedlayout.setCurrentWidget(curve)
        
        elif "manage graph" == text:
            self.stackedlayout.setCurrentWidget(self.insertplot)

        elif "add graph" in text:
            self.num_plot += 1
            self.current_plot = self.num_plot
            self.treeview_list["Graph"].insert(-1,f"Graph {self.current_plot}")
            self.treeview.setData(self.treeview_list)
            
        elif "tick " in text:
            self.tick.choose_axis_func(text.split()[-1].title())
            self.stackedlayout.setCurrentWidget(self.tick)
        
        elif "spine " in text:
            self.spine.choose_axis_func(text.split()[-1].title())
            self.stackedlayout.setCurrentWidget(self.spine)
        
        elif text in ["plot size", "grid"]:
            self.stackedlayout.setCurrentWidget(self.grid)
        
        elif text == 'title':
            self.stackedlayout.setCurrentWidget(self.title)
        
    def keyPressEvent(self, key: QKeyEvent) -> None:

        if key.key() == Qt.Key.Key_Slash:
            self.search_box.setFocus()
            self.stackedlayout.setCurrentWidget(self.treeview)
        
        super().keyPressEvent(key)

    def paintEvent(self, a0: QPaintEvent) -> None:
        dock_area = config["dock area"]
        if dock_area == "Left":
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        elif dock_area == "Right":
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        elif dock_area == "Top":
            self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.dock)
        elif dock_area == "Bottom":
            self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock)
            
        return super().paintEvent(a0)

