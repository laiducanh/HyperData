from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from plot.curve.base_elements.line import LineBase
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.button import Toggle, ComboBox
from matplotlib.lines import Line2D
from matplotlib.collections import Collection
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import SingleColorCollection

class Line (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.gid = gid
        self.canvas = canvas

        line = LineBase(gid, canvas, parent)
        line.sig.connect(self.sig.emit)
        self._layout.addWidget(line)

        self._layout.addStretch()

class Step (Line):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, parent)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        widget.setLayout(layout)
        self._layout.insertWidget(0,widget)
        self._layout.addSpacing(10)

        self.canvas = canvas
        self.gid = gid
        self.obj = self.find_obj()

        layout.addWidget(TitleLabel("Step"))
        layout.addWidget(SeparateHLine())

        self.toggle = Toggle(text="apply to all")
        self.toggle.button.checkedChanged.connect(self.set_where)
        layout.addWidget(self.toggle)

        self.where = ComboBox(items=['pre', 'post', 'mid'], text="where")
        self.where.button.currentTextChanged.connect(self.set_where)
        self.where.button.setCurrentText(self.get_where().title())
        layout.addWidget(self.where)
    
    def find_obj (self) -> Line2D:
        for obj in self.canvas.fig.findobj(match=Line2D):
            if obj._gid != None and obj._gid == self.gid:
                return obj
    
    def set_where (self, value:str):
        value = self.where.button.currentText().lower()
        if self.toggle.button.isChecked():
            for obj in self.canvas.fig.findobj(match=Line2D):
                if obj._gid != None and self.gid.split(".")[0] in obj._gid:
                    obj.set_drawstyle(f"steps-{value}")
        else:
            self.obj.set_drawstyle(f"steps-{value}")

        self.sig.emit()
    
    def get_where (self):
        return self.obj.get_drawstyle().split("-")[-1]

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_obj()
        return super().paintEvent(a0)
    
class Area (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas: Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_obj()
        self.step = None

        self._layout.addWidget(TitleLabel('Area'))
        self._layout.addWidget(SeparateHLine())

        self.toggle = Toggle(text="apply to all")
        self.toggle.button.checkedChanged.connect(self.sig.emit)
        self._layout.addWidget(self.toggle)

        step = ComboBox(text='Step',items=['pre','post','mid','none'])
        step.button.currentTextChanged.connect(self.set_step)
        step.button.setCurrentText(self.get_step().title())
        self._layout.addWidget(step)

        self._layout.addSpacing(10)

        self._layout.addWidget(TitleLabel('PolyCollection'))
        self._layout.addWidget(SeparateHLine())

        patch = SingleColorCollection(gid, canvas, parent)
        patch.sig.connect(self.update_plot)
        self._layout.addWidget(patch)
        
        self._layout.addStretch()
    
    def find_obj (self) -> Collection:
        for obj in self.canvas.fig.findobj(match=Collection):
            if obj._gid != None and obj._gid == self.gid:
                return obj
    
    def update_plot(self):
        
        self.plot.plotting(step=self.step)
        self.sig.emit()
    
    def set_step(self, value:str):
        self.step = value.lower()
        if self.step == 'none': self.step = None
        self.update_plot()
    
    def get_step(self) -> str:
        return self.obj.step

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_obj()
        return super().paintEvent(a0)