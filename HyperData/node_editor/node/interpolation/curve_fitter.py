from PySide6.QtWidgets import QStackedLayout
from PySide6.QtGui import QAction
from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import _TransparentPushButton, DropDownPrimaryPushButton
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.menu import Menu
from node_editor.node.interpolation.base import FitBase
from node_editor.node.interpolation.equation import EquationFit
from node_editor.node.interpolation.b_spline import BSpline
from node_editor.node.interpolation.cubic_hermite import CubicHermite
from node_editor.node.interpolation.akima import Akima
from node_editor.node.interpolation.pchip import PCHIP1D
from node_editor.node.interpolation.barycentric import Barycentric
from node_editor.node.interpolation.krogh import Krogh
import pandas as pd
import numpy as np

DEBUG = True

class CurveFitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("X")
        self.node.input_sockets[1].setSocketLabel("Y")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Data out")

        self.result_btn = _TransparentPushButton()
        self.result_btn.setText("Result")
        self.result_btn.released.connect(self.result_dialog)
        self.vlayout.insertWidget(2,self.result_btn)
        
        self._config = dict(
            method = "Equation fitting",
            config = dict(input = "a*x + b",params = "a, b",variable = "x"),
        )

        self.X, self.Y = None, None
        self.method_list = ["B-Spline","Cubic Hermite Spline","Akima Interpolator","PCHIP 1D",
                            "Barycentric Interpolator","Krogh Interpolator","Equation fitting"]

        self._initMenu()
        self.initDialog()
    
    def _initMenu(self):
        self.menu_method = Menu()
        interpolation = Menu("Interpolation")
        self.menu_method.addMenu(interpolation)
        for i in ["B-Spline","Cubic Hermite Spline","Akima Interpolator","PCHIP 1D",
                  "Barycentric Interpolator","Krogh Interpolator"]:
            action = QAction(i, self)
            interpolation.addAction(action)
        eqn = QAction("Equation fitting", self.menu_method)
        self.menu_method.addAction(eqn)

        self.menu_method.triggered.connect(lambda s: self.method.button.setText(s.text()))
        self.menu_method.triggered.connect(lambda s: self.stackedlayout.setCurrentIndex(self.method_list.index(s.text())))
    
    def initDialog(self):
        self.dialog = Dialog("Configuration", self.parent)
        
        self.method = DropDownPrimaryPushButton(text="Method")
        self.method.button.setMenu(self.menu_method)
        self.method.button.setText(self._config["method"])
        self.dialog.main_layout.addWidget(self.method)
        self.dialog.main_layout.addWidget(SeparateHLine())

        self.stackedlayout = QStackedLayout()
        self.dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(BSpline())
        self.stackedlayout.addWidget(CubicHermite())
        self.stackedlayout.addWidget(Akima())
        self.stackedlayout.addWidget(PCHIP1D())
        self.stackedlayout.addWidget(Barycentric())
        self.stackedlayout.addWidget(Krogh())
        self.stackedlayout.addWidget(EquationFit())
        

        self.stackedlayout.setCurrentIndex(self.method_list.index(self.method.button.text()))
        self.currentWidget().set_config(self._config["config"])
    
    def config(self):
        if self.dialog.exec():
            self.currentWidget().update_config()
            self._config.update(
                method = self.method.button.text(),
                config = self.currentWidget()._config
            )
            self.exec()

    def currentWidget(self) -> FitBase:
        return self.stackedlayout.currentWidget()
        
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            X = np.arange(10)
            Y = 3*np.exp(X) + 4
            self.node.input_sockets[0].socket_data = pd.DataFrame(X, columns=["X"])
            self.node.input_sockets[1].socket_data = pd.DataFrame(Y, columns=["Y"])
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            self.X = self.node.input_sockets[0].socket_data.copy(deep=True)
            self.Y = self.node.input_sockets[1].socket_data.copy(deep=True)
            data = pd.concat([self.X, self.Y], axis=1)
    
            try:
                self.currentWidget().run(self.X.to_numpy().ravel(), self.Y.to_numpy().ravel())
                data["Fitted"] = self.currentWidget().predict(self.X)
                data["Residues"] = self.currentWidget().predict(self.X.to_numpy().ravel()) - self.Y.to_numpy().ravel()

                # change progressbar's color
                self.progress.changeColor('success')
                # write log
                logger.info(f"{self.name} {self.node.id}: run successfully.")

            except RuntimeError as e:
                # change progressbar's color
                self.progress.changeColor('fail')
                # write log
                logger.info(f"{self.name} {self.node.id}: failed.")
                
            
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = self
        self.node.output_sockets[1].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    
    
    def predict(self, X):
        """ this function behaves the same as estimator in machine learning 
        to use with predictor node """
        self.currentWidget().predict(X)

    def result_dialog(self):
        self.currentWidget().result_dialog()

    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        self.node.input_sockets[1].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
        