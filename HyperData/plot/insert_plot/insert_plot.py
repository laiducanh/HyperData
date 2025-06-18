from PySide6.QtCore import Signal, QSize, Qt, QPropertyAnimation
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QAbstractItemView, 
                               QDockWidget, QMainWindow, QTreeWidgetItem)
from PySide6.QtGui import QCursor, QPaintEvent
import os
from matplotlib.artist import Artist
from plot.plot_plottype_window import Plottype_Window
from plot.insert_plot.menu import Menu_type_2D, Menu_type_3D
from plot.insert_plot.input import widget_2input, widget_1input, widget_3input, widget_4input
from plot.insert_plot.input.widget_1input import *
from plot.insert_plot.input.widget_2input import *
from plot.insert_plot.input.widget_3input import *
from plot.insert_plot.input.widget_4input import *
from ui.base_widgets.button import _TransparentPushButton, DropDownPrimaryPushButton
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.window import ProgressBar
from ui.base_widgets.frame import Frame
from ui.base_widgets.list import TreeWidget
from ui.base_widgets.line_edit import _SearchBox
from plot.canvas import Canvas
from data_processing.utlis import split_input
from plot.plotting.plotting import rescale_plot, plotting
from node_editor.node_node import Node
from config.settings import GLOBAL_DEBUG, logger, config

DEBUG = False

AXES = 0
AXES_Y2 = 1
AXES_X2 = 2
AXES_PIE = 3

class InsertPlot (QMainWindow):
    sig = Signal() # emit when new plot was created, also when a plot needs to be updated

    def __init__(self, canvas:Canvas, node:Node, plot3d=False, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas
        self.node = node
        self.plot3d = plot3d
        self.plot_type = '2d line'
        self.widget = None

        self.mainlayout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainlayout)
        self.setCentralWidget(self.central_widget)

        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        if plot3d:
            self.plot_list = {
                "Line": ['3d line','3d step','3d stem'],
                "Column": ['3d column'],
                "Scatter": ['3d scatter','3d bubble'],
                "Pie": ['pie','doughnut'],
                "Statistics": ['histogram','stacked histogram','boxplot','violinplot'],
                "Surface": ['3d surface','triangular 3d surface']
            }
        else:
            self.plot_list = {
                "Line": ['2d line','2d step','2d stem'],
                "Area": ['fill between','2d area','2d stacked area','2d 100% stacked area'],
                "Column": ['2d column','2d clustered column','2d stacked column', 
                           '2d 100% stacked column','2d waterfall column'],
                "Dot": ['dot','clustered dot','stacked dot','dumbbell'],
                "Treemap": ['marimekko','treemap'],
                "Scatter": ['2d scatter','2d bubble'],
                "Pie": ['pie','coxcomb','doughnut','multilevel doughnut','semicircle doughnut'],
                "Statistics": ['histogram','stacked histogram','hist2d','error bar','boxplot', 
                               'violinplot','eventplot'],
                "Mesh": ['heatmap','contour']
            }

        self.search_box = _SearchBox(parent=self.parent())
        self.search_box.setPlaceholderText("Type / to search")
        self.sidebar_layout.addWidget(self.search_box)

        self.treeview = TreeWidget()
        self.treeview.currentItemChanged.connect(self.treeview_func)
        self.treeview.setData(self.plot_list)
        self.sidebar_layout.addWidget(self.treeview)
        self.search_box.set_TreeView(self.treeview)

        self.dock = QDockWidget('Insert_plot')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dock.setWidget(self.sidebar)
        self.dock.setTitleBarWidget(QWidget())
    
    def treeview_func(self, item:QTreeWidgetItem):

        if item.text(0) not in self.plot_list.keys():
            self.canvas._config["plot_type"] = item.text(0).lower()
            if self.widget: self.widget.deleteLater()
            self.initUI()
            self.plotting()

    def initUI(self):
        self.plot_type = self.canvas._config["plot_type"]
        args = [self.node, self.canvas._config["data_input"], self.parent()]

        if   self.plot_type == "2d line":                   self.widget = Line2D(*args)
        elif self.plot_type == "2d step":                   self.widget = Step2D(*args)
        elif self.plot_type == "2d stem":                   self.widget = Stem2D(*args)
        elif self.plot_type == "2d spline":                 self.widget = Spline2D(*args)
        elif self.plot_type == "2d area":                   self.widget = Fillbetween(*args)
        elif self.plot_type == "fill between":              self.widget = Fillbetween(*args)
        elif self.plot_type == "2d stacked area":           self.widget = StackedArea(*args)
        elif self.plot_type == "2d 100% stacked area":      self.widget = StackedArea100(*args)
        elif self.plot_type == "2d column":                 self.widget = Column2D(*args)
        elif self.plot_type == "dot":                       self.widget = Dot2D(*args)
        elif self.plot_type == "dumbbell":                  self.widget = Dumbbell(*args)
        elif self.plot_type == "2d clustered column":       self.widget = ClusteredColumn2D(*args)
        elif self.plot_type == "clustered dot":             self.widget = ClusteredDot(*args)
        elif self.plot_type == "2d stacked column":         self.widget = StackedColumn2D(*args)
        elif self.plot_type == "stacked dot":               self.widget = StackedDot(*args)
        elif self.plot_type == "2d 100% stacked column":    self.widget = StackedColumn2D100(*args)
        elif self.plot_type == "2d waterfall column":       self.widget = Waterfall(*args)
        elif self.plot_type == "marimekko":                 self.widget = Marimekko(*args)
        elif self.plot_type == "treemap":                   self.widget = Treemap(*args)
        elif self.plot_type == "2d scatter":                self.widget = Scatter2D(*args)
        elif self.plot_type == "2d bubble":                 self.widget = Bubble2D(*args)
        elif self.plot_type == "pie":                       self.widget = Pie(*args)
        elif self.plot_type == "coxcomb":                   self.widget = Coxcomb(*args)
        elif self.plot_type == "doughnut":                  self.widget = Doughnut(*args)
        elif self.plot_type == "multilevel doughnut":       self.widget = MultilevelDoughnut(*args)
        elif self.plot_type == "semicircle doughnut":       self.widget = SemicircleDoughnut(*args)
        elif self.plot_type == "histogram":                 self.widget = Histogram(*args)
        elif self.plot_type == "stacked histogram":         self.widget = StackedHistogram(*args)
        elif self.plot_type == "boxplot":                   self.widget = Boxplot(*args)
        elif self.plot_type == "violinplot":                self.widget = Violinplot(*args)
        elif self.plot_type == "eventplot":                 self.widget = Eventplot(*args)
        elif self.plot_type == "hist2d":                    self.widget = Hist2D(*args)
        elif self.plot_type == "error bar":                 self.widget = Errorbar(*args)
        elif self.plot_type == "heatmap":                   self.widget = Heatmap(*args)
        elif self.plot_type == "contour":                   self.widget = Contour(*args)

        elif self.plot_type == "3d line":                   self.widget = Line3D(*args)
        elif self.plot_type == "3d step":                   self.widget = Step3D(*args)
        elif self.plot_type == "3d stem":                   self.widget = Stem3D(*args)
        elif self.plot_type == "3d column":                 self.widget = Column3D(*args)
        elif self.plot_type == "3d scatter":                self.widget = Scatter3D(*args)
        elif self.plot_type == "3d bubble":                 self.widget = Bubble3D(*args)

        self.widget.sig.connect(self.plotting)
        self.mainlayout.addWidget(self.widget)

    def plotting(self, _ax:int=AXES, **kwargs):
        for idx, inp in enumerate(self.widget.input):
            self.canvas._config["data_input"][idx] = inp

        input = self.canvas._config["data_input"]

        if self.plot3d:
            ax = self.canvas.axes
        else:
            self.canvas.axes.set_axis_on()
            self.canvas.axesx2.set_axis_on()
            self.canvas.axesy2.set_axis_on()
            self.canvas.axespie.set_axis_off()
            
            if _ax == AXES:    ax = self.canvas.axes
            elif _ax == AXES_Y2: ax = self.canvas.axesy2
            elif _ax == AXES_X2:     ax = self.canvas.axesx2
            elif _ax == AXES_PIE: 
                ax = self.canvas.axespie
                self.canvas.axes.set_axis_off()
                self.canvas.axesx2.set_axis_off()
                self.canvas.axesy2.set_axis_off()
            

        X, Y, Z, T  = list(), list(), list(), list()
        if len(input) >= 1:
            X = split_input(input[0], self.node.input_sockets[0].socket_data)
        if len(input) >= 2:
            Y = split_input(input[1], self.node.input_sockets[0].socket_data)
        if len(input) >= 3:
            Z = split_input(input[2], self.node.input_sockets[0].socket_data)
        if len(input) >= 4:
            T = split_input(input[3], self.node.input_sockets[0].socket_data)
        try:
            self.artist = plotting(X, Y, Z, T, ax=ax, gid="graph", plot_type=self.canvas._config["plot_type"], **kwargs)
        except Exception as e:
            logger.exception(e)

        self.sig.emit()
    
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
                    


      
