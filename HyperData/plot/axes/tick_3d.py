from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QStackedLayout
from ui.base_widgets.button import ComboBox, Toggle, SegmentedWidget
from ui.base_widgets.spinbox import DoubleSpinBox, Slider
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.list import TreeWidget, TreeWidgetItem
from plot.utilis import find_mpl_object
from config.settings import logger, marker_lib, linestyle_lib
from matplotlib import ticker, lines, colors
from matplotlib.axis import Axis
from plot.canvas import Canvas

DEBUG = False

class TickBase (TreeWidgetItem):
    def __init__(self, axis:str, canvas: Canvas, treeview:TreeWidget):
        super().__init__(treeview)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_obj()
        self.treeview = treeview

        self.initUI()
    
    def initUI(self):
        self.setText(0, 'General')

        child = TreeWidgetItem(self)
        visible = Toggle(
            text  = "Visible",
            text2 = f"Toggle {self.axis} ticks' visibility"
        )
        visible.button.checkedChanged.connect(self.set_visible)
        visible.button.setChecked(self.get_visible())
        self.treeview.setItemWidget(child, 0, visible)

        child = TreeWidgetItem(self)
        self.min = LineEdit(
            text  = "Min Value",
            text2 = f"Set {self.axis} axis view minimum"
        )
        self.min.button.setFixedWidth(150)
        self.min.button.textChanged.connect(self.set_min)
        self.min.button.setText(str(round(self.get_lim()[0],5)))
        self.treeview.setItemWidget(child, 0, self.min)

        child = TreeWidgetItem(self)
        self.max = LineEdit(
            text  = 'Max Value',
            text2 = f"Set {self.axis} axis view maximum"
        )
        self.max.button.setFixedWidth(150)
        self.max.button.textChanged.connect(self.set_max)
        self.max.button.setText(str(round(self.get_lim()[1],5)))
        self.treeview.setItemWidget(child, 0, self.max)

        child = TreeWidgetItem(self)
        scale = ComboBox(
            items = ['linear','log','symlog','logit','asinh'],
            text  = 'Scale',
            text2 = f"Set {self.axis} axis' scale"
        )
        scale.button.currentTextChanged.connect(self.set_scale)
        scale.button.setCurrentText(self.get_scale())
        self.treeview.setItemWidget(child, 0, scale)

    def find_obj(self) -> Axis:
        obj = find_mpl_object(self.canvas.fig, match=[Axis], gid=self.axis)
        return obj[0]
    
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

    def get_lim(self):
        
        if self.axis == "x3d": return self.obj.axes.get_xlim()
        elif self.axis == "y3d": return self.obj.axes.get_ylim()
        elif self.axis == "z3d": return self.obj.axes.get_zlim()
    
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

class TickBase2 (TickBase):
    def __init__(self, axis:str, type:str, canvas: Canvas, treeview:TreeWidget):

        self.ticktype = type

        super().__init__(axis, canvas, treeview)
    
    def initUI(self):

        self.setText(0, self.ticktype.title())

        child = TreeWidgetItem(self)
        self.tickinterval = ComboBox(
            items = ['Tick Interval','Tick Values'],
            text  = 'Type' 
        )
        self.tickinterval.button.setCurrentText('Tick Interval')
        self.tickinterval.button.currentTextChanged.connect(self.set_tickvalues)
        self.treeview.setItemWidget(child, 0, self.tickinterval)

        child = TreeWidgetItem(self)
        self.value = LineEdit(
            text = 'Tick values'
        )
        self.value.button.textChanged.connect(self.set_tickvalues)
        self.treeview.setItemWidget(child, 0, self.value)

        child = TreeWidgetItem(self)
        self.tick_label = LineEdit(
            text  = 'Tick labels',
            text2 = f"Set {self.axis} axis' {self.ticktype} tick labels"
        )
        self.tick_label.button.textChanged.connect(self.set_ticklabels)
        self.tick_label.button.setPlaceholderText(self.get_ticklabels())
        self.treeview.setItemWidget(child, 0, self.tick_label)

        child = TreeWidgetItem(self)
        tick_position = ComboBox(
            items = ["lower","upper","both"], 
            text  = "Tick position"
        )
        tick_position.button.currentTextChanged.connect(self.set_tick_position)
        tick_position.button.setCurrentText(self.get_tick_position())
        self.treeview.setItemWidget(child, 0, tick_position)

        child = TreeWidgetItem(self)
        tick_labelsize = DoubleSpinBox(
            text  = 'Label size',
            text2 = f"Set {self.axis} axis' {self.ticktype} tick label size",
            min = 1, max = 100, step = 1
        )
        tick_labelsize.button.valueChanged.connect(self.set_labelsize)
        tick_labelsize.button.setValue(self.get_labelsize())
        self.treeview.setItemWidget(child, 0, tick_labelsize)

        child = TreeWidgetItem(self)
        tick_labelcolor = ColorDropdown(
            text  = 'Label color', 
            color = self.get_labelcolor()
        )
        tick_labelcolor.button.colorChanged.connect(self.set_labelcolor)
        self.treeview.setItemWidget(child, 0, tick_labelcolor)

        child = TreeWidgetItem(self)
        tickcolor = ColorDropdown(
            text  = 'Tick color', 
            color = self.get_tickcolor()
        )
        tickcolor.button.colorChanged.connect(self.set_tickcolor)
        self.treeview.setItemWidget(child, 0, tickcolor)

        child = TreeWidgetItem(self)
        tick_rotation = DoubleSpinBox(
            text = 'Tick label rotation',
            min = -180, max = 180, step = 10
        )
        tick_rotation.button.valueChanged.connect(self.set_labelrotation)
        tick_rotation.button.setValue(self.get_labelrotation())
        self.treeview.setItemWidget(child, 0, tick_rotation)

        child = TreeWidgetItem(self)
        tick_labelpad = DoubleSpinBox(
            text = 'Tick labelpad',
            min = 0, max = 50, step = 0.5
        )
        tick_labelpad.button.valueChanged.connect(self.set_tickpadding)
        tick_labelpad.button.setValue(self.get_tickpadding())
        self.treeview.setItemWidget(child, 0, tick_labelpad)
    
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
            if self.type == 'major': self.obj.set_ticklabels(value)
            else: self.obj.set_ticklabels(value,minor=True)
            self.canvas.draw_idle()
        except:pass
    
    def get_ticklabels(self):
        
        label_list = list()
        if self.type == 'major':
            label_list = [i.get_text() for i in self.obj.get_majorticklabels()]

        else:
            label_list = [i.get_text() for i in self.obj.get_minorticklabels()]
            
        return ", ".join(label_list)

    def set_tick_position(self, value):
        self.obj.set_ticks_position(value)
        self.canvas.draw_idle()
    
    def get_tick_position(self):
        return self.obj.get_ticks_position()
    
    def set_labelsize (self,value):
        self.obj.set_tick_params(which=self.ticktype,labelsize=value)
        self.canvas.draw_idle()
    
    def get_labelsize (self):
        if self.ticktype == 'major': return self.obj.get_majorticklabels()[0].get_fontsize()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_fontsize() 
            except: return 7
    
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

class SpineBase (TreeWidgetItem):
    def __init__(self, axis:str, canvas: Canvas, treeview:TreeWidget):
        super().__init__(treeview)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_object()
        self.treeview = treeview

        self.initUI()

    def initUI(self):
        self.setText(0, 'Spine')

        child = TreeWidgetItem(self)
        visible = Toggle(text='Spine visible')
        visible.button.checkedChanged.connect(self.set_visible)
        visible.button.setChecked(self.get_visible())
        self.treeview.setItemWidget(child, 0, visible)

        child = TreeWidgetItem(self)
        arrow = ComboBox(
            text  = 'Arrow Style',
            items = marker_lib.values()
        )
        arrow.button.setCurrentText(self.get_arrow())
        arrow.button.currentTextChanged.connect(self.set_arrow)
        self.treeview.setItemWidget(child, 0, arrow)

        child = TreeWidgetItem(self)
        color = ColorDropdown(text='Spine color')
        color.button.colorChanged.connect(self.set_color)
        color.button.setColor(self.get_color())
        self.treeview.setItemWidget(child, 0, color)

        child = TreeWidgetItem(self)
        arrowcolor = ColorDropdown(text="Arrow color")
        arrowcolor.button.colorChanged.connect(self.set_arrowcolor)
        arrowcolor.button.setColor(self.get_arrowcolor())
        self.treeview.setItemWidget(child, 0, arrowcolor)

        child = TreeWidgetItem(self)
        alpha = Slider(
            text ='Transparent',
            min = 0, max = 100, step = 1
        )
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        self.treeview.setItemWidget(child, 0, alpha)

        child = TreeWidgetItem(self)
        linestyle = ComboBox(
            text  = 'Line style',
            items = linestyle_lib.values()
        )
        linestyle.button.currentTextChanged.connect(self.set_linestyle)
        linestyle.button.setCurrentText(self.get_linestyle())
        self.treeview.setItemWidget(child, 0, linestyle)

        child = TreeWidgetItem(self)
        linewidth = DoubleSpinBox(
            text = 'Line width',
            min = 0, max = 20, step = 0.5
        )
        linewidth.button.valueChanged.connect(self.set_linewidth)
        linewidth.button.setValue(self.get_linewidth())
        self.treeview.setItemWidget(child, 0, linewidth)

    def find_object (self) -> lines.Line2D:
        return find_mpl_object(
            self.canvas.fig, 
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

class TickBase3D (TreeWidget):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.setColumnCount(1)
        self.setUniformRowHeights(True)
    
        base = TickBase(axis, canvas, self)
        major = TickBase2(axis, 'major', canvas, self)
        minor = TickBase2(axis, 'minor', canvas, self)
        spine = SpineBase(axis, canvas, self)

class Tick3D (QMainWindow):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

    # Layout
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10,0,10,15)

        self.canvas = canvas

        self.choose_axis = SegmentedWidget(parent)
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='X3D', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Y3D', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Z3D', func=lambda: self.stackedlayout.setCurrentIndex(2))

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)
        
        self.bot = TickBase3D('x3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.bot)
        self.left = TickBase3D('y3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.left)
        self.top = TickBase3D('z3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.top)

    def choose_axis_func(self, axis):
        self.choose_axis._onClick(axis)