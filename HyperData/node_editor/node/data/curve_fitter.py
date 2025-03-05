from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import _TransparentPushButton
from plot.canvas import Canvas
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
from sympy import sympify, lambdify
import warnings

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
                if warn == "warn":
                    self.main_layout.addWidget(BodyLabel("Covariance of the parameters could not be estimated."))
                elif warn == "other":
                    self.main_layout.addWidget(BodyLabel("There was a uncategorized warning."))
                
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

        ax.plot(xdata, ydata, label="data", color="b")
        ax.plot(xdata, func(xdata, *popt),label=label,color="r")
        ax.legend()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        self.canvas.draw_idle()


class CurveFitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("X")
        self.node.input_sockets[1].setSocketLabel("Y")
        self.node.output_sockets[0].setSocketLabel("Data out")

        self.result_btn = _TransparentPushButton()
        self.result_btn.setText("Result")
        self.result_btn.released.connect(self.result_dialog)
        self.vlayout.insertWidget(2,self.result_btn)
        
        self._config = dict(
            input = "a*x + b",
            params = "a, b",
            variable = "x"
        )

        self.popt, self.pcov = None, None
        self.X, self.Y = None, None
        self.fail, self.warn = False, None
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        params = LineEdit(text="Parameters")
        params.button.setText(self._config["params"])
        dialog.main_layout.addWidget(params)

        var = LineEdit(text="Variable")
        var.button.setText(self._config["variable"])
        dialog.main_layout.addWidget(var)
        
        func = LineEdit(text="Function")
        func.button.setText(self._config["input"])
        dialog.main_layout.addWidget(func)
 
        if dialog.exec():
            self._config.update(
                input = func.button.text(),
                params = params.button.text(),
                variable = var.button.text()
            )
            self.exec()

    def make_f(self, input:str, params:str, variable:str):
        """ make function for scipy.optimize.curve_fit from user input """
        input = input.replace(" ","")
        params = params.replace(" ","").split(",")
        variable = variable.replace(" ","")
        return lambdify((variable, *params), sympify(input))
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            X = np.arange(10)
            Y = 3*X + 4
            self.node.input_sockets[0].socket_data = pd.DataFrame(X, columns=["X"])
            self.node.input_sockets[1].socket_data = pd.DataFrame(Y, columns=["Y"])
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            self.X = self.node.input_sockets[0].socket_data.copy(deep=True)
            self.Y = self.node.input_sockets[1].socket_data.copy(deep=True)
            data = pd.concat([self.X, self.Y], axis=1)
            p0 = [1]*(len(self._config["params"].split(",")))
            self.popt, self.pcov = None, None
            self.fail, self.warn = False, None
    
            try:
                with warnings.catch_warnings(record=True) as caught_warnings:
                    warnings.simplefilter("always", category=OptimizeWarning)

                    self.popt, self.pcov, infodict, mesg, ier = curve_fit(
                        self.make_f(**self._config), 
                        self.X.to_numpy().ravel(), 
                        self.Y.to_numpy().ravel(), 
                        p0=p0,
                        full_output=True
                    )

                    if caught_warnings:
                        for warning in caught_warnings:
                            if issubclass(warning.category, OptimizeWarning): 
                                self.warn = "warn"
                            else: 
                                self.warn = "other"

                    data["Residues"] = infodict["fvec"]

                    # change progressbar's color
                    self.progress.changeColor('success')
                    # write log
                    logger.info(f"{self.name} {self.node.id}: run successfully.")

            except RuntimeError as e:
                self.warn = 'error'
                # change progressbar's color
                self.progress.changeColor('fail')
                # write log
                logger.info(f"{self.name} {self.node.id}: failed.")
                logger.info(f"{self.name} {self.node.id}: Optimal parameters not found: The maximum number of function evaluations is exceeded.")
            
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
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

    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        self.node.input_sockets[1].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data