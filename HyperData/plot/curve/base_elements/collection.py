from PySide6.QtCore import Signal
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout, QWidget
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import DoubleSpinBox, Slider
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib.collections import Collection, PolyCollection
from matplotlib.collections import QuadMesh as Mesh
from mpl_toolkits.mplot3d import art3d
from matplotlib import colors, scale
from matplotlib.pyplot import colormaps
import matplotlib, numpy
from typing import List

DEBUG = False

class SingleColorCollection (QWidget):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()
        self.setParent(parent)
        self.initUI()

    def initUI (self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self._layout.addWidget(TitleLabel('PolyCollection'))
        self._layout.addWidget(SeparateHLine())

        self.edgewidth = DoubleSpinBox(text='Edge Width',min=0,max=5,step=0.1)
        self.edgewidth.button.setValue(self.get_edgewidth())
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        self._layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='Edge Style',items=linestyle_lib.values())
        self.edgestyle.button.setCurrentText(self.get_edgestyle())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        self._layout.addWidget(self.edgestyle)

        self.facecolor = ColorDropdown(text='Face Color',color=self.get_facecolor(), parent=self.parent())
        self.facecolor.button.colorChanged.connect(self.set_facecolor)
        self._layout.addWidget(self.facecolor)

        self.edgecolor = ColorDropdown(text='Edge Color',color=self.get_edgecolor(), parent=self.parent())
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        self._layout.addWidget(self.edgecolor)

        self.alpha = Slider(text='Transparency',min=0,max=100)
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        self._layout.addWidget(self.alpha)

        self._layout.addStretch()
    
    def find_object (self) -> List[Collection | PolyCollection]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[Collection, PolyCollection],
                               gid=self.gid)
    
    def update_props(self, button=None):
        if button != self.edgewidth.button:
            self.edgewidth.button.setValue(self.get_edgewidth())
        if button != self.edgestyle.button:
            self.edgestyle.button.setCurrentText(self.get_edgestyle())
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

    def set_edgewidth (self, value):
        try: 
            for obj in self.obj:
                obj.set_linewidth(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgewidth.button)
    
    def get_edgewidth (self):
        try:
            return self.obj[0].get_linewidth()
        except: return 1

    def set_edgestyle (self, value:str):
        try: 
            for obj in self.obj:
                obj.set_linestyle(value.lower())
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgestyle.button)
    
    def get_edgestyle (self):
        try:
            ls = self.obj[0].get_linestyle()
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
            for obj in self.obj:
                obj.set_facecolor(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.facecolor.button)
    
    def get_facecolor(self):
        try: 
            return colors.to_hex(self.obj[0].get_facecolor()[0])
        except: return "black"

    def set_edgecolor (self, value):
        try: 
            for obj in self.obj:
                obj.set_edgecolor(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgecolor.button)
    
    def get_edgecolor (self):
        try:
            return colors.to_hex(self.obj[0].get_edgecolor()[0])
        except: return "black"

    def set_alpha (self, value):
        try: 
            for obj in self.obj:
                obj.set_alpha(value/100)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.alpha.button)

    def get_alpha (self):
        try:
            if self.obj[0].get_alpha():
                return int(self.obj[0].get_alpha()*100)
            return 100
        except: return 100

    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()
        return super().paintEvent(a0)

class CmapCollection (QWidget):
    sig = Signal()
    def __init__(self, gid, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()
        self.setParent(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('CmapCollection'))
        layout.addWidget(SeparateHLine())

        self.edgewidth = DoubleSpinBox(text='Edge Width',min=0,max=5,step=0.1)
        self.edgewidth.button.setValue(self.get_edgewidth())
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='Edge Style',items=linestyle_lib.values())
        self.edgestyle.button.setCurrentText(self.get_edgestyle())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        layout.addWidget(self.edgestyle)

        self.cmap_on = Toggle(text="Colormap On")
        self.cmap_on.button.setChecked(self.get_cmap_on())
        self.cmap_on.button.checkedChanged.connect(self.set_cmap_on)
        layout.addWidget(self.cmap_on)

        self.cmap_widget = QWidget()
        self.cmap_widget.setEnabled(self.get_cmap_on())
        cmap_layout = QVBoxLayout()
        cmap_layout.setContentsMargins(0,0,0,0)
        self.cmap_widget.setLayout(cmap_layout)
        layout.addWidget(self.cmap_widget)

        self.cmap = ComboBox(items=colormaps(), text="Colormap")
        self.cmap.button.setCurrentText(self.get_cmap())
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        cmap_layout.addWidget(self.cmap)

        self.norm = ComboBox(items=['linear', 'log', 'logit', 'symlog','asinh'], text="Norm")
        self.norm.button.setCurrentText(self.get_norm())
        self.norm.button.currentTextChanged.connect(self.set_norm)
        cmap_layout.addWidget(self.norm)

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

        layout.addStretch()
    
    def find_object (self) -> list[Collection]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[Collection],
                               gid=self.gid)
    
    def update_props(self, button=None):
        if button != self.edgewidth.button:
            self.edgewidth.button.setValue(self.get_edgewidth())
        if button != self.edgestyle.button:
            self.edgestyle.button.setCurrentText(self.get_edgestyle())
        if button != self.cmap_on.button:
            self.cmap_on.button.setChecked(self.get_cmap_on())
        if button != self.cmap.button:
            self.cmap.button.setCurrentText(self.get_cmap())
        if button != self.norm.button:
            self.norm.button.setCurrentText(self.get_norm())
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
    
    def set_cmap_on (self, checked):
        self.cmap_widget.setEnabled(checked)
        self.facecolor.setEnabled(not checked)
        if checked:
            self.set_cmap(self.cmap.button.currentText().lower())
            self.set_norm(self.norm.button.currentText().lower())
        else:
            self.set_cmap(None)
            self.set_norm(None)
        
        self.update_props(self.cmap_on.button)
        
    def get_cmap_on(self):
        if isinstance(self.obj[0].get_array(), numpy.ma.core.MaskedArray):
            return True
        return False
    
    def set_edgewidth (self, value):
        try: 
            for obj in self.obj:
                obj.set_linewidth(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgewidth.button)
    
    def get_edgewidth (self):
        return self.obj[0].get_linewidth()
    
    def set_edgestyle (self, value:str):
        try: 
            for obj in self.obj:
                obj.set_linestyle(value.lower())
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgestyle.button)
    
    def get_edgestyle (self):
        ls = self.obj[0].get_linestyle()
        if ls[0][1] == [3.7, 1.6]:
            return "dashed"
        elif ls[0][1] == [6.4, 1.6, 1.0, 1.6]:
            return "dashdot"
        elif ls[0][1] == [1.0, 1.65]:
            return "dotted"
        else:
            return "solid"
    
    def set_cmap(self, value:str|None):
        try:
            if value:
                for obj in self.obj:
                    obj.set_array(self.obj[0].get_offsets().transpose()[0])
                for _cmap in colormaps():
                    if _cmap.lower() == value.lower():
                        for obj in self.obj:
                            obj.set_cmap(_cmap)
            else:
                for obj in self.obj:
                    obj.set_array(value)
                    obj.set_cmap(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.cmap.button)
    
    def get_cmap(self) -> str:
        return self.obj[0].get_cmap().name

    def set_norm (self, value:str|None):
        try:
            if value: 
                value = value.lower()
            for obj in self.obj:
                obj.set_norm(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.norm.button)

    def get_norm(self) -> str:
        _scale_mapping = scale._scale_mapping
        for key, value in _scale_mapping.items():
            if type(self.obj[0].norm._scale) == value:
                return key
        return "linear"
    
    def set_facecolor (self, value):
        try: 
            for obj in self.obj:
                obj.set_facecolor(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.facecolor.button)
    
    def get_facecolor(self):
        return colors.to_hex(self.obj[0].get_facecolor()[0])
    
    def set_edgecolor (self, value):
        try: 
            for obj in self.obj:
                obj.set_edgecolor(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgecolor.button)
    
    def get_edgecolor (self):
        if len(self.obj[0].get_edgecolor()) > 1:
            return colors.to_hex(self.obj[0].get_edgecolor()[0])
        return self.get_facecolor()

    def set_alpha (self, value):
        try: 
            for obj in self.obj:
                obj.set_alpha(value/100)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.alpha.button)

    def get_alpha (self):
        if self.obj[0].get_alpha() != None:
            return int(self.obj[0].get_alpha()*100)
        return 100

    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()
        return super().paintEvent(a0)
    
class QuadMesh(QWidget):
    sig = Signal()
    def __init__(self, gid, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()
        self.setParent(parent)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.edgewidth = DoubleSpinBox(text='Edge Width',min=0,max=5,step=0.1)
        self.edgewidth.button.setValue(self.get_edgewidth())
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='Edge Style',items=linestyle_lib.values())
        self.edgestyle.button.setCurrentText(self.get_edgestyle())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        layout.addWidget(self.edgestyle)

        self.edgecolor = ColorDropdown(text='Edge Color',color=self.get_edgecolor(), parent=self.parent())
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(self.edgecolor)

        self.cmap_widget = QWidget()
        cmap_layout = QVBoxLayout()
        cmap_layout.setContentsMargins(0,0,0,0)
        self.cmap_widget.setLayout(cmap_layout)
        layout.addWidget(self.cmap_widget)

        self.cmap = ComboBox(items=colormaps(), text="Colormap")
        self.cmap.button.setCurrentText(self.get_cmap())
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        cmap_layout.addWidget(self.cmap)

        self.norm = ComboBox(items=['linear', 'log', 'logit', 'symlog','asinh'], text="Norm")
        self.norm.button.setCurrentText(self.get_norm())
        self.norm.button.currentTextChanged.connect(self.set_norm)
        cmap_layout.addWidget(self.norm)

        self.alpha = Slider(text='Transparency',min=0,max=100)
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)

        layout.addStretch()
    
    def find_object (self) -> list[Mesh]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[Mesh],
                               gid=self.gid)
    
    def update_props(self, button=None):
        if button != self.edgewidth.button:
            self.edgewidth.button.setValue(self.get_edgewidth())
        if button != self.edgestyle.button:
            self.edgestyle.button.setCurrentText(self.get_edgestyle())
        if button != self.edgecolor.button:
            self.edgecolor.button.setColor(self.get_edgecolor())
        if button != self.cmap.button:
            self.cmap.button.setCurrentText(self.get_cmap())
        if button != self.norm.button:
            self.norm.button.setCurrentText(self.get_norm())
        if button != self.alpha.button:
            self.alpha.button.setValue(self.get_alpha())
    
    def update_plot(self, *args, **kwargs):
        # self.sig.emit()
        self.canvas.draw_idle()
        self.update_props(*args, **kwargs)
    
    def set_edgewidth (self, value):
        try: 
            for obj in self.obj:
                obj.set_linewidth(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgewidth.button)
    
    def get_edgewidth (self):
        return self.obj[0].get_linewidth()
    
    def set_edgestyle (self, value:str):
        try: 
            for obj in self.obj:
                obj.set_linestyle(value.lower())
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgestyle.button)
    
    def get_edgestyle (self):
        ls = self.obj[0].get_linestyle()
        if ls[0][1] == [3.7, 1.6]:
            return "dashed"
        elif ls[0][1] == [6.4, 1.6, 1.0, 1.6]:
            return "dashdot"
        elif ls[0][1] == [1.0, 1.65]:
            return "dotted"
        else:
            return "solid"
    
    def set_edgecolor (self, value):
        try: 
            for obj in self.obj:
                obj.set_edgecolor(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.edgecolor.button)
    
    def get_edgecolor (self):
        if len(self.obj[0].get_edgecolor()) > 1:
            return colors.to_hex(self.obj[0].get_edgecolor()[0])
        return colors.to_hex(self.obj[0].get_facecolor()[0])
    
    def set_cmap(self, value:str):
        try:
            for obj in self.obj:
                    obj.set_cmap(value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.cmap.button)
    
    def get_cmap(self) -> str:
        return self.obj[0].get_cmap().name

    def set_norm (self, value:str):
        try:
            for obj in self.obj:
                obj.set_norm(value.lower())
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.norm.button)

    def get_norm(self) -> str:
        _scale_mapping = scale._scale_mapping
        for key, value in _scale_mapping.items():
            if type(self.obj[0].norm._scale) == value:
                return key
        return "linear"

    def set_alpha (self, value):
        try: 
            for obj in self.obj:
                obj.set_alpha(value/100)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.alpha.button)

    def get_alpha (self):
        if self.obj[0].get_alpha() != None:
            return int(self.obj[0].get_alpha()*100)
        return 100

    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()
        return super().paintEvent(a0)
    
class Poly3DCollection (QWidget):
    sig = Signal()
    def __init__(self, gid, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()
        self.setParent(parent)
        self.initUI()
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.zsort = ComboBox(items=["average","min","max"], text="Zsort")
        self.zsort.button.setCurrentText(self.get_zsort())
        self.zsort.button.currentTextChanged.connect(self.set_zsort)
        self._layout.addWidget(self.zsort)

        self.alpha = Slider(text='Transparency',min=0,max=100)
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        self._layout.addWidget(self.alpha)

        self._layout.addStretch()

    def find_object(self) -> List[art3d.Poly3DCollection]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[art3d.Poly3DCollection],
                               gid=self.gid)
    
    def update_props(self, button=None):
        if button != self.zsort.button:
            self.zsort.button.setCurrentText(self.get_zsort())
        if button != self.alpha.button:
            self.alpha.button.setValue(self.get_alpha())
    
    def update_plot(self, *args, **kwargs):
        # self.sig.emit()
        self.canvas.draw_idle()
        self.update_props(*args, **kwargs)

    def set_zsort(self, value:str):
        try:
            for obj in self.obj:
                obj.set_zsort(value.lower())
            self.update_plot(self.zsort.button)
        except Exception as e:
            logger.exception(e)
    
    def get_zsort(self) -> str:
        zsort_functions = self.obj[0]._zsort_functions
        zsort_func = self.obj[0]._zsortfunc
        return list(zsort_functions.keys())[list(zsort_functions.values()).index(zsort_func)]

    def set_alpha (self, value):
        try: 
            for obj in self.obj:
                obj.set_alpha(value/100)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.alpha.button)

    def get_alpha (self):
        try:
            if self.obj[0].get_alpha():
                return int(self.obj[0].get_alpha()*100)
            return 100
        except: return 100
        

    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()
        return super().paintEvent(a0)