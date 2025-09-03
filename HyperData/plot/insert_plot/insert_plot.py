from PySide6.QtCore import Signal, Qt, QPropertyAnimation
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, 
                               QDockWidget, QMainWindow, QDialog)
from PySide6.QtGui import QPaintEvent
from plot.insert_plot.menu import Menu_type_2D, Menu_type_3D
from plot.insert_plot.input.widget_1input import *
from plot.insert_plot.input.widget_2input import *
from plot.insert_plot.input.widget_3input import *
from plot.insert_plot.input.widget_4input import *
from ui.base_widgets.button import DropDownPrimaryPushButton
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.window import ProgressBar
from ui.base_widgets.frame import Frame, ScrollArea
from ui.base_widgets.list import TreeWidget
from ui.base_widgets.line_edit import SearchBox
from plot.canvas import Canvas
from data_processing.utlis import split_input
from plot.plotting.plotting import rescale_plot, plotting
from node_editor.base.node_graphics_node import NodeGraphicsNode
from plot.insert_plot.utilis import load_InputIcon, load_MenuIcon
from config.settings import GLOBAL_DEBUG, logger, config

DEBUG = False

class NewPlot(Frame):
    """ This Widget will be created when creating a new plot to display input fields for the new plot """

    sig = Signal()
    sig_delete = Signal(object)

    def __init__(self, plot_gid:str, plot_type:str, canvas: Canvas, node:NodeGraphicsNode, plot3d=False, parent=None):
        super().__init__(parent)
        #self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.plot_gid = plot_gid
        self.plot_type = plot_type
        self.canvas = canvas
        self.artist = list()
        try: self.props = self.canvas._config[plot_gid]["plot_props"]
        except: self.props = dict()
        #self.widget = QWidget()
        self.node = node
        self.plot3d = plot3d

        # effect = QGraphicsOpacityEffect(self)
        # effect.setOpacity(0.5)
        # ani = QPropertyAnimation(effect, b'opacity', self)
        # ani.setDuration(100)
        # self.setGraphicsEffect(effect)
        # ani.setStartValue(0)
        # ani.setEndValue(1)
        # ani.start()

        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)

        layout = QHBoxLayout()
        mainlayout.addLayout(layout)
        self.text = TitleLabel(self.plot_gid.title())
        layout.addWidget(self.text)
        layout.addStretch()
        self.type = TransparentToolButton(
            icon='play.png',
            setter=self.plotting,
            layout=layout
        )        

        if plot3d: self.menu = Menu_type_3D(self)
        else: self.menu = Menu_type_2D(self)
        self.menu.sig.connect(self.update_layout)

        DropDownPrimaryPushButton(
            text=self.plot_type,
            menu=self.menu,
            layout=layout
        )

        self.progressbar = ProgressBar()
        mainlayout.addWidget(self.progressbar)

        self.layout_input = QVBoxLayout()
        mainlayout.addLayout(self.layout_input) 

        self.initUI()

    def initUI(self, input=None, axes=None):

        if not input: 
            try: input = self.canvas._config[self.plot_gid]["data_input"]
            except: input = [str(), str(), str(), str()]
        
        if not axes:
            try: axes = self.canvas._config[self.plot_gid]["axes"]
            except: axes = ["axis bottom", "axis left"]

        args = [self.node, input, axes, self.parent()]

        if   self.plot_type == "2d line":                   self.widget = Line2D(*args)
        elif self.plot_type == "2d step":                   self.widget = Step2D(*args)
        elif self.plot_type == "2d stem":                   self.widget = Stem2D(*args)
        elif self.plot_type == "2d spline":                 self.widget = Spline2D(*args)
        elif self.plot_type == "2d area":                   self.widget = Area2D(*args)
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
        elif self.plot_type == "radar":                     self.widget = Radar(*args)
        elif self.plot_type == "histogram":                 self.widget = Histogram(*args)
        elif self.plot_type == "stacked histogram":         self.widget = StackedHistogram(*args)
        elif self.plot_type == "boxplot":                   self.widget = Boxplot(*args)
        elif self.plot_type == "violinplot":                self.widget = Violinplot(*args)
        elif self.plot_type == "eventplot":                 self.widget = Eventplot(*args)
        elif self.plot_type == "hist2d":                    self.widget = Hist2D(*args)
        elif self.plot_type == "error bar":                 self.widget = Errorbar(*args)
        elif self.plot_type == "pareto":                    self.widget = Pareto(*args)
        elif self.plot_type == "andrews plot":              self.widget = Andrews(*args)
        elif self.plot_type == "covariance ellipse":        self.widget = CovEllipse(*args)
        elif self.plot_type == "heatmap":                   self.widget = Heatmap(*args)
        elif self.plot_type == "contour":                   self.widget = Contour(*args)

        elif self.plot_type == "3d line":                   self.widget = Line3D(*args)
        elif self.plot_type == "3d step":                   self.widget = Step3D(*args)
        elif self.plot_type == "3d stem":                   self.widget = Stem3D(*args)
        elif self.plot_type == "3d column":                 self.widget = Column3D(*args)
        elif self.plot_type == "3d scatter":                self.widget = Scatter3D(*args)
        elif self.plot_type == "3d bubble":                 self.widget = Bubble3D(*args)

        # self.widget.sig.connect(self.plotting)
        self.layout_input.addWidget(self.widget)

        self.update_config()

    def update_layout (self, plot_type:str):

        logger.info(f"Canvas {self.canvas.id}: {self.plot_gid} changes from "
                    f"type {self.plot_type} to type {plot_type}.")
        
        self.plot_type = plot_type
        self.props = dict()
        self.type.setText(plot_type.title())

        try: self.widget.deleteLater()
        except Exception as e: logger.exception(e)

        if plot_type == "delete":
            for obj in self.artist:
                obj.remove()
            rescale_plot(self.canvas.axes.figure)
            self.canvas.draw_idle()
            self.sig_delete.emit(self)
            self.deleteLater()
            self.canvas._config.pop(self.plot_gid)
            return None
        else:
            self.initUI()

        self.update_config()
        self.plotting()


    def plotting (self):
        self.progressbar.setValue(0)
        self.progressbar.set_value(0)

        _ax = self.widget.axes
  
        if self.plot3d:
            ax = self.canvas.axes
        else:
            self.canvas.axes.set_axis_on()
            self.canvas.axesx2.set_axis_on()
            self.canvas.axesy2.set_axis_on()
            self.canvas.axespie.set_axis_off()
            self.canvas.axespolar.set_axis_off()

            if _ax == ["axis bottom", "axis left"]:    ax = self.canvas.axes
            elif _ax == ["axis bottom", "axis right"]: ax = self.canvas.axesy2
            elif _ax == ["axis top", "axis left"]:     ax = self.canvas.axesx2
            elif _ax == "polar":
                ax = self.canvas.axespolar
                self.canvas.axes.set_axis_off()
                self.canvas.axesx2.set_axis_off()
                self.canvas.axesy2.set_axis_off()
                self.canvas.axespolar.set_axis_on()
            else:
                ax = self.canvas.axespie
                self.canvas.axes.set_axis_off()
                self.canvas.axesx2.set_axis_off()
                self.canvas.axesy2.set_axis_off()
                self.canvas.axespolar.set_axis_off()

        X, Y, Z, T  = list(), list(), list(), list()
        if len(self.widget.input) >= 1:
            X = split_input(self.widget.input[0], self.node.input_sockets[0].socket_data)
        if len(self.widget.input) >= 2:
            Y = split_input(self.widget.input[1], self.node.input_sockets[0].socket_data)
        if len(self.widget.input) >= 3:
            Z = split_input(self.widget.input[2], self.node.input_sockets[0].socket_data)
        if len(self.widget.input) >= 4:
            T = split_input(self.widget.input[3], self.node.input_sockets[0].socket_data)
        try:
            self.artist, self.props = plotting(
                X, Y, Z, T, ax=ax, gid=self.plot_gid, 
                plot_type=self.plot_type, 
                **self.props
            )

            self.update_config()
            self.progressbar.changeColor('success')

            logger.info(f"Canvas {self.canvas.id}: Plot {self.plot_gid} ({len(self.artist)} artists), "
                        f"type {self.plot_type}, on {self.widget.axes}.")

        except Exception as e:
            self.progressbar.changeColor('fail')
            logger.exception(e)
        
        self.sig.emit()
        self.progressbar.setValue(100)
        self.canvas.draw_idle()

    def update_config(self):
        self.canvas._config[self.plot_gid] = {
            "plot_type": self.plot_type,
            "axes": self.widget.axes,
            "data_input": [str(),str(),str(),str()],
            "plot_props": self.props,
        }
        
        for idx in range(len(self.widget.input)):
            self.canvas._config[self.plot_gid]["data_input"][idx] = self.widget.input[idx]

class InsertPlot(QMainWindow):
    sig = Signal() # emit when new plot was created, also when a plot needs to be updated

    def __init__(self, canvas:Canvas, node:NodeGraphicsNode, plot3d=False, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas
        self.node = node
        self.plot3d = plot3d
        self.widget = None
        self.plot_idx = 1
        self.plot_list: list[NewPlot] = list()

        self.mainlayout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainlayout)
        self.setCentralWidget(self.central_widget)

        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        if plot3d:
            self.type_list = {
                "Line": ['3d line','3d step','3d stem'],
                "Column": ['3d column'],
                "Scatter": ['3d scatter','3d bubble'],
                "Surface": ['3d surface','triangular 3d surface']
            }
        else:
            self.type_list = {
                "Line": ['2d line','2d step','2d stem'],
                "Area": ['fill between','2d area','2d stacked area','2d 100% stacked area'],
                "Column": ['2d column','2d clustered column','2d stacked column', 
                           '2d 100% stacked column','2d waterfall column'],
                "Dot": ['dot','clustered dot','stacked dot','dumbbell'],
                "Treemap": ['marimekko','treemap'],
                "Scatter": ['2d scatter','2d bubble'],
                "Polar": ['pie','coxcomb','doughnut','multilevel doughnut','semicircle doughnut',
                          'radar'],
                "Statistics": ['histogram','stacked histogram','hist2d','error bar','boxplot', 
                               'violinplot','eventplot','Pareto','Andrews plot','covariance ellipse',
                               ],
                "Mesh": ['heatmap','contour']
            }

        self.search_box = SearchBox(parent=self.parent())
        self.search_box.setPlaceholderText("Type / to search")
        self.sidebar_layout.addWidget(self.search_box)

        self.treeview = TreeWidget()
        self.treeview.itemPressed.connect(lambda item: self.add_plot(item.text(0)))
        self.treeview.setData(self.type_list)
        self.sidebar_layout.addWidget(self.treeview)
        self.search_box.set_TreeView(self.treeview)

        self.dock = QDockWidget('Insert_plot')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dock.setWidget(self.sidebar)
        self.dock.setTitleBarWidget(QWidget())

        self.graph_widget = ScrollArea()
        self.graph_widget.verticalScrollBar().rangeChanged.connect(lambda min, max: 
            self.graph_widget.verticalScrollBar().setSliderPosition(max))
        self.mainlayout.addWidget(self.graph_widget)

        # preload icons
        load_InputIcon()
        load_MenuIcon()
        
        for key in self.canvas._config.keys():
            if key.startswith("graph"):
                self.add_plot(self.canvas._config[key]["plot_type"], key)
        
        self.setMinimumSize(800, 500)
    
    def add_plot(self, plot_type:str, plot_gid:str=None):
        # this function can be either called when a new plot added, or 
        # reconstruction of NewPlot class when QMainWindow is recontructed
        
        if plot_type not in self.type_list.keys():
            if not plot_gid: plot_gid = f"graph {self.plot_idx}"
        
            newplot = NewPlot(plot_gid, plot_type, self.canvas, self.node, self.plot3d, self)
            self.plot_list.append(newplot)
            newplot.sig.connect(self.sig.emit)
            newplot.sig_delete.connect(self.delete_plot)
            self.graph_widget.vlayout.addWidget(newplot)

            # keep track of current plot index
            if plot_gid: self.plot_idx = int(plot_gid.split()[1])+1
            else: self.plot_idx += 1
        
    def delete_plot(self, plot:NewPlot):
        self.plot_list.remove(plot)
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
    
    def show(self):
        self.raise_() # ensure the window is on top of the stacking order
        return super().show()
                    


      
