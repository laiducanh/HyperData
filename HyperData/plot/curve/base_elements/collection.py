from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.button import TransparentComboBox, Toggle
from ui.base_widgets.spinbox import TransparentDoubleSpinBox, TransparentSpinBox
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

class SingleColorCollection(ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()

    def initUI(self):

        self.edgewidth = TransparentDoubleSpinBox(
            text = 'Edge Width',
            min = 0, max = 5, step = 0.1,
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
            min = 0, max = 100, step = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.vlayout
        )
    
    def find_object (self) -> List[Union[collections.Collection, collections.PolyCollection]]:
        return find_mpl_object(
            source=self.canvas.figure,
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
        except: self.get_facecolor()

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

class CmapCollection(ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()

    def initUI(self):

        self.edgewidth = TransparentDoubleSpinBox(
            text = 'Edge Width'
            ,min = 0, max = 5, step = 0.1,
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

        self.cmap_on = Toggle(
            text="Colormap On",
            getter=self.get_cmap_on,
            setter=self.set_cmap_on,
            layout=self.vlayout
        )

        self.cmap = TransparentComboBox(
            items = colormaps(), 
            text  = "Colormap",
            getter=self.get_cmap,
            setter=self.set_cmap,
            layout=self.vlayout
        )

        self.norm = TransparentComboBox(
            items = ['linear', 'log', 'logit', 'symlog','asinh'], 
            text  = "Norm",
            getter=self.get_norm,
            setter=self.set_norm,
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
            min = 0, max = 100, step = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.vlayout
        )
    
    def find_object (self) -> list[collections.Collection]:
        return find_mpl_object(
            source=self.canvas.figure,
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

class QuadMesh(ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()

    def initUI(self):

        self.edgewidth = TransparentDoubleSpinBox(
            text = 'Edge Width',
            min  = 0, max  = 5, step = 0.1,
            getter=self.get_edgewidth,
            setter=self.set_edgewidth,
            layout=self.vlayout
        )

        # linestyle in QuadMesh is a bug
        # self.edgestyle = TransparentComboBox(
        #     text  = 'Edge Style',
        #     items = linestyle_lib.values(),
        #     getter=self.get_edgestyle,
        #     setter=self.set_edgestyle,
        #     layout=self.mainlayout
        # )

        self.edgecolor = ColorDropdown(
            text  = 'Edge Color',
            getter=self.get_edgecolor,
            setter=self.set_edgecolor,
            layout=self.vlayout
        )

        self.cmap = TransparentComboBox(
            items = colormaps(), 
            text  = "Colormap",
            getter=self.get_cmap,
            setter=self.set_cmap,
            layout=self.vlayout
        )

        self.norm = TransparentComboBox(
            items = ['linear', 'log', 'logit', 'symlog','asinh'], 
            text  = "Norm",
            getter=self.get_norm,
            setter=self.set_norm,
            layout=self.vlayout
        )

        self.alpha = TransparentSpinBox(
            text = 'Transparency',
            min  = 0, max  = 100, step = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.vlayout
        )
    
    def find_object (self) -> list[collections.QuadMesh]:
        return find_mpl_object(source=self.canvas.figure,
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
                print(obj, value, obj.get_linestyle())
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
        except Exception as e:
            logger.exception(e)
    
    def set_edgecolor (self, value):
        try: 
            for obj in self.find_object():
                obj.set_edgecolor(value)
            self.prepare_update()
        except Exception as e:
            logger.exception(e)
    
    def get_edgecolor (self):
        try:
            if len(self.find_object()[0].get_edgecolor()) == 0:
                return colors.to_hex(self.find_object()[0].get_facecolor()[0])
            return colors.to_hex(self.find_object()[0].get_edgecolor()[0])
        except Exception as e:
            logger.exception(e)
    
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

class Poly3DCollection(ArtistConfigBase):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(gid, canvas, parent)

        self.initUI()

    def initUI(self):

        self.zsort = TransparentComboBox(
            items = ["average","min","max"], 
            text  = "Zsort",
            getter=self.get_zsort,
            setter=self.set_zsort,
            layout=self.vlayout
        )

        self.alpha = TransparentSpinBox(
            text = 'Transparency',
            min  = 0, max  = 100, step = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.vlayout
        )

    def find_object(self) -> List[art3d.Poly3DCollection]:
        return find_mpl_object(
            source=self.canvas.figure,
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