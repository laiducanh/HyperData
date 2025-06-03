from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from ui.base_widgets.color import ColorDropdown
from plot.curve.base_elements.base import ArtistConfigBase
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib import scale, colors, collections, rcParams
from matplotlib.pyplot import colormaps
from mpl_toolkits.mplot3d import art3d
from typing import Union, List
import numpy

DEBUG = False

class SingleColorCollection (ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.edgewidth = DoubleSpinBox(
            text = 'Edge Width',
            min = 0, max = 5, step = 0.1
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
            min = 0, max = 100, step = 10
        )
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)
    
    def find_object (self) -> List[Union[collections.Collection, collections.PolyCollection]]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[collections.Collection, collections.PolyCollection],
            gid=self.gid
        )
    
    def set_edgewidth (self, value):
        try: 
            for obj in self.find_object():
                obj.set_linewidth(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgewidth (self):
        try:
            return self.find_object()[0].get_linewidth()
        except: return 1

    def set_edgestyle (self, value:str):
        try: 
            for obj in self.find_object():
                obj.set_linestyle(value.lower())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgestyle (self):
        try:
            ls = self.find_object()[0].get_linestyle()
            if ls[0][1] == [3.7, 1.6]:
                return "dashed"
            elif ls[0][1] == [6.4, 1.6, 1.0, 1.6]:
                return "dashdot"
            elif ls[0][1] == [1.0, 1.65]:
                return "dotted"
            else:
                return "solid"
        except: return "solid"
    
    def set_facecolor (self, value):
        try: 
            for obj in self.find_object():
                obj.set_facecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_facecolor(self):
        try: 
            return colors.to_hex(self.find_object()[0].get_facecolor()[0])
        except: return "black"

    def set_edgecolor (self, value):
        try: 
            for obj in self.find_object():
                obj.set_edgecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgecolor (self):
        try:
            return colors.to_hex(self.find_object()[0].get_edgecolor()[0])
        except: return "black"

    def set_alpha (self, value):
        try: 
            for obj in self.find_object():
                obj.set_alpha(value/100)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)

    def get_alpha (self):
        try:
            if self.find_object()[0].get_alpha():
                return int(self.find_object()[0].get_alpha()*100)
            return 100
        except: return 100

class CmapCollection (ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.edgewidth = DoubleSpinBox(
            text = 'Edge Width'
            ,min = 0, max = 5, step = 0.1
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

        self.cmap_on = Toggle(text="Colormap On")
        self.cmap_on.button.setChecked(self.get_cmap_on())
        self.cmap_on.button.checkedChanged.connect(self.set_cmap_on)
        layout.addWidget(self.cmap_on)

        self.cmap = ComboBox(
            items = colormaps(), 
            text  = "Colormap"
        )
        self.cmap.button.setCurrentText(self.get_cmap())
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        layout.addWidget(self.cmap)

        self.norm = ComboBox(
            items = ['linear', 'log', 'logit', 'symlog','asinh'], 
            text  = "Norm"
        )
        self.norm.button.setCurrentText(self.get_norm())
        self.norm.button.currentTextChanged.connect(self.set_norm)
        layout.addWidget(self.norm)

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
            min = 0, max = 100, step = 10
        )
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)
    
    def find_object (self) -> list[collections.Collection]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[collections.Collection],
            gid=self.gid
        )
    
    def set_cmap_on (self, checked):
        if checked:
            self.set_cmap(self.cmap.button.currentText().lower())
            self.set_norm(self.norm.button.currentText().lower())
        else:
            self.set_cmap(None)
            self.set_norm(None)
                
    def get_cmap_on(self):
        if isinstance(self.find_object()[0].get_array(), numpy.ma.core.MaskedArray):
            return True
        return False
    
    def set_edgewidth (self, value):
        try: 
            for obj in self.find_object():
                obj.set_linewidth(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgewidth (self):
        return self.find_object()[0].get_linewidth()
    
    def set_edgestyle (self, value:str):
        try: 
            for obj in self.find_object():
                obj.set_linestyle(value.lower())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgestyle (self):
        ls = self.find_object()[0].get_linestyle()
        if ls[0][1] == [3.7, 1.6]:
            return "dashed"
        elif ls[0][1] == [6.4, 1.6, 1.0, 1.6]:
            return "dashdot"
        elif ls[0][1] == [1.0, 1.65]:
            return "dotted"
        else:
            return "solid"
    
    def set_cmap(self, value:Union[str,None]):
        try:
            if value:
                for obj in self.find_object():
                    obj.set_array(self.find_object()[0].get_offsets().transpose()[0])
                for _cmap in colormaps():
                    if _cmap.lower() == value.lower():
                        for obj in self.find_object():
                            obj.set_cmap(_cmap)
            else:
                for obj in self.find_object():
                    obj.set_array(value)
                    obj.set_cmap(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_cmap(self) -> str:
        return self.find_object()[0].get_cmap().name

    def set_norm (self, value:Union[str,None]):
        try:
            if value: 
                value = value.lower()
            for obj in self.find_object():
                obj.set_norm(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)

    def get_norm(self) -> str:
        _scale_mapping = scale._scale_mapping
        for key, value in _scale_mapping.items():
            if type(self.find_object()[0].norm._scale) == value:
                return key
        return "linear"
    
    def set_facecolor (self, value):
        try: 
            for obj in self.find_object():
                obj.set_facecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_facecolor(self):
        return colors.to_hex(self.find_object()[0].get_facecolor()[0])
    
    def set_edgecolor (self, value):
        try: 
            for obj in self.find_object():
                obj.set_edgecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgecolor (self):
        if len(self.find_object()[0].get_edgecolor()) > 1:
            return colors.to_hex(self.find_object()[0].get_edgecolor()[0])
        return self.get_facecolor()

    def set_alpha (self, value):
        try: 
            for obj in self.find_object():
                obj.set_alpha(value/100)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)

    def get_alpha (self):
        if self.find_object()[0].get_alpha():
            return int(self.find_object()[0].get_alpha()*100)
        return 100

class QuadMesh (ArtistConfigBase):
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
            step = 0.1
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

        self.edgecolor = ColorDropdown(
            text  = 'Edge Color',
            color = self.get_edgecolor()
        )
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(self.edgecolor)

        self.cmap = ComboBox(
            items = colormaps(), 
            text  = "Colormap"
        )
        self.cmap.button.setCurrentText(self.get_cmap())
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        layout.addWidget(self.cmap)

        self.norm = ComboBox(
            items = ['linear', 'log', 'logit', 'symlog','asinh'], 
            text  = "Norm"
        )
        self.norm.button.setCurrentText(self.get_norm())
        self.norm.button.currentTextChanged.connect(self.set_norm)
        layout.addWidget(self.norm)

        self.alpha = SpinBox(
            text = 'Transparency',
            min  = 0,
            max  = 100,
            step = 10
        )
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)
    
    def find_object (self) -> list[collections.QuadMesh]:
        return find_mpl_object(source=self.canvas.fig,
                               match=[collections.QuadMesh],
                               gid=self.gid)
    
   
    def set_edgewidth (self, value):
        try: 
            for obj in self.find_object():
                obj.set_linewidth(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgewidth (self):
        try: return self.find_object()[0].get_linewidth()
        except: return 1 
    
    def set_edgestyle (self, value:str):
        try: 
            for obj in self.find_object():
                obj.set_linestyle(value.lower())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgestyle (self):
        try: 
            ls = self.find_object()[0].get_linestyle()
            if ls[0][1] == [3.7, 1.6]:
                return "dashed"
            elif ls[0][1] == [6.4, 1.6, 1.0, 1.6]:
                return "dashdot"
            elif ls[0][1] == [1.0, 1.65]:
                return "dotted"
            else:
                return "solid"
        except: return "solid"
    
    def set_edgecolor (self, value):
        try: 
            for obj in self.find_object():
                obj.set_edgecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgecolor (self):
        try:
            if len(self.find_object()[0].get_edgecolor()) > 1:
                return colors.to_hex(self.find_object()[0].get_edgecolor()[0])
            return colors.to_hex(self.find_object()[0].get_facecolor()[0])
        except: "black"
    
    def set_cmap(self, value:str):
        try:
            for obj in self.find_object():
                obj.set_cmap(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_cmap(self) -> str:
        try: return self.find_object()[0].get_cmap().name
        except: return rcParams["image.cmap"]

    def set_norm (self, value:str):
        try:
            for obj in self.find_object():
                obj.set_norm(value.lower())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)

    def get_norm(self) -> str:
        try:
            _scale_mapping = scale._scale_mapping
            for key, value in _scale_mapping.items():
                if type(self.find_object()[0].norm._scale) == value:
                    return key
            return "linear"
        except: return "linear"

    def set_alpha (self, value):
        try: 
            for obj in self.find_object():
                obj.set_alpha(value/100)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)

    def get_alpha (self):
        try:
            if self.find_object()[0].get_alpha():
                return int(self.find_object()[0].get_alpha()*100)
            return 100
        except: return 100

class Poly3DCollection (ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.zsort = ComboBox(
            items = ["average","min","max"], 
            text  = "Zsort"
        )
        self.zsort.button.setCurrentText(self.get_zsort())
        self.zsort.button.currentTextChanged.connect(self.set_zsort)
        layout.addWidget(self.zsort)

        self.alpha = SpinBox(
            text = 'Transparency',
            min  = 0,
            max  = 100,
            step = 10
        )
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)

    def find_object(self) -> List[art3d.Poly3DCollection]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[art3d.Poly3DCollection],
            gid=self.gid
        )
    
    def update_props(self):
        self.zsort.button.setCurrentText(self.get_zsort())
        self.alpha.button.setValue(self.get_alpha())

    def set_zsort(self, value:str):
        try:
            for obj in self.find_object():
                obj.set_zsort(value.lower())
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_zsort(self) -> str:
        zsort_functions = self.find_object()[0]._zsort_functions
        zsort_func = self.find_object()[0]._zsortfunc
        return list(zsort_functions.keys())[list(zsort_functions.values()).index(zsort_func)]

    def set_alpha (self, value):
        try: 
            for obj in self.find_object():
                obj.set_alpha(value/100)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)

    def get_alpha (self):
        try:
            if self.find_object()[0].get_alpha():
                return int(self.find_object()[0].get_alpha()*100)
            return 100
        except: return 100