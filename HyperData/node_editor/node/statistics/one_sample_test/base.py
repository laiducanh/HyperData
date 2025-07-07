from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt
from ui.base_widgets.button import HButton
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.frame import SeparateHLine
from plot.canvas import Canvas
from scipy.stats._continuous_distns import norm_gen
import numpy as np

class TestBase (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)   

        _layout = QVBoxLayout()
        _layout.setContentsMargins(0,0,0,0)
        self.setLayout(_layout)
        self.scroll_area = QScrollArea(parent)
        _layout.addWidget(self.scroll_area)
        
        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)

        self._config = dict()
        self.set_config(config=None)
        
    def clear_layout (self):
        for i in reversed(range(self.vlayout.count())):
            item = self.vlayout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, HButton):
                self.vlayout.removeWidget(widget)
                widget.deleteLater()
    
    def set_config(self, config=None):
        self.clear_layout()
    
    def update_config(self):
        pass

    def result_dialog(self, samples, dist, result):
        pass

class ResultDialogBase(Dialog):
    def __init__(self, samples:np.ndarray=None, dist:norm_gen=None, result=None, parent=None):
        super().__init__(parent)

        self.dist = dist
        self.samples = samples
        self._result = result

        if result:
            self.initStats(result)
            self.main_layout.addWidget(SeparateHLine())
            self.initPlot()
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
    
    def initStats(self, result):
        pass

    def initPlot(self):
        self.canvas = Canvas()
        self.main_layout.addWidget(self.canvas)
        for _ax in self.canvas.figure.axes: _ax.remove()
    
    def plot(self):
        # clear plot
        self.canvas.figure.clear()

        # add axis
        self.ax = self.canvas.figure.add_subplot()
        self.ax2 = self.ax.twinx()
        self.axleg = self.canvas.figure.add_subplot()
        self.axleg.set_axis_off()