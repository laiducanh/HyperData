from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from ui.base_widgets.color import ColorDropdown
from plot.curve.base_elements.base import ArtistConfigBase
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib import patches, colors
import numpy as np

DEBUG = False

class Rectangle (ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.edgewidth = DoubleSpinBox(
            text = 'Edge Width',
            min  = 0, 
            max  = 5, 
            step = 0.5
        )
        self.edgewidth.button.setValue(self.get_edgewidth())
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(
            text  = 'Edge Style',
            items = linestyle_lib.values()
        )
        self.edgestyle.button.setCurrentText(self.get_edgestyle())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        layout.addWidget(self.edgestyle)

        self.facecolor = ColorDropdown(
            text  = 'Face Color',
            color = self.get_facecolor()
        )
        self.facecolor.button.colorChanged.connect(self.set_facecolor)
        layout.addWidget(self.facecolor)

        self.edgecolor = ColorDropdown(
            text  = 'Edge Color',
            color = self.get_edgecolor()
        )
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(self.edgecolor)

        self.alpha = SpinBox(
            text = 'Transparency',
            min  = 0, 
            max  = 100, 
            step = 10
        )
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)

    def find_object (self) -> list[patches.Patch]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Rectangle, patches.PathPatch, patches.FancyBboxPatch],
            gid=self.gid,
        )

    def set_edgestyle(self, value:str):
        try:
            for obj in self.find_object():
                obj.set_linestyle(value.lower())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgestyle(self):
        return self.find_object()[0].get_linestyle()
    
    def set_edgewidth(self, value):
        try:
            for obj in self.find_object():
                obj.set_linewidth(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgewidth (self):
        return self.find_object()[0].get_linewidth()
    
    def set_alpha(self, value):
        try: 
            for obj in self.find_object():
                obj.set_alpha(float(value/100))
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_alpha (self):
        if not self.find_object()[0].get_alpha():
            return 100
        return int(self.find_object()[0].get_alpha()*100)

    def set_facecolor (self, value):
        try:
            for obj in self.find_object():
                obj.set_facecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_facecolor(self):
        return colors.to_hex(self.find_object()[0].get_facecolor())
    
    def set_edgecolor (self, value):
        try:
            for obj in self.find_object():
                obj.set_edgecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgecolor (self):
        return colors.to_hex(self.find_object()[0].get_edgecolor())

class Wedge (Rectangle):
    """ same as Rectangle, but overwrite find_object() """
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

    def find_object(self) -> list[patches.Wedge]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Wedge],
            gid=self.gid
        )

class MultiWedges (Wedge):
    """ 
        this class behaves the same as Wedge except for 
        set_facecolor function lightenes the color to 
        set for multiple wedges 
    """
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

    def set_facecolor (self, value):
        try:
            i = 1
            for obj in self.find_object():
                c = np.asarray(colors.to_rgba(value))
                color = (1-1/i)*(1-c) + c
                obj.set_facecolor(color)
                i += 1/len(self.find_object())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)