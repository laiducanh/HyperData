from node_editor.node.classifier.report import scoring, Report
from node_editor.node.train_test_split.train_test_split import TrainTestSplitter
from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.button import _TransparentPushButton, Toggle, PrimaryComboBox
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.window import Dialog
from config.settings import logger, GLOBAL_DEBUG
from sklearn import ensemble
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
import pandas as pd
import numpy as np

DEBUG = False

class BaggingClassifier(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.X, self.Y = pd.DataFrame(), pd.DataFrame()
        self.estimator = None
        self.X_test, self.Y_test, self.Y_pred = list(), list(), list()

        self.node.input_sockets[0].setSocketLabel("Estimator")
        self.node.input_sockets[1].setSocketLabel("Splitter")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Data out")

        self.score_btn = _TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "Accuracy"

        
        self._config = dict(
            n_estimators=10,
            max_samples=1.0,
            max_features=1.0,
            bootstrap=True,
            bootstrap_features=False,
            oob_score=False,
        )
        self.multiclass_strategy = "One vs. Rest"
        self.create_model()
            
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        multiclass = PrimaryComboBox(items=["One vs. Rest","One vs. One"],text="Multiclass strategy")
        dialog.main_layout.addWidget(multiclass)

        n_estimators = SpinBox(min=1,text="Number of estimators")
        n_estimators.button.setValue(self._config["n_estimators"])
        dialog.main_layout.addWidget(n_estimators)

        max_samples = SpinBox(min=1, max=100, text="Sample sizes")
        max_samples.button.setValue(int(self._config["max_samples"]*100))
        dialog.main_layout.addWidget(max_samples)

        max_features = SpinBox(min=1, max=100, text="Feature sizes")
        max_features.button.setValue(int(self._config["max_features"]*100))
        dialog.main_layout.addWidget(max_features)

        bootstrap = Toggle(text="Bootstrap")
        bootstrap.button.setChecked(self._config["bootstrap"])
        dialog.main_layout.addWidget(bootstrap)

        bootstrap_features = Toggle(text="Bootstrap features")
        bootstrap_features.button.setChecked(self._config["bootstrap_features"])
        dialog.main_layout.addWidget(bootstrap_features)

        oob_score = Toggle(text="Out-of-bag samples")
        oob_score.button.setChecked(self._config["oob_score"])
        oob_score.button.checkedChanged.connect(lambda checked: oob_score.button.setChecked(False if not bootstrap.button.isChecked() else checked))
        bootstrap.button.checkedChanged.connect(lambda checked: oob_score.button.setChecked(False if not checked else self._config["oob_score"]))
        dialog.main_layout.addWidget(oob_score)

        if dialog.exec():
            self._config.update(
                n_estimators=n_estimators.button.value(),
                max_samples=max_samples.button.value()/100,
                max_features=max_features.button.value()/100,
                bootstrap=bootstrap.button.isChecked(),
                bootstrap_features=bootstrap_features.button.isChecked(),
                oob_score=oob_score.button.isChecked()
            )
            self.multiclass_strategy = multiclass.button.currentText()
            self.create_model()
            self.exec()
    
    def create_model(self):
        if self.multiclass_strategy == "One vs. Rest":
            self.model = OneVsRestClassifier(ensemble.BaggingClassifier(self.estimator,**self._config))
        elif self.multiclass_strategy == "One vs. One":
            self.model = OneVsOneClassifier(ensemble.BaggingClassifier(self.estimator,**self._config))
    
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection, preprocessing, tree
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
            self.node.input_sockets[0].socket_data = tree.DecisionTreeClassifier()
            self.node.input_sockets[1].socket_data = [result, X, Y]
            # print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            if DEBUG or (self.node.input_sockets[0].edges and isinstance(self.node.input_sockets[1].edges[0].start_socket.node.content, TrainTestSplitter)):
                self.estimator = self.node.input_sockets[0].socket_data
                cv = self.node.input_sockets[1].socket_data[0]
                self.X = self.node.input_sockets[1].socket_data[1]
                self.Y = self.node.input_sockets[1].socket_data[2]

                data = self.node.input_sockets[1].socket_data[1].copy()
                n_classes = self.Y.shape[1]   
                n_samples = self.Y.shape[0]
                
                data[f"Encoded Label"] = str()
                for i in range(n_samples):
                    for j in range(n_classes):
                        data.iloc[i,-1] += str(self.Y.iloc[i,j])
                
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
                self.score_btn.setText(f"Score: {score[self.score_function]:.2f}")

                # change progressbar's color   
                self.progress.changeColor('success')
                # write log
                if DEBUG or GLOBAL_DEBUG: print('data out', data)
                logger.info(f"{self.name} {self.node.id}: {self.model} run successfully.")
            
            else:
                data = pd.DataFrame()
                self.score_btn.setText(f"Score: --")
                # change progressbar's color   
                self.progress.changeColor('fail')
                # write log
                logger.warning(f"{self.name} {self.node.id}: Did not define splitter, return an empty Dataframe.")
        
        except Exception as e:
            data = pd.DataFrame()
            self.score_btn.setText(f"Score: --")
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = self.model
        self.node.output_sockets[1].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def score_dialog(self):
        dialog = Report(self.model, self.X_test, self.Y_test, self.Y_pred)
        
        if dialog.exec():
            self.score_function = dialog.score_function
    
    def eval(self):
        self.resetStatus()
        # reset socket data
        self.node.input_sockets[0].socket_data = None
        self.node.input_sockets[1].socket_data = [[],pd.DataFrame(), pd.DataFrame()]
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
        
    
    