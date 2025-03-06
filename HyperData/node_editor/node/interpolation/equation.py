from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import BodyLabel
from node_editor.node.interpolation.base import FitBase
from plot.canvas import Canvas
from sympy import sympify, lambdify
from scipy.optimize import curve_fit
import numpy as np

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, xdata, ydata, func, params:str, input:str, 
                 popt, pcov, fail=False, warn:str=None, parent=None):
        super().__init__(parent)

        if fail:
            self.main_layout.addWidget(BodyLabel("Curve Fitter failed to find any results.")) 
        else:
            if warn == "error":
                self.main_layout.addWidget(BodyLabel("Optimal parameters not found: The maximum number of function evaluations is exceeded."))
            else:
                for p, val in zip(params.split(","),popt):
                    input = input.replace(p, str(round(val, 5)))

                self.main_layout.addWidget(BodyLabel(f"Function: {input}"))
                self.main_layout.addWidget(BodyLabel(f"Condition number of the covariance matrix: {np.linalg.cond(pcov)}"))
                self.main_layout.addWidget(BodyLabel(f"Diagonal elements of the covariance matrix: {np.diag(pcov)}"))
                
                self.canvas = Canvas()
                for _ax in self.canvas.fig.axes: _ax.remove()
                self.plot(xdata, ydata, func, popt, params)
                self.main_layout.addWidget(self.canvas)

    def plot(self, xdata, ydata, func, popt, params):
        # clear plot
        self.canvas.fig.clear()

        # add axis
        ax = self.canvas.fig.add_subplot()

        label = "fit: "
        for p, v in zip(params.split(","),popt):
            label += f"{p}=" + "%5.3f," %v
        label = label[:-1] # remove the last comma

        ax.scatter(xdata, ydata, label="data", color="b")
        ax.plot(xdata, func(xdata, *popt),label=label,color="r",marker=None)
        ax.legend()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        self.canvas.draw_idle()

class EquationFit (FitBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.popt, self.pcov = None, None
        self.fail, self.warn = False, None

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            input = "a*x + b",
            params = "a, b",
            variable = "x",
        )
        else: self._config = config
    
        self.params = LineEdit(text="Parameters")
        self.params.button.setText(self._config["params"])
        self.vlayout.addWidget(self.params)

        self.var = LineEdit(text="Variable")
        self.var.button.setText(self._config["variable"])
        self.vlayout.addWidget(self.var)
        
        self.func = LineEdit(text="Function")
        self.func.button.setText(self._config["input"])
        self.vlayout.addWidget(self.func)
    
    def update_config(self):
        self._config.update(
            input = self.func.button.text(),
            params = self.params.button.text(),
            variable = self.var.button.text(),
        )

    def make_f(self, input:str, params:str, variable:str):
        """ make function for scipy.optimize.curve_fit from user input """
        input = input.replace(" ","")
        params = params.replace(" ","").split(",")
        variable = variable.replace(" ","")
        return lambdify((variable, *params), sympify(input))

    def run(self, X, Y):
        try:
            self.popt, self.pcov = None, None
            self.X = X
            self.Y = Y
            p0 = [1]*(len(self._config["params"].split(",")))
            self.fail, self.warn = False, None

            self.popt, self.pcov, infodict, mesg, ier = curve_fit(
                    self.make_f(**self._config), 
                    X, 
                    Y, 
                    p0=p0,
                    full_output=True
                )
        
        except RuntimeError as e:
            self.warn = 'error'
            logger.info("Optimal parameters not found: The maximum number of function evaluations is exceeded.")
        except Exception as e:
            logger.exception(e)
    
    def predict(self, X, *args, **kwargs):
        return self.make_f(**self._config)(X, *self.popt)

    def result_dialog(self):
        dialog = ResultDialog(
            self.X,
            self.Y,
            self.make_f(**self._config),
            self._config["params"], 
            self._config["input"], 
            self.popt, 
            self.pcov,
            self.fail,
            self.warn,
        )
        dialog.exec()
