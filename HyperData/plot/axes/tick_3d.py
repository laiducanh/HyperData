from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QScrollArea, QApplication
from ui.base_widgets.button import ComboBox, Toggle, _ComboBox, SegmentedWidget
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.line_edit import LineEdit, _LineEdit
from ui.base_widgets.frame import Frame
from ui.base_widgets.window import ProgressDialog
from plot.utilis import find_mpl_object
import matplotlib
from matplotlib.axis import Axis
from plot.canvas import Canvas
from config.settings import logger, GLOBAL_DEBUG

class TickBase3D_1 (QWidget):
    def __init__(self,axis,canvas:Canvas, parent=None):
        super().__init__(parent)
        self.axis = axis
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_obj()
        self.first_show = True
        
    
    def initUI(self):
        self.diag = ProgressDialog("Waiting", None, self.parent())
        self.diag.progressbar._setValue(0)
        self.diag.show()
        QApplication.processEvents()
        

        mainwidget = QWidget()
        mainwidget_layout = QVBoxLayout(mainwidget)
        mainwidget_layout.setContentsMargins(0,0,0,0)
        self.vlayout.addWidget(mainwidget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setContentsMargins(0,0,0,0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(mainwidget)
        self.scroll_area.verticalScrollBar().setValue(1900)
        self.vlayout.addWidget(self.scroll_area)

        card1 = Frame(self.parent())
        layout1 = QVBoxLayout(card1)
        mainwidget_layout.addWidget(card1)

        visible = Toggle(text="Visible",text2=f"Toggle {self.axis} ticks' visibility")
        visible.button.checkedChanged.connect(self.set_visible)
        visible.button.setChecked(self.get_visible())
        layout1.addWidget(visible)
        
        self.diag.progressbar._setValue(10)
        QApplication.processEvents()

        self.min = LineEdit(text="Min Value",text2=f"Set {self.axis} axis view minimum")
        self.min.button.setFixedWidth(150)
        self.min.button.textChanged.connect(self.set_min)
        self.min.button.setText(str(round(self.get_lim()[0],5)))
        layout1.addWidget(self.min)
        
        self.diag.progressbar._setValue(20)
        QApplication.processEvents()

        self.max = LineEdit(text='Max Value',text2=f"Set {self.axis} axis view maximum")
        self.max.button.setFixedWidth(150)
        self.max.button.textChanged.connect(self.set_max)
        self.max.button.setText(str(round(self.get_lim()[1],5)))
        layout1.addWidget(self.max)
        self.diag.progressbar._setValue(30)
        QApplication.processEvents()

        scale = ComboBox(items=['Linear','Log','Symlog','Logit','Asinh'],
                         text='Scale',text2=f"Set {self.axis} axis' scale")
        scale.button.currentTextChanged.connect(self.set_scale)
        scale.button.setCurrentText(self.get_scale())
        layout1.addWidget(scale) 
        
        self.diag.progressbar._setValue(40)
        QApplication.processEvents()  

        self.choose_tick = SegmentedWidget()
        mainwidget_layout.addWidget(self.choose_tick)

        card2 = Frame(self.parent())
        layout2 = QVBoxLayout()
        card2.setLayout(layout2)
        mainwidget_layout.addWidget(card2)

        self.layout6 = QVBoxLayout()
        layout2.addLayout(self.layout6)

        self.choose_tick.addButton(text='Major', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_tick.addButton(text='Minor', func=lambda: self.stackedlayout.setCurrentIndex(1))

        self.stackedlayout = QStackedLayout()
        self.layout6.addLayout(self.stackedlayout)

        self.majortick = TickBase3D_2(self.axis, 'major',self.canvas, self.parent())
        self.stackedlayout.addWidget(self.majortick)
        self.diag.progressbar._setValue(70)
        QApplication.processEvents()

        self.minortick = TickBase3D_2(self.axis,'minor', self.canvas, self.parent())
        self.stackedlayout.addWidget(self.minortick)
        self.diag.progressbar._setValue(100)
        QApplication.processEvents()
        
        self.choose_tick._onClick("Major")

        self.diag.close()
    
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
    
    def showEvent(self, a0: QShowEvent) -> None:
        # update min, max when show
        # self.min.button.setText(str(round(self.get_lim()[0],5)))
        # self.max.button.setText(str(round(self.get_lim()[1],5)))
        if self.first_show: 
            self.initUI()
            self.first_show = False
        return super().showEvent(a0)

class TickBase3D_2 (QWidget):
    def __init__(self,axis,type,canvas:Canvas, parent=None):
        super().__init__(parent)
        self.type = type
        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_obj()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.first_show = True
    
    def initUI(self):

        layout1 = QHBoxLayout()
        self.layout().addLayout(layout1)
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
        
        self.tick_label = LineEdit(text='Tick labels',text2=f"Set {self.axis} axis' {self.type} tick labels")
        self.tick_label.button.textChanged.connect(self.set_ticklabels)
        self.tick_label.button.setPlaceholderText(self.get_ticklabels())
        self.layout().addWidget(self.tick_label)

        tick_position = ComboBox(items=["lower","upper","both"], text="Tick position")
        tick_position.button.currentTextChanged.connect(self.set_tick_position)
        tick_position.button.setCurrentText(self.get_tick_position())
        self.layout().addWidget(tick_position)

        tick_labelsize = DoubleSpinBox(text='Label size',text2=f"Set {self.axis} axis' {self.type} tick label size",
                                       min=1,max=100,step=1)
        tick_labelsize.button.valueChanged.connect(self.set_labelsize)
        tick_labelsize.button.setValue(self.get_labelsize())
        self.layout().addWidget(tick_labelsize)

        tick_labelcolor = ColorDropdown(text='Label color', color=self.get_labelcolor())
        tick_labelcolor.button.colorChanged.connect(self.set_labelcolor)
        self.layout().addWidget(tick_labelcolor)

        tickcolor = ColorDropdown(text='Tick color', color=self.get_tickcolor())
        tickcolor.button.colorChanged.connect(self.set_tickcolor)
        self.layout().addWidget(tickcolor)

        tick_rotation = DoubleSpinBox(text='Tick label rotation',min=-180,max=180,step=10)
        tick_rotation.button.valueChanged.connect(self.set_labelrotation)
        tick_rotation.button.setValue(self.get_labelrotation())
        self.layout().addWidget(tick_rotation)

        tick_labelpad = DoubleSpinBox(text='Tick labelpad',min=0,max=50,step=0.5)
        tick_labelpad.button.valueChanged.connect(self.set_tickpadding)
        tick_labelpad.button.setValue(self.get_tickpadding())
        self.layout().addWidget(tick_labelpad)
    
    def find_obj(self) -> Axis:
        obj = find_mpl_object(self.canvas.fig, match=[Axis], gid=self.axis)
        return obj[0]
            
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
            self.canvas.draw_idle()
        except:pass
    
    def set_tickvalues (self, value:str):
        try:
            value = [float(i) for i in value.split(',')]
            if self.type == 'major': self.obj.set_ticks(value)
            else: self.obj.set_ticks(value,minor=True)
            self.canvas.draw_idle()
        except:pass
    
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
        self.obj.set_tick_params(which=self.type,labelsize=value)
        self.canvas.draw_idle()
    
    def get_labelsize (self):
        if self.type == 'major': return self.obj.get_majorticklabels()[0].get_fontsize()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_fontsize() 
            except: return 7
    
    def set_labelcolor(self, color):
        self.obj.set_tick_params(which=self.type,labelcolor=color)
        self.canvas.draw_idle()
    
    def get_labelcolor(self):
        if self.type == 'major': return self.obj.get_majorticklabels()[0].get_color()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_color()
            except: return "black"

    def set_tickcolor(self, color):
        self.obj.set_tick_params(which=self.type,color=color)
        self.canvas.draw_idle()
    
    def get_tickcolor(self):
        if self.type == 'major': return self.obj.get_majorticklines()[0].get_color()
        else: 
            try: return self.obj.get_minorticklines()[0].get_color()
            except: return "black"
    
    def set_labelrotation (self,value):
        self.obj.set_tick_params(which=self.type,labelrotation=value)
        self.canvas.draw_idle()
    
    def get_labelrotation (self):
        if self.type == 'major': return self.obj.get_majorticklabels()[0].get_rotation()
        else: 
            try: return self.obj.get_minorticklabels()[0].get_rotation()
            except: return 0
    
    def set_tickpadding (self,value):
        self.obj.set_tick_params(which=self.type,pad=value)
        self.canvas.draw_idle()
    
    def get_tickpadding (self):
        if self.type == 'major': return self.obj.get_major_ticks()[0].get_tick_padding()
        else: 
            try: return self.obj.get_minor_ticks()[0].get_tick_padding()
            except: return 0
    
    def showEvent(self, a0):
        if self.first_show: 
            self.initUI()
            self.first_show = False
        return super().showEvent(a0)

class Tick3D (QWidget):
    def __init__(self,canvas:Canvas, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(10,0,10,15)
        self.canvas = canvas

        self.choose_axis = SegmentedWidget(parent)
        self.layout().addWidget(self.choose_axis)

        self.choose_axis.addButton(text='X3D', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Y3D', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Z3D', func=lambda: self.stackedlayout.setCurrentIndex(2))

        self.stackedlayout = QStackedLayout()
        self.layout().addLayout(self.stackedlayout)
        
        self.bot = TickBase3D_1('x3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.bot)
        self.left = TickBase3D_1('y3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.left)
        self.top = TickBase3D_1('z3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.top)