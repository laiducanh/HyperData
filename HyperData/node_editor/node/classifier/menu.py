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
        for i in ["Ridge","Logistic Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            linear_model.addAction(action)
        self.addMenu(linear_model)

        da = Menu('Discriminant Analysis', self)
        for i in ["Linear Discriminant Analysis", "Quadratic Discriminant Analysis"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            da.addAction(action)
        self.addMenu(da)
        
        svm = Menu("Support Vector Machines", self)
        for i in ["SVC", "NuSVC"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            svm.addAction(action)
        self.addMenu(svm)

        neighbors = Menu("Nearest Neighbors", self)
        for i in ["K Neighbors","Nearest Centroid", "Radius Neighbors",
                  "Neighborhood Component Analysis"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            neighbors.addAction(action)
        self.addMenu(neighbors)

        tree = Menu('Tree', self)
        for i in ["Decision Tree","Extra Tree"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            tree.addAction(action)
        self.addMenu(tree)

        bayes = Menu('Naive Bayes')
        for i in ["Gaussian Naive Bayes","Multinomial Naive Bayes","Complement Naive Bayes",
                  "Bernoulli Naive Bayes","Categorical Naive Bayes"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            bayes.addAction(action)
        self.addMenu(bayes)

        ensembles = Menu("Ensembles", self)
        for i in ["Gradient Boosting","Histogram Gradient Boosting","Random Forest","Extra Trees"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            ensembles.addAction(action)
        self.addMenu(ensembles)

        others = Menu("Others", self)
        for i in ["Gaussian Process","Dummy"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            others.addAction(action)
        self.addMenu(others)