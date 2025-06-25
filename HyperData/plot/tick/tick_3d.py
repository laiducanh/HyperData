from PySide6.QtWidgets import  QVBoxLayout, QStackedLayout, QDialog, QSizePolicy
from ui.base_widgets.button import TransparentComboBox, Toggle, SegmentedWidget
from ui.base_widgets.spinbox import TransparentDoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.frame import ScrollArea
from plot.utilis import find_mpl_object
from plot.label.base import FontStyle
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
        
        visible = Toggle(
            text  = "Visible",
            text2 = f"Toggle {self.axis} ticks' visibility",
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        self.min = LineEdit(
            text  = "Min Value",
            text2 = f"Set {self.axis} axis view minimum",
            setter=self.set_min,
            getter=self.get_min,
            layout=self.vlayout
        )

        self.max = LineEdit(
            text  = 'Max Value',
            text2 = f"Set {self.axis} axis view maximum",
            setter=self.set_max,
            getter=self.get_max,
            layout=self.vlayout
        )

        scale = TransparentComboBox(
            items = ['linear','log','symlog','logit','asinh'],
            text  = 'Scale',
            text2 = f"Set {self.axis} axis' scale",
            setter=self.set_scale,
            getter=self.get_scale,
            layout=self.vlayout
        )

    def find_obj(self) -> Axis:
        return find_mpl_object(self.canvas.figure, match=[Axis], gid=self.axis)[0]
    
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

class TickBase2(TickBase):
    def __init__(self, axis:str, type:str, canvas:Canvas, parent=None):

        self.ticktype = type

        super().__init__(axis, canvas, parent)
    
    def initUI(self):

        self.ticklocator = TransparentComboBox(
            items=['Auto', 'Tick Interval','Tick Values', 'None'],
            text='Type',
            setter=self.set_ticklocator,
            getter=self.get_ticklocator,
            layout=self.vlayout
        )

        self.value = LineEdit(
            text='Tick values',
            text2=f"Set {self.axis} axis' tick positions",
            setter=self.set_ticklocator,
            getter=self.get_tickvalues,
            layout=self.vlayout
        )

        self.label = Toggle(
            text='Label',
            text2=f"Toggle {self.axis} axis' {self.ticktype} tick label",
            getter=self.get_label,
            setter=self.set_label,
            layout=self.vlayout
        )

        tick_position = TransparentComboBox(
            items = ["lower","upper","both"], 
            text  = "Tick position",
            getter=self.get_tick_position,
            setter=self.set_tick_position,
            layout=self.vlayout
        )

        tick_labelsize = TransparentDoubleSpinBox(
            text  = 'Label size',
            text2 = f"Set {self.axis} axis' {self.ticktype} tick label size",
            min = 1, max = 100, step = 1,
            setter=self.set_labelsize,
            getter=self.get_labelsize,
            layout=self.vlayout
        )

        tick_labelcolor = ColorDropdown(
            text  = 'Label color', 
            setter=self.set_labelcolor,
            getter=self.get_labelcolor,
            layout=self.vlayout
        )

        tickcolor = ColorDropdown(
            text  = 'Tick color', 
            getter=self.get_tickcolor,
            setter=self.set_tickcolor,
            layout=self.vlayout
        )

        tick_rotation = TransparentDoubleSpinBox(
            text = 'Tick label rotation',
            min = -180, max = 180, step = 10,
            setter=self.set_labelrotation,
            getter=self.get_labelrotation,
            layout=self.vlayout
        )

        tick_labelpad = TransparentDoubleSpinBox(
            text = 'Tick labelpad',
            min = 0, max = 50, step = 0.5,
            setter=self.set_tickpadding,
            getter=self.get_tickpadding,
            layout=self.vlayout
        )
    
    def set_ticklocator(self):
        try:
            locator = self.ticklocator.button.currentText()
            if locator == 'Auto':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.AutoLocator())
                    self.obj.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:g}"))
                else:
                    self.obj.set_minor_locator(ticker.AutoMinorLocator())
                    self.obj.set_minor_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:g}"))
            elif locator == 'Tick Interval':
                value = float(self.value.button.text())
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.MultipleLocator(value))
                    self.obj.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:g}"))
                else:
                    self.obj.set_minor_locator(ticker.MultipleLocator(value))
                    self.obj.set_minor_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:g}"))
            elif locator == 'Tick Values':
                value = [float(i) for i in self.value.button.text().split(',')]
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.FixedLocator(value))
                    self.obj.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:g}"))
                else:
                    self.obj.set_minor_locator(ticker.FixedLocator(value))
                    self.obj.set_minor_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:g}"))
            elif locator == 'None':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.NullLocator())
                    self.obj.set_major_formatter(ticker.NullFormatter())
                else:
                    self.obj.set_minor_locator(ticker.NullLocator())
                    self.obj.set_minor_formatter(ticker.NullFormatter())            
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)

    def get_ticklocator(self) -> str:
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
           
            if isinstance(locator, (ticker.AutoLocator, ticker.AutoMinorLocator)):
                return 'Auto'
            elif isinstance(locator, ticker.MultipleLocator):
                return 'Tick Interval'
            elif isinstance(locator, ticker.FixedLocator):
                return 'Tick Values'
            elif isinstance(locator, ticker.NullLocator):
                return 'None'
        except Exception as e:
            logger.exception(e)
    
    def get_tickvalues(self):
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
            
            if isinstance(locator, (ticker.AutoLocator, ticker.AutoMinorLocator)):
                return
            elif isinstance(locator, ticker.MultipleLocator):
                return str(locator._edge.step)
            elif isinstance(locator, ticker.FixedLocator):
                return ', '.join(str(x) for x in locator.locs)
            elif isinstance(locator, ticker.NullLocator):
                return 
        except Exception as e:
            logger.exception(e)
    
    def set_label(self, value:bool):
        try:
            self.obj.set_tick_params(which=self.ticktype, labelleft=value)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)
    
    def get_label(self) -> bool:
        return self.obj.get_tick_params(which=self.ticktype)['labelleft']

    def set_tick_position(self, value):
        self.obj.set_ticks_position(value)
        self.canvas.draw_idle()
    
    def get_tick_position(self):
        return self.obj.get_ticks_position()
    
    def set_labelsize (self,value):
        self.obj.set_tick_params(which=self.ticktype,labelsize=value)
        self.canvas.draw_idle()
    
    def get_labelsize (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_majorticklabels()[0].get_fontsize()
            else: 
                return self.obj.get_minorticklabels()[0].get_fontsize() 
        except: return self.obj.get_majorticklabels()[0].get_fontsize()
    
    def set_labelcolor(self, color):
        self.obj.set_tick_params(which=self.ticktype,labelcolor=color)
        self.canvas.draw_idle()
    
    def get_labelcolor(self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_majorticklabels()[0].get_color()
            else: 
                return self.obj.get_minorticklabels()[0].get_color()
        except: return self.get_tickcolor()

    def set_tickcolor(self, color):
        self.obj.set_tick_params(which=self.ticktype,color=color)
        self.canvas.draw_idle()
    
    def get_tickcolor(self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_majorticklines()[0].get_color()
            else: 
                return self.obj.get_minorticklines()[0].get_color()
        except: return rcParams['xtick.color']
    
    def set_labelrotation (self,value):
        self.obj.set_tick_params(which=self.ticktype,labelrotation=value)
        self.canvas.draw_idle()
    
    def get_labelrotation (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_majorticklabels()[0].get_rotation()
            else: 
                return self.obj.get_minorticklabels()[0].get_rotation()
        except: return 0
    
    def set_tickpadding (self,value):
        self.obj.set_tick_params(which=self.ticktype,pad=value)
        self.canvas.draw_idle()
    
    def get_tickpadding (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_major_ticks()[0].get_tick_padding()
            else: 
                return self.obj.get_minor_ticks()[0].get_tick_padding()
        except: return rcParams[f'xtick.{self.ticktype}.pad']

class SpineBase(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_object()

        self.initUI()

    def initUI(self):
        
        visible = Toggle(
            text='Spine visible',
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        arrow = TransparentComboBox(
            text  = 'Arrow Style',
            items = marker_lib.values(),
            setter=self.set_arrow,
            getter=self.get_arrow,
            layout=self.vlayout
        )

        color = ColorDropdown(
            text='Spine color',
            setter=self.set_color,
            getter=self.get_color,
            layout=self.vlayout
        )
        
        arrowcolor = ColorDropdown(
            text="Arrow color",
            setter=self.set_arrowcolor,
            getter=self.get_arrowcolor,
            layout=self.vlayout
        )

        alpha = TransparentDoubleSpinBox(
            text ='Transparent',
            min = 0, max = 100, step = 10,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )

        linestyle = TransparentComboBox(
            text  = 'Line style',
            items = linestyle_lib.values(),
            setter=self.set_linestyle,
            getter=self.get_linestyle,
            layout=self.vlayout
        )

        linewidth = TransparentDoubleSpinBox(
            text = 'Line width',
            min = 0, max = 20, step = 0.5,
            setter=self.set_linewidth,
            getter=self.get_linewidth,
            layout=self.vlayout
        )

    def find_object (self) -> lines.Line2D:
        return find_mpl_object(
            self.canvas.figure, 
            match=[Axis], 
            gid=self.axis
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
        return self.obj.get_linestyle()

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

        label = LineEdit(
            text='Label',
            getter=self.get_label,
            setter=self.set_label,
            layout=self.vlayout
        )
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        font = TransparentComboBox(
            items = font_lib,
            text  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=self.vlayout
        )

        size = TransparentDoubleSpinBox(
            text = 'Font size',
            min = 1, max = 100, step = 1,
            setter=self.set_fontsize,
            getter=self.get_fontsize,
            layout=self.vlayout
        )

        style = FontStyle(
            obj = [self.text], 
            canvas = self.canvas,
            layout=self.vlayout
        )

        color = ColorDropdown(
            text  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.backgroundcolor = ColorDropdown(
            text  = 'Background color',
            getter=self.get_backgroundcolor,
            setter=self.set_backgroundcolor,
            layout=self.vlayout
        )

        edgecolor = ColorDropdown(
            text  = 'Edge color',
            getter=self.get_edgecolor,
            setter=self.set_edgecolor,
            layout=self.vlayout
        )

        alpha = TransparentDoubleSpinBox(
            text = 'Transparency',
            step = 10,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )
    
    def find_axis(self) -> Axis:
        return find_mpl_object(self.canvas.figure,[Axis], self.axis)[0]
    
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