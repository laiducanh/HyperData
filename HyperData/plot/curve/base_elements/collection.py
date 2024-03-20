from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from config.settings import linestyle_lib
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox, Slider
from ui.base_widgets.text import LineEdit
from ui.base_widgets.color import ColorDropdown
from plot.canvas import Canvas
from matplotlib.collections import Collection
from matplotlib import colors, scale
from matplotlib.pyplot import colormaps
import matplotlib, numpy

class SingleColorCollection (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()
        self.parent = parent
        self.initUI()

    def initUI (self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.edgewidth = DoubleSpinBox(text='edge width',min=0,max=5,step=0.1)
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        self.edgewidth.button.setValue(self.get_edgewidth())
        layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='edge style',items=linestyle_lib.values())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        self.edgestyle.button.setCurrentText(self.get_edgestyle().title())
        layout.addWidget(self.edgestyle)

        self.facecolor = ColorDropdown(text='face color',color=self.get_facecolor(), parent=self.parent)
        self.facecolor.button.colorChanged.connect(self.set_facecolor)
        layout.addWidget(self.facecolor)

        self.edgecolor = ColorDropdown(text='edge color',color=self.get_edgecolor(), parent=self.parent)
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(self.edgecolor)

        alpha = Slider(text='Transparency',min=0,max=100)
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)
    
    def find_object (self) -> Collection:
        for obj in self.canvas.fig.findobj(match=Collection):
            if obj._gid != None and obj._gid == self.gid:
                return obj
    
    def set_edgewidth (self, value):
        self.obj.set_linewidth(value)
        self.sig.emit()
    
    def get_edgewidth (self):
        return self.obj.get_linewidth()

    def set_edgestyle (self, value):
        self.obj.set_linestyle(value.lower())
        self.sig.emit()
    
    def get_edgestyle (self) -> str:
        return linestyle_lib[self.obj.get_linestyle()[0]]
    
    def set_facecolor (self, value):
        self.obj.set_facecolor(value)
        self.sig.emit()
    
    def get_facecolor(self):
        return colors.to_hex(self.obj.get_facecolor()[0])
    
    def set_edgecolor (self, value):
        self.obj.set_edgecolor(value)
        self.sig.emit()
    
    def get_edgecolor (self):
        if len(self.obj.get_edgecolor()) > 1:
            return colors.to_hex(self.obj.get_edgecolor()[0])
        self.set_edgecolor(self.get_facecolor())
        return self.get_facecolor()

    def set_alpha (self, value):
        self.obj.set_alpha(value/100)
        self.sig.emit()

    def get_alpha (self):
        if self.obj.get_alpha() != None:
            return int(self.obj.get_alpha()*100)
        return 100

    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()

        return super().paintEvent(a0)

class CmapCollection (SingleColorCollection):
    def __init__(self, gid, canvas: Canvas, parent=None):
        super().__init__(gid, canvas, parent)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.edgewidth = DoubleSpinBox(text='edge width',min=0,max=5,step=0.1)
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        self.edgewidth.button.setValue(self.get_edgewidth())
        layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='edge style',items=linestyle_lib.values())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        self.edgestyle.button.setCurrentText(self.get_edgestyle().title())
        layout.addWidget(self.edgestyle)

        self.cmap_on = Toggle(text="colormap on")
        self.cmap_on.button.checkedChanged.connect(self.set_cmap_on)
        layout.addWidget(self.cmap_on)

        self.cmap_widget = QWidget()
        self.cmap_widget.setEnabled(self.get_cmap_on())
        cmap_layout = QVBoxLayout()
        cmap_layout.setContentsMargins(0,0,0,0)
        self.cmap_widget.setLayout(cmap_layout)
        layout.addWidget(self.cmap_widget)

        self.cmap = ComboBox(items=colormaps(), text="Colormap")
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        self.cmap.button.setCurrentText(self.get_cmap().title())
        cmap_layout.addWidget(self.cmap)

        self.norm = ComboBox(items=['linear', 'log', 'logit', 'symlog','asinh'], text="norm")
        self.norm.button.setCurrentText(self.get_norm().title())
        self.norm.button.currentTextChanged.connect(self.set_norm)
        cmap_layout.addWidget(self.norm)

        self.facecolor = ColorDropdown(text='face color',color=self.get_facecolor(), parent=self.parent)
        self.facecolor.button.colorChanged.connect(self.set_facecolor)
        layout.addWidget(self.facecolor)

        self.edgecolor = ColorDropdown(text='edge color',color=self.get_edgecolor(), parent=self.parent)
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(self.edgecolor)

        alpha = Slider(text='Transparency',min=0,max=100)
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)

        self.cmap_on.button.setChecked(self.get_cmap_on()) # only call when all other widgets created
    
    def set_cmap_on (self, checked):
        self.cmap_widget.setEnabled(checked)
        self.facecolor.setEnabled(not checked)
        if checked:
            self.set_cmap(self.cmap.button.currentText().lower())
            self.set_norm(self.norm.button.currentText().lower())
        else:
            self.set_cmap(None)
            self.set_norm(None)
        
    def get_cmap_on(self):
        if isinstance(self.obj.get_array(), numpy.ma.core.MaskedArray):
            return True
        return False
    
    def set_cmap(self, value):
        if value != None:
            self.obj.set_array(self.obj.get_offsets().transpose()[0])
        else:
            self.obj.set_array(None)
        for _cmap in colormaps():
            if _cmap.lower() == value.lower():
                self.obj.set_cmap(_cmap)
        self.sig.emit()
    
    def get_cmap(self) -> str:
        return self.obj.get_cmap().name

    def set_norm (self, value):
        if value != None: 
            value = value.lower()
        self.obj.set_norm(value)
        self.sig.emit()

    def get_norm(self) -> str:
        _scale_mapping = scale._scale_mapping
        for key, value in _scale_mapping.items():
            if type(self.obj.norm._scale) == value:
                return key
        return "linear"