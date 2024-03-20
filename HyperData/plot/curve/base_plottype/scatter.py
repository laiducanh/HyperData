from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit
from ui.base_widgets.separator import SeparateHLine
from ui.base_widgets.text import TextEdit, StrongBodyLabel
from ui.base_widgets.spinbox import SpinBox
from matplotlib.collections import Collection
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import CmapCollection

class Scatter(QWidget):
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
        self.obj = self.find_obj()

        self._layout.addWidget(StrongBodyLabel('Scatter'))
        self._layout.addWidget(SeparateHLine())

        self.sizes = SpinBox(min=1,max=1000,step=2,text="sizes")
        self.sizes.button.setValue(self.get_sizes())
        self.sizes.button.valueChanged.connect(self.set_sizes)
        self._layout.addWidget(self.sizes)

        line = CmapCollection(gid, canvas, parent)
        line.sig.connect(self.sig.emit)
        self._layout.addWidget(line)

        self._layout.addStretch()
    
    def find_obj (self) -> Collection:
        for obj in self.canvas.fig.findobj(match=Collection):
            if obj._gid != None and obj._gid == self.gid:
                return obj
    
    def update_plot(self, **kwargs):
        self.plot.plotting(**kwargs)
        self.sig.emit()
    
    def set_sizes(self, value:int):
        self.update_plot(sizes=value)
    
    def get_sizes(self) -> int:
        return int(self.obj.sizes)

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_obj()
        return super().paintEvent(a0)