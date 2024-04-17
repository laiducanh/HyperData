from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QScrollArea
from ui.base_widgets.button import ComboBox, Toggle, _ComboBox, SegmentedWidget
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.line_edit import LineEdit, _LineEdit
from ui.base_widgets.frame import Frame
import matplotlib
from matplotlib.axis import Axis
from plot.canvas import Canvas

class TickBase2D_1 (QWidget):
    def __init__(self,axis,canvas:Canvas):
        super().__init__()
        self.axis = axis
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_object()

        widget = QWidget()
        widget.layout = QVBoxLayout()
        widget.setLayout(widget.layout)
        widget.layout.setContentsMargins(0,0,0,0)
        layout.addWidget(widget)

        self.scroll_area = QScrollArea(parent=self)
        self.scroll_area.setContentsMargins(0,0,0,0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(widget)
        self.scroll_area.verticalScrollBar().setValue(1900)
        layout.addWidget(self.scroll_area)

        card1 = Frame()
        layout1 = QVBoxLayout()
        card1.setLayout(layout1)
        widget.layout.addWidget(card1)

        visible = Toggle(text='tick visible')
        visible.button.checkedChanged.connect(self.set_visible)
        visible.button.setChecked(self.get_visible())
        layout1.addWidget(visible)

        self.min = LineEdit(text='min value')
        self.min.button.setFixedWidth(150)
        self.min.button.textChanged.connect(self.set_min)
        self.min.button.setText(str(round(self.get_lim()[0],5)))
        layout1.addWidget(self.min)

        self.max = LineEdit(text='max value')
        self.max.button.setFixedWidth(150)
        self.max.button.textChanged.connect(self.set_max)
        self.max.button.setText(str(round(self.get_lim()[1],5)))
        layout1.addWidget(self.max)

        scale = ComboBox(items=['Linear','Log','Symlog','Logit','Asinh'],text='scale')
        scale.button.currentTextChanged.connect(self.set_scale)
        scale.button.setCurrentText(self.get_scale())
        layout1.addWidget(scale)   

        self.choose_tick = SegmentedWidget()
        widget.layout.addWidget(self.choose_tick)

        card2 = Frame()
        layout2 = QVBoxLayout()
        card2.setLayout(layout2)
        widget.layout.addWidget(card2)

        self.layout6 = QVBoxLayout()
        layout2.addLayout(self.layout6)

        self.choose_tick.addButton(text='Major', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_tick.addButton(text='Minor', func=lambda: self.stackedlayout.setCurrentIndex(1))

        self.stackedlayout = QStackedLayout()
        self.layout6.addLayout(self.stackedlayout)

        self.majortick = TickBase2D_2(self.axis, 'major',self.canvas)
        self.stackedlayout.addWidget(self.majortick)

        self.minortick = TickBase2D_2(self.axis,'minor', self.canvas)
        self.stackedlayout.addWidget(self.minortick)
        
        self.choose_tick._onClick("Major")

    def find_object(self) -> Axis:
        for obj in self.canvas.fig.findobj(match=Axis):
            if obj._gid == self.axis:
                return obj
    
    def set_visible(self, value):
        self.obj.set_visible(value)
        self.canvas.draw()
    
    def get_visible(self):
        return self.obj.get_visible()

    def set_min(self, value):
            
        try:
            if self.axis in ['bottom','top']:
                self.obj.axes.set_xlim(left=float(value))
            else:
                self.obj.axes.set_ylim(bottom=float(value))
        except Exception as e: print(e)

        self.canvas.draw()
    
    def set_max (self, value):
            
        try:
            if self.axis in ['bottom','top']:
                self.obj.axes.set_xlim(right=float(value))
            else:
                self.obj.axes.set_ylim(top=float(value))
        except Exception as e: print(e)

        self.canvas.draw()

    def get_lim(self):
        if self.axis in ['bottom','top']: return self.obj.axes.get_xlim()
        else: return self.obj.axes.get_ylim()
    
    def set_scale (self, value:str):
        try:
            if self.axis in ['bottom','top']: self.obj.axes.set_xscale(value)
            else: self.obj.axes.set_yscale(value)
            self.canvas.draw()
        except:pass
    
    def get_scale (self):
        if self.axis in ['bottom','top']: return self.obj.axes.get_xscale()
        else: return self.obj.axes.get_yscale()

class TickBase2D_2 (QWidget):
    def __init__(self,axis,type,canvas:Canvas):
        super().__init__()
        self.type = type
        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_object()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout1 = QHBoxLayout()
        self.layout.addLayout(layout1)
        tickinterval = _ComboBox(items=['Tick Interval','Tick Values'])
        tickinterval.setCurrentText('Tick Interval')
        tickinterval.currentTextChanged.connect(self.func)
        layout1.addWidget(tickinterval)

        self.interval = _LineEdit()
        self.interval.textChanged.connect(self.set_interval)
        layout1.addWidget(self.interval)
        self.value = _LineEdit()
        self.value.textChanged.connect(self.set_tickvalues)
        self.value.hide()
        layout1.addWidget(self.value)
        
        self.tick_label = LineEdit(text='tick labels')
        self.tick_label.button.textChanged.connect(self.set_ticklabels)
        self.tick_label.button.setPlaceholderText(self.get_ticklabels())
        self.layout.addWidget(self.tick_label)

        tick_labelsize = DoubleSpinBox(text='tick label size',min=1,max=100,step=1)
        tick_labelsize.button.valueChanged.connect(self.set_labelsize)
        tick_labelsize.button.setValue(self.get_labelsize())
        self.layout.addWidget(tick_labelsize)

        tick_direction = ComboBox(text='tick direction',items=['In','Out','InOut'])
        tick_direction.button.currentTextChanged.connect(self.set_tickdir)
        tick_direction.button.setCurrentText(self.get_tickdir())
        self.layout.addWidget(tick_direction)

        tick_labelcolor = ColorDropdown(text='label color', color=self.get_labelcolor())
        tick_labelcolor.button.colorChanged.connect(self.set_labelcolor)
        self.layout.addWidget(tick_labelcolor)

        tickcolor = ColorDropdown(text='tick color', color=self.get_tickcolor())
        tickcolor.button.colorChanged.connect(self.set_tickcolor)
        self.layout.addWidget(tickcolor)

        tick_rotation = DoubleSpinBox(text='tick label rotation',min=-180,max=180,step=10)
        tick_rotation.button.valueChanged.connect(self.set_labelrotation)
        tick_rotation.button.setValue(self.get_labelrotation())
        self.layout.addWidget(tick_rotation)

        tick_labelpad = DoubleSpinBox(text='tick labelpad',min=0,max=50,step=0.5)
        tick_labelpad.button.valueChanged.connect(self.set_tickpadding)
        tick_labelpad.button.setValue(self.get_tickpadding())
        self.layout.addWidget(tick_labelpad)

        tick_length = DoubleSpinBox(text='tick length',min=0,max=50,step=0.5)
        tick_length.button.valueChanged.connect(self.set_ticklength)
        tick_length.button.setValue(self.get_ticklength())
        self.layout.addWidget(tick_length)

        tick_width = DoubleSpinBox(text='tick width',min=0,max=50,step=0.5)
        tick_width.button.valueChanged.connect(self.set_tickwidth)
        tick_width.button.setValue(self.get_tickwidth())
        self.layout.addWidget(tick_width)

    def find_object(self) -> Axis:
        for obj in self.canvas.fig.findobj(match=Axis):
            if obj._gid == self.axis:
                return obj
            
    def func (self,s):
        if s == 'Tick Interval':
            self.value.hide()
            self.interval.show()

        else:
            self.value.show()
            self.interval.hide()

    def set_interval (self, value):
        try:
            if self.type == 'major': self.obj.set_major_locator(matplotlib.ticker.MultipleLocator(float(value)))
            else: self.obj.set_minor_locator(matplotlib.ticker.MultipleLocator(float(value)))
            self.canvas.draw()
        except:pass
    
    def set_tickvalues (self, value:str):
        try:
            value = [float(i) for i in value.split(',')]
            if self.type == 'major': self.obj.axes.set_xticks(value)
            else: self.obj.axes.set_xticks(value,minor=True)
            self.canvas.draw()
        except:pass
    
    def set_ticklabels (self, value:str):
        try:
            value = value.split(',')
            if self.type == 'major': self.obj.axes.set_xticklabels(value)
            else: self.obj.axes.set_xticklabels(value,minor=True)
            self.canvas.draw()
        except:pass
    
    def get_ticklabels(self):
        
        label_list = list()
        if self.type == 'major':
            label_list = [i.get_text() for i in self.obj.get_majorticklabels()]

        else:
            label_list = [i.get_text() for i in self.obj.get_minorticklabels()]
            
        return ", ".join(label_list)
    
    def set_labelsize (self,value):
        axis = 'x' if self.axis in ['bottom','top'] else 'y'
        self.obj.axes.tick_params(which=self.type,axis=axis,labelsize=value)
        self.canvas.draw()
    
    def get_labelsize (self):
        if self.type == 'major': return self.obj.get_majorticklabels()[0].get_fontsize()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_fontsize() 
            except: return 7
        
    def set_tickdir (self,value):
        axis = 'x' if self.axis in ['bottom','top'] else 'y'
        self.obj.axes.tick_params(which=self.type,axis=axis,direction=value.lower())
        self.canvas.draw()

    def get_tickdir (self):
        if self.type == 'major': return self.obj.get_major_ticks()[0].get_tickdir().title()
        else: 
            try: return self.obj.get_minor_ticks()[0].get_tickdir().title()
            except: return 'out'.title()
    
    def set_labelcolor(self, color):
        axis = 'x' if self.axis in ['bottom','top'] else 'y'
        self.obj.axes.tick_params(which=self.type,axis=axis,labelcolor=color)
        self.canvas.draw()
    
    def get_labelcolor(self):
        if self.type == 'major': return self.obj.get_majorticklabels()[0].get_color()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_color()
            except: return "black"

    def set_tickcolor(self, color):
        axis = 'x' if self.axis in ['bottom','top'] else 'y'
        self.obj.axes.tick_params(which=self.type,axis=axis,color=color)
        self.canvas.draw()
    
    def get_tickcolor(self):
        if self.type == 'major': return self.obj.get_majorticklines()[0].get_color()
        else: 
            try: return self.obj.get_minorticklines()[0].get_color()
            except: return "black"
    
    def set_labelrotation (self,value):
        axis = 'x' if self.axis in ['bottom','top'] else 'y'
        self.obj.axes.tick_params(which=self.type,axis=axis,labelrotation=value)
        self.canvas.draw()
    
    def get_labelrotation (self):
        if self.type == 'major': return self.obj.get_majorticklabels()[0].get_rotation()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_rotation()
            except: return 0
    
    def set_tickpadding (self,value):
        axis = 'x' if self.axis in ['bottom','top'] else 'y'
        self.obj.axes.tick_params(which=self.type,axis=axis,pad=value)
        self.canvas.draw()
    
    def get_tickpadding (self):
        if self.type == 'major': return self.obj.get_major_ticks()[0].get_tick_padding()
        else: 
            try: return self.obj.get_minor_ticks()[0].get_tick_padding()
            except: return 0
    
    def set_ticklength (self,value):
        axis = 'x' if self.axis in ['bottom','top'] else 'y'
        self.obj.axes.tick_params(which=self.type,axis=axis,length=value)
        self.canvas.draw()
    
    def get_ticklength (self):
        if self.type == 'major': return self.obj.get_major_ticks()[0]._size
        else: 
            try: return self.obj.get_minor_ticks()[0]._size
            except: return matplotlib.rcParams['ytick.minor.size']
    
    def set_tickwidth (self,value):
        axis = 'x' if self.axis in ['bottom','top'] else 'y'
        self.obj.axes.tick_params(which=self.type,axis=axis,width=value)
        self.canvas.draw()
    
    def get_tickwidth (self):
        if self.type == 'major': return self.obj.get_major_ticks()[0]._width
        else: 
            try: return self.obj.get_minor_ticks()[0]._width
            except: return matplotlib.rcParams['ytick.minor.width']

class Tick2D (QWidget):
    def __init__(self,canvas:Canvas):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10,0,10,15)
        self.canvas = canvas

        self.choose_axis = SegmentedWidget()
        self.layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='Bottom', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Left', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Top', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.choose_axis.addButton(text='Right', func=lambda: self.stackedlayout.setCurrentIndex(3))

        self.stackedlayout = QStackedLayout()
        self.layout.addLayout(self.stackedlayout)

        self.bot = TickBase2D_1('bottom',self.canvas)
        self.stackedlayout.addWidget(self.bot)
        self.left = TickBase2D_1('left',self.canvas)
        self.stackedlayout.addWidget(self.left)
        self.top = TickBase2D_1('top',self.canvas)
        self.stackedlayout.addWidget(self.top)
        self.right = TickBase2D_1('right',self.canvas)
        self.stackedlayout.addWidget(self.right)

    