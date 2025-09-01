from ui.base_widgets.frame import ScrollArea
from ui.base_widgets.button import HTransparentComboBox, SegmentedWidget
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.line_edit import HLineEdit
from plot.label.base import FontStyle
from plot.canvas import MultiFigureCanvas
from PySide6.QtWidgets import QVBoxLayout, QStackedLayout, QDialog, QSizePolicy
from typing import Literal
from config.settings import logger, GLOBAL_DEBUG, font_lib
from matplotlib.text import Text

DEBUG = False

class _AxisLabel(ScrollArea):
    def __init__(self, axis:Literal['x','y'], canvas:MultiFigureCanvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas
        self.axis = axis

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
            obj = [self.findobj()], 
            canvas = self.canvas,
            layout=self.vlayout
        )

        color = HColorDropdown(
            label  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        backgroundcolor = HColorDropdown(
            label  = 'Background color',
            getter=self.get_backgroundcolor,
            setter=self.set_backgroundcolor,
            layout=self.vlayout
        )

        edgecolor = HColorDropdown(
            text  = 'Edge color',
            getter=self.get_edgecolor,
            setter=self.set_edgecolor,
            layout=self.vlayout
        )

        alpha = HTransparentSpinBox(
            label = 'Transparency',
            singleStep = 10, maximum = 100, minimum = 0,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )
    
    def findobj(self) -> Text:
        if self.axis == 'x':
            return self.canvas.figure._supxlabel
        else:
            return self.canvas.figure._supylabel
        
    def set_label(self, value:str):
        if self.axis == 'x':
            self.canvas.figure.supxlabel(value)
        else:
            self.canvas.figure.supylabel(value)
        self.canvas.draw_idle()
    
    def get_label(self) -> str:
        if self.axis == 'x':
            return self.canvas.figure.get_supxlabel()
        else:
            return self.canvas.figure.get_supylabel()

    def set_fontname (self, font:str):
        self.findobj().set_fontname(font)
        self.canvas.draw_idle()
    
    def get_fontname(self):
        return self.findobj().get_fontname()
    
    def set_fontsize(self, value):
        self.findobj().set_fontsize(value)
        self.canvas.draw_idle()
    
    def get_fontsize(self):
        return self.findobj().get_fontsize()
    
    def set_color (self, color):
        self.findobj().set_color(color)
        self.canvas.draw_idle()
    
    def get_color (self):
        return self.findobj().get_color()

    def set_backgroundcolor (self, color):
        self.findobj().set_backgroundcolor(color)
        self.canvas.draw_idle()
    
    def get_backgroundcolor(self):
        if self.findobj().get_bbox_patch() != None:
            return self.findobj().get_bbox_patch().get_facecolor()
        return 'white'
    
    def set_edgecolor (self, color):
        self.findobj().set_bbox({"edgecolor":color})
        self.canvas.draw_idle()
    
    def get_edgecolor(self):
        if self.findobj().get_bbox_patch():
            return self.findobj().get_bbox_patch().get_edgecolor()
        return 'white'
    
    def set_alpha (self, value):
        self.findobj().set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_alpha (self):
        if self.findobj().get_alpha() != None:
            return int(self.findobj().get_alpha()*100)
        return 100

class MFAxisLabel(QDialog):
    def __init__(self, canvas:MultiFigureCanvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f'Axis Label')
        layout = QVBoxLayout(self)
        self.canvas = canvas

        self.choose_axis = SegmentedWidget(parent)
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='X Axis', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Y Axis', func=lambda: self.stackedlayout.setCurrentIndex(1))
       
        self.choose_axis.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        xlabel = _AxisLabel('x', canvas, parent)
        self.stackedlayout.addWidget(xlabel)

        ylabel = _AxisLabel('y', canvas, parent)
        self.stackedlayout.addWidget(ylabel)
