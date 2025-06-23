from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.button import TransparentComboBox
from ui.base_widgets.spinbox import TransparentDoubleSpinBox, TransparentSpinBox
from ui.base_widgets.color import ColorDropdown
from plot.curve.base_elements.base import ArtistConfigBase
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib import patches, colors
import numpy as np

DEBUG = False

class Rectangle(ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()
    
    def initUI(self):

        self.edgewidth = TransparentDoubleSpinBox(
            text = 'Edge Width',
            min  = 0, max  = 5, step = 0.5,
            getter=self.get_edgewidth,
            setter=self.set_edgewidth,
            layout=self.vlayout
        )

        self.edgestyle = TransparentComboBox(
            text  = 'Edge Style',
            items = linestyle_lib.values(),
            getter=self.get_edgestyle,
            setter=self.set_edgestyle,
            layout=self.vlayout
        )

        self.facecolor = ColorDropdown(
            text  = 'Face Color',
            getter=self.get_facecolor,
            setter=self.set_facecolor,
            layout=self.vlayout
        )

        self.edgecolor = ColorDropdown(
            text  = 'Edge Color',
            getter=self.get_edgecolor,
            setter=self.set_edgecolor,
            layout=self.vlayout
        )

        self.alpha = TransparentSpinBox(
            text = 'Transparency',
            min  = 0, max  = 100, step = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.vlayout
        )

    def find_object (self) -> list[patches.Patch]:
        return find_mpl_object(
            source=self.canvas.figure,
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

class Wedge(Rectangle):
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

    def find_object(self) -> list[patches.Wedge]:
        return find_mpl_object(
            source=self.canvas.figure,
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
            for obj in self.find_object():
                c = np.asarray(colors.to_rgba(value))
                color = (1-1/i)*(1-c) + c
                obj.set_facecolor(color)
                i += 1/len(self.find_object())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)