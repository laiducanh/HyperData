from PySide6.QtCore import Signal
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout, QWidget
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, Slider
from ui.base_widgets.color import ColorDropdown
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib import patches
from matplotlib import colors, scale
from typing import List

DEBUG = False

class Rectangle (QWidget):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()
        self.setParent(parent)
        self.initUI()
    
    def initUI (self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.edgewidth = DoubleSpinBox(text='Edge Width',min=0,max=5,step=0.5)
        self.edgewidth.button.setValue(self.get_edgewidth())
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='Edge Style',items=linestyle_lib.values())
        self.edgestyle.button.setCurrentText(self.get_edgestyle())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        layout.addWidget(self.edgestyle)

        self.facecolor = ColorDropdown(text='Face Color',color=self.get_facecolor(), parent=self.parent())
        self.facecolor.button.colorChanged.connect(self.set_facecolor)
        layout.addWidget(self.facecolor)

        self.edgecolor = ColorDropdown(text='Edge Color',color=self.get_edgecolor(), parent=self.parent())
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(self.edgecolor)

        self.alpha = Slider(text='Transparency',min=0,max=100)
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)
    
    def find_object (self) -> List[patches.Rectangle | patches.PathPatch]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[patches.Rectangle, patches.PathPatch],
                               gid=self.gid)

    def update_props(self, button=None):
        if button != self.edgestyle.button:
            self.edgestyle.button.setCurrentText(self.get_edgestyle())

        if button != self.edgewidth.button:
            self.edgewidth.button.setValue(self.get_edgewidth())
        
        if button != self.facecolor.button:
            self.facecolor.button.setColor(self.get_facecolor())
        
        if button != self.edgecolor.button:
            self.edgecolor.button.setColor(self.get_edgecolor())
        
        if button != self.alpha.button:
            self.alpha.button.setValue(self.get_alpha())
    
    def update_plot(self, *args, **kwargs):
        # self.sig.emit()
        self.canvas.draw_idle()
        self.update_props(*args, **kwargs)

    def set_edgestyle(self, value:str):
        try:
            for obj in self.obj:
                obj.set_linestyle(value.lower())
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgestyle.button)
    
    def get_edgestyle(self):
        return self.obj[0].get_linestyle()
    
    def set_edgewidth(self, value):
        try:
            for obj in self.obj:
                obj.set_linewidth(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgewidth.button)
    
    def get_edgewidth (self):
        return self.obj[0].get_linewidth()
    
    def set_alpha(self, value):
        try: 
            for obj in self.obj:
                obj.set_alpha(float(value/100))
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.alpha.button)
    
    def get_alpha (self):
        if self.obj[0].get_alpha() == None:
            return 100
        return int(self.obj[0].get_alpha()*100)

    def set_facecolor (self, value):
        try:
            for obj in self.obj:
                obj.set_facecolor(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.facecolor.button)
    
    def get_facecolor(self):
        return colors.to_hex(self.obj[0].get_facecolor())
    
    def set_edgecolor (self, value):
        try:
            for obj in self.obj:
                obj.set_edgecolor(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgecolor.button)
    
    def get_edgecolor (self):
        return colors.to_hex(self.obj[0].get_edgecolor())
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()
        return super().paintEvent(a0)
    
class Wedge(Rectangle):
    """ same as Rectangle, but overwrite set and get functions """
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

    def find_object(self) -> List[patches.Wedge]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[patches.Wedge],
                               gid=self.gid)