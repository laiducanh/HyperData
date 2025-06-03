from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QStackedLayout, QDialog, QSizePolicy
from ui.base_widgets.button import ComboBox, Toggle, SegmentedWidget
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.line_edit import LineEdit
from plot.utilis import find_mpl_object
from plot.label.base import FontStyle
from config.settings import logger, marker_lib, linestyle_lib, font_lib
from matplotlib import ticker, spines, lines, colors, rcParams
from matplotlib.axis import Axis
from typing import Union
from plot.canvas import Canvas

DEBUG = False

class TickBase (QWidget):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_obj()

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)

        visible = Toggle(
            text  = "Visible",
            text2 = f"Toggle {self.axis} ticks' visibility"
        )
        visible.button.checkedChanged.connect(self.set_visible)
        visible.button.setChecked(self.get_visible())
        layout.addWidget(visible)

        self.min = LineEdit(
            text  = "Min Value",
            text2 = f"Set {self.axis} axis view minimum"
        )
        self.min.button.setFixedWidth(150)
        self.min.button.textChanged.connect(self.set_min)
        self.min.button.setText(str(round(self.get_lim()[0],5)))
        layout.addWidget(self.min)

        self.max = LineEdit(
            text  = 'Max Value',
            text2 = f"Set {self.axis} axis view maximum"
        )
        self.max.button.setFixedWidth(150)
        self.max.button.textChanged.connect(self.set_max)
        self.max.button.setText(str(round(self.get_lim()[1],5)))
        layout.addWidget(self.max)

        scale = ComboBox(
            items = ['linear','log','symlog','logit','asinh'],
            text  = 'Scale',
            text2 = f"Set {self.axis} axis' scale"
        )
        scale.button.currentTextChanged.connect(self.set_scale)
        scale.button.setCurrentText(self.get_scale())
        layout.addWidget(scale)

    def find_obj(self) -> Axis:
        return find_mpl_object(self.canvas.fig, match=[Axis], gid=self.axis)[0]
    
    def set_visible(self, value):
        self.obj.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible(self):
        return self.obj.get_visible()

    def set_min(self, value):
        value = None if value == "" else value
        try:
            if self.axis in ['bottom','top']:
                self.obj.axes.set_xlim(left=float(value))
            else:
                self.obj.axes.set_ylim(bottom=float(value))
        except Exception as e: logger.exception(e)
        
        self.canvas.draw_idle()
    
    def set_max (self, value):
        value = None if value == "" else value
        try:
            if self.axis in ['bottom','top']:
                self.obj.axes.set_xlim(right=float(value))
            else:
                self.obj.axes.set_ylim(top=float(value))
        except Exception as e: logger.exception(e)

        self.canvas.draw_idle()

    def get_lim(self):
        
        if self.axis in ['bottom','top']: return self.obj.axes.get_xlim()
        else: return self.obj.axes.get_ylim()
    
    def set_scale (self, value:str):
        try:
            if self.axis in ['bottom','top']: self.obj.axes.set_xscale(value)
            else: self.obj.axes.set_yscale(value)
            self.canvas.draw_idle()
        except Exception as e: logger.exception(e)
    
    def get_scale (self):
        if self.axis in ['bottom','top']: return self.obj.axes.get_xscale()
        else: return self.obj.axes.get_yscale()

class TickBase2 (TickBase):
    def __init__(self, axis:str, type:str, canvas: Canvas, parent=None):

        self.ticktype = type

        super().__init__(axis, canvas, parent)

    def initUI(self):

        layout = QVBoxLayout(self)

        self.tickinterval = ComboBox(
            items = ['Tick Interval','Tick Values'],
            text  = 'Type' 
        )
        self.tickinterval.button.setCurrentText('Tick Interval')
        self.tickinterval.button.currentTextChanged.connect(self.set_tickvalues)
        layout.addWidget(self.tickinterval)

        self.value = LineEdit(
            text = 'Tick values'
        )
        self.value.button.textChanged.connect(self.set_tickvalues)
        layout.addWidget(self.value)

        self.tick_label = LineEdit(
            text  = 'Tick labels',
            text2 = f"Set {self.axis} axis' {self.ticktype} tick labels"
        )
        self.tick_label.button.textChanged.connect(self.set_ticklabels)
        self.tick_label.button.setPlaceholderText(self.get_ticklabels())
        layout.addWidget(self.tick_label)

        tick_labelsize = DoubleSpinBox(
            text  = 'Label size',
            text2 = f"Set {self.axis} axis' {self.ticktype} tick label size",
            min = 1, max = 100, step = 1
        )
        tick_labelsize.button.valueChanged.connect(self.set_labelsize)
        tick_labelsize.button.setValue(self.get_labelsize())
        layout.addWidget(tick_labelsize)

        tick_direction = ComboBox(
            text  = 'Tick direction',
            text2 = f"Put {self.ticktype}ticks inside/outside {self.axis} axis, or both",
            items = ['In','Out','InOut']
        )
        tick_direction.button.currentTextChanged.connect(self.set_tickdir)
        tick_direction.button.setCurrentText(self.get_tickdir())
        layout.addWidget(tick_direction)

        tick_labelcolor = ColorDropdown(
            text  = 'Label color', 
            color = self.get_labelcolor()
        )
        tick_labelcolor.button.colorChanged.connect(self.set_labelcolor)
        layout.addWidget(tick_labelcolor)

        tickcolor = ColorDropdown(
            text  = 'Tick color', 
            color = self.get_tickcolor()
        )
        tickcolor.button.colorChanged.connect(self.set_tickcolor)
        layout.addWidget(tickcolor)

        tick_rotation = DoubleSpinBox(
            text = 'Tick label rotation',
            min = -180, max = 180, step = 10
        )
        tick_rotation.button.valueChanged.connect(self.set_labelrotation)
        tick_rotation.button.setValue(self.get_labelrotation())
        layout.addWidget(tick_rotation)

        tick_labelpad = DoubleSpinBox(
            text = 'Tick labelpad',
            min = 0, max = 50, step = 0.5
        )
        tick_labelpad.button.valueChanged.connect(self.set_tickpadding)
        tick_labelpad.button.setValue(self.get_tickpadding())
        layout.addWidget(tick_labelpad)

        tick_length = DoubleSpinBox(
            text = 'Tick length',
            min = 0, max = 50, step = 0.5
        )
        tick_length.button.valueChanged.connect(self.set_ticklength)
        tick_length.button.setValue(self.get_ticklength())
        layout.addWidget(tick_length)

        tick_width = DoubleSpinBox(
            text = 'Tick width',
            min = 0, max = 50, step = 0.5
        )
        tick_width.button.valueChanged.connect(self.set_tickwidth)
        tick_width.button.setValue(self.get_tickwidth())
        layout.addWidget(tick_width)
    
    def set_tickvalues (self, value:str):
        try:
            if self.tickinterval.button.currentText() == 'Tick Interval':
                if self.ticktype == 'major': 
                    self.obj.set_major_locator(ticker.MultipleLocator(float(value)))
                else: 
                    self.obj.set_minor_locator(ticker.MultipleLocator(float(value)))
            else:
                value = [float(i) for i in value.split(',')]
                if self.ticktype == 'major': 
                    self.obj.set_ticks(value)
                else: 
                    self.obj.set_ticks(value,minor=True)
            self.canvas.draw_idle()
        except Exception as e: logger.exception(e)
    
    def set_ticklabels (self, value:str):
        try:
            value = value.split(',')
            if self.ticktype == 'major': self.obj.set_ticklabels(value)
            else: self.obj.set_ticklabels(value,minor=True)
            self.canvas.draw_idle()
        except Exception as e: logger.exception(e)
    
    def get_ticklabels(self):
        
        label_list = list()
        if self.ticktype == 'major':
            label_list = [i.get_text() for i in self.obj.get_majorticklabels()]

        else:
            label_list = [i.get_text() for i in self.obj.get_minorticklabels()]
            
        return ", ".join(label_list)
    
    def set_labelsize (self,value):
        self.obj.set_tick_params(which=self.ticktype,labelsize=value)
        self.canvas.draw_idle()
    
    def get_labelsize (self):
        if self.ticktype == 'major': return self.obj.get_majorticklabels()[0].get_fontsize()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_fontsize() 
            except: return 7
        
    def set_tickdir (self,value):
        self.obj.set_tick_params(which=self.ticktype,direction=value.lower())
        self.canvas.draw_idle()

    def get_tickdir (self):
        if self.ticktype == 'major': return self.obj.get_major_ticks()[0].get_tickdir().title()
        else: 
            try: return self.obj.get_minor_ticks()[0].get_tickdir().title()
            except: return 'out'.title()
    
    def set_labelcolor(self, color):
        self.obj.set_tick_params(which=self.ticktype,labelcolor=color)
        self.canvas.draw_idle()
    
    def get_labelcolor(self):
        if self.ticktype == 'major': return self.obj.get_majorticklabels()[0].get_color()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_color()
            except: return "black"

    def set_tickcolor(self, color):
        self.obj.set_tick_params(which=self.ticktype,color=color)
        self.canvas.draw_idle()
    
    def get_tickcolor(self):
        if self.ticktype == 'major': return self.obj.get_majorticklines()[0].get_color()
        else: 
            try: return self.obj.get_minorticklines()[0].get_color()
            except: return "black"
    
    def set_labelrotation (self,value):
        self.obj.set_tick_params(which=self.ticktype,labelrotation=value)
        self.canvas.draw_idle()
    
    def get_labelrotation (self):
        if self.ticktype == 'major': return self.obj.get_majorticklabels()[0].get_rotation()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_rotation()
            except: return 0
    
    def set_tickpadding (self,value):
        self.obj.set_tick_params(which=self.ticktype,pad=value)
        self.canvas.draw_idle()
    
    def get_tickpadding (self):
        if self.ticktype == 'major': return self.obj.get_major_ticks()[0].get_tick_padding()
        else: 
            try: return self.obj.get_minor_ticks()[0].get_tick_padding()
            except: return 0
    
    def set_ticklength (self,value):
        self.obj.set_tick_params(which=self.ticktype,length=value)
        self.canvas.draw_idle()
    
    def get_ticklength (self):
        if self.ticktype == 'major': return self.obj.get_major_ticks()[0]._size
        else: 
            try: return self.obj.get_minor_ticks()[0]._size
            except: return rcParams['ytick.minor.size']
    
    def set_tickwidth (self,value):
        self.obj.set_tick_params(which=self.ticktype,width=value)
        self.canvas.draw_idle()
    
    def get_tickwidth (self):
        if self.ticktype == 'major': return self.obj.get_major_ticks()[0]._width
        else: 
            try: return self.obj.get_minor_ticks()[0]._width
            except: return rcParams['ytick.minor.width']

class SpineBase (QWidget):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.axis = axis
        self.canvas = canvas
        self.spines, self.arrows = self.find_object()

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)

        visible = Toggle(text='Spine visible')
        visible.button.checkedChanged.connect(self.set_visible)
        visible.button.setChecked(self.get_visible())
        layout.addWidget(visible)

        arrow = ComboBox(
            text  = 'Arrow Style',
            items = marker_lib.values()
        )
        arrow.button.setCurrentText(self.get_arrow())
        arrow.button.currentTextChanged.connect(self.set_arrow)
        layout.addWidget(arrow)

        color = ColorDropdown(text='Spine color')
        color.button.colorChanged.connect(self.set_color)
        color.button.setColor(self.get_color())
        layout.addWidget(color)

        arrowcolor = ColorDropdown(text="Arrow color")
        arrowcolor.button.colorChanged.connect(self.set_arrowcolor)
        arrowcolor.button.setColor(self.get_arrowcolor())
        layout.addWidget(arrowcolor)

        alpha = DoubleSpinBox(
            text ='Transparent',
            min = 0, max = 100, step = 10
        )
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)

        linestyle = ComboBox(
            text  = 'Line style',
            items = linestyle_lib.values()
        )
        linestyle.button.currentTextChanged.connect(self.set_linestyle)
        linestyle.button.setCurrentText(self.get_linestyle())
        layout.addWidget(linestyle)

        linewidth = DoubleSpinBox(
            text = 'Line width',
            min = 0, max = 20, step = 0.5
        )
        linewidth.button.valueChanged.connect(self.set_linewidth)
        linewidth.button.setValue(self.get_linewidth())
        layout.addWidget(linewidth)

    def find_object (self) -> tuple[list[spines.Spine], list[lines.Line2D]]:
        s = find_mpl_object(
            self.canvas.fig, 
            [spines.Spine],
            gid = f"spine {self.axis}",
        )
        a = find_mpl_object(
            self.canvas.fig, 
            [lines.Line2D],
            gid = f"spine {self.axis}",
        )
        return s, a
    
    def set_visible (self, value:bool):
        for obj in self.spines+self.arrows:
            obj.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible (self):
        return self.spines[0].get_visible()  

    def set_arrow(self, marker):
        try:
            marker = list(marker_lib.keys())[list(marker_lib.values()).index(marker.lower())]
            for obj in self.arrows:
                obj.set_marker(marker)
        except Exception as e:
            logger.exception(e)
        self.canvas.draw_idle()
    
    def get_arrow(self):
        return marker_lib[self.arrows[0].get_marker()]
    
    def set_alpha (self, value):
        for obj in self.spines+self.arrows:
            obj.set_alpha(float(value/100))
        self.canvas.draw_idle()
    
    def get_alpha(self):
        if self.spines[0].get_alpha() == None:
            return 100
        return self.spines[0].get_alpha()*100
    
    def set_linestyle(self, value):
        for obj in self.spines:
            obj.set_linestyle(value)
        self.canvas.draw_idle()
    
    def get_linestyle(self):
        return self.spines[0].get_linestyle()

    def set_linewidth(self, value):
        for obj in self.spines+self.arrows:
            obj.set_linewidth(value)
        self.canvas.draw_idle()
    
    def get_linewidth (self):
        return self.spines[0].get_linewidth()

    def set_color(self, color):
        for obj in self.spines+self.arrows:
            obj.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        return colors.rgb2hex(self.spines[0].get_edgecolor())

    def set_arrowcolor(self, color):
        for obj in self.arrows:
            obj.set_markerfacecolor(color)
        self.canvas.draw_idle()
    
    def get_arrowcolor(self):
        return colors.rgb2hex(self.arrows[0].get_markerfacecolor())

class AxisLabel (QWidget):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.canvas = canvas
        self.axis = axis
        self.ax = self.find_axis()
        self.text = self.ax.get_label()

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)

        label = LineEdit(text='Label')
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        label.button.setText(self.get_label())
        label.button.textChanged.connect(self.set_label)
        layout.addWidget(label)

        font = ComboBox(
            items = font_lib,
            text  = 'Font'
        )
        font.button.currentTextChanged.connect(self.set_fontname)
        font.button.setCurrentText(self.get_fontname())
        layout.addWidget(font)

        size = DoubleSpinBox(
            text = 'Font size',
            min = 1, max = 100, step = 1
        )
        size.button.valueChanged.connect(self.set_fontsize)
        size.button.setValue(self.get_fontsize())
        layout.addWidget(size)

        style = FontStyle(
            obj = [self.text], 
            canvas = self.canvas
        )
        layout.addWidget(style)

        color = ColorDropdown(
            text  = 'Font color',
            color = self.get_color()
        )
        color.button.colorChanged.connect(self.set_color)
        layout.addWidget(color)

        self.backgroundcolor = ColorDropdown(
            text  = 'Background color',
            color = self.get_backgroundcolor()
        )
        self.backgroundcolor.button.colorChanged.connect(self.set_backgroundcolor)
        layout.addWidget(self.backgroundcolor)

        edgecolor = ColorDropdown(
            text  = 'Edge color',
            color = self.get_edgecolor()
        )
        edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(edgecolor)

        alpha = DoubleSpinBox(
            text = 'Transparency',
            step = 10
        )
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)
    
    def find_axis(self) -> Axis:
        return find_mpl_object(self.canvas.fig,[Axis], self.axis)[0]
    
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
    
class Tick2D (QDialog):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f'{axis.title()} Axis')
        layout = QVBoxLayout(self)
        self.canvas = canvas

        self.choose_axis = SegmentedWidget(parent)
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='General', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Major', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Minor', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.choose_axis.addButton(text='Spine', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.choose_axis.addButton(text='Label', func=lambda: self.stackedlayout.setCurrentIndex(4))

        self.choose_axis.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        base = TickBase(axis, canvas, parent)
        self.stackedlayout.addWidget(base)

        major = TickBase2(axis, 'major', canvas, parent)
        self.stackedlayout.addWidget(major)

        minor = TickBase2(axis, 'minor', canvas, parent)
        self.stackedlayout.addWidget(minor)

        spine = SpineBase(axis, canvas, parent)
        self.stackedlayout.addWidget(spine)

        label = AxisLabel(axis, canvas, parent)
        self.stackedlayout.addWidget(label)
