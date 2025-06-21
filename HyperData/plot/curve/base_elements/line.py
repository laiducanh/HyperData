from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.button import TransparentComboBox, Toggle
from ui.base_widgets.spinbox import TransparentDoubleSpinBox, TransparentSpinBox
from ui.base_widgets.color import ColorDropdown
from plot.curve.base_elements.base import ArtistConfigBase
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib, marker_lib
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib import lines, colors, collections

DEBUG = False

class Line (ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()
    
    def initUI(self):

        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.setContentsMargins(0,0,0,0)
        
        self.linestyle = TransparentComboBox(
            text  = 'Line Style',
            items = linestyle_lib.values(),
            getter=self.get_linestyle,
            setter=self.set_linestyle,
            layout=self.mainlayout
        )

        self.solid_capstyle = TransparentComboBox(
            text  = "Solid Capstyle", 
            items = ['butt', 'projecting', 'round'],
            setter=self.set_solid_capstyle,
            getter=self.get_solid_capstyle,
            layout=self.mainlayout
        )
        
        self.solid_joinstyle = TransparentComboBox(
            text  = "Solid Joinstyle", 
            items = ['miter', 'round', 'bevel'],
            setter=self.set_solid_joinstyle,
            getter=self.get_solid_joinstyle,
            layout=self.mainlayout
        )

        self.dash_capstyle = TransparentComboBox(
            text  = "Dash Capstyle", 
            items = ['butt', 'projecting', 'round'],
            getter=self.get_dash_capstyle,
            setter=self.set_dash_capstyle,
            layout=self.mainlayout
        )
        self.dash_capstyle.hide()

        self.dash_joinstyle = TransparentComboBox(
            text  = "Dash Joinstyle", 
            items = ['miter', 'round', 'bevel'],
            getter=self.get_dash_joinstyle,
            setter=self.set_dash_joinstyle,
            layout=self.mainlayout
        )
        self.dash_joinstyle.hide()

        self.linewidth = TransparentDoubleSpinBox(
            text = 'Line Width',
            min = 0, max = 10, step = 0.5,
            getter=self.get_linewidth,
            setter=self.set_linewidth,
            layout=self.mainlayout
        )

        self.color = ColorDropdown(
            text  = 'Line Color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.mainlayout
        )

        self.alpha = TransparentSpinBox(
            text = 'Transparency',
            min = 0, max = 100, step = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.mainlayout
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
        try: return self.find_object()[0].get_linestyle()
        except: return "solid"
    
    def set_solid_capstyle(self, value):
        try:
            for obj in self.find_object():
                obj.set_solid_capstyle(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_solid_capstyle(self):
        try: return self.find_object()[0].get_solid_capstyle()
        except: return "butt"
    
    def set_solid_joinstyle(self, value):
        try:
            for obj in self.find_object():
                obj.set_solid_joinstyle(value)
            self.prepare_update()
        except Exception as e: 
            logger.exception(e)
    
    def get_solid_joinstyle(self):
        try: return self.find_object()[0].get_solid_joinstyle()
        except: return "miter"

    def set_dash_capstyle(self, value):
        try: 
            for obj in self.find_object():
                obj.set_dash_capstyle(value)
            self.prepare_update()
        except Exception as e: 
            logger.exception(e)
    
    def get_dash_capstyle(self):
        try: return self.find_object()[0].get_dash_capstyle()
        except: return "butt"

    def set_dash_joinstyle(self, value):
        try:
            for obj in self.find_object():
                obj.set_dash_joinstyle(value)
            self.prepare_update()
        except Exception as e: 
            logger.exception(e)
    
    def get_dash_joinstyle(self):
        try: return self.find_object()[0].get_dash_joinstyle()
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
        
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.setContentsMargins(0,0,0,0)

        self.marker = TransparentComboBox(
            text  = 'Marker Style',
            items = marker_lib.values(),
            getter=self.get_marker,
            setter=self.set_marker,
            layout=self.mainlayout
        )

        self.markersize = TransparentDoubleSpinBox(
            text = 'Marker Size',
            min = 0, step = 2,
            getter=self.get_markersize,
            setter=self.set_markersize,
            layout=self.mainlayout
        )

        self.markeredgewidth = TransparentDoubleSpinBox(
            text = 'Marker Edge Width',
            min = 0, max = 5, step = 0.5,
            getter=self.get_markeredgewidth,
            setter=self.set_markeredgewidth,
            layout=self.mainlayout
        )

        self.markerfacecolor = ColorDropdown(
            text  = 'Marker Face Color',
            getter=self.get_markerfacecolor,
            setter=self.set_markerfacecolor,
            layout=self.mainlayout
        )

        self.markeredgecolor = ColorDropdown(
            text  = 'Marker Edge Color',
            getter=self.get_markeredgecolor,
            setter=self.set_markeredgecolor,
            layout=self.mainlayout
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

class LineCollection (ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()
    
    def initUI(self):

        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.setContentsMargins(0,0,0,0)

        self.visible = Toggle(
            text="Visible",
            getter=self.get_visible,
            setter=self.set_visible,
            layout=self.mainlayout
        )

        self.linewidth = TransparentDoubleSpinBox(
            text = 'Line Width',
            min = 0, max = 10, step = 0.5,
            getter=self.get_linewidth,
            setter=self.set_linewidth,
            layout=self.mainlayout
        )

        self.color = ColorDropdown(
            text  = 'Line Color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.mainlayout
        )

        self.alpha = TransparentSpinBox(
            text = 'Transparency',
            min = 0, max = 100, step = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.mainlayout
        )
        
    def find_object(self) -> list[collections.LineCollection]:
        return find_mpl_object(
            source=self.canvas.figure,
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

class ErrorBarCollection (LineCollection):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)
    
    def find_object(self) -> list[collections.LineCollection, lines.Line2D]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[collections.LineCollection, lines.Line2D],
            gid=self.gid,
        )