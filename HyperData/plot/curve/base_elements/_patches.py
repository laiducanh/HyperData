from PySide6.QtCore import Signal, QTimer
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, Slider
from ui.base_widgets.color import ColorDropdown
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from plot.curve.base_elements.base import ArtistConfigBase
from matplotlib import patches
from matplotlib import colors
import numpy as np

DEBUG = False

class Rectangle (ArtistConfigBase):
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent=parent)

        self.obj: list[patches.Patch]
    
    def initUI (self):
        super().initUI()

        self.edgewidth = DoubleSpinBox(text='Edge Width',min=0,max=5,step=0.5)
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        self._layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='Edge Style',items=linestyle_lib.values())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        self._layout.addWidget(self.edgestyle)

        self.facecolor = ColorDropdown(text='Face Color',color=self.get_facecolor(), parent=self.parent())
        self.facecolor.button.colorChanged.connect(self.set_facecolor)
        self._layout.addWidget(self.facecolor)

        self.edgecolor = ColorDropdown(text='Edge Color',color=self.get_edgecolor(), parent=self.parent())
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        self._layout.addWidget(self.edgecolor)

        self.alpha = Slider(text='Transparency',min=0,max=100)
        self.alpha.button.valueChanged.connect(self.set_alpha)
        self._layout.addWidget(self.alpha)
    
    def find_object (self) -> list[patches.Patch]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Rectangle, patches.PathPatch, patches.FancyBboxPatch],
            gid=self.gid,
        )

    def update_props(self):
        self.edgestyle.button.setCurrentText(self.get_edgestyle())
        self.edgewidth.button.setValue(self.get_edgewidth())
        self.facecolor.button.setColor(self.get_facecolor())
        self.edgecolor.button.setColor(self.get_edgecolor())
        self.alpha.button.setValue(self.get_alpha())

    def set_edgestyle(self, value:str):
        try:
            for obj in self.obj:
                obj.set_linestyle(value.lower())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgestyle(self):
        return self.obj[0].get_linestyle()
    
    def set_edgewidth(self, value):
        try:
            for obj in self.obj:
                obj.set_linewidth(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgewidth (self):
        return self.obj[0].get_linewidth()
    
    def set_alpha(self, value):
        try: 
            for obj in self.obj:
                obj.set_alpha(float(value/100))
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_alpha (self):
        if not self.obj[0].get_alpha():
            return 100
        return int(self.obj[0].get_alpha()*100)

    def set_facecolor (self, value):
        try:
            for obj in self.obj:
                obj.set_facecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_facecolor(self):
        return colors.to_hex(self.obj[0].get_facecolor())
    
    def set_edgecolor (self, value):
        try:
            for obj in self.obj:
                obj.set_edgecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgecolor (self):
        return colors.to_hex(self.obj[0].get_edgecolor())
    
class Wedge(Rectangle):
    """ same as Rectangle, but overwrite set and get functions """
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.obj: list[patches.Wedge]

    def find_object(self) -> list[patches.Wedge]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Wedge],
            gid=self.gid
        )

class MultiWedges(Wedge):
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
            for obj in self.obj:
                c = np.asarray(colors.to_rgba(value))
                color = (1-1/i)*(1-c) + c
                obj.set_facecolor(color)
                i += 1/len(self.obj)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
