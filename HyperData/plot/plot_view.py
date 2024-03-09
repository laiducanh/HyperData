### Import libraries from Python
import sys, requests, os, datetime, qfluentwidgets, pandas, matplotlib

### Import libraries from PyQt6
from PyQt6.QtCore import QThreadPool, Qt, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QDockWidget,
                             QStackedLayout, QPushButton, QTreeWidgetItem, QFileDialog)
from PyQt6.QtGui import QGuiApplication, QKeyEvent, QPaintEvent, QPixmap, QColor, QIcon, QShowEvent

### Import self classes
from plot.insert_plot.insert_plot import InsertPlot
from plot.curve.curve import Curve
from plot.axes.axes import Tick, Spine
from plot.plot_graphics_view import GraphicsView
from ui.base_widgets.list import TreeWidget
from ui.base_widgets.button import _ToolButton
from ui.base_widgets.text import _Search_Box
from plot.canvas import Canvas
from plot.grid.grid import Grid
from plot.label.graph_title import GraphTitle

DEBUG = False
  
class PlotView (QMainWindow):
    sig_back_to_grScene = pyqtSignal()
    def __init__(self, node, canvas:Canvas, parent=None):
        super().__init__(parent)
        
        ### 
        #self.data_window = DataView(data,self)

        self.node = node
        self.canvas = canvas
        self.num_plot = 0
        self.current_plot = 0
        self.curvelist = list()

        self.treeview_list = {"Graph":["Manage graph"],
                               "Tick":["Tick bottom","Tick left","Tick top","Tick right"],
                               "Spine":["Spine bottom","Spine left","Spine top","Spine right"],
                               "Figure":["Plot size","Grid"],
                               "Label":["Title","Axis lebel","Legend","Data annotation"],}

        ### Initialize UI components

        self.setup_visual()
        self.setup_sidebar()
        ###

    def setup_visual (self):
        self.plot_visual = GraphicsView(self.canvas)
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
        self.sidebar_layout.addLayout(static_layout)

        self.graphicscreen_btn = _ToolButton()
        self.graphicscreen_btn.pressed.connect(self.sig_back_to_grScene.emit)
        static_layout.addWidget(self.graphicscreen_btn)
        self.treeview_btn = _ToolButton()
        self.treeview_btn.pressed.connect(lambda: self.stackedlayout.setCurrentIndex(0))
        static_layout.addWidget(self.treeview_btn)
        self.search_box = _Search_Box()
        static_layout.addWidget(self.search_box)
        

        self.stackedlayout = QStackedLayout()
        self.sidebar_layout.addLayout(self.stackedlayout)

        self.treeview = TreeWidget()
        self.treeview.itemPressed.connect(self.treeview_func)
        self.treeview.setData(self.treeview_list)
        self.stackedlayout.addWidget(self.treeview)

        self.search_box.set_TreeView(self.treeview)

        self.dock = QDockWidget('Figure')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.dock.setWidget(self.sidebar)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

    

    def add_plot (self):
        self.treeview_list["Graph"] = ["Manage graph"]
        for gid in self.insertplot.gidlist:
            self.treeview_list["Graph"].insert(-1,str(gid))
        
        self.treeview.setData(self.treeview_list)

        pixmap = QPixmap(12,12)
        for item in self.treeview.findItems("Graph",Qt.MatchFlag.MatchExactly):
            for child in range(item.childCount()):
                name = item.child(child).text(0).lower()
                if "graph " in name:
                    for graph in self.canvas.fig.findobj():
                        if graph._gid != None and name in graph._gid:
                            color = graph.get_color()
                            break
                    pixmap.fill(QColor(color))
                    item.child(child).setIcon(0,QIcon(pixmap))        

    def treeview_func (self, s:QTreeWidgetItem):
        text = s.text(0).lower()
        if "graph " in text:
            curve = Curve(text, self.plot_visual.canvas)
            self.stackedlayout.addWidget(curve)
            self.stackedlayout.setCurrentWidget(curve)
        
        elif "manage graph" == text:
            if not hasattr(self, "insertplot"):
                self.insertplot = InsertPlot (self.canvas, self.node)
                self.insertplot.sig.connect(self.add_plot)
                self.stackedlayout.addWidget(self.insertplot)
                print('insert plot')
            self.stackedlayout.setCurrentWidget(self.insertplot)

        elif "add graph" in text:
            self.num_plot += 1
            self.current_plot = self.num_plot
            self.treeview_list["Graph"].insert(-1,f"Graph {self.current_plot}")
            self.treeview.setData(self.treeview_list)
            
        elif "tick " in text:
            if not hasattr(self, "tick"):
                self.tick = Tick(self.canvas)
                self.stackedlayout.addWidget(self.tick)
                print('tick')
            self.tick.choose_axis(text.split()[-1])
            self.stackedlayout.setCurrentWidget(self.tick)
        
        elif "spine " in text:
            if not hasattr(self, 'spine'):
                self.spine = Spine(self.canvas)
                self.stackedlayout.addWidget(self.spine)
                print('spine')
            self.spine.choose_axis(text.split()[-1])
            self.stackedlayout.setCurrentWidget(self.spine)
        
        elif text in ["plot size", "grid"]:
            if not hasattr(self, 'grid'):
                self.grid = Grid(self.canvas)
                self.stackedlayout.addWidget(self.grid)
            self.stackedlayout.setCurrentWidget(self.grid)
        
        elif text == 'title':
            if not hasattr(self, 'title'):
                self.title = GraphTitle(self.canvas)
                self.stackedlayout.addWidget(self.title)
            self.stackedlayout.setCurrentWidget(self.title)
        
    def keyPressEvent(self, key: QKeyEvent) -> None:

        if key.key() == Qt.Key.Key_Slash:
            self.search_box.setFocus()
            self.stackedlayout.setCurrentWidget(self.treeview)
        
        super().keyPressEvent(key)


        
  