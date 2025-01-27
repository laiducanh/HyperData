from PySide6.QtCore import Signal, QSize, Qt, QPropertyAnimation
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QScrollArea, QWidget)
from PySide6.QtGui import QCursor
import os
from matplotlib.artist import Artist
from plot.plot_plottype_window import Plottype_Window
from plot.insert_plot.menu import Menu_type_2D, Menu_type_3D
from plot.insert_plot.input import widget_2input, widget_1input, widget_3input, widget_4input
from ui.base_widgets.button import _TransparentPushButton, _DropDownPrimaryPushButton
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.window import ProgressBar
from ui.base_widgets.frame import Frame
from plot.canvas import Canvas
from data_processing.utlis import split_input
from plot.plotting.plotting import rescale_plot, plotting
from plot.insert_plot.utilis import load_MenuIcon, load_InputIcon
from node_editor.node_node import Node
from config.settings import GLOBAL_DEBUG, logger, color_cycle
from typing import List

DEBUG = False

ICON_PATH_2D = {'2d line':os.path.join("Plot","line.png"),
                '2d area':os.path.join("Plot","area.png"),
                '2d column':os.path.join("Plot","bar.png"),
                '2d scatter':os.path.join("Plot","scatter.png"),
                'pie':os.path.join("Plot","pie.png"),}
ICON_PATH_3D = {'3d line':os.path.join("Plot","line.png"),
                '3d area':os.path.join("Plot","area.png"),
                '3d column':os.path.join("Plot","bar.png"),
                '3d scatter':os.path.join("Plot","scatter.png"),
                '3d surface':os.path.join("Plot","surface.png")}


class Grid_Plottype (QHBoxLayout):
    """ Grid plot type display on top of Insert tab """

    sig = Signal(str) # emit when a button in grid was triggered and a new plot was created
                            # str is the plot type chosen from the grid

    def __init__(self, plot3d=False, parent=None):
        super().__init__()
               
        if plot3d:
            for basic_plot in ['3d line','3d area','3d column','3d scatter','3d surface']:
                self.button = _TransparentPushButton()
                self.button.setIcon(ICON_PATH_3D[basic_plot])
                self.button.setIconSize(QSize(40,40))
                self.button.setFixedSize(QSize(50,50))
                self.button.setToolTip(basic_plot.title())
                self.button.pressed.connect(lambda s=basic_plot: self.sig.emit(s))
                self.addWidget(self.button)
        else:
            for basic_plot in ['2d line','2d area','2d column','2d scatter','pie']:
                self.button = _TransparentPushButton()
                self.button.setIcon(ICON_PATH_2D[basic_plot])
                self.button.setIconSize(QSize(40,40))
                self.button.setFixedSize(QSize(50,50))
                self.button.setToolTip(basic_plot.title())
                self.button.pressed.connect(lambda s=basic_plot: self.sig.emit(s))
                self.addWidget(self.button)
        ###

        self.plottype_window = Plottype_Window(plot3d, parent) # Plot type window
        self.plottype_window.sig.connect(lambda s: self.sig.emit(s))
        
        add_plot = _TransparentPushButton()
        add_plot.setIcon("add.png")
        add_plot.setIconSize(QSize(30,30))
        add_plot.setFixedSize(QSize(50,50))
        add_plot.setToolTip('More Graphs')
        add_plot.setToolTipDuration(1000)
        add_plot.clicked.connect(lambda: self.plottype_window.show()) # open up Plot type window when this button was triggered
        self.addWidget(add_plot)
        

class NewPlot (Frame):
    """ This Widget will be created when creating a new plot to display input fields for the new plot """

    sig = Signal()
    sig_delete = Signal(object)

    def __init__(self, plot_index, plot_type, canvas: Canvas, node:Node, plot3d=False, parent=None):
        super().__init__(parent)
        #self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.plot_index = plot_index
        self.plot_type = plot_type
        self.canvas = canvas
        self.artist = list()
        #self.widget = QWidget()
        self.node = node
        self.plot3d = plot3d
        self.plot_1input = ["pie","coxcomb",
                            "doughnut","multilevel doughnut","semicircle doughnut",
                            "treemap","marimekko",
                            "histogram","stacked histogram",
                            "boxplot","violinplot","eventplot"]
        self.plot_3input = ["fill between","2d bubble","dumbbell"]
        self.plot_3dtype = ["3d line","3d step","3d stem","3d column",
                        "3d scatter"]
        self.plot_4input = ["3d bubble"]

        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(0.5)
        ani = QPropertyAnimation(effect, b'opacity', self)
        ani.setDuration(100)
        self.setGraphicsEffect(effect)
        ani.setStartValue(0)
        ani.setEndValue(1)
        ani.start()

        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)

        layout = QHBoxLayout()
        mainlayout.addLayout(layout)
        self.text = TitleLabel("Graph %d"%self.plot_index)
        layout.addWidget(self.text)
        layout.addStretch()
        self.type = _DropDownPrimaryPushButton()
        self.type.setText(self.plot_type)
        
        
        if plot3d: self.menu = Menu_type_3D(self)
        else: self.menu = Menu_type_2D(self)
        self.menu.sig.connect(self.update_layout)
        self.type.setMenu(self.menu)
        #self.type.released.connect(lambda: self.menu.exec(QCursor().pos()))
        layout.addWidget(self.type)

        self.progressbar = ProgressBar()
        mainlayout.addWidget(self.progressbar)
        
        self.layout_input = QVBoxLayout()
        mainlayout.addLayout(self.layout_input) 

        self.initUI()

    def initUI(self):
        
        _input = [str(), str(), str(), str()]
        if self.plot_type in self.plot_1input:
            self.widget = widget_1input.WidgetPie(self.node, _input, self.parent())
        elif self.plot_type in self.plot_3input:
            self.widget = widget_3input.Widget2D_3input(self.node, _input, self.parent())
        elif self.plot_type in self.plot_3dtype:
            self.widget = widget_3input.Widget3D(self.node, _input, self.parent())
        elif self.plot_type in self.plot_4input:
            self.widget = widget_4input.Widget3D_4input(self.node, _input, self.parent())
        else:
            self.widget = widget_2input.Widget2D_2input(self.node, _input, self.parent())

        self.widget.sig.connect(self.plotting)
        self.layout_input.addWidget(self.widget)
        

    def update_layout (self, plot_type):

        self.plot_type = plot_type
        self.type.setText(plot_type.title())

        
        _input = [str(), str(), str(), str()]
        try: 
            for ind, val in enumerate(self.widget.input):
                _input[ind] = val
            self.widget.deleteLater()
        except Exception as e: logger.exception(e)
            

        if plot_type == "delete":
            for obj in self.artist:
                obj.remove()
            rescale_plot(self.canvas.axes.figure)
            self.canvas.draw_idle()
            self.sig_delete.emit(self)
            self.deleteLater()
            return None
        elif plot_type in self.plot_1input:
            self.widget = widget_1input.WidgetPie(self.node, _input, self.parent())
        elif plot_type in self.plot_3input:
            self.widget = widget_3input.Widget2D_3input(self.node, _input, self.parent())
        elif self.plot_type in self.plot_3dtype:
            self.widget = widget_3input.Widget3D(self.node, _input, self.parent())
        elif self.plot_type in self.plot_4input:
            self.widget = widget_4input.Widget3D_4input(self.node, _input, self.parent())
        else:
            self.widget = widget_2input.Widget2D_2input(self.node, _input, self.parent())

        self.widget.sig.connect(self.plotting)
        self.layout_input.addWidget(self.widget)

        self.plotting()
    

    def plotting (self, **kwargs):
        self.progressbar.setValue(0)
        self.progressbar._setValue(0)
        
        input = self.widget.input
        _ax = self.widget.axes

        if self.plot3d:
            ax = self.canvas.axes
        else:
            self.canvas.axes.set_axis_on()
            self.canvas.axesx2.set_axis_on()
            self.canvas.axesy2.set_axis_on()
            self.canvas.axespie.set_axis_off()
            
            match _ax:
                case ["axis bottom", "axis left"]:  ax = self.canvas.axes
                case ["axis bottom", "axis right"]: ax = self.canvas.axesy2
                case ["axis top", "axis left"]:     ax = self.canvas.axesx2
                case "pie": 
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
            self.artist = plotting(X, Y, Z, T, ax=ax, gid=f"graph {self.plot_index}", 
                                   plot_type=self.plot_type, **kwargs)
            for art in self.artist:
                art.plot_type = self.plot_type
        except Exception as e:
            logger.exception(e)

        self.sig.emit()
        self.progressbar.setValue(100)

class InsertPlot (QWidget):
    sig = Signal() # emit when new plot was created, also when a plot needs to be updated

    def __init__(self, canvas:Canvas, node, plot3d=False, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10,0,10,15)
        self.canvas = canvas
        self.num_plot = 0 # keep track of the indexes of plots
        self.plotlist = list()
        self.plotlist: List[NewPlot]
        self.node = node
        self.plot3d = plot3d
        load_MenuIcon()
        load_InputIcon()

        plottype = Grid_Plottype(plot3d, parent)
        self.layout.addLayout(plottype)
        plottype.sig.connect(self.add_plot)
        
        self.scroll_area = QScrollArea(parent)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        widget = QWidget(parent) 
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.scroll_area)
        widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignJustify)
        self.scroll_area.verticalScrollBar().rangeChanged.connect(lambda min, max: self.scroll_area.verticalScrollBar().setSliderPosition(max))
  
    def add_plot (self, plot_type):
 
        self.num_plot += 1   
        newplot = NewPlot(self.num_plot, plot_type, self.canvas, self.node, self.plot3d)
        self.plotlist.append(newplot)
        newplot.sig.connect(self.sig.emit)
        newplot.sig_delete.connect(self.delete_plot)
        self.vlayout.addWidget(newplot)
    
    def delete_plot(self, plot:NewPlot):
        self.plotlist.remove(plot)
        self.sig.emit()
    
                    


      
