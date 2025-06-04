from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        
        self.linestyle = ComboBox(
            text  = 'Line Style',
            items = linestyle_lib.values()
        )
        self.linestyle.button.setCurrentText(self.get_linestyle())
        self.linestyle.button.currentTextChanged.connect(self.set_linestyle)
        layout.addWidget(self.linestyle)

        self.solid_capstyle = ComboBox(
            text  = "Solid Capstyle", 
            items = ['butt', 'projecting', 'round']
        )
        self.solid_capstyle.button.setCurrentText(self.get_solid_capstyle())
        self.solid_capstyle.button.currentTextChanged.connect(self.set_solid_capstyle)
        layout.addWidget(self.solid_capstyle)

        self.solid_joinstyle = ComboBox(
            text  = "Solid Joinstyle", 
            items = ['miter', 'round', 'bevel']
        )
        self.solid_joinstyle.button.setCurrentText(self.get_solid_joinstyle())
        self.solid_joinstyle.button.currentTextChanged.connect(self.set_solid_joinstyle)
        layout.addWidget(self.solid_joinstyle)

        self.dash_capstyle = ComboBox(
            text  = "Dash Capstyle", 
            items = ['butt', 'projecting', 'round']
        )
        self.dash_capstyle.button.setCurrentText(self.get_dash_capstyle())
        self.dash_capstyle.button.currentTextChanged.connect(self.set_dash_capstyle)
        self.dash_capstyle.hide()
        layout.addWidget(self.dash_capstyle)

        self.dash_joinstyle = ComboBox(
            text  = "Dash Joinstyle", 
            items = ['miter', 'round', 'bevel']
        )
        self.dash_joinstyle.button.setCurrentText(self.get_dash_joinstyle())
        self.dash_joinstyle.button.currentTextChanged.connect(self.set_dash_joinstyle)
        self.dash_joinstyle.hide()
        layout.addWidget(self.dash_joinstyle)

        self.linewidth = DoubleSpinBox(
            text = 'Line Width',
            min = 0, max = 10, step = 0.5
        )
        self.linewidth.button.setValue(self.get_linewidth())
        self.linewidth.button.valueChanged.connect(self.set_linewidth)
        layout.addWidget(self.linewidth)

        self.color = ColorDropdown(
            text  = 'Line Color',
            color = self.get_color()
        )
        self.color.button.colorChanged.connect(self.set_color)
        layout.addWidget(self.color)

        self.alpha = SpinBox(
            text = 'Transparency',
            min = 0, max = 100, step = 10
        )
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)

    def find_object(self) -> list[lines.Line2D]:
        return find_mpl_object(
            self.canvas.fig, 
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
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.marker = ComboBox(
            text  = 'Marker Style',
            items = marker_lib.values()
        )
        self.marker.button.setCurrentText(self.get_marker())
        self.marker.button.currentTextChanged.connect(self.set_marker)
        layout.addWidget(self.marker)

        self.markersize = DoubleSpinBox(
            text = 'Marker Size',
            min = 0, step = 2
        )
        self.markersize.button.setValue(self.get_markersize())
        self.markersize.button.valueChanged.connect(self.set_markersize)
        layout.addWidget(self.markersize)

        self.markeredgewidth = DoubleSpinBox(
            text = 'Marker Edge Width',
            min = 0, max = 5, step = 0.5
        )
        self.markeredgewidth.button.setValue(self.get_markeredgewidth())
        self.markeredgewidth.button.valueChanged.connect(self.set_markeredgewidth)
        layout.addWidget(self.markeredgewidth)

        self.markerfacecolor = ColorDropdown(
            text  = 'Marker Face Color',
            color = self.get_markerfacecolor()
        )
        self.markerfacecolor.button.setColor(self.get_markerfacecolor())
        self.markerfacecolor.button.colorChanged.connect(self.set_markerfacecolor)
        layout.addWidget(self.markerfacecolor)

        self.markeredgecolor = ColorDropdown(
            text  = 'Marker Edge Color',
            color = self.get_markeredgecolor()
        )
        self.markeredgecolor.button.setColor(self.get_markeredgecolor())
        self.markeredgecolor.button.colorChanged.connect(self.set_markeredgecolor)
        layout.addWidget(self.markeredgecolor)

    def find_object (self) -> list[lines.Line2D]:
        return find_mpl_object(
            self.canvas.fig, 
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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.visible = Toggle(text="Visible")
        self.visible.button.setChecked(self.get_visible())
        self.visible.button.checkedChanged.connect(self.set_visible)
        layout.addWidget(self.visible)

        self.linewidth = DoubleSpinBox(
            text = 'Line Width',
            min = 0, max = 10, step = 0.5
        )
        self.linewidth.button.setValue(self.get_linewidth())
        self.linewidth.button.valueChanged.connect(self.set_linewidth)
        layout.addWidget(self.linewidth)

        self.color = ColorDropdown(
            text  = 'Line Color',
            color = self.get_color()
        )
        self.color.button.setColor(self.get_color())
        self.color.button.colorChanged.connect(self.set_color)
        layout.addWidget(self.color)

        self.alpha = SpinBox(
            text = 'Transparency',
            min = 0, max = 100, step = 10
        )
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)
        
    def find_object(self) -> list[collections.LineCollection]:
        return find_mpl_object(
            source=self.canvas.fig,
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
            return colors.to_hex(self.find_object()[0].get_edgecolor()[0])
        except: return "black"

class ErrorBarCollection (LineCollection):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)
    
    def find_object(self) -> list[collections.LineCollection, lines.Line2D]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[collections.LineCollection, lines.Line2D],
            gid=self.gid,
        )