from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal
from ui.base_widgets.menu import Menu

DEBUG = False

class AlgorithmMenu(Menu):
    sig = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        linear_model = Menu("Linear Model", self)
        for i in ["Ridge Classifier","Logistic Regression","SGD Classifier",
                  "Passive Aggressive Classifier"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            linear_model.addAction(action)
        self.addMenu(linear_model)
        
        svm = Menu("Support Vector Machines", self)
        for i in ["SVC", "NuSVC","Linear SVC"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            svm.addAction(action)
        self.addMenu(svm)

        neighbors = Menu("Nearest Neighbors", self)
        for i in ["K Neighbors Classifier","Nearest Centroid", "Radius Neighbors Classifier"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            neighbors.addAction(action)
        self.addMenu(neighbors)

        ensembles = Menu("Ensembles", self)
        for i in ["Gradient Boosting Classifier","Histogram Gradient Boosting Classifier",
                  "Random Forest Classifier","Extra Trees Classifier"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            ensembles.addAction(action)
        self.addMenu(ensembles)

        others = Menu("Others", self)
        for i in ["Decision Tree Classifier", "Gaussian Process Classifier"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            others.addAction(action)
        self.addMenu(others)