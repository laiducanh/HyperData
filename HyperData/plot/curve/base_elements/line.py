from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from ui.base_widgets.color import HColorDropdown
from plot.curve.base_elements.base import ArtistConfigBase
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib, marker_lib
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib import lines, colors, collections

DEBUG = False

class Line(ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()
    
    def initUI(self):
        
        self.linestyle = HTransparentComboBox(
            label  = 'Line Style',
            items = linestyle_lib.values(),
            getter=self.get_linestyle,
            setter=self.set_linestyle,
            layout=self.vlayout
        )

        self.capstyle = HTransparentComboBox(
            label  = "Capstyle", 
            items = ['butt', 'projecting', 'round'],
            setter=self.set_capstyle,
            getter=self.get_capstyle,
            layout=self.vlayout
        )
        
        self.joinstyle = HTransparentComboBox(
            label  = "Joinstyle", 
            items = ['miter', 'round', 'bevel'],
            setter=self.set_joinstyle,
            getter=self.get_joinstyle,
            layout=self.vlayout
        )

        self.linewidth = HTransparentDoubleSpinBox(
            label = 'Line Width',
            minimum = 0, maximum = 10, singleStep = 0.5,
            getter=self.get_linewidth,
            setter=self.set_linewidth,
            layout=self.vlayout
        )

        self.color = HColorDropdown(
            label  = 'Line Color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.alpha = HTransparentSpinBox(
            label = 'Transparency',
            minimum = 0, maximum = 100, singleStep = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.vlayout
        )

    def find_object(self) -> list[lines.Line2D]:
        return find_mpl_object(
            self.canvas.figure, 
            match=[lines.Line2D], 
            gid=self.gid
        )
    
    def set_visible(self, value:bool):
        try:
            for obj in self.find_object():
                obj.set_visible(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_visible(self) -> bool:
        return self.find_object()[0].get_visible()
    
    def set_linestyle(self, value:str):
        try:
            for obj in self.find_object():
                obj.set_linestyle(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_linestyle(self):
        try: return linestyle_lib[self.find_object()[0].get_linestyle()]
        except: return "solid"
    
    def set_capstyle(self, value):
        try:
            for obj in self.find_object():
                obj.set_solid_capstyle(value)
                obj.set_dash_capstyle(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_capstyle(self):
        try: return self.find_object()[0].get_solid_capstyle()
        except: return "butt"
    
    def set_joinstyle(self, value):
        try:
            for obj in self.find_object():
                obj.set_solid_joinstyle(value)
                obj.set_dash_joinstyle(value)
            self.prepare_update()
        except Exception as e: 
            logger.exception(e)
    
    def get_joinstyle(self):
        try: return self.find_object()[0].get_solid_joinstyle()
        except: return "miter"
    
    def set_linewidth(self, value):
        try: 
            for obj in self.find_object():
                obj.set_linewidth(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_linewidth (self):
        try: return self.find_object()[0].get_linewidth()
        except: return 1
    
    def set_alpha(self, value):
        try: 
            for obj in self.find_object():
                obj.set_alpha(float(value/100))
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_alpha (self):
        try:
            if self.find_object()[0].get_alpha() == None:
                return 100
            return int(self.find_object()[0].get_alpha()*100)
        except: return 100

    def set_color(self, color):
        try: 
            for obj in self.find_object():
                obj.set_color(color)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_color(self):
        try: return colors.to_hex(self.find_object()[0].get_color())
        except: return "black"


class Marker(ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()
    
    def initUI(self):

        self.marker = HTransparentComboBox(
            label  = 'Marker Style',
            items = marker_lib.values(),
            getter=self.get_marker,
            setter=self.set_marker,
            layout=self.vlayout
        )

        self.markersize = HTransparentDoubleSpinBox(
            label = 'Marker Size',
            minimum = 0, singleStep = 2,
            getter=self.get_markersize,
            setter=self.set_markersize,
            layout=self.vlayout
        )

        self.markeredgewidth = HTransparentDoubleSpinBox(
            label = 'Marker Edge Width',
            minimum = 0, maximum = 5, singleStep = 0.5,
            getter=self.get_markeredgewidth,
            setter=self.set_markeredgewidth,
            layout=self.vlayout
        )

        self.markerfacecolor = HColorDropdown(
            label  = 'Marker Face Color',
            getter=self.get_markerfacecolor,
            setter=self.set_markerfacecolor,
            layout=self.vlayout
        )

        self.markeredgecolor = HColorDropdown(
            label  = 'Marker Edge Color',
            getter=self.get_markeredgecolor,
            setter=self.set_markeredgecolor,
            layout=self.vlayout
        )

    def find_object (self) -> list[lines.Line2D]:
        return find_mpl_object(
            self.canvas.figure, 
            [lines.Line2D], 
            gid=self.gid
        )
    
    def set_marker (self, marker):
        try:
            marker = list(marker_lib.keys())[list(marker_lib.values()).index(marker.lower())]
            for obj in self.find_object():
                obj.set_marker(marker)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_marker(self):
        try:
            if not self.find_object()[0].get_marker():
                return "None"
            return marker_lib[self.find_object()[0].get_marker()]
        except: return "None"

    def set_markersize (self, value):
        try: 
            for obj in self.find_object():
                obj.set_markersize(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_markersize(self):
        try: return self.find_object()[0].get_markersize()
        except: return 0

    def set_markeredgewidth(self, value):
        try: 
            for obj in self.find_object():
                obj.set_markeredgewidth(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_markeredgewidth(self):
        try: return self.find_object()[0].get_markeredgewidth()
        except: return 0

    def set_markerfacecolor(self, color):
        try: 
            for obj in self.find_object():
                obj.set_markerfacecolor(color)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_markerfacecolor(self):
        try: return colors.to_hex(self.find_object()[0].get_markerfacecolor())
        except: return "black"

    def set_markeredgecolor(self, color):
        try: 
            for obj in self.find_object():
                obj.set_markeredgecolor(color)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_markeredgecolor(self):
        try: return colors.to_hex(self.find_object()[0].get_markeredgecolor())
        except: return "black"

class LineCollection(ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()
    
    def initUI(self):

        self.visible = HToggle(
            label="Visible",
            getter=self.get_visible,
            setter=self.set_visible,
            layout=self.vlayout
        )

        self.linewidth = HTransparentDoubleSpinBox(
            label = 'Line Width',
            minimum = 0, maximum = 10, singleStep = 0.5,
            getter=self.get_linewidth,
            setter=self.set_linewidth,
            layout=self.vlayout
        )

        self.color = HColorDropdown(
            label  = 'Line Color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.alpha = HTransparentSpinBox(
            label = 'Transparency',
            minimum = 0, maximum = 100, singleStep = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.vlayout
        )
        
    def find_object(self) -> list[collections.LineCollection]:
        return find_mpl_object(
            figure=self.canvas.figure,
            match=[collections.LineCollection],
            gid=self.gid,
        )

    def set_visible(self, value:bool):
        try:
            for obj in self.find_object():
                obj.set_visible(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_visible(self) -> bool:
        return self.find_object()[0].get_visible()
    
    def set_linestyle(self, value:str):
        try:
            for obj in self.find_object():
                obj.set_linestyle(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_linestyle(self):
        try: return self.find_object()[0].get_linestyle()
        except: return "solid"
    
    def set_linewidth(self, value):
        try: 
            for obj in self.find_object():
                obj.set_linewidth(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_linewidth (self):
        try: return self.find_object()[0].get_linewidth()
        except: return 1
    
    def set_alpha(self, value):
        try: 
            for obj in self.find_object():
                obj.set_alpha(float(value/100))
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_alpha (self):
        try:
            if self.find_object()[0].get_alpha() == None:
                return 100
            return int(self.find_object()[0].get_alpha()*100)
        except: return 100

    def set_color(self, color):
        try: 
            for obj in self.find_object():
                obj.set_edgecolor(color)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_color(self):
        try:
            return colors.to_hex(self.find_object()[0].get_color()[0])
        except: return "black"

class ErrorBarCollection(LineCollection):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)
    
    def find_object(self) -> list[collections.LineCollection, lines.Line2D]:
        return find_mpl_object(
            figure=self.canvas.figure,
            match=[collections.LineCollection, lines.Line2D],
            gid=self.gid,
        )