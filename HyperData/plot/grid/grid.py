from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import Slider, DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine, Frame
from plot.canvas import Canvas
import matplotlib
from config.settings import linestyle_lib

class PlotSize2D (Frame):
    def __init__(self, canvas:Canvas):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        #layout.setContentsMargins(0,0,0,0)
        self.canvas = canvas

        layout.addWidget(TitleLabel('Figure Margin'))
        layout.addWidget(SeparateHLine())

        top = DoubleSpinBox(text='margin top',min=0,max=1,step=0.05)
        top.button.valueChanged.connect(self.set_top)
        top.button.setValue(self.get_top())
        layout.addWidget(top)

        bottom = DoubleSpinBox(text='margin bottom',min=0,max=1,step=0.05)
        bottom.button.valueChanged.connect(self.set_bottom)
        bottom.button.setValue(self.get_bottom())
        layout.addWidget(bottom)

        left = DoubleSpinBox(text='margin left',min=0,max=1,step=0.05)
        left.button.valueChanged.connect(self.set_left)
        left.button.setValue(self.get_left())
        layout.addWidget(left)

        right = DoubleSpinBox(text='margin right',min=0,max=1,step=0.05)
        right.button.valueChanged.connect(self.set_right)
        right.button.setValue(self.get_right())
        layout.addWidget(right)
        #layout.addStretch()
    
    def set_top(self,value):
        self.canvas.fig.subplots_adjust(top=value)
        self.canvas.draw()
    
    def get_top(self):
        return self.canvas.fig.subplotpars.top
    
    def set_bottom(self,value):
        self.canvas.fig.subplots_adjust(bottom=value)
        self.canvas.draw()
    
    def get_bottom(self):
        return self.canvas.fig.subplotpars.bottom
    
    def set_left(self,value):
        self.canvas.fig.subplots_adjust(left=value)
        self.canvas.draw()
    
    def get_left(self):
        return self.canvas.fig.subplotpars.left
    
    def set_right(self,value):
        self.canvas.fig.subplots_adjust(right=value)
        self.canvas.draw()
    
    def get_right(self):
        return self.canvas.fig.subplotpars.right

    
class Grid2D (Frame):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        #layout.setContentsMargins(0,0,0,0)
        self.canvas = canvas

        layout.addWidget(TitleLabel('Grid'))
        layout.addWidget(SeparateHLine())

        self.visible = Toggle(text='visible')
        layout.addWidget(self.visible)
        self.visible.button.checkedChanged.connect(self.set_grid)
        self.visible.button.setChecked(self.get_visible())

        self.type = ComboBox(items=['Major','Minor','Both'],text='Type')
        self.type.button.currentTextChanged.connect(self.set_grid)
        self.type.button.setCurrentText(self.get_gridtype())
        layout.addWidget(self.type)

        self.axis = ComboBox(text='axis',items=['X','Y','Both'])
        self.axis.button.currentTextChanged.connect(self.set_grid)
        self.axis.button.setCurrentText(self.get_gridaxis())
        layout.addWidget(self.axis)

        self.color = ColorDropdown(text='line color',color=self.get_color())
        self.color.button.colorChanged.connect(self.set_grid)
        self.color.button.setColor(self.get_color())
        layout.addWidget(self.color)

        self.linewidth = DoubleSpinBox(text='line width',min=0.1,max=10,step=0.5)
        self.linewidth.button.valueChanged.connect(self.set_grid)
        self.linewidth.button.setValue(self.get_linewidth())
        layout.addWidget(self.linewidth)

        self.linestyle = ComboBox(text='line style',items=linestyle_lib.values())
        self.linestyle.button.currentTextChanged.connect(self.set_grid)
        self.linestyle.button.setCurrentText(self.get_linestyle())
        layout.addWidget(self.linestyle)

        self.transparency = Slider(text='grid transparency')
        self.transparency.button.valueChanged.connect(self.set_grid)
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
                                    linestyle=linestyle, color=color,
                                    gid = f'_grid.{which}.{axis}.{alpha}.{linewidth}.{linestyle}.{color}',
                                    )
            self.canvas.draw()
        except: pass
    
    def get_visible(self):
        for obj in self.canvas.fig.findobj(match=matplotlib.lines.Line2D):
            if obj._gid != None and '_grid' in obj._gid:
                return obj.get_visible()
        return False
    
    def get_gridtype (self):
        for obj in self.canvas.fig.findobj(match=matplotlib.lines.Line2D):
            if obj._gid != None and obj._gid == '_grid':
                return obj._gid.split('.')[1].title()
        return matplotlib.rcParams['axes.grid.which'].title()
    
    def get_gridaxis (self):
        for obj in self.canvas.fig.findobj(match=matplotlib.lines.Line2D):
            if obj._gid != None and obj._gid == '_grid':
                return obj._gid.split('.')[2].title()
        return matplotlib.rcParams['axes.grid.axis'].title()

    def get_alpha(self):
        for obj in self.canvas.fig.findobj(match=matplotlib.lines.Line2D):
            if obj._gid != None and obj._gid == '_grid':
                return int(obj._gid.split('.')[3]*100)
        return int(matplotlib.rcParams['grid.alpha']*100)
    
    def get_linewidth(self):
        for obj in self.canvas.fig.findobj(match=matplotlib.lines.Line2D):
            if obj._gid != None and obj._gid == '_grid':
                return obj._gid.split('.')[4]
        return matplotlib.rcParams['grid.linewidth']

    def get_linestyle (self):
        for obj in self.canvas.fig.findobj(match=matplotlib.lines.Line2D):
            if obj._gid != None and obj._gid == '_grid':
                return obj._gid.split('.')[5].title()
        return linestyle_lib[matplotlib.lines._get_dash_pattern(matplotlib.rcParams['grid.linestyle'])].lower()

    def get_color(self):
        for obj in self.canvas.fig.findobj(match=matplotlib.lines.Line2D):
            if obj._gid != None and obj._gid == '_grid':
                return obj._gid.split('.')[6]
        return matplotlib.rcParams['grid.color']


class Pane(Frame):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        #layout.setContentsMargins(0,0,0,0)
        self.canvas = canvas

        layout.addWidget(TitleLabel('Pane'))
        layout.addWidget(SeparateHLine())

        self.visible = Toggle(text='visible')
        layout.addWidget(self.visible)
        self.visible.button.checkedChanged.connect(self.set_visible)
        self.visible.button.setChecked(self.get_visible())

        self.facecolor = ColorDropdown(text='pane color',color=self.get_color())
        self.facecolor.button.colorChanged.connect(self.set_color)
        layout.addWidget(self.facecolor)

        self.alpha = Slider(text='axes transparency')
        self.alpha.button.valueChanged.connect(self.set_patch_alpha)
        self.alpha.button.setValue(self.get_patch_alpha())
        layout.addWidget(self.alpha)
    
    def set_visible(self,value):
        self.canvas.axes.patch.set_visible(value)
        self.canvas.draw()
    
    def get_visible(self):
        return self.canvas.axes.patch.get_visible()
    
    def set_color(self, color):
        self.canvas.axes.patch.set_color(color)
        self.canvas.draw()
    
    def get_color(self):
        try: return self.canvas.axes.patch.get_color()
        except: return matplotlib.rcParams['axes.facecolor']

    def set_patch_alpha (self, value):
        self.canvas.axes.patch.set_alpha(value/100)
        self.canvas.draw()
    
    def get_patch_alpha (self):
        if self.canvas.axes.patch.get_alpha() != None: return int(self.canvas.axes.patch.get_alpha()*100)
        else: return 100

class Grid (QScrollArea):
    def __init__(self, canvas:Canvas,parent=None):
        super().__init__(parent)

        widget = QWidget()
        layout = QVBoxLayout()
        #layout.setContentsMargins(10,0,10,15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        widget.setLayout(layout)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.verticalScrollBar().setValue(1900)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        
        self.plotsize = PlotSize2D(canvas)
        layout.addWidget(self.plotsize)

        self.pane = Pane(canvas)
        layout.addWidget(self.pane)
        
        self.grid = Grid2D(canvas,parent)
        layout.addWidget(self.grid)
 




