from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QApplication
import matplotlib.pyplot
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import Slider, DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine, Frame
from ui.base_widgets.window import ProgressDialog
from plot.canvas import Canvas
import matplotlib
from config.settings import linestyle_lib, GLOBAL_DEBUG, logger

DEBUG = False

class PlotSize2D (Frame):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)
        self.canvas = canvas

        layout.addWidget(TitleLabel('Figure Margin'))
        layout.addWidget(SeparateHLine())

        top = DoubleSpinBox(text='Margin top',text2="The position of the top edge",
                            min=0,max=1,step=0.05)
        top.button.valueChanged.connect(self.set_top)
        top.button.setValue(self.get_top())
        layout.addWidget(top)

        bottom = DoubleSpinBox(text='Margin bottom',text2='The position of the bottom edge',
                               min=0,max=1,step=0.05)
        bottom.button.valueChanged.connect(self.set_bottom)
        bottom.button.setValue(self.get_bottom())
        layout.addWidget(bottom)

        left = DoubleSpinBox(text='Margin left',text2='The position of the left edge',
                             min=0,max=1,step=0.05)
        left.button.valueChanged.connect(self.set_left)
        left.button.setValue(self.get_left())
        layout.addWidget(left)

        right = DoubleSpinBox(text='Margin right',text2='The position of the right edge',
                              min=0,max=1,step=0.05)
        right.button.valueChanged.connect(self.set_right)
        right.button.setValue(self.get_right())
        layout.addWidget(right)
        #layout.addStretch()
    
    def set_top(self,value):
        self.canvas.fig.subplots_adjust(top=value)
        self.canvas.draw_idle()
    
    def get_top(self):
        return self.canvas.fig.subplotpars.top
    
    def set_bottom(self,value):
        self.canvas.fig.subplots_adjust(bottom=value)
        self.canvas.draw_idle()
    
    def get_bottom(self):
        return self.canvas.fig.subplotpars.bottom
    
    def set_left(self,value):
        self.canvas.fig.subplots_adjust(left=value)
        self.canvas.draw_idle()
    
    def get_left(self):
        return self.canvas.fig.subplotpars.left
    
    def set_right(self,value):
        self.canvas.fig.subplots_adjust(right=value)
        self.canvas.draw_idle()
    
    def get_right(self):
        return self.canvas.fig.subplotpars.right

    
class Grid2D (Frame):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)
        self.canvas = canvas

        layout.addWidget(TitleLabel('Grid'))
        layout.addWidget(SeparateHLine())

        self.visible = Toggle(text='Visible',text2='Whether to show the grid lines')
        layout.addWidget(self.visible)
        self.visible.button.checkedChanged.connect(self.set_grid)
        self.visible.button.setChecked(self.get_visible())

        self.type = ComboBox(items=['Major','Minor','Both'],
                             text='Type',text2='The grid lines to apply the changes on')
        self.type.button.currentTextChanged.connect(self.set_gridtype)
        self.type.button.setCurrentText(self.get_gridtype())
        layout.addWidget(self.type)

        self.axis = ComboBox(text='Axis',text2='The axis to apply the changes on',
                             items=['X','Y','Both'])
        self.axis.button.currentTextChanged.connect(self.set_gridaxis)
        self.axis.button.setCurrentText(self.get_gridaxis())
        layout.addWidget(self.axis)

        self.color = ColorDropdown(text='Line color',text2='Set the color of the grid',
                                   color=self.get_color())
        self.color.button.colorChanged.connect(self.set_color)
        layout.addWidget(self.color)

        self.linewidth = DoubleSpinBox(text='Line width',text2='Set the width of the grid lines',
                                       min=0.1,max=10,step=0.5)
        self.linewidth.button.valueChanged.connect(self.set_linewidth)
        self.linewidth.button.setValue(self.get_linewidth())
        layout.addWidget(self.linewidth)

        self.linestyle = ComboBox(text='Line style',text2='Set the style of the grid lines',
                                  items=linestyle_lib.values())
        self.linestyle.button.currentTextChanged.connect(self.set_linestyle)
        self.linestyle.button.setCurrentText(self.get_linestyle())
        layout.addWidget(self.linestyle)

        self.transparency = Slider(text='Transparency', text2='Set the transparency of the grid lines')
        self.transparency.button.valueChanged.connect(self.set_alpha)
        self.transparency.button.setValue(self.get_alpha())
        layout.addWidget(self.transparency)

    def set_grid(self):
        try:
            self.canvas.axes.grid(visible=False)
            if self.visible.button.isChecked():
                which = self.type.button.currentText().lower()
                axis = self.axis.button.currentText().lower()
                alpha = self.transparency.button.value()/100
                linewidth = self.linewidth.button.value()
                linestyle = self.linestyle.button.currentText().lower()
                color = self.color.button.color.name()

                self.canvas.axes.grid(which=which, axis=axis, alpha=alpha, linewidth=linewidth,
                                    linestyle=linestyle, color=color,gid="_grid")
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)
    
    def get_visible(self):
        for obj in self.canvas.fig.findobj(match=matplotlib.lines.Line2D):
            if obj._gid != None and '_grid' in obj._gid:
                return obj.get_visible()
        return False
    
    def set_gridtype(self, value:str):
        matplotlib.rcParams['axes.grid.which'] = value.lower()
        self.set_grid()
    
    def get_gridtype (self):
        return matplotlib.rcParams['axes.grid.which'].title()
    
    def set_gridaxis(self, value:str):
        matplotlib.rcParams['axes.grid.axis'] = value.lower()
        self.set_grid()

    def get_gridaxis (self):
        return matplotlib.rcParams['axes.grid.axis'].title()

    def set_alpha(self, value:int):
        matplotlib.rcParams['grid.alpha'] = value/100
        self.set_grid()

    def get_alpha(self):
        return int(matplotlib.rcParams['grid.alpha']*100)
    
    def set_linewidth(self, value:float):
        matplotlib.rcParams['grid.linewidth'] = value
        self.set_grid()
    
    def get_linewidth(self) -> str:
        return matplotlib.rcParams['grid.linewidth']
    
    def set_linestyle(self, value:str):
        linestyle_lib[matplotlib.rcParams['grid.linestyle']] = value
        self.set_grid()

    def get_linestyle (self) -> str:
        return linestyle_lib[matplotlib.rcParams['grid.linestyle']].lower()

    def set_color(self, color):
        matplotlib.rcParams['grid.color'] = color
        self.set_grid()
       
    def get_color(self) -> str:
        return matplotlib.rcParams['grid.color']


class Pane(Frame):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)
        self.canvas = canvas

        layout.addWidget(TitleLabel('Pane'))
        layout.addWidget(SeparateHLine())

        self.visible = Toggle(text='Visible',text2='Whether to show the color')
        layout.addWidget(self.visible)
        self.visible.button.checkedChanged.connect(self.set_visible)
        self.visible.button.setChecked(self.get_visible())

        self.facecolor = ColorDropdown(text='Color',text2='Set the color of the Pane',
                                       color=self.get_color())
        self.facecolor.button.colorChanged.connect(self.set_color)
        layout.addWidget(self.facecolor)

        self.alpha = Slider(text='Transparency',text2='Set the transparency of the Pane')
        self.alpha.button.valueChanged.connect(self.set_patch_alpha)
        self.alpha.button.setValue(self.get_patch_alpha())
        layout.addWidget(self.alpha)
    
    def set_visible(self,value):
        self.canvas.axes.patch.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible(self):
        return self.canvas.axes.patch.get_visible()
    
    def set_color(self, color):
        self.canvas.axes.patch.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        try: return self.canvas.axes.patch.get_color()
        except: return matplotlib.rcParams['axes.facecolor']

    def set_patch_alpha (self, value):
        self.canvas.axes.patch.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_patch_alpha (self):
        if self.canvas.axes.patch.get_alpha() != None: return int(self.canvas.axes.patch.get_alpha()*100)
        else: return 100

class Grid3D (QScrollArea):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        widget = QWidget()
        self.vlayout = QVBoxLayout()
        #layout.setContentsMargins(10,0,10,15)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        widget.setLayout(self.vlayout)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.verticalScrollBar().setValue(1900)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.first_show = True
        self.canvas = canvas
        
 
    def showEvent(self, a0):
        if self.first_show:
            self.diag = ProgressDialog("Waiting", None, self.parent())
            self.diag.progressbar._setValue(0)
            self.diag.show()
            QApplication.processEvents()

            self.plotsize = PlotSize2D(self.canvas, self.parent())
            self.vlayout.addWidget(self.plotsize)

            self.diag.progressbar._setValue(20)
            QApplication.processEvents()

            # self.pane = Pane(self.canvas, self.parent())
            # self.vlayout.addWidget(self.pane)

            # self.diag.progressbar._setValue(60)
            # QApplication.processEvents()
            
            # self.grid = Grid2D(self.canvas,self.parent())
            # self.vlayout.addWidget(self.grid)

            # self.diag.progressbar._setValue(100)
            # QApplication.processEvents()

            self.diag.close()

            self.first_show = False

        return super().showEvent(a0)



