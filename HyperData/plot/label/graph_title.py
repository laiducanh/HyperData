from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QSizePolicy, QWidget, QDialog
from plot.canvas import Canvas
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.frame import SeparateHLine
from plot.utilis import find_mpl_object
from plot.label.base import FontStyle
from config.settings import font_lib

DEBUG = False

class GraphTitle (QDialog):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Graph Title')
        self.canvas = canvas
        self.obj = self.canvas.axes.set_title('Graph Title')
        self.initUI()
    
    def initUI(self):  

        layout = QVBoxLayout(self)

        label = LineEdit(text='Label')
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        label.button.setText(self.get_title())
        label.button.textChanged.connect(self.set_title)
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
            min = 1, max = 100, step = 2
        )
        size.button.valueChanged.connect(self.set_fontsize)
        size.button.setValue(self.get_fontsize())
        layout.addWidget(size)
        
        style = FontStyle(
            obj = [self.obj], 
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

        # #align = FontAlignment(type='graph')
        # #align.sig.connect(lambda: self.sig.emit())
        # #layout.addWidget(align)
        
        # #pad = DoubleSpinBox(text='label pad',min=-100,max=100,step=5)
        # #pad.button.valueChanged.connect(lambda: self.sig.emit())
        # #layout.addWidget(pad)

        alpha = DoubleSpinBox(
            text = 'Transparency',
            step = 10
        )
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)
    
    def set_title (self, title:str):
        self.canvas.axes.set_title(title) 
        self.canvas.draw_idle()
    
    def get_title(self):
        return self.canvas.axes.get_title()

    def set_fontname (self, font:str):
        self.obj.set_fontname(font.lower())
        self.canvas.draw_idle()
    
    def get_fontname(self):
        return self.obj.get_fontname().title()

    def set_fontsize(self, value):
        self.obj.set_fontsize(value)
        self.canvas.draw_idle()
    
    def get_fontsize(self):
        return self.obj.get_fontsize()

    def set_color (self, color):
        self.obj.set_color(color)
        self.canvas.draw_idle()
    
    def get_color (self):
        return self.obj.get_color()

    def set_backgroundcolor (self, color):
        self.obj.set_backgroundcolor(color)
        self.canvas.draw_idle()
    
    def get_backgroundcolor(self):
        if self.obj.get_bbox_patch():
            return self.obj.get_bbox_patch().get_facecolor()
        return 'white'

    def set_edgecolor (self, color):
        self.obj.set_bbox(
            {"edgecolor" : color,
            "facecolor"  : self.backgroundcolor.button.color.name()
            }
        )
        self.canvas.draw_idle()
    
    def get_edgecolor(self):
        if self.obj.get_bbox_patch():
            return self.obj.get_bbox_patch().get_edgecolor()
        return 'white'

    def set_pad (self, value):
        pass

    def get_pad (self):
        pass

    def set_alpha (self, value):
        self.obj.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_alpha (self):
        if self.obj.get_alpha():
            return int(self.obj.get_alpha()*100)
        return 100