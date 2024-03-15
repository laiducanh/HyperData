from PyQt6.QtCore import QThreadPool, pyqtSignal, QSize, Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QLabel, QProgressBar,
                             QGraphicsOpacityEffect, QScrollArea, QWidget)
from PyQt6.QtGui import QCursor
import os, matplotlib, qfluentwidgets, time
from plot.plot_plottype_window import Plottype_Window
from plot.insert_plot.menu import Menu_type
from plot.insert_plot.input import widget_2input
from ui.base_widgets.button import _ToolButton, PrimaryDropDownPushButton
from ui.base_widgets.text import StrongBodyLabel
from ui.base_widgets.icons import Icon
from plot.canvas import Canvas
from data_processing.utlis import split_input
from plot.plotting.plotting import plotting
from node_editor.node_node import Node
import pandas as pd

DEBUG = False

icon={'2d line':os.path.join("Plot","line.png"),
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
            self.button = _ToolButton()
            self.button.setIcon(Icon(icon[self.basic_plot]))
            self.button.setIconSize(QSize(50,50))
            self.button.setFixedSize(QSize(50,50))
            self.button.setToolTip(self.basic_plot.title())
            self.button.installEventFilter(qfluentwidgets.ToolTipFilter(self, 0, qfluentwidgets.ToolTipPosition.BOTTOM))
            self.button.clicked.connect(lambda checked, s=self.basic_plot: self.sig.emit(s))
            self.addWidget(self.button,xpos)
            
            ypos += 1
            if ypos > 2:
                xpos += 1
                ypos = 0
        ###

        self.plottype_window = Plottype_Window(parent) # Plot type window
        self.plottype_window.sig.connect(lambda s: self.sig.emit(s))
        
        add_plot = _ToolButton()
        add_plot.setIcon(Icon(os.path.join("add.png")))
        add_plot.setIconSize(QSize(30,30))
        add_plot.setFixedSize(QSize(50,50))
        add_plot.setToolTip('More Graphs')
        add_plot.setToolTipDuration(1000)
        add_plot.clicked.connect(lambda: self.plottype_window.show()) # open up Plot type window when this button was triggered
        self.addWidget(add_plot,xpos)
        

class NewPlot (qfluentwidgets.CardWidget):
    """ This Widget will be created when creating a new plot to display input fields for the new plot """

    sig = pyqtSignal()
    sig_choose_type = pyqtSignal()
    sig_ani = pyqtSignal()

    def __init__(self, current_plot, plot_type, canvas: Canvas, node:Node, parent=None):
        super().__init__(parent)
        #self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.current_plot = current_plot
        self.plot_type = plot_type
        self.canvas = canvas
        self.gidlist = list()
        self.widget = QWidget()
        self.node = node

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
        #mainlayout.setContentsMargins(0,0,0,0)
        #mainlayout.addWidget(Shape.SeparateHLine())

        layout = QHBoxLayout()
        mainlayout.addLayout(layout)
        self.text = StrongBodyLabel("Graph %d"%self.current_plot)
        layout.addWidget(self.text)
        layout.addStretch()
        self.type = PrimaryDropDownPushButton()
        self.type.button.setText(self.plot_type)
        
        
        self.menu = Menu_type(self)
        self.menu.sig.connect(self.update_layout)
        self.menu.sig.connect(self.sig_choose_type.emit)
        self.type.button.setMenu(self.menu)
        self.type.button.released.connect(lambda: self.menu.exec(QCursor().pos()))
        layout.addWidget(self.type)
        
        self.layout1 = QVBoxLayout()
        mainlayout.addLayout(self.layout1) 

        self.update_layout(self.plot_type) 


    def update_layout (self, plot_type):
        self.plot_type = plot_type
        self.type.button.setText(plot_type.title())

        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(1)
        ani = QPropertyAnimation(effect, b'opacity', self)
        ani.setDuration(500)
        self.setGraphicsEffect(effect)
        ani.setStartValue(0)
        ani.setEndValue(1)
        ani.start()
        ani.finished.connect(self.sig_ani.emit)

        try: self.widget.deleteLater()
        except:pass

        if plot_type in ["2d line","2d step"]:
            self.widget = widget_2input.Widget2D_2input(self.node)

        self.widget.sig.connect(self.plotting)
        self.layout1.addWidget(self.widget)

        self.plotting()    

    def plotting (self):

        input = self.widget.input
        X, Y  = list(), list()
        if input != list():
            X = split_input(input[0], self.node.input_sockets[0].socket_data)
            Y = split_input(input[1], self.node.input_sockets[0].socket_data)
        
        self.gidlist = plotting(X, Y, ax=self.canvas.axes, gid=f"graph {self.current_plot}", plot_type=self.plot_type)
        self.sig.emit()
        

class InsertPlot (QWidget):
    sig = pyqtSignal() # emit when new plot was created, also when a plot needs to be updated

    def __init__(self, canvas:Canvas, node, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.canvas = canvas
        self.num_plot = 0 # keep track of the indexes of plots
        self.plotlist = list()
        self.gidlist = list()
        self.node = node

        plottype = Grid_Plottype(parent)
        self.layout.addLayout(plottype)
        plottype.sig.connect(self.add_plot)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName('QScrollArea')
        self.scroll_area.setStyleSheet('QScrollArea {border: none; background-color:transparent}')
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        widget = QWidget() 
        widget.setObjectName('InsertTab')
        widget.setStyleSheet("QWidget#InsertTab {border: none}")
        self.layout2 = QVBoxLayout()
        self.layout.addWidget(self.scroll_area)
        widget.setLayout(self.layout2)
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignJustify)
        #self.setScrollAnimation(Qt.Orientation.Vertical,400, QEasingCurve.)
        #self.setStyleSheet("""border: none""")
        self.scroll_area.verticalScrollBar().rangeChanged.connect(lambda min, max: self.scroll_area.verticalScrollBar().setSliderPosition(max))

    def add_plot (self, plot_type):

        self.num_plot += 1   

        progressbar = qfluentwidgets.ProgressBar()
        self.layout2.addWidget(progressbar)

        newplot = NewPlot(self.num_plot, plot_type, self.canvas, self.node)
        self.plotlist.append(newplot)
        newplot.sig.connect(self.func)
        self.layout2.addWidget(newplot)
        newplot.sig_choose_type.connect(lambda: progressbar.setValue(0))
        newplot.sig_ani.connect(lambda: progressbar.setValue(100))

        progressbar.setValue(100)
    
    def func(self):
        self.gidlist = list()
        for i in self.plotlist:
            self.gidlist += i.gidlist
        
        self.sig.emit()

                    


      
