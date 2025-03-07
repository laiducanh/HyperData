from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import BodyLabel
from node_editor.node.interpolation.base import FitBase
from plot.canvas import Canvas
from scipy.interpolate import KroghInterpolator
import numpy as np

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, xdata, ydata, interpolator: KroghInterpolator,  parent=None):
        super().__init__(parent)
        self.xdata = xdata
        self.xi = xdata
        self.ydata = ydata
        self.interpolator = interpolator

        if not interpolator:
            self.main_layout.addWidget(BodyLabel("Could not determine Krogh interpolator."))
        else:    
            smooth = ComboBox(items=[str(i) for i in np.arange(0,10000,50)], text="Smoothness")
            smooth.button.setCurrentText(str(len(xdata)))
            smooth.button.currentTextChanged.connect(self.onSmoothChange)
            self.main_layout.addWidget(smooth)

            self.canvas = Canvas()
            for _ax in self.canvas.fig.axes: _ax.remove()
            self.plot()
            self.main_layout.addWidget(self.canvas)
    
    def onSmoothChange(self, value):
        self.xi = np.linspace(min(self.xdata), max(self.xdata), int(value))
        self.plot()

    def plot(self):
        # clear plot
        self.canvas.fig.clear()

        # add axis
        ax = self.canvas.fig.add_subplot()

        ax.plot(self.xi, self.interpolator.__call__(self.xi),label="fit",color="r",marker='',lw=2)
        ax.plot(self.xdata, self.ydata, label="data", color="b", lw=0)
        ax.legend()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title("Krogh Interpolation")
        self.canvas.draw_idle()

class Krogh (FitBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interpolator = None
        
    def run(self, X, Y):
        try:
            self.X = X
            self.Y = Y
            self.interpolator = KroghInterpolator(X, Y)
        
        except Exception as e:
            self.interpolator = None
            logger.exception(e)
    
    def predict(self, X, *args, **kwargs):
        return self.interpolator.__call__(X)

    def result_dialog(self):
        dialog = ResultDialog(self.X, self.Y, self.interpolator)
        dialog.exec()
