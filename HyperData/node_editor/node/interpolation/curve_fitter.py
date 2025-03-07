from PySide6.QtWidgets import QStackedLayout
from PySide6.QtGui import QAction
from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import _TransparentPushButton, PrimaryComboBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.menu import Menu
from node_editor.node.interpolation.base import FitBase
from node_editor.node.interpolation.equation import EquationFit
from node_editor.node.interpolation.b_spline import BSpline
from node_editor.node.interpolation.akima import Akima
from node_editor.node.interpolation.pchip import PCHIP1D
from node_editor.node.interpolation.barycentric import Barycentric
from node_editor.node.interpolation.krogh import Krogh
from node_editor.node.interpolation.lagrange import Lagrange
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
        self.method_list = ["B-Spline","Akima Interpolator","PCHIP 1D","Barycentric Interpolator",
                            "Krogh Interpolator","Lagrange Polynomial","Equation fitting"]

        self.initDialog()
    
    def initDialog(self):
        self.dialog = Dialog("Configuration", self.parent)
        
        self.method = PrimaryComboBox(items=self.method_list, text="Method")
        self.method.button.setCurrentText(self._config["method"])
        self.method.button.currentIndexChanged.connect(lambda s: self.stackedlayout.setCurrentIndex(s))
        self.dialog.main_layout.addWidget(self.method)
        self.dialog.main_layout.addWidget(SeparateHLine())

        self.stackedlayout = QStackedLayout()
        self.dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(BSpline())
        self.stackedlayout.addWidget(Akima())
        self.stackedlayout.addWidget(PCHIP1D())
        self.stackedlayout.addWidget(Barycentric())
        self.stackedlayout.addWidget(Krogh())
        self.stackedlayout.addWidget(Lagrange())
        self.stackedlayout.addWidget(EquationFit())
        
        self.stackedlayout.setCurrentIndex(self.method_list.index(self.method.button.currentText()))
        self.currentWidget().set_config(self._config["config"])
    
    def config(self):
        if self.dialog.exec():
            self.currentWidget().update_config()
            self._config.update(
                method = self.method.button.currentText(),
                config = self.currentWidget()._config
            )
            self.exec()

    def currentWidget(self) -> FitBase:
        return self.stackedlayout.currentWidget()
        
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            X = np.linspace(0, np.pi, 20)
            Y = 3*np.sin(X**2) + 4
            self.node.input_sockets[0].socket_data = pd.DataFrame(X)
            self.node.input_sockets[1].socket_data = pd.DataFrame(Y)
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            self.X = self.node.input_sockets[0].socket_data.copy(deep=True)
            self.Y = self.node.input_sockets[1].socket_data.copy(deep=True)
            data = pd.concat([self.X, self.Y], axis=1)
      
            try:
                self.currentWidget().run(self.X.iloc[:,0], self.Y.iloc[:,0])
                data["Fitted"] = self.currentWidget().predict(self.X.iloc[:,0])
                data["Residues"] = self.currentWidget().predict(self.X.iloc[:,0]) - self.Y.iloc[:,0]

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
        