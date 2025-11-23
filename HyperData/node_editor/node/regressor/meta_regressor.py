from node_editor.base.node_graphics_content import NodeContentWidget
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (HDropDownPrimaryPushButton, TransparentPushButton)
from ui.base_widgets.frame import SeparateHLine
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.train_test_split import TrainTestSplitter
from node_editor.node.regressor.menu import AlgorithmMenu
from node_editor.node.regressor.report import scoring, Report
from node_editor.node.regressor.base import RegressorBase
from node_editor.node.regressor.bagging import Bagging
from node_editor.node.regressor.voting import Voting
from node_editor.node.regressor.stacking import Stacking
from node_editor.node.regressor.adaboost import AdaBoost
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import HPrimaryComboBox
from PySide6.QtWidgets import QStackedLayout
from sklearn import ensemble
import pandas as pd

DEBUG = False

class MetaRegressor(NodeContentWidget):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)

        self.X, self.Y = list(), list()
        self.Y_test_score, self.Y_pred_score = list(), list()

        self.node.input_sockets[0].setSocketLabel("Splitter")
        self.node.input_sockets[1].setSocketLabel("Estimators")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Estimator")
        self.node.output_sockets[2].setSocketLabel("Data out")

        self.score_btn = TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "r2 score"

        self._config = dict(
            estimator = "Bagging",
            config = dict(),
        )
        
        self.estimator_list = ["Bagging","Voting","Stacking","AdaBoost"]
        
        self.create_model()

    def create_model(self):
        estimators = self.node.input_sockets[1].socket_data
        if not estimators:
            estimators = [None]
        if self._config['estimator'] == 'Bagging':
            model = ensemble.BaggingRegressor(
                estimator=estimators[0],
                **self._config['config']
            )
        elif self._config['estimator'] == 'Voting':
            model = ensemble.VotingRegressor(
                estimators=estimators,
                **self._config['config']
            )
        elif self._config['estimator'] == 'Stacking':
            model = ensemble.StackingRegressor(
                estimators=estimators,
                **self._config['config']
            )
        elif self._config['estimator'] == 'AdaBoost':
            model = ensemble.AdaBoostRegressor(
                estimator=estimators[0],
                **self._config['config']
            )
        self.estimator = model
        self.model = model
    
    def currentWidget(self) -> RegressorBase:
        return self.stackedlayout.currentWidget()

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        algorithm = HPrimaryComboBox(
            items=self.estimator_list,
            label='Algorithm',
            getter=lambda: self._config['estimator'],
            setter=lambda s: self.stackedlayout.setCurrentIndex(self.estimator_list.index(s)),
            layout=dialog.main_layout
        )
        dialog.main_layout.addWidget(SeparateHLine())
        estimators = []
        for i in self.node.input_sockets[1].socket_data:
            estimators.append(i.__class__.__name__)
        estimators = ', '.join(estimators)
        dialog.main_layout.addWidget(BodyLabel(f"Estimators: {estimators}"))
        dialog.main_layout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)

        self.stackedlayout.addWidget(Bagging())
        self.stackedlayout.addWidget(Voting())
        self.stackedlayout.addWidget(Stacking())
        self.stackedlayout.addWidget(AdaBoost())

        self.stackedlayout.setCurrentIndex(self.estimator_list.index(algorithm.get_value()))

        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                estimator = algorithm.button.currentText()
            )
            self.exec()
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection, preprocessing
            from sklearn.utils.validation import check_is_fitted
            from sklearn.exceptions import NotFittedError
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
            if DEBUG or isinstance(self.node.input_sockets[0].edges[0].start_socket.node.content, TrainTestSplitter):
                # cv is an array of indexes corresponding to (train, test)
                cv = self.node.input_sockets[0].socket_data[0]
                self.X = self.node.input_sockets[0].socket_data[1]
                self.Y = self.node.input_sockets[0].socket_data[2]

                data = pd.concat([self.X, self.Y], axis=1)

                # convert self.X and self.Y into numpy arrays!
                self.X = self.X.to_numpy()
                self.Y = self.Y.to_numpy()
            
                for fold, (train_idx, test_idx) in enumerate(cv):
                    X_train, X_test = self.X[train_idx], self.X[test_idx]
                    Y_train, Y_test = self.Y[train_idx], self.Y[test_idx]

                    self.model = self.create_model()                   
                    self.model.fit(X_train, Y_train)
                    Y_pred = self.model.predict(X_test)
                    Y_pred_all = self.model.predict(self.X)

                    self.Y_test_score.append(Y_test)
                    self.Y_pred_score.append(Y_pred)

                    data[f"Fold{fold+1}_Prediction"] = Y_pred_all

                score = scoring(self.Y_test_score, self.Y_pred_score)
                self.score_btn.setText(f"Score: {score[self.score_function]}")
                # change progressbar's color   
                self.progress.changeColor('success')
                # write log
                logger.info(f"{self.name} {self.node.id}: {self.estimator} run successfully.")
            else:
                data = pd.DataFrame()
                self.score_btn.setText(f"Score: --")
                # change progressbar's color   
                self.progress.changeColor('fail')
                # write log
                logger.warning(f"{self.name} {self.node.id}: not a valid splitter, return an empty Dataframe.")
        
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
        dialog = Report(self.Y_test_score, self.Y_pred_score)
        score = scoring(self.Y_test_score, self.Y_pred_score)
        dialog.metricChange.connect(lambda s: self.score_btn.setText(f"Score {score[s]}"))
        if dialog.exec():
            self.score_function = dialog.score_function
    
    def eval(self):
        self.resetNode()
        # reset input sockets
        self.node.input_sockets[0].socket_data = [[],pd.DataFrame(), pd.DataFrame()]
        self.node.input_sockets[1].socket_data = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data.append(edge.start_socket.socket_data)
    
    def resetNode(self):
        try: self.score_btn.setText(f"Score: --")
        except: pass
        return super().resetNode()