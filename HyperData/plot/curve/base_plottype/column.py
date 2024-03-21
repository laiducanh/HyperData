from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit
from ui.base_widgets.separator import SeparateHLine
from ui.base_widgets.text import LineEdit, StrongBodyLabel
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import ComboBox
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.patches import Rectangle
from matplotlib import patches
from typing import List

class Column (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()

        self._layout.addWidget(StrongBodyLabel("Column"))
        self._layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(items=["vertical","horizontal"],text="orientation")
        self.orientation.button.setCurrentText(self.get_orientation().title())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.returnPressed.connect(self.set_bottom)
        self.bottom.button.setText(self.get_bottom())
        self._layout.addWidget(self.bottom)

        self.align = ComboBox(items=["center","edge"],text="alignment")
        self.align.button.setCurrentText(self.get_alignment().title())
        self.align.button.currentTextChanged.connect(self.set_alignment)
        self._layout.addWidget(self.align)

        self.barwidth = DoubleSpinBox(text='bar width',min=0,max=5,step=0.1)
        self.barwidth.button.valueChanged.connect(self.set_barwidth)
        self.barwidth.button.setValue(self.get_barwidth())
        self._layout.addWidget(self.barwidth)

        column = Rectangle(gid, canvas, parent)
        column.sig.connect(self.sig.emit)
        self._layout.addWidget(column)

        self._layout.addStretch()

    def find_object (self) -> List[patches.Rectangle]:
        obj_list = list()
        for obj in self.canvas.fig.findobj(match=patches.Rectangle):
            if obj._gid != None and obj._gid == self.gid:
                obj_list.append(obj)
        return obj_list
    
    def update_plot(self, orientation=None, width=None, **kwargs):
        if orientation == None: orientation = self.get_orientation()
        if width == None: width = self.barwidth.button.value()
        self.plot.plotting(orientation=orientation,width=width,**kwargs)
        self.sig.emit()


    def set_orientation(self, value:str):
        self.update_plot(orientation=value.lower())
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom (self):
        if self.bottom.button.text() == "":
            self.bottom.button.setText("0")
        self.update_plot(bottom=float(self.bottom.button.text()))
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)

    def set_alignment (self, value:str):
        self.update_plot(align=value.lower())
    
    def get_alignment(self) -> str:
        return self.obj[0].align

    def set_barwidth (self, value):
        self.update_plot(width=value)
    
    def get_barwidth (self):
        return self.obj[0].width

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)
    

class ClusteredColumn(Column):
    def __init__(self, gid, canvas: Canvas, plot: NewPlot = None, parent=None):
        super().__init__(gid, canvas, plot, parent)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        widget.setLayout(layout)
        self._layout.insertWidget(0,widget)
        self._layout.addSpacing(10)

        layout.addWidget(StrongBodyLabel("Clustered Column"))
        layout.addWidget(SeparateHLine())

        self.distance = DoubleSpinBox(min=0,max=1,step=0.1,text="distance")
        self.distance.button.setValue(self.get_distance())
        self.distance.button.valueChanged.connect(self.set_distance)
        layout.addWidget(self.distance)
    
    def update_plot(self, **kwargs):
        
        self.plot.plotting(**kwargs)
        self.sig.emit()
    
    def set_distance(self, value):
        self.update_plot(distance=value)
    
    def get_distance(self) -> float:
        return self.obj[0].distance


class Marimekko (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()

        self._layout.addWidget(StrongBodyLabel("Column"))
        self._layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(items=["vertical","horizontal"],text="orientation")
        self.orientation.button.setCurrentText(self.get_orientation().title())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        column = Rectangle(gid, canvas, parent)
        column.sig.connect(self.sig.emit)
        self._layout.addWidget(column)

        self._layout.addStretch()
    
    def find_object (self) -> List[patches.Rectangle]:
        obj_list = list()
        for obj in self.canvas.fig.findobj(match=patches.Rectangle):
            if obj._gid != None and obj._gid == self.gid:
                obj_list.append(obj)
        return obj_list
    
    def update_plot(self, orientation=None):
        if orientation == None: orientation = self.get_orientation()
        self.plot.plotting(orientation=orientation)
        self.sig.emit()
    
    def set_orientation(self, value:str):
        self.update_plot(orientation=value.lower())
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)
    