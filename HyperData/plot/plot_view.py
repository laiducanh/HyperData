### Import libraries from Python
from mpl_toolkits import mplot3d
from matplotlib.artist import Artist

### Import libraries from PySide6
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QDockWidget,
                             QStackedLayout, QTreeWidgetItem, QApplication, QFileDialog)
from PySide6.QtGui import QKeyEvent, QPaintEvent, QPixmap, QColor, QIcon

### Import self classes
from plot.insert_plot.insert_plot import InsertPlot
from plot.curve.curve import Curve
from plot.tick.tick_2d import Tick2D
from plot.tick.tick_3d import Tick3D
from plot.plot_graphics_view import GraphicsView, GraphicsViewMultiFig
from plot.multifigure.layout import Layout
from ui.base_widgets.list import TreeWidget
from ui.base_widgets.button import TransparentToolButton
from ui.base_widgets.line_edit import SearchBox
from ui.base_widgets.window import FileDialog
from plot.canvas import Canvas
from plot.axes.axes_2d import Axes2D
from plot.axes.axes_3d import Axes3D, View3D
from plot.label.graph_title import GraphTitle
from plot.label.legend import LegendLabel
from plot.toolbar import PlotView_ToolBar
from config.settings import GLOBAL_DEBUG, logger, config
from node_editor.base.node_graphics_node import NodeGraphicsNode
from plot.utilis import get_color, find_mpl_object

DEBUG = False

class PlotView(QMainWindow):
    sig_back_to_grScene = Signal()
    def __init__(self, node:NodeGraphicsNode, canvas:Canvas, parent:QMainWindow=None):
        super().__init__()
        
        ### 
        #self.data_window = DataView(data,self)
        self.node = node
        self.canvas = canvas
        self.num_plot = 0
        self.current_plot = 0
        self.curvelist = list()
        self.plot3d = isinstance(self.canvas.axes, mplot3d.axes3d.Axes3D)
        self.main_layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        ### Initialize UI components
        self.setup_visual()
        self.setup_sidebar()
        self.setup_toolbar()

        ###
        if GLOBAL_DEBUG or DEBUG: self.debug()

    def debug(self):
        self.statusBar()
            
    def setup_visual (self):
        self.plot_visual = GraphicsView(self.canvas,parent=self.parent())
        self.plot_visual.key_pressed.connect(self.keyPressEvent)
        self.plot_visual.save_figure.connect(self.save_figure)
        self.plot_visual.backtoScene.connect(self.sig_back_to_grScene.emit)
        self.plot_visual.mouse_released.connect(self.treeview_func)
        self.plot_visual.selected_obj.connect(self.update_toolbar)
        self.plot_visual.draw_obj.connect(self.update_objectlist)
        self.main_layout.addWidget(self.plot_visual)
    
    def setup_toolbar(self):
        self.toolbar = PlotView_ToolBar(self.canvas, self)
        self.toolbar.sig_back_to_grScene.connect(self.sig_back_to_grScene.emit)
        self.toolbar.sig_ruler.connect(self.plot_visual._scene.toggle_ruler)
        self.addToolBar(self.toolbar)
    
    def setup_sidebar(self):

        if self.plot3d:
            self.treeview_data = {
                "Manage graph":["Add graph"],
                "Axis":["X Axis","Y Axis","Z Axis"],
                "Pane":["XY Pane","YZ Pane","XZ Pane"],
                "Figure 3D": [],
                "Label":["Title","Legend"],
                "Drawings": []
            }

        else:
            self.treeview_data = {
                "Manage graph":["Add graph"],
                "Axis":["Bottom Axis","Left Axis","Top Axis","Right Axis"],
                "Figure 2D":[],
                "Label":["Title", "Legend"],
                "Drawings": []
            }

        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        # self.sidebar_layout.setContentsMargins(0,0,0,0)
        self.sidebar.setLayout(self.sidebar_layout)

        static_layout = QHBoxLayout()
        # static_layout.setContentsMargins(10,0,10,15)
        self.sidebar_layout.addLayout(static_layout)
 
        self.search_box = SearchBox(parent=self.parent())
        self.search_box.setPlaceholderText("Type / to search")
        static_layout.addWidget(self.search_box)
        
        # self.stackedlayout = QStackedLayout()
        # self.sidebar_layout.addLayout(self.stackedlayout)

        self.treeview = TreeWidget()
        self.treeview.itemPressed.connect(lambda item: self.treeview_func(item.text(0)))
        self.treeview.setData(self.treeview_data)
        self.sidebar_layout.addWidget(self.treeview)
        self.search_box.set_TreeView(self.treeview)

        self.dock = QDockWidget('Figure')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dock.setWidget(self.sidebar)
        self.dock.setTitleBarWidget(QWidget())

        self.insertplot = InsertPlot(self.canvas, self.node, self.plot3d, self)
        self.insertplot.sig.connect(self.update_plotlist)

    def treeview_func (self, text:str):
        text = text.lower()
        if text.startswith("graph"):
            plot_gid = text.split("/")[0].split(".")[0]
            for pt in self.insertplot.plot_list:
                if pt.plot_gid == plot_gid:
                    _plot = pt
                    break
            curve = Curve(text, self.plot_visual.canvas, _plot, self)
            curve.sig.connect(self.update_plotlist)
            curve.exec()
        
        elif "add graph" == text:
            # self.insertplot = InsertPlot(self.canvas, self.node, self.plot3d, self.parent())
            # self.insertplot.sig.connect(self.update_plotlist)
            self.insertplot.show()
            
        elif text == "bottom axis":
            self.botax = Tick2D('bottom', self.canvas, self)
            self.botax.exec()
        
        elif text == "left axis":
            self.lefax = Tick2D('left', self.canvas, self)
            self.lefax.exec()

        elif text == "top axis":
            self.topax = Tick2D('top', self.canvas, self)
            self.topax.exec()

        elif text == "right axis":
            self.rigax = Tick2D('right', self.canvas, self)
            self.rigax.exec()
        
        elif text == 'x axis':
            self.xax = Tick3D('x3d', self.canvas, self)
            self.xax.exec()
        
        elif text == 'y axis':
            self.yax = Tick3D('y3d', self.canvas, self)
            self.yax.exec()
        
        elif text == 'z axis':
            self.zax = Tick3D('z3d', self.canvas, self)
            self.zax.exec()
        
        elif text == 'xy pane':
            self.zpane = Axes3D('XY Pane', self.canvas, self)
            self.zpane.exec()
        
        elif text == 'xz pane':
            self.ypane = Axes3D('XZ Pane', self.canvas, self)
            self.ypane.exec()
        
        elif text == 'yz pane':
            self.xpane = Axes3D('YZ Pane', self.canvas, self)
            self.xpane.exec()
        
        elif text == 'figure 2d':
            self.axes  = Axes2D(self.canvas, self)
            self.axes.exec()
        
        elif text == 'figure 3d':
            self.axes = View3D(self.canvas, self)
            self.axes.exec()
        
        elif text == 'title':
            self.title = GraphTitle(self.canvas, self)
            self.title.exec()
        
        elif text == 'legend':
            self.legendlabel = LegendLabel(self.canvas, self)
            self.legendlabel.exec()
    
    def update_plotlist(self):
        try:
            # reset treeview items
            self.treeview_data["Manage graph"] = ["Add graph"]
            # append list of graphs
            for obj in self.canvas.figure.artists:
                if not obj.get_gid().startswith("_") and 'graph' in obj.get_gid():
                    if obj.get_gid().split('/')[0].title() not in self.treeview_data["Manage graph"]:
                        self.treeview_data["Manage graph"].append(obj.get_gid().split('/')[0].title())
            self.treeview.setData(self.treeview_data)

            # update color icon for each graph
            pixmap = QPixmap(12,12)
            for item in self.treeview.findItems("Manage graph",Qt.MatchFlag.MatchExactly):
                for child in range(item.childCount()):
                    name = item.child(child).text(0).lower()
                    if name.startswith("graph"):
                        color = 'white' # whenever color changes to white, there is an error!
                        if find_mpl_object(self.canvas.figure,gid=name,rule="exact"):
                            color = get_color(find_mpl_object(self.canvas.figure,gid=name,rule="exact")[0])
                        else:
                            color = get_color(find_mpl_object(self.canvas.figure,gid=name,rule="index")[0])
                        pixmap.fill(QColor(color))
                        item.child(child).setIcon(0,QIcon(pixmap))  

        except Exception as e: 
            logger.exception(e)

    def update_objectlist(self):
        self.treeview_data["Drawings"] = []
        for obj in find_mpl_object(self.canvas.figure, gid='drawing'):
            self.treeview_data["Drawings"].append(obj.get_gid().title())
        self.treeview.setData(self.treeview_data)
        self.update_plotlist()

    def update_toolbar(self, gid:str):
        self.toolbar.update(gid)

    def save_figure(self):
        dialog = FileDialog(
            caption="Save As",
            directory='untitled.png',
            filter="""Portable Network Graphics (*.png);;Tagged Image File Format (*.tiff);;JPEG (*.jpg *.jpeg);;
                      PDF (*.pdf);;Scalable Vector Graphics (*.svg);;PostScript formats (*.ps *.eps);;All Files (*)""",
            acceptMode=QFileDialog.AcceptMode.AcceptSave,
            viewMode=QFileDialog.ViewMode.Detail
        )
        if dialog.exec():
            self.canvas.figure.savefig(
                fname=dialog.selectedFiles()[0], 
                dpi=config["plot_dpi"]
            )

    def keyPressEvent(self, key: QKeyEvent) -> None:

        if key.key() == Qt.Key.Key_Slash:
            self.search_box.setFocus()
        
        elif key.key() == Qt.Key.Key_N and key.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.sig_back_to_grScene.emit()
        
        elif key.key() == Qt.Key.Key_F and key.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.save_figure()
        else:
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

    def showEvent(self, event):
        self.update_objectlist()
        return super().showEvent(event)
    
class PlotViewMultiFig (PlotView):
    def __init__(self, node:NodeGraphicsNode, canvas:Canvas, parent=None):       
        super().__init__(node, canvas, parent)
    
    def setup_visual (self):
        self.plot_visual = GraphicsViewMultiFig(self.canvas,parent=self.parent())
        self.plot_visual.key_pressed.connect(self.keyPressEvent)
        self.plot_visual.save_figure.connect(self.save_figure)
        # self.plot_visual.backtoHome.connect(lambda: self.stackedlayout.setCurrentIndex(0))
        self.plot_visual.backtoScene.connect(self.sig_back_to_grScene.emit)
        self.main_layout.addWidget(self.plot_visual)
    
    def setup_toolbar(self):
        pass

    def setup_sidebar(self):

        self.treeview_data = {
            "Layout":["Grid","Subfigure"],
            "Label":["Title","Axis label"],
        }

        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(0,0,0,0)
        self.sidebar.setLayout(self.sidebar_layout)

        static_layout = QHBoxLayout()
        static_layout.setContentsMargins(10,0,10,15)
        self.sidebar_layout.addLayout(static_layout)

        self.graphicscreen_btn = TransparentToolButton()
        self.graphicscreen_btn.setIcon("stack.png")
        self.graphicscreen_btn.pressed.connect(self.sig_back_to_grScene.emit)
        self.graphicscreen_btn.setToolTip("Node View")
        static_layout.addWidget(self.graphicscreen_btn)
        self.treeview_btn = TransparentToolButton()
        self.treeview_btn.setIcon("home.svg")
        self.treeview_btn.pressed.connect(lambda: self.stackedlayout.setCurrentIndex(0))
        self.treeview_btn.setToolTip("Home")
        static_layout.addWidget(self.treeview_btn)
        self.search_box = SearchBox(parent=self.parent())
        self.search_box.setPlaceholderText("Type / to search")
        static_layout.addWidget(self.search_box)
        

        self.stackedlayout = QStackedLayout()
        self.sidebar_layout.addLayout(self.stackedlayout)

        self.treeview = TreeWidget()
        self.treeview.itemPressed.connect(self.treeview_func)
        self.treeview.setData(self.treeview_data)
        self.stackedlayout.addWidget(self.treeview)
        self.search_box.set_TreeView(self.treeview)

        self.dock = QDockWidget('Figure')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dock.setWidget(self.sidebar)
        self.dock.setTitleBarWidget(QWidget())

        self.grid_layout = Layout(self.node, self.canvas, self.parent())
        self.stackedlayout.addWidget(self.grid_layout)

        # self.title = GraphTitle(self.canvas, self.parent())
        # self.stackedlayout.addWidget(self.title)
    
    def treeview_func(self, item:QTreeWidgetItem):
        text = item.text(0).lower()

        if text in ["grid","subfigure"]:
            self.stackedlayout.setCurrentWidget(self.grid_layout)
        
        elif text == 'title':
            self.title = GraphTitle(self.canvas, self.parent())
            self.title.show()
    
    def showEvent(self, event):
        return QMainWindow().showEvent(event)