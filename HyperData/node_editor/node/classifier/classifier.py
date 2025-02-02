from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import linear_model
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import DropDownPrimaryPushButton, _TransparentPushButton, PrimaryComboBox
from ui.base_widgets.frame import SeparateHLine
from node_editor.node.train_test_split.train_test_split import TrainTestSplitter
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout
from node_editor.node.classifier.menu import AlgorithmMenu
from node_editor.node.classifier.report import scoring, Report
from node_editor.node.classifier.base import ClassifierBase
from node_editor.node.classifier.ridge import RidgeClassifier
from node_editor.node.classifier.logistic import LogisticRegression
from node_editor.node.classifier.sgd import SGDClassifier
from node_editor.node.classifier.passive_aggressive import PassiveAggressiveClassifier
from node_editor.node.classifier.svc import SVC
from node_editor.node.classifier.nu_svc import NuSVC
from node_editor.node.classifier.linear_svc import Linear_SVC
from node_editor.node.classifier.kneighbors import KNeighbors
from node_editor.node.classifier.nearest_centroid import NearestCentroid
from node_editor.node.classifier.radius_neighbors import RadiusNeighbors
from node_editor.node.classifier.gradient_boosting import GradientBoosting
from node_editor.node.classifier.histgrad_boosting import HistGradientBoosting
from node_editor.node.classifier.random_forest import RandomForest
from node_editor.node.classifier.extra_trees import ExtraTrees
from node_editor.node.classifier.decision_tree import DecisionTree
from node_editor.node.classifier.gaussian_process import GaussianProcess

DEBUG = False

class Classifier (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.X, self.Y = list(), list()
        self.X_test, self.Y_test, self.Y_pred = list(), list(), list()

        self.node.input_sockets[0].setSocketLabel("Train/Test")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Estimator")
        self.node.output_sockets[2].setSocketLabel("Data out")

        self.score_btn = _TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "Accuracy"
        
        self._config = dict(
            estimator = "Logistic Regression",
            config = dict(),
        )
        
        self.estimator_list = ["Ridge Classifier","Logistic Regression","SGD Classifier",
                               "Passive Aggressive Classifier", "SVC", "NuSVC", "Linear SVC",
                               "K Neighbors Classifier","Nearest Centroid", "Radius Neighbors Classifier",
                               "Gradient Boosting Classifier", "Histogram Gradient Boosting Classifier",
                               "Random Forest Classifier", "Extra Trees Classifier",
                               "Decision Tree Classifier","Gaussian Process Classifier"]
        
        self.estimator = linear_model.LogisticRegression(**self._config["config"])
        self.multiclass_strategy = "One vs. Rest"
        self.create_model()
    
    def currentWidget(self) -> ClassifierBase:
        return self.stackedlayout.currentWidget()       

    def create_model(self):
        if self.multiclass_strategy == "One vs. Rest":
            self.model = OneVsRestClassifier(self.estimator)
        elif self.multiclass_strategy == "One vs. One":
            self.model = OneVsOneClassifier(self.estimator)    

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        multiclass = PrimaryComboBox(items=["One vs. Rest","One vs. One"],text="Multiclass strategy")
        dialog.main_layout.addWidget(multiclass)
        dialog.main_layout.addWidget(SeparateHLine())
        menu = AlgorithmMenu()
        menu.sig.connect(lambda s: algorithm.button.setText(s))
        menu.sig.connect(lambda s: self.stackedlayout.setCurrentIndex(self.estimator_list.index(s)))
        algorithm = DropDownPrimaryPushButton(text="Algorithm")
        algorithm.button.setText(self._config["estimator"])
        algorithm.button.setMenu(menu)
        dialog.main_layout.addWidget(algorithm)
        dialog.main_layout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(RidgeClassifier())
        self.stackedlayout.addWidget(LogisticRegression())
        self.stackedlayout.addWidget(SGDClassifier())
        self.stackedlayout.addWidget(PassiveAggressiveClassifier())
        self.stackedlayout.addWidget(SVC())
        self.stackedlayout.addWidget(NuSVC())
        self.stackedlayout.addWidget(Linear_SVC())
        self.stackedlayout.addWidget(KNeighbors())
        self.stackedlayout.addWidget(NearestCentroid())
        self.stackedlayout.addWidget(RadiusNeighbors())
        self.stackedlayout.addWidget(GradientBoosting())
        self.stackedlayout.addWidget(HistGradientBoosting())
        self.stackedlayout.addWidget(RandomForest())
        self.stackedlayout.addWidget(ExtraTrees())
        self.stackedlayout.addWidget(DecisionTree())
        self.stackedlayout.addWidget(GaussianProcess())
        self.stackedlayout.setCurrentIndex(self.estimator_list.index(algorithm.button.text()))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                estimator = algorithm.button.text()
            )
            self.estimator = self.currentWidget().estimator
            self.multiclass_strategy = multiclass.button.currentText()
            self.create_model()
            self.exec()

    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection, preprocessing
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            X = df.iloc[:,:4]
            Y = preprocessing.LabelEncoder().fit_transform(df.iloc[:,4])
            Y = pd.DataFrame(data=Y)
            split = model_selection.ShuffleSplit(n_splits=5, test_size=0.2).split(X, Y)
            result = list()
            for fold, (train_idx, test_idx) in enumerate(split):
                result.append((train_idx, test_idx))
            self.node.input_sockets[0].socket_data = [result, X, Y]
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            if DEBUG or (self.node.input_sockets[0].edges and isinstance(self.node.input_sockets[0].edges[0].start_socket.node.content, TrainTestSplitter)):
                cv = self.node.input_sockets[0].socket_data[0]
                self.X = self.node.input_sockets[0].socket_data[1]
                self.Y = self.node.input_sockets[0].socket_data[2]
                
                data = self.node.input_sockets[0].socket_data[1].copy()
                n_classes = self.Y.shape[1]   
                n_samples = self.Y.shape[0]
                
                data[f"Encoded Label"] = str()
                for i in range(n_samples):
                    for j in range(n_classes):
                        data.iloc[i,-1] += str(self.Y.iloc[i,j])

                # convert self.X and self.Y into numpy arrays!
                self.X = self.X.to_numpy()
                self.Y = self.Y.to_numpy()
                
                for fold, (train_idx, test_idx) in enumerate(cv):

                    X_train, X_test = self.X[train_idx], self.X[test_idx]
                    Y_train, Y_test = self.Y[train_idx], self.Y[test_idx]
                    
                    self.create_model()
                    self.model.fit(X_train, Y_train)
                    Y_pred = self.model.predict(X_test)
                    Y_pred_all = self.model.predict(self.X)

                    self.X_test.append(X_test)
                    self.Y_test.append(Y_test)
                    self.Y_pred.append(Y_pred)

                    Y_pred_all = np.reshape(Y_pred_all, (n_samples, n_classes))
                    data[f"Fold{fold+1}_Prediction"] = str()
                    for i in range(n_samples):
                        for j in range(n_classes):
                            data.iloc[i,-1] += str(Y_pred_all[i,j])
                                
                score = scoring(self.Y_test, self.Y_pred)
                self.score_btn.setText(f"Score: {score[self.score_function]}")
                
                # change progressbar's color   
                self.progress.changeColor('success')
                # write log
                if DEBUG or GLOBAL_DEBUG: print('data out', data)
                logger.info(f"{self.name} {self.node.id}: {self.model} run successfully.")

            else:
                data = pd.DataFrame()
                self.score_btn.setText(f"Score: --")
                # write log
                logger.warning(f"{self.name} {self.node.id}: Did not define splitter, return an empty Dataframe.")
                logger.info(f"{self.name} {self.node.id}: use the estimator for meta-classifiers.")
        
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
        dialog = Report(self.model, self.X_test, self.Y_test, self.Y_pred)
        
        if dialog.exec():
            self.score_function = dialog.score_function
     
    def eval (self):
        self.resetStatus()
        # reset socket data
        self.node.input_sockets[0].socket_data = [[],pd.DataFrame(), pd.DataFrame()]
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
