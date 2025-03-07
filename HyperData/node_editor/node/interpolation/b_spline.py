from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import BodyLabel
from node_editor.node.interpolation.base import FitBase
from plot.canvas import Canvas
from scipy.interpolate import make_interp_spline
import numpy as np

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, xdata, ydata, spline,  parent=None):
        super().__init__(parent)
        self.xdata = xdata
        self.xi = xdata
        self.ydata = ydata
        self.spline = spline

        if not spline:
            self.main_layout.addWidget(BodyLabel("Could not determine B-Spline."))
        else:
            self.main_layout.addWidget(BodyLabel(f"B-Spline degree: {spline.k}"))
            self.main_layout.addWidget(BodyLabel(f"B-Spline coefficients: {spline.c}"))
            self.main_layout.addWidget(BodyLabel(f"Knots {spline.t}"))

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

        ax.plot(self.xi, self.spline(self.xi),label="fit",color="r",marker='', lw=2)
        ax.plot(self.xdata, self.ydata, label="data", color="b",lw=0)
        ax.legend()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title("B-Spline Interpolation")
        self.canvas.draw_idle()

class BSpline (FitBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.spline = None

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            k = 3,
            bc_type = "not-a-knot"
        )
        else: self._config = config
    
        self.k = SpinBox(text="B-Spline degree")
        self.k.button.setValue(self._config["k"])
        self.vlayout.addWidget(self.k)

        self.bc_type = ComboBox(items=["clamped","natural","not-a-knot","periodic"], 
                                text="Boundary condition")
        self.bc_type.button.setCurrentText(self._config["bc_type"])
        self.vlayout.addWidget(self.bc_type)
    
    def update_config(self):
        self._config.update(
            k = self.k.button.value(),
            bc_type = self.bc_type.button.currentText()
        )

    def run(self, X, Y):
        try:
            self.X = X
            self.Y = Y
            self.spline = make_interp_spline(X, Y, **self._config)
       
        except Exception as e:
            self.spline = None
            logger.exception(e)
    
    def predict(self, X, *args, **kwargs):
        return self.spline(X)

    def result_dialog(self):
        dialog = ResultDialog(self.X, self.Y, self.spline)
        dialog.exec()
