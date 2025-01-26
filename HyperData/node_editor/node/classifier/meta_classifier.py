from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.classifier.classifier import ClassifierBase, AlgorithmMenu
from node_editor.node.classifier.bagging import BaggingClassifier
from node_editor.node.classifier.voting import VotingClassifier
from node_editor.node.classifier.stacking import Stacking
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import DropDownPushButton, _TransparentPushButton, ComboBox
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.menu import Menu
from config.settings import logger
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout
from PySide6.QtGui import QAction, QCursor
from sklearn import ensemble, tree

class MetaClassifier(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Train/Test")
        self.node.input_sockets[1].setSocketLabel("Classifier")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Data out")

        self.score_btn = _TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        #self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "Accuracy"
        
        self._config = dict(
            estimator = "Bagging Classifier",
            config = dict(),
        )
        
        self.estimator_list = ["Bagging Classifier","Voting Classifier","Stacking Classifier"]
        
        self.estimator = ensemble.BaggingClassifier(**self._config["config"])
    
    def setMenu(self) -> Menu:
        menu = Menu(self)
        for i in self.estimator_list:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))


    def config(self):
        dialog = Dialog("Configuration", self.parent)
        menu = Menu(self)
        for i in self.estimator_list:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: algorithm.button.setText(s))
            action.triggered.connect(lambda _, s=i: stackedlayout.setCurrentIndex(self.estimator_list.index(s)))
            menu.addAction(action)
        algorithm = DropDownPushButton(text="Algorithm")
        algorithm.button.setText(self._config["estimator"])
        algorithm.button.setMenu(menu)
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
