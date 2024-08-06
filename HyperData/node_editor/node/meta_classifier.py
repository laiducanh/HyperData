from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.classifier import ClassifierBase, AlgorithmMenu
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import DropDownPushButton, Toggle, ComboBox
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from ui.base_widgets.frame import SeparateHLine
from config.settings import logger
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout
from PyQt6.QtGui import QAction, QCursor
from sklearn import ensemble, tree


class Bagging(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(estimator=tree.DecisionTreeClassifier(),
                                               n_estimators=10,max_samples=1.0,max_features=1.0,
                                               bootstrap=True,bootstrap_features=False,
                                               oob_score=False,warm_start=False,verbose=0)
        else: self._config = config
        self.estimator = ensemble.BaggingClassifier(**self._config)

        self.estimator = ComboBox

        
    def set_estimator(self):
        
        self.estimator = ensemble.BaggingClassifier(**self._config)

class MetaClassifier(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setTitle("Train/Test")
        self.node.input_sockets[1].setTitle("Classifier")
        self.node.output_sockets[0].setTitle("Model")
        self.node.output_sockets[1].setTitle("Data out")

    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)
        menu = AlgorithmMenu()
        menu.sig.connect(lambda string: algorithm.button.setText(string))
        menu.sig.connect(lambda string: stackedlayout.setCurrentIndex(self.estimator_list.index(string)))
        algorithm = DropDownPushButton(text="Algorithm")
        algorithm.button.setText(self._config["estimator"].title())
        algorithm.button.setMenu(menu)
        algorithm.button.released.connect(lambda: menu.exec(QCursor().pos()))
        dialog.main_layout.addWidget(algorithm)
        dialog.main_layout.addWidget(SeparateHLine())
        stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(stackedlayout)
    
    def eval(self):
        # reset input sockets
        for socket in self.node.input_sockets:
            socket.socket_data = None

        # update input sockets
        self.node.input_sockets[1].socket_data = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data.append(edge.start_socket.socket_data)
