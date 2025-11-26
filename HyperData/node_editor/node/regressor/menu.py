from ui.base_widgets.menu import Menu
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction

DEBUG = False

class AlgorithmMenu(Menu):
    sig = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        linear_model = Menu("Linear Model", self)
        for i in ["Linear Regression","Ridge","Lasso","Multi-task Lasso","ElasticNet",
                  "Multi-task ElasticNet","Least Angle Regression","LARS Lasso",
                  "Orthogonal Matching Pursuit","Bayesian Ridge",
                  "Automatic Relevance Determination","Generalized Linear Model",
                  "Theil-Sen Regression","Huber Regression","Quantile Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            linear_model.addAction(action)
        self.addMenu(linear_model)

        svm = Menu("Support Vector Machines", self)
        for i in ["SVR","NuSVR"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            svm.addAction(action)
        self.addMenu(svm)

        neighbors = Menu("Nearest Neighbors", self)
        for i in ["K Neighbors","Radius Neighbors"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            neighbors.addAction(action)
        self.addMenu(neighbors)

        tree = Menu('Tree', self)
        for i in ['Decision Tree','Extra Tree']:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            tree.addAction(action)
        self.addMenu(tree)

        ensemble = Menu('Ensemble', self)
        for i in ['Random Forest','Extra Trees','Gradient Boosting','Histogram Gradient Boosting']:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            ensemble.addAction(action)
        self.addMenu(ensemble)

        others = Menu("Others", self)
        for i in ["Kernel Ridge","Gaussian Process","Partial Least Squares","Dummy"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            others.addAction(action)
        self.addMenu(others)