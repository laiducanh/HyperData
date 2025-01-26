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
        for i in ["Linear Regression","Ridge Regression","Lasso","ElasticNet",
                  "Least Angle Regression","LARS Lasso","Orthogonal Matching Pursuit",
                  "Bayesian Ridge Regression","Automatic Relevance Determination",
                  "Stochastic Gradient Descent","Passive Aggressive Regression",
                  "Random Sample Consensus","Theil-Sen Regression","Huber Regression",
                  "Quantile Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            linear_model.addAction(action)
        self.addMenu(linear_model)

        generalizedlinear_model = Menu("Generalized Linear Model", self)
        for i in ["Tweedie Regression","Poisson Regression","Gamma Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            generalizedlinear_model.addAction(action)
        self.addMenu(generalizedlinear_model)

        svm = Menu("Support Vector Machines", self)
        for i in ["SVR","NuSVR","Linear SVR"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            svm.addAction(action)
        self.addMenu(svm)

        neighbors = Menu("Nearest Neighbors", self)
        for i in ["K Neighbors Regression","Radius Neighbors Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            neighbors.addAction(action)
        self.addMenu(neighbors)

        gaussian = Menu("Gaussian Process", self)
        for i in ["Gaussian Process Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            gaussian.addAction(action)
        self.addMenu(gaussian)