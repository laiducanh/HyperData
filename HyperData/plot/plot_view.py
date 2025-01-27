### Import libraries from Python
import matplotlib

### Import libraries from PySide6
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QDockWidget,
                             QStackedLayout, QTreeWidgetItem, QApplication)
from PySide6.QtGui import QKeyEvent, QPaintEvent, QPixmap, QColor, QIcon

### Import self classes
from plot.insert_plot.insert_plot import InsertPlot
from plot.curve.curve import Curve
from plot.axes.axes import Tick, Spine
from plot.plot_graphics_view import GraphicsView
from ui.base_widgets.list import TreeWidget
from ui.base_widgets.button import _TransparentToolButton
from ui.base_widgets.line_edit import _SearchBox
from ui.base_widgets.window import ProgressDialog, FileDialog
from plot.canvas import Canvas
from plot.grid.grid import Grid
from plot.label.graph_title import GraphTitle
from plot.label.axes_label import AxesLabel2D
from plot.label.legend import LegendLabel
from config.settings import GLOBAL_DEBUG, logger, config
from node_editor.node_node import Node
from plot.utilis import get_color, find_mpl_object

DEBUG = False

class PlotView (QMainWindow):
    sig_back_to_grScene = Signal()
    def __init__(self, node:Node, canvas:Canvas, plot3d=False, parent=None):
        super().__init__(parent)
        
        ### 
        #self.data_window = DataView(data,self)

        self.node = node
        self.canvas = canvas
        self.num_plot = 0
        self.current_plot = 0
        self.plot3d = plot3d
        self.curvelist = list()
        self.main_layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.treeview_data = {"Graph":["Manage graph"],
                               "Tick":["Tick bottom","Tick left","Tick top","Tick right"],
                               "Spine":["Spine bottom","Spine left","Spine top","Spine right"],
                               "Figure":["Plot size","Grid"],
                               "Label":["Title","Axis label","Legend","Data annotation"],}
        
        self.diag = ProgressDialog("Initializing figure", None, parent)
        self.diag.progressbar._setValue(0)
        self.diag.show()
        QApplication.processEvents()

        ### Initialize UI components
        self.setup_visual()
        self.setup_sidebar()
        
        ###
        if GLOBAL_DEBUG or DEBUG: self.debug()

    def debug(self):
        self.statusBar()
            
    def setup_visual (self):
        self.plot_visual = GraphicsView(self.canvas,parent=self.parent())
        self.plot_visual.mpl_pressed.connect(self.update_sidebar)
        self.plot_visual.key_pressed.connect(self.keyPressEvent)
        self.plot_visual.mouse_released.connect(self.treeview_func)
        self.plot_visual.save_figure.connect(self.save_figure)
        self.plot_visual.backtoHome.connect(lambda: self.stackedlayout.setCurrentIndex(0))
        self.plot_visual.backtoScene.connect(self.sig_back_to_grScene.emit)
        self.main_layout.addWidget(self.plot_visual)
    
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
        self.graphicscreen_btn.setToolTip("Node View")
        static_layout.addWidget(self.graphicscreen_btn)
        self.treeview_btn = _TransparentToolButton()
        self.treeview_btn.setIcon("home.svg")
        self.treeview_btn.pressed.connect(lambda: self.stackedlayout.setCurrentIndex(0))
        self.treeview_btn.setToolTip("Home")
        static_layout.addWidget(self.treeview_btn)
        self.search_box = _SearchBox(parent=self.parent())
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
        self.diag.progressbar._setValue(10)

        self.diag.setLabelText("Loading plot types")
        QApplication.processEvents()
        self.insertplot = InsertPlot (self.canvas, self.node, self.plot3d, self.parent())
        self.insertplot.sig.connect(self.update_plotlist)
        self.stackedlayout.addWidget(self.insertplot)
        self.diag.progressbar._setValue(20)

        self.diag.setLabelText("Loading ticks")
        QApplication.processEvents()
        self.tick = Tick(self.canvas, self.parent())
        self.stackedlayout.addWidget(self.tick)
        self.diag.progressbar._setValue(60)

        self.diag.setLabelText("Loading spines")
        QApplication.processEvents()
        self.spine = Spine(self.canvas, self.parent())
        self.stackedlayout.addWidget(self.spine)
        self.diag.progressbar._setValue(70)

        self.diag.setLabelText("Loading grid")
        QApplication.processEvents()
        self.grid = Grid(self.canvas,self.parent())
        self.stackedlayout.addWidget(self.grid)
        self.diag.progressbar._setValue(80)
        
        self.diag.setLabelText("Loading labels")
        QApplication.processEvents()
        self.title = GraphTitle(self.canvas, self.parent())
        self.stackedlayout.addWidget(self.title)
        self.axeslabel = AxesLabel2D(self.canvas, self.parent())
        self.stackedlayout.addWidget(self.axeslabel)
        self.legendlabel = LegendLabel(self.canvas, self.parent())
        self.stackedlayout.addWidget(self.legendlabel)
        self.diag.progressbar._setValue(100)
        self.diag.close()

    def treeview_func (self, item:QTreeWidgetItem):
        text = item.text(0).lower()
        self.update_sidebar(text)
    
    def update_sidebar(self, text:str):
        text = text.lower()
        if "graph " in text:
            
            _plot_index = int(text.split("/")[0].split(".")[0].split()[-1])
            for pt in self.insertplot.plotlist:
                if pt.plot_index == _plot_index:
                    _plot = pt
                    break
            curve = Curve(text, self.plot_visual.canvas, _plot, self.parent())
            curve.sig.connect(self.update_plotlist)
            self.stackedlayout.addWidget(curve)
            self.stackedlayout.setCurrentWidget(curve)
        
        elif "manage graph" == text:
            self.stackedlayout.setCurrentWidget(self.insertplot)

        elif "add graph" in text:
            self.num_plot += 1
            self.current_plot = self.num_plot
            self.treeview_data["Graph"].insert(-1,f"Graph {self.current_plot}")
            self.treeview.setData(self.treeview_data)
            
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
        
        elif text == 'axis label':
            self.stackedlayout.setCurrentWidget(self.axeslabel)
        
        elif text == 'legend':
            self.stackedlayout.setCurrentWidget(self.legendlabel)
    
    def update_plotlist(self):
        try:
            self.treeview_data["Graph"] = ["Manage graph"]
            plot_list = [s for s in find_mpl_object(self.canvas.fig,gid="graph ")]
            for gid in set([s.get_gid() for s in plot_list]):
                _gid = gid.split("/")[0].title()
                self.treeview_data["Graph"].insert(-1,_gid)
            self.treeview.setData(self.treeview_data)

            # update color icon for each graph
            pixmap = QPixmap(12,12)
            for item in self.treeview.findItems("Graph",Qt.MatchFlag.MatchExactly):
                for child in range(item.childCount()):
                    name = item.child(child).text(0).lower()
                    if "graph " in name:
                        color = 'white' # whenever color changes to white, there is an error!
                        color = get_color(find_mpl_object(self.canvas.fig,gid=name,rule="exact")[0])
                        pixmap.fill(QColor(color))
                        item.child(child).setIcon(0,QIcon(pixmap))  
        except Exception as e: 
            logger.exception(e)

    def save_figure(self):
        dialog = FileDialog(
            caption="Save Figure",
            filter="""Portable Network Graphics (*.png);;Tagged Image File Format (*.tiff);;JPEG (*.jpg *.jpeg);;
                      PDF (*.pdf);;Scalable Vector Graphics (*.svg);;PostScript formats (*.ps *.eps)"""
        )
        if dialog.exec():
            self.canvas.fig.savefig(
                fname=dialog.getSaveFileName()[0], 
                dpi=config["plot_dpi"]
            )

    def keyPressEvent(self, key: QKeyEvent) -> None:

        if key.key() == Qt.Key.Key_Slash:
            self.search_box.setFocus()
            self.stackedlayout.setCurrentWidget(self.treeview)
        
        elif key.key() == Qt.Key.Key_M:
            point_to_show = self.mapToGlobal(self.plot_visual.scene().sceneRect().center().toPoint())
            self.plot_visual.menu.exec(point_to_show)
        
        elif key.key() == Qt.Key.Key_N and key.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.sig_back_to_grScene.emit()
        
        elif key.key() == Qt.Key.Key_H and key.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.stackedlayout.setCurrentIndex(0)
        
        elif key.key() == Qt.Key.Key_F and key.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.save_figure()

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

