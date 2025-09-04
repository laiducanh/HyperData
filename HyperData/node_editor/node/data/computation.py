from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HDropDownTransparentPushButton
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from ui.base_widgets.frame import SeparateHLine, VFrame
from ui.base_widgets.menu import Menu, Action
from ui.base_widgets.text import TitleLabel, BodyLabel

DEBUG = False

class DataComputation(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
        
        self._config = dict(
            function = "add",
            base = 1
        )
    
    def config(self):
        dialog = Dialog(title="Configuration", parent=self.parent)
        dialog.setMinimumSize(600, 400)
        dialog.main_layout.addWidget(TitleLabel("Data Computation"))
        dialog.main_layout.addWidget(BodyLabel("Arithmetic operation on the DataFrame"))
        dialog.main_layout.addWidget(SeparateHLine())

        menu = Menu()
        binary = Menu("Binary operator")
        menu.addMenu(binary)
        for text in ['add','subtract','multiply','floating divide',
                     'integer divide', 'remainder']:
            action = Action(text=text, parent=binary)
            action.triggered.connect(lambda _, text=text: func.set_value(text))
            binary.addAction(action)
        power = Menu('Power')
        menu.addMenu(power)
        for text in ['power','root','exponential power','natural exponential',
                     'logarithm','natural logarithm']:
            action = Action(text=text, parent=power)
            action.triggered.connect(lambda _, text=text: func.set_value(text))
            power.addAction(action)
        rounding = Menu("Rounding")
        menu.addMenu(rounding)
        for text in ['ceil','floor','fix','nearest integer','truncated value']:
            action = Action(text=text, parent=rounding)
            action.triggered.connect(lambda _, text=text: func.set_value(text))
            rounding.addAction(action)
        trigonometric = Menu('Trigonometric functions')
        menu.addMenu(trigonometric)
        for text in ['sine','cosine','tangent','arcsin','arccos','arctan',
                     'hypotenuse','radians to degrees','degrees to radians',
                     'sinh','cosh','tanh','arcsinh','arccosh','arctanh']:
            action = Action(text=text, parent=trigonometric)
            action.triggered.connect(lambda _, text=text: func.set_value(text))
            trigonometric.addAction(action)
        linalg = Menu("Linear algebra")
        menu.addMenu(linalg)
        for text in ['transpose','inverse','(Moore-Penrose) pseudo-inverse']:
            action = Action(text=text, parent=linalg)
            action.triggered.connect(lambda _, text=text: func.set_value(text))
            linalg.addAction(action)
        
        fr = VFrame(dialog.main_layout)
        base = HTransparentDoubleSpinBox(
            label='Base',
            getter=lambda: self._config['base'],
            layout=fr.vlayout
        )

        func = HDropDownTransparentPushButton(
            label='Function',
            getter=lambda: self._config['function'],
            menu=menu, 
            layout=fr.vlayout
        )

        if dialog.exec():
            self._config.update(
                function = func.get_value(),
                base = base.get_value()
            )
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()    
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            self.node.input_sockets[0].socket_data = df.copy()
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data.copy(deep=True)
            base = self._config['base']
            if self._config["function"] == "add":
                data = np.add(data, base)
            if self._config["function"] == "subtract":
                data = np.subtract(data, base)
            if self._config["function"] == "multiply":
                data = np.multiply(data, base)
            if self._config["function"] == "floating divide":
                data = np.true_divide(data, base)
            if self._config["function"] == "integer divide":
                data = np.floor_divide(data, base)
            if self._config["function"] == "remainder":
                data = np.remainder(data, base)
            if self._config["function"] == "power":
                data = np.power(data, base)
            if self._config["function"] == "root":
                data = np.power(data, 1/base)
            if self._config["function"] == "exponential power":
                data = base**data
            if self._config["function"] == "natural exponential":
                data = np.exp(data)
            if self._config["function"] == "logarithm":
                data = np.log(data)/np.log(base)
            if self._config["function"] == "natural logarithm":
                data = np.log(data)
            if self._config["function"] == "ceil":
                data = np.ceil(data)
            if self._config["function"] == "floor":
                data = np.floor(data)
            if self._config["function"] == "fix":
                data = np.fix(data)
            if self._config["function"] == "nearest integer":
                data = np.rint(data)
            if self._config["function"] == "truncated value":
                data = np.trunc(data)
            if self._config["function"] == "sine":
                data = np.sin(data)
            if self._config["function"] == "sine":
                data = np.sin(data)
            if self._config["function"] == "cosine":
                data = np.cos(data)
            if self._config["function"] == "tangent":
                data = np.tan(data)
            if self._config["function"] == "arcsine":
                data = np.arcsin(data)
            if self._config["function"] == "arccos":
                data = np.arccos(data)
            if self._config["function"] == "arctan":
                data = np.arctan(data)
            if self._config["function"] == "hypotenuse":
                data = np.hypot(data)
            if self._config["function"] == "radians to degrees":
                data = np.degrees(data)
            if self._config["function"] == "degrees to radians":
                data = np.radians(data)
            if self._config["function"] == "sinh":
                data = np.sinh(data)
            if self._config["function"] == "cosinh":
                data = np.cosh(data)
            if self._config["function"] == "tanh":
                data = np.tanh(data)
            if self._config["function"] == "arcsinh":
                data = np.arcsinh(data)
            if self._config["function"] == "arccosh":
                data = np.arccosh(data)
            if self._config["function"] == "arctanh":
                data = np.arctanh(data)
            if self._config["function"] == "transpose":
                data = np.transpose(data)
            if self._config["function"] == "inverse":
                data = np.linalg.inv(data)
            if self._config["function"] == '(Moore-Penrose) pseudo-inverse':
                data = np.linalg.pinv(data)
            
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")
           
        except Exception as e:
            data = self.node.input_sockets[0].socket_data
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: fail, return the original DataFrame.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()

    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data