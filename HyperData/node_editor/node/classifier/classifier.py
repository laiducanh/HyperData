from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import linear_model
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HDropDownPrimaryPushButton, TransparentPushButton, HPrimaryComboBox
from ui.base_widgets.frame import SeparateHLine
from node_editor.node.train_test_split.train_test_split import TrainTestSplitter
from node_editor.node.train_test_split.cv_split import CVSplitter
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout
from node_editor.node.classifier.menu import AlgorithmMenu
from node_editor.node.classifier.report import scoring, Report
from node_editor.node.classifier.base import ClassifierBase
from node_editor.node.classifier.ridge import RidgeClassifier
from node_editor.node.classifier.logistic import LogisticRegression
from node_editor.node.classifier.discriminant_analysis import LDA, QDA
from node_editor.node.classifier.svc import SVC
from node_editor.node.classifier.nu_svc import NuSVC
from node_editor.node.classifier.kneighbors import KNeighbors
from node_editor.node.classifier.nearest_centroid import NearestCentroid
from node_editor.node.classifier.radius_neighbors import RadiusNeighbors
from node_editor.node.classifier.nca import NCA
from node_editor.node.classifier.bayes import GaussianNB, MultinomialNB, ComplementNB, BernoulliNB, CategoricalNB
from node_editor.node.classifier.gradient_boosting import GradientBoosting
from node_editor.node.classifier.histgrad_boosting import HistGradientBoosting
from node_editor.node.classifier.random_forest import RandomForest
from node_editor.node.classifier.extra_tree import ExtraTree, ExtraTrees
from node_editor.node.classifier.decision_tree import DecisionTree
from node_editor.node.classifier.gaussian_process import GaussianProcess
from node_editor.node.classifier.dummy import Dummy

DEBUG = False

class Classifier (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.X, self.Y = list(), list()
        self.X_test, self.Y_test, self.Y_pred = list(), list(), list()

        self.node.input_sockets[0].setSocketLabel("Splitter")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Estimator")
        self.node.output_sockets[2].setSocketLabel("Data out")

        self.score_btn = TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "Accuracy"
        
        self._config = dict(
            estimator = "Logistic Regression",
            config = dict(),
            multiclass_strategy = "None"
        )
        
        self.estimator_list = ["Ridge","Logistic Regression","Linear Discriminant Analysis",
                               "Quadratic Discriminant Analysis","SVC", "NuSVC",
                               "K Neighbors","Nearest Centroid","Radius Neighbors",
                               "Neighborhood Component Analysis","Gaussian Process","Gaussian Naive Bayes",
                               "Multinomial Naive Bayes","Complement Naive Bayes","Bernoulli Naive Bayes",
                               "Categorical Naive Bayes","Decision Tree","Extra Tree","Random Forest",
                               "Extra Trees","Gradient Boosting", "Histogram Gradient Boosting","Dummy",
                                ]
        
        self.estimator = linear_model.LogisticRegression(**self._config["config"])
        self.create_model()
    
    def currentWidget(self) -> ClassifierBase:
        return self.stackedlayout.currentWidget()       

    def create_model(self):
        if self._config['multiclass_strategy'] == "One vs. Rest":
            self.model = OneVsRestClassifier(self.estimator)
        elif self._config['multiclass_strategy'] == "One vs. One":
            self.model = OneVsOneClassifier(self.estimator) 
        else:
            self.model = self.estimator

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        multiclass = HPrimaryComboBox(
            items=["One vs. Rest","One vs. One","None"],
            label="Multiclass Strategy",
            getter=lambda: self._config['multiclass_strategy'],
            layout=dialog.main_layout
        )
        dialog.main_layout.addWidget(SeparateHLine())
        menu = AlgorithmMenu()
        menu.sig.connect(lambda s: algorithm.button.setText(s))
        menu.sig.connect(lambda s: self.stackedlayout.setCurrentIndex(self.estimator_list.index(s)))
        algorithm = HDropDownPrimaryPushButton(label="Algorithm")
        algorithm.button.setText(self._config["estimator"])
        algorithm.button.setMenu(menu)
        dialog.main_layout.addWidget(algorithm)
        dialog.main_layout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(RidgeClassifier())
        self.stackedlayout.addWidget(LogisticRegression())
        self.stackedlayout.addWidget(LDA())
        self.stackedlayout.addWidget(QDA())
        self.stackedlayout.addWidget(SVC())
        self.stackedlayout.addWidget(NuSVC())
        self.stackedlayout.addWidget(KNeighbors())
        self.stackedlayout.addWidget(NearestCentroid())
        self.stackedlayout.addWidget(RadiusNeighbors())
        self.stackedlayout.addWidget(NCA())
        self.stackedlayout.addWidget(GaussianProcess())
        self.stackedlayout.addWidget(GaussianNB())
        self.stackedlayout.addWidget(MultinomialNB())
        self.stackedlayout.addWidget(ComplementNB())
        self.stackedlayout.addWidget(BernoulliNB())
        self.stackedlayout.addWidget(CategoricalNB())
        self.stackedlayout.addWidget(DecisionTree())
        self.stackedlayout.addWidget(ExtraTree())
        self.stackedlayout.addWidget(RandomForest())
        self.stackedlayout.addWidget(ExtraTrees())
        self.stackedlayout.addWidget(GradientBoosting())
        self.stackedlayout.addWidget(HistGradientBoosting())
        self.stackedlayout.addWidget(Dummy())
        
        self.stackedlayout.setCurrentIndex(self.estimator_list.index(algorithm.button.text()))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                estimator = algorithm.button.text(),
                multiclass_strategy = multiclass.get_value()
            )
            self.estimator = self.currentWidget().estimator
            self.create_model()
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()

    def func(self):
        # reset UI
        self.score_btn.setText(f"Score: --")
        self.label.setText('Shape: (--, --)') 
        self.data_to_view = pd.DataFrame()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection
            X, Y = datasets.make_classification(
                n_samples=1000,      # number of rows
                n_features=20,       # total number of features
                n_informative=5,     # features that actually affect the label
                n_redundant=2,       # linear combinations of informative features
                n_classes=2,         # binary classification
                flip_y=0.05,         # 5% noisy labels
                weights=[0.9, 0.1],  # 90% class 0, 10% class 1
                random_state=42
            )
            split = model_selection.ShuffleSplit(n_splits=5, test_size=0.2).split(X, Y)
            result = list()
            for fold, (train_idx, test_idx) in enumerate(split):
                result.append((train_idx, test_idx))
            self.node.input_sockets[0].socket_data = [result, pd.DataFrame(X), pd.DataFrame(Y)]
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            if DEBUG or (isinstance(self.node.input_sockets[0].edges[0].start_socket.node.content, 
                            (TrainTestSplitter, CVSplitter))):
                cv = self.node.input_sockets[0].socket_data[0]
                self.X = self.node.input_sockets[0].socket_data[1]
                self.Y = self.node.input_sockets[0].socket_data[2]
                self.X_test, self.Y_test, self.Y_pred = list(), list(), list()
               
                data = self.node.input_sockets[0].socket_data[1].copy()
                n_samples = self.Y.shape[0]
                n_classes = self.Y.shape[1]   
                
                data["Encoded Label"] = None
                for i in range(n_samples):
                    for j in range(n_classes):
                        data.iloc[i,-1] = str(self.Y.iloc[i,j])
                            
                # convert self.X and self.Y into numpy arrays!
                X = self.X.to_numpy()
                Y = self.Y.to_numpy()
                
                for fold, (train_idx, test_idx) in enumerate(cv):

                    X_train, X_test = X[train_idx], X[test_idx]
                    Y_train, Y_test = Y[train_idx], Y[test_idx]

                    self.create_model()
                    self.model.fit(X_train, Y_train.ravel())
                    Y_pred = self.model.predict(X_test)
                    Y_pred_all = self.model.predict(X)

                    self.X_test.append(X_test)
                    self.Y_test.append(Y_test)
                    self.Y_pred.append(Y_pred)

                    Y_pred_all = np.reshape(Y_pred_all, (n_samples, n_classes))
                    data[f"Fold{fold+1}_Prediction"] = str()
                    for i in range(n_samples):
                        for j in range(n_classes):
                            data.iloc[i,-1] += str(Y_pred_all[i,j])
                                
                score = scoring(self.Y_test, self.Y_pred, self.score_function)
                self.score_btn.setText(f"Score: {score}")
                
                # change progressbar's color   
                self.progress.changeColor('success')
                # write log
                logger.info(f"{self.name} {self.node.id}: {self.model.__class__.__name__} run successfully.")

            else:
                data = pd.DataFrame()
                self.score_btn.setText(f"Score: --")
                # write log
                logger.warning(f"{self.name} {self.node.id}: Splitter is not valid, return an empty Dataframe.")
                logger.info(f"{self.name} {self.node.id}: use the estimator {self.estimator.__class__.__name__} for meta-classifiers.")
        
        except Exception as e:
            data = pd.DataFrame()
            self.score_btn.setText(f"Score: --")
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = self.model
        self.node.output_sockets[1].socket_data = self.estimator
        self.node.output_sockets[2].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def score_dialog(self):
        dialog = Report(self.model, self.estimator, self.X, self.Y, self.X_test, self.Y_test, self.Y_pred, self.score_function)
        
        if dialog.exec():
            self.score_function = dialog.score_function
            score = scoring(self.Y_test, self.Y_pred, self.score_function)
            self.score_btn.setText(f"Score: {score}")
     
    def eval (self):
        self.resetNode()
        # reset socket data
        self.node.input_sockets[0].socket_data = [[],pd.DataFrame(), pd.DataFrame()]
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data

    def resetNode(self):
        try: self.score_btn.setText(f"Score: --")
        except: pass
        return super().resetNode()
