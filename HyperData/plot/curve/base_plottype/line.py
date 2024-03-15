from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit
from plot.curve.base_widget.line import LineBase
from plot.curve.base_widget.marker import MarkerBase
from ui.base_widgets.separator import SeparateHLine
from ui.base_widgets.text import TextEdit, StrongBodyLabel
from ui.base_widgets.button import Toggle, ComboBox
from matplotlib.lines import Line2D
from plot.canvas import Canvas
from plot.plotting.base import line

class Line (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.gid = gid
        self.canvas = canvas

        self._layout.addWidget(StrongBodyLabel('Line'))
        self._layout.addWidget(SeparateHLine())

        line = LineBase(gid, canvas)
        line.sig.connect(self.sig.emit)
        self._layout.addWidget(line)

        self._layout.addSpacing(10)

        self._layout.addWidget(StrongBodyLabel('Marker'))
        self._layout.addWidget(SeparateHLine())

        marker = MarkerBase(gid, canvas)
        self._layout.addWidget(marker)

        self._layout.addStretch()

class Step (Line):
    def __init__(self, gid, canvas:Canvas, parent=None):
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

        layout.addWidget(StrongBodyLabel("Step"))
        layout.addWidget(SeparateHLine())

        self.toggle = Toggle(text="Apply to all")
        layout.addWidget(self.toggle)

        where = ComboBox(items=['pre', 'post', 'mid'], text="where")
        where.button.currentTextChanged.connect(self.set_where)
        where.button.setCurrentText(self.get_where().title())
        layout.addWidget(where)
    
    def find_obj (self) -> Line2D:
        for obj in self.canvas.fig.findobj(match=Line2D):
            if obj._gid != None and obj._gid == self.gid:
                return obj
    
    def set_where (self, value:str):
        
        obj_old = self.obj
        ax = self.obj.axes
        self.obj.remove()
        curve = line.step2d(*obj_old.get_data(), ax=ax, where=value.lower())
        for ind, art in enumerate(curve):
            art.set_gid(obj_old.get_gid())
            art.plot_type = "2d step"
            art.update_from(obj_old)

        self.sig.emit()
    
    def get_where (self):
        return self.obj.where

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_obj()
        return super().paintEvent(a0)
    

    