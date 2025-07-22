from PySide6.QtWidgets import  QVBoxLayout, QStackedLayout, QDialog, QSizePolicy
from ui.base_widgets.button import HTransparentComboBox, HToggle, SegmentedWidget
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.frame import ScrollArea, SeparateHLine
from ui.base_widgets.text import TitleLabel
from plot.label.base import FontStyle
from plot.tick.tick_2d import TickBase2
from config.settings import logger, marker_lib, linestyle_lib, font_lib
from matplotlib import ticker, lines, colors, rcParams
from matplotlib.axis import Axis
from plot.canvas import Canvas

DEBUG = False

class TickBase(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_obj()

        self.initUI()
    
    def initUI(self):
        
        visible = HToggle(
            label  = "Visible",
            label2 = f"Toggle {self.axis} ticks' visibility",
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        self.min = HLineEdit(
            label  = "Min Value",
            label2 = f"Set {self.axis} axis view minimum",
            setter=self.set_min,
            getter=self.get_min,
            layout=self.vlayout
        )

        self.max = HLineEdit(
            label  = 'Max Value',
            label2 = f"Set {self.axis} axis view maximum",
            setter=self.set_max,
            getter=self.get_max,
            layout=self.vlayout
        )

        scale = HTransparentComboBox(
            items = ['linear','log','symlog','logit','asinh'],
            label  = 'Scale',
            label2 = f"Set {self.axis} axis' scale",
            setter=self.set_scale,
            getter=self.get_scale,
            layout=self.vlayout
        )

    def find_obj(self) -> Axis:
        return self.canvas.figure.findobj(
            lambda a: isinstance(a, Axis) and a.get_gid() \
            and a.get_gid() == self.axis
        )[0]
    
    def set_visible(self, value):
        try:
            for line in self.obj.get_ticklines():
                line.set_alpha(value)
        except Exception as e: logger.exception(e)
        self.canvas.draw_idle()
    
    def get_visible(self):
        if self.obj.get_ticklines()[0].get_alpha(): return True
        elif self.obj.get_ticklines()[0].get_alpha() == None: return True
        return False

    def set_min(self, value):
       
        value = None if value == "" else value
        
        try:
            if self.axis == "x3d":
                self.obj.axes.set_xlim(left=float(value))
            elif self.axis == "y3d":
                self.obj.axes.set_ylim(bottom=float(value))
            elif self.axis == "z3d":
                self.obj.axes.set_zlim(bottom=float(value))
        except Exception as e: logger.exception(e)
        
        self.canvas.draw_idle()
    
    def set_max (self, value):
        value = None if value == "" else value
        try:
            if self.axis == 'x3d':
                self.obj.axes.set_xlim(right=float(value))
            elif self.axis == "y3d":
                self.obj.axes.set_ylim(top=float(value))
            elif self.axis == "z3d":
                self.obj.axes.set_zlim(top=float(value))
        except Exception as e: logger.exception(e)

        self.canvas.draw_idle()
    
    def get_min(self):
        if self.axis == "x3d": return str(round(self.obj.axes.get_xlim()[0],5))
        elif self.axis == "y3d": return str(round(self.obj.axes.get_ylim()[0],5))
        elif self.axis == "z3d": return str(round(self.obj.axes.get_zlim()[0],5))

    def get_max(self):
        if self.axis == "x3d": return str(round(self.obj.axes.get_xlim()[1],5))
        elif self.axis == "y3d": return str(round(self.obj.axes.get_ylim()[1],5))
        elif self.axis == "z3d": return str(round(self.obj.axes.get_zlim()[1],5))
    
    def set_scale (self, value:str):
        try:
            if self.axis == "x3d": self.obj.axes.set_xscale(value)
            elif self.axis == "y3d": self.obj.axes.set_yscale(value)
            elif self.axis == "z3d": self.obj.axes.set_zscale(value)
            
        except Exception as e: logger.exception(e)
        self.canvas.draw_idle()
    
    def get_scale (self):
        if self.axis == "x3d": return self.obj.axes.get_xscale()
        elif self.axis == "y3d": return self.obj.axes.get_yscale()
        elif self.axis == "z3d": return self.obj.axes.get_zscale()

class SpineBase(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_object()

        self.initUI()

    def initUI(self):
        
        visible = HToggle(
            label='Spine visible',
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        arrow = HTransparentComboBox(
            label  = 'Arrow Style',
            items = marker_lib.values(),
            setter=self.set_arrow,
            getter=self.get_arrow,
            layout=self.vlayout
        )

        color = HColorDropdown(
            label='Spine color',
            setter=self.set_color,
            getter=self.get_color,
            layout=self.vlayout
        )
        
        arrowcolor = HColorDropdown(
            label="Arrow color",
            setter=self.set_arrowcolor,
            getter=self.get_arrowcolor,
            layout=self.vlayout
        )

        alpha = HTransparentDoubleSpinBox(
            label ='Transparent',
            minimum = 0, maximum = 100, singleStep = 10,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )

        linestyle = HTransparentComboBox(
            label  = 'Line style',
            items = linestyle_lib.values(),
            setter=self.set_linestyle,
            getter=self.get_linestyle,
            layout=self.vlayout
        )

        linewidth = HTransparentDoubleSpinBox(
            label = 'Line width',
            minimum = 0, maximum = 20, singleStep = 0.5,
            setter=self.set_linewidth,
            getter=self.get_linewidth,
            layout=self.vlayout
        )

    def find_object (self) -> lines.Line2D:
        return self.canvas.figure.findobj(
            lambda a: isinstance(a, Axis) and a.get_gid() \
            and a.get_gid() == self.axis
        )[0].line
    
    def set_visible (self, value:bool):
        self.obj.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible (self):
        return self.obj.get_visible()  

    def set_arrow(self, marker):
        try:
            marker = list(marker_lib.keys())[list(marker_lib.values()).index(marker.lower())]
            self.obj.set_marker(marker)
            self.obj.set_markevery((1,1))
        except Exception as e:
            logger.exception(e)
        self.canvas.draw_idle()
    
    def get_arrow(self):
        return marker_lib[self.obj.get_marker()]
    
    def set_alpha (self, value):
        self.obj.set_alpha(float(value/100))
        self.canvas.draw_idle()
    
    def get_alpha(self):
        if self.obj.get_alpha() == None:
            return 100
        return self.obj.get_alpha()*100
    
    def set_linestyle(self, value):
        self.obj.set_linestyle(value)
        self.canvas.draw_idle()
    
    def get_linestyle(self):
        return linestyle_lib[self.obj.get_linestyle()]

    def set_linewidth(self, value):
        self.obj.set_linewidth(value)
        self.canvas.draw_idle()
    
    def get_linewidth (self):
        return self.obj.get_linewidth()

    def set_color(self, color):
        self.obj.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        return colors.rgb2hex(self.obj.get_color())

    def set_arrowcolor(self, color):
        self.obj.set_markerfacecolor(color)
        self.canvas.draw_idle()
    
    def get_arrowcolor(self):
        return colors.rgb2hex(self.obj.get_markerfacecolor())

class AxisLabel(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas
        self.axis = axis
        self.ax = self.find_axis()
        self.text = self.ax.get_label()

        self.initUI()
    
    def initUI(self):

        label = HLineEdit(
            label='Label',
            getter=self.get_label,
            setter=self.set_label,
            layout=self.vlayout
        )
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        font = HTransparentComboBox(
            items = font_lib,
            label  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=self.vlayout
        )

        size = HTransparentDoubleSpinBox(
            label = 'Font size',
            minimum = 1, maximum = 100, singleStep = 1,
            setter=self.set_fontsize,
            getter=self.get_fontsize,
            layout=self.vlayout
        )

        style = FontStyle(
            obj = [self.text], 
            canvas = self.canvas,
            layout=self.vlayout
        )

        color = HColorDropdown(
            label  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.backgroundcolor = HColorDropdown(
            label  = 'Background color',
            getter=self.get_backgroundcolor,
            setter=self.set_backgroundcolor,
            layout=self.vlayout
        )

        edgecolor = HColorDropdown(
            label  = 'Edge color',
            getter=self.get_edgecolor,
            setter=self.set_edgecolor,
            layout=self.vlayout
        )

        alpha = HTransparentDoubleSpinBox(
            label = 'Transparency',
            singleStep = 10, maximum = 100, minimum = 0,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )
    
    def find_axis(self) -> Axis:
        return self.canvas.figure.findobj(
            lambda a: isinstance(a, Axis) and a.get_gid() \
            and a.get_gid() == self.axis
        )[0]
    
    def set_label(self, value:str):
        self.ax.set_label_text(value)
        self.canvas.draw_idle()
    
    def get_label(self) -> str:
        return self.ax.get_label_text()

    def set_fontname (self, font:str):
        self.text.set_fontfamily(font)
        self.canvas.draw_idle()
    
    def get_fontname(self):
        return self.text.get_fontname()
    
    def set_fontsize(self, value):
        self.text.set_fontsize(value)
        self.canvas.draw_idle()
    
    def get_fontsize(self):
        return self.text.get_fontsize()
    
    def set_color (self, color):
        self.text.set_color(color)
        self.canvas.draw_idle()
    
    def get_color (self):
        return self.text.get_color()

    def set_backgroundcolor (self, color):
        self.text.set_backgroundcolor(color)
        self.canvas.draw_idle()
    
    def get_backgroundcolor(self):
        if self.text.get_bbox_patch() != None:
            return self.text.get_bbox_patch().get_facecolor()
        return 'white'
    
    def set_edgecolor (self, color):
        self.text.set_bbox({"edgecolor":color,
                           "facecolor":self.backgroundcolor.button.color.name()})
        self.canvas.draw_idle()
    
    def get_edgecolor(self):
        if self.text.get_bbox_patch() != None:
            return self.text.get_bbox_patch().get_edgecolor()
        return 'white'
    
    def set_alpha (self, value):
        self.text.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_alpha (self):
        if self.text.get_alpha() != None:
            return int(self.text.get_alpha()*100)
        return 100
    
class Tick3D(QDialog):
    def __init__(self, axis:str, canvas:Canvas, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(f'{axis.title()} Axis')
        layout = QVBoxLayout(self)
        self.canvas = canvas

        self.choose_axis = SegmentedWidget(parent)
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='General', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Major', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Spine', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.choose_axis.addButton(text='Label', func=lambda: self.stackedlayout.setCurrentIndex(3))

        self.choose_axis.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)
        
        base = TickBase(axis, canvas, parent)
        self.stackedlayout.addWidget(base)

        ticks = TickBase2(axis, 'major', canvas, parent)
        self.stackedlayout.addWidget(ticks)

        spine = SpineBase(axis, canvas, parent)
        self.stackedlayout.addWidget(spine)

        label = AxisLabel(axis, canvas, parent)
        self.stackedlayout.addWidget(label)