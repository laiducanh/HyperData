### Import libraries from Python
import os

### Import libraries from PySide6
from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QDockWidget,
                             QStackedLayout, QTreeWidgetItem, QApplication)
from PySide6.QtGui import QKeyEvent, QPaintEvent, QPixmap, QColor, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView

from ui.base_widgets.list import TreeWidget
from ui.base_widgets.button import _TransparentToolButton
from ui.base_widgets.line_edit import _SearchBox
from ui.base_widgets.window import ProgressDialog, FileDialog
from config.settings import GLOBAL_DEBUG, logger, config

DEBUG = True

class PlotView (QMainWindow):
    sig_back_to_grScene = Signal()
    def __init__(self, node, canvas, parent=None):
        super().__init__(parent)

        self.main_layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.plot3d = False

        self.setup_visual()
        self.setup_sidebar()

        print(self.plot_visual.size())

    def setup_visual (self):
        self.plot_visual = QWebEngineView()
        html_path = os.path.abspath("plot_js/d3.html")
        self.plot_visual.load(QUrl.fromLocalFile(html_path))
        self.main_layout.addWidget(self.plot_visual)

    def setup_sidebar(self):

        if self.plot3d:
            self.treeview_data = {
                "Graph":["Manage graph"],
                "Tick":["Tick X3D","Tick Y3D","Tick Z3D"],
                "Spine":["Spine X3D","Spine Y3D","Spine Z3D"],
                "Figure":["Plot size","Grid"],
                "Label":["Title","Axis label","Legend","Data annotation"],
            }

        else:
            self.treeview_data = {
                "Graph":["Manage graph"],
                "Tick":["Tick bottom","Tick left","Tick top","Tick right"],
                "Spine":["Spine bottom","Spine left","Spine top","Spine right"],
                "Figure":["Plot size","Grid"],
                "Label":["Title","Axis label","Legend","Data annotation"],
            }

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
        # self.treeview.itemPressed.connect(self.treeview_func)
        self.treeview.setData(self.treeview_data)
        self.stackedlayout.addWidget(self.treeview)
        self.search_box.set_TreeView(self.treeview)

        self.dock = QDockWidget('Figure')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dock.setWidget(self.sidebar)
        self.dock.setTitleBarWidget(QWidget())

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
        

        