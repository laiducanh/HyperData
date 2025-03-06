from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import BodyLabel
from node_editor.node.interpolation.base import FitBase
from plot.canvas import Canvas
from scipy.interpolate import KroghInterpolator

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, xdata, ydata, interpolator: KroghInterpolator,  parent=None):
        super().__init__(parent)
        if not interpolator:
            self.main_layout.addWidget(BodyLabel("Could not determine Barycentric interpolator."))
        else:            
            self.canvas = Canvas()
            for _ax in self.canvas.fig.axes: _ax.remove()
            self.plot(xdata, ydata, interpolator)
            self.main_layout.addWidget(self.canvas)

    def plot(self, xdata, ydata, interpolator: KroghInterpolator):
        # clear plot
        self.canvas.fig.clear()

        # add axis
        ax = self.canvas.fig.add_subplot()

        ax.scatter(xdata, ydata, label="data", color="b")
        ax.plot(xdata, interpolator.__call__(xdata),label="fit",color="r",marker=None)
        ax.legend()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
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
