from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from typing import Union
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import model_selection
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox
from ui.base_widgets.frame import SeparateHLine
from node_editor.node.train_test_split.base import SplitterBase
from node_editor.node.train_test_split.group_kfold import GroupKFold
from node_editor.node.train_test_split.group_shuffle import GroupShuffleSplit
from node_editor.node.train_test_split.kfold import Kfold
from node_editor.node.train_test_split.logo import LeaveOneGroupOut
from node_editor.node.train_test_split.loo import LeaveOneOut
from node_editor.node.train_test_split.lpgo import LeavePGroupOut
from node_editor.node.train_test_split.lpo import LeavePOut
from node_editor.node.train_test_split.repeated_kfold import RepeatedKFold
from node_editor.node.train_test_split.repeated_stratified_kfold import RepeatedStratifiedKFold
from node_editor.node.train_test_split.shuffle import ShuffleSplit
from node_editor.node.train_test_split.stratified_group_kfold import StratifiedGroupKFold
from node_editor.node.train_test_split.stratified_kfold import StratifiedKFold
from node_editor.node.train_test_split.stratified_shuffle import StratifiedShuffleSplit
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QVBoxLayout, QStackedLayout

DEBUG = False

class CVSplitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Feature (X)")
        self.node.input_sockets[1].setSocketLabel("Label (Y)")
        self.node.output_sockets[0].setSocketLabel("Splitter")
        self.node.output_sockets[1].setSocketLabel("Data")
        self.data_to_view = pd.DataFrame()
        self._config = dict(
            splitter = "K Fold",
            config = None,
        )
        self.splitter = model_selection.KFold()
    
    def currentWidget(self) -> SplitterBase:
        return self.stackedlayout.currentWidget()

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.main_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMaximumSize)
        splitter = ComboBox(items=["Group K Fold","Group Shuffle Split","K Fold",
                                   "Leave One Group Out", "Leave p Group Out",
                                   "Geave One Out", "Leave p Out","Repeated K Fold",
                                   "Repeated Stratified K Fold","Shuffle Split",
                                   "Stratified K Fold","Stratified Shuffle Split",
                                   "Stratified Group K Fold"], text="Splitter")
        splitter.button.setCurrentText(self._config["splitter"])
        splitter.button.setMinimumWidth(200)
        splitter.button.currentTextChanged.connect(lambda: self.stackedlayout.setCurrentIndex(splitter.button.currentIndex()))
        dialog.main_layout.addWidget(splitter)
        dialog.main_layout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(GroupKFold())
        self.stackedlayout.addWidget(GroupShuffleSplit())
        self.stackedlayout.addWidget(Kfold())
        self.stackedlayout.addWidget(LeaveOneGroupOut())
        self.stackedlayout.addWidget(LeavePGroupOut())
        self.stackedlayout.addWidget(LeaveOneOut())
        self.stackedlayout.addWidget(LeavePOut())
        self.stackedlayout.addWidget(RepeatedKFold())
        self.stackedlayout.addWidget(RepeatedStratifiedKFold())
        self.stackedlayout.addWidget(ShuffleSplit())
        self.stackedlayout.addWidget(StratifiedKFold())
        self.stackedlayout.addWidget(StratifiedShuffleSplit())
        self.stackedlayout.addWidget(StratifiedGroupKFold())
        self.stackedlayout.setCurrentIndex(splitter.button.currentIndex())

        if dialog.exec():
            self.splitter = self.currentWidget().splitter
            self.splitter: Union[model_selection.BaseCrossValidator, model_selection.BaseShuffleSplit]
            self._config["splitter"] = splitter.button.currentText()
            self._config["config"] = self.currentWidget()._config
            self.exec()

    def func(self):
        self.eval()
        result = list()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, preprocessing
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            X = df.iloc[:,:4]
            Y = preprocessing.LabelEncoder().fit_transform(df.iloc[:,4])
            Y = pd.DataFrame(data=Y)
            self.node.input_sockets[0].socket_data = X
            self.node.input_sockets[1].socket_data = Y
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            if isinstance(self.node.input_sockets[0].socket_data, pd.DataFrame) and isinstance(self.node.input_sockets[1].socket_data, pd.DataFrame):
                X = self.node.input_sockets[0].socket_data
                Y = self.node.input_sockets[1].socket_data

                data = X.copy()
                data["Encoded Label"] = str()
                n_classes = Y.shape[1]   
                n_samples = Y.shape[0]
                for i in range(n_samples):
                    for j in range(n_classes):
                        data.iloc[i,-1] += str(Y.iloc[i,j])

                for fold, (train_idx, test_idx) in enumerate(self.splitter.split(X, Y)):
                    data.loc[train_idx.tolist(),f"Fold{fold+1}"] = "Train"
                    data.loc[test_idx.tolist(),f"Fold{fold+1}"] = "Test"     
                    result.append((train_idx, test_idx)) 

                # change progressbar's color                     
                self.progress.changeColor("success")
                # write log
                logger.info(f"{self.name} {self.node.id}: splitted data successfully.")
            else:
                X, Y = pd.DataFrame(), pd.DataFrame()
                data = pd.DataFrame()
                # change progressbar's color   
                self.progress.changeColor('fail')
                # write log
                logger.warning(f"{self.name} {self.node.id}: Not enough input data, return an empty DataFrame.")

        except Exception as e:
            X, Y = pd.DataFrame(), pd.DataFrame()
            data = pd.DataFrame()
            # change progressbar's color   
            self.progress.changeColor("fail")
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = [result, X, Y]
        self.node.output_sockets[1].socket_data = data.copy()
        self.data_to_view = data.copy()
     
    def eval(self):
        self.resetStatus()
        # reset socket data
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
