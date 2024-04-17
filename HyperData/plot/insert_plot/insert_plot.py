from PyQt6.QtCore import pyqtSignal, QSize, Qt
from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QScrollArea, QWidget)
from PyQt6.QtGui import QCursor
import os
from plot.plot_plottype_window import Plottype_Window
from plot.insert_plot.menu import Menu_type
from plot.insert_plot.input import widget_2input, widget_1input, widget_3input
from ui.base_widgets.button import _PushButton, DropDownPrimaryPushButton
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.window import ProgressBar
from ui.base_widgets.frame import Frame
from plot.canvas import Canvas
from data_processing.utlis import split_input
from plot.plotting.plotting import plotting
from node_editor.node_node import Node
from typing import List

DEBUG = False

ICON_PATH={'2d line':os.path.join("Plot","line.png"),
      '2d area':os.path.join("Plot","area.png"),
      '2d column':os.path.join("Plot","clustered-column.png"),
      '2d scatter':os.path.join("Plot","scatter.png"),
      'pie':os.path.join("Plot","pie.png"),}


class Grid_Plottype (QHBoxLayout):
    """ Grid plot type display on top of Insert tab """

    sig = pyqtSignal(str) # emit when a button in grid was triggered and a new plot was created
                            # str is the plot type chosen from the grid

    def __init__(self, parent=None):
        super().__init__()
               
        ### Create grid 
        xpos, ypos = 0,0
        for self.basic_plot in ['2d line','2d area','2d column','2d scatter','pie']:
            self.button = _PushButton()
            self.button.setIcon(ICON_PATH[self.basic_plot])
            self.button.setIconSize(QSize(50,50))
            self.button.setFixedSize(QSize(50,50))
            self.button.setToolTip(self.basic_plot.title())
            #self.button.installEventFilter(qfluentwidgets.ToolTipFilter(self, 0, qfluentwidgets.ToolTipPosition.BOTTOM))
            self.button.clicked.connect(lambda checked, s=self.basic_plot: self.sig.emit(s))
            self.addWidget(self.button,xpos)
            
            ypos += 1
            if ypos > 2:
                xpos += 1
                ypos = 0
        ###

        self.plottype_window = Plottype_Window(parent) # Plot type window
        self.plottype_window.sig.connect(lambda s: self.sig.emit(s))
        
        add_plot = _PushButton()
        add_plot.setIcon("add.png")
        add_plot.setIconSize(QSize(30,30))
        add_plot.setFixedSize(QSize(50,50))
        add_plot.setToolTip('More Graphs')
        add_plot.setToolTipDuration(1000)
        add_plot.clicked.connect(lambda: self.plottype_window.show()) # open up Plot type window when this button was triggered
        self.addWidget(add_plot,xpos)
        

class NewPlot (Frame):
    """ This Widget will be created when creating a new plot to display input fields for the new plot """

    sig = pyqtSignal()
    sig_delete = pyqtSignal(object)

    def __init__(self, current_plot, plot_type, canvas: Canvas, node:Node, parent=None):
        super().__init__(parent)
        #self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.current_plot = current_plot
        self.plot_type = plot_type
        self.canvas = canvas
        self.gidlist = list()
        #self.widget = QWidget()
        self.node = node
        self.parent = parent
        self.change_type = False

        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(1)
        #ani = QPropertyAnimation(effect, b'opacity', self)
        #ani.setDuration(100)
        #self.setGraphicsEffect(effect)
        #ani.setStartValue(0)
        #ani.setEndValue(1)
        #ani.start()
        #ani.finished.connect(self.sig_ani.emit)

        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)

        layout = QHBoxLayout()
        mainlayout.addLayout(layout)
        self.text = TitleLabel("Graph %d"%self.current_plot)
        layout.addWidget(self.text)
        layout.addStretch()
        self.type = DropDownPrimaryPushButton()
        self.type.button.setText(self.plot_type)
        
        
        self.menu = Menu_type(self)
        self.menu.sig.connect(self.update_layout)
        self.type.button.setMenu(self.menu)
        self.type.button.released.connect(lambda: self.menu.exec(QCursor().pos()))
        layout.addWidget(self.type)

        self.progressbar = ProgressBar()
        mainlayout.addWidget(self.progressbar)
        
        self.layout1 = QVBoxLayout()
        mainlayout.addLayout(self.layout1) 

        self.update_layout(self.plot_type) 


    def update_layout (self, plot_type):

        self.change_type = True
        self.plot_type = plot_type
        self.type.button.setText(plot_type.title())

        
        _input = [str(), str(), str(), str()]
        try: 
            for ind, val in enumerate(self.widget.input):
                _input[ind] = val
            self.widget.deleteLater()
        except: pass
            

        if plot_type == "delete":
            self.sig_delete.emit(self)
            self.deleteLater()
            return None
        elif plot_type in ["pie","doughnut","treemap","marimekko"]:
            self.widget = widget_1input.WidgetPie(self.node, _input, self.parent)
        elif plot_type in ["fill between","bubble"]:
            self.widget = widget_3input.Widget2D_3input(self.node, _input, self.parent)
        else:
            self.widget = widget_2input.Widget2D_2input(self.node, _input, self.parent)

        self.widget.sig.connect(self.plotting)
        self.layout1.addWidget(self.widget)

        self.plotting()

    def plotting (self, fire_signal=True, **kwargs):
        
        self.progressbar.setValue(0)
        self.progressbar._setValue(0)
        
        input = self.widget.input
        _ax = self.widget.axes

        self.canvas.axes.set_axis_on()
        self.canvas.axesx2.set_axis_on()
        self.canvas.axesy2.set_axis_on()
        self.canvas.axespie.set_axis_off()

        if _ax == ["axis bottom", "axis left"]:
            ax = self.canvas.axes
        elif _ax == ["axis bottom", "axis right"]:
            ax = self.canvas.axesy2
        elif _ax == ["axis top", "axis left"]:
            ax = self.canvas.axesx2
        elif _ax == "pie":
            # only allow 1 graph at a time
            self.canvas.fig.delaxes(self.canvas.axespie)
            self.canvas.axespie = self.canvas.fig.add_subplot()
            ax = self.canvas.axespie
            self.canvas.axespie.set_axis_off()
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
            self.gidlist = plotting(X, Y, Z, T, ax=ax, gid=f"graph {self.current_plot}", plot_type=self.plot_type, update=not self.change_type, **kwargs)
            if fire_signal: self.sig.emit()
        except Exception as e:
            print("NewPlot::plotting", e)
        
        self.change_type = False
        
        self.progressbar.setValue(100)

class InsertPlot (QWidget):
    sig = pyqtSignal() # emit when new plot was created, also when a plot needs to be updated

    def __init__(self, canvas:Canvas, node, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10,0,10,15)
        self.canvas = canvas
        self.num_plot = 0 # keep track of the indexes of plots
        self.plotlist = list()
        self.plotlist: List[NewPlot]
        self.gidlist = list()
        self.node = node

        plottype = Grid_Plottype(parent)
        self.layout.addLayout(plottype)
        plottype.sig.connect(self.add_plot)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        widget = QWidget() 
        widget.setObjectName('InsertTab')
        widget.setStyleSheet("QWidget#InsertTab {border: none}")
        self.layout2 = QVBoxLayout()
        self.layout2.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.scroll_area)
        widget.setLayout(self.layout2)
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignJustify)
        self.scroll_area.verticalScrollBar().rangeChanged.connect(lambda min, max: self.scroll_area.verticalScrollBar().setSliderPosition(max))

    def add_plot (self, plot_type):

        self.num_plot += 1   

        newplot = NewPlot(self.num_plot, plot_type, self.canvas, self.node)
        self.plotlist.append(newplot)
        newplot.sig.connect(self.update_gidlist)
        newplot.sig_delete.connect(self.delete_plot)
        self.layout2.addWidget(newplot)
    
    def delete_plot (self, plot:NewPlot):
        self.plotlist.remove(plot)
        self.num_plot = 0 # reset number of plots
        for _ax in self.canvas.fig.axes: _ax.cla() # reset all axes
        for i in self.plotlist:
            self.num_plot += 1
            i.text.setText("Graph %d"%self.num_plot)
            i.current_plot = self.num_plot
            i.plotting(False)
        
        self.update_gidlist()

    def update_gidlist(self):
        """ this function is used for updating a list of graphs that are visible on screen 
            and fire signal to update the graph list on under "insert" of side panel """
        
        self.gidlist = list()
        for i in self.plotlist:
            self.gidlist += i.gidlist
        
        self.sig.emit()

    
                    


      
