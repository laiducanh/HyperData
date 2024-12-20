from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from typing import Union
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import model_selection
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from ui.base_widgets.frame import SeparateHLine
from config.settings import logger
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout
from PySide6.QtCore import Qt

class SplitterBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.vlayout)
        self._config = dict()
        self.splitter = None # Union[model_selection.BaseCrossValidator, model_selection.BaseShuffleSplit]
        
    def clear_layout (self):
        for widget in self.findChildren(QWidget):
            self.vlayout.removeWidget(widget)

class GroupKFold (SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)        
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(n_splits=5)
        else: self._config = config
        self.splitter = model_selection.GroupKFold(**self._config)
    
        self.splits = SpinBox(min=2, max=1000, step=1, text="number of folds")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self.splitter = model_selection.GroupKFold(**self._config)

class GroupShuffleSplit (SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):
        
        self.clear_layout()

        if config == None: self._config = dict(n_splits=5,test_size=0.2)
        else: self._config = config
        self.splitter = model_selection.GroupShuffleSplit(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of splits")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.test_size = DoubleSpinBox(min=0, max=1, step=0.01, text="test size")
        self.test_size.button.valueChanged.connect(self.set_splitter)
        self.test_size.button.setValue(self._config["test_size"])
        self.vlayout.addWidget(self.test_size)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["test_size"] = self.test_size.button.value()
        self.splitter = model_selection.GroupShuffleSplit(**self._config)

class Kfold (SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)

    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(n_splits=5,shuffle=False)
        else: self._config = config
        self.splitter = model_selection.KFold(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of folds")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.shuffle = Toggle(text="shuffle")
        self.shuffle.button.checkedChanged.connect(self.set_splitter)
        self.shuffle.button.setChecked(self._config["shuffle"])
        self.vlayout.addWidget(self.shuffle)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["shuffle"] = self.shuffle.button.isChecked()
        self.splitter = model_selection.KFold(**self._config)

class LeaveOneGroupOut(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)

    def set_config(self, config):

        self.clear_layout()

        self.set_splitter()
    
    def set_splitter(self):
        self.splitter = model_selection.LeaveOneGroupOut()

class LeavePGroupOut(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)

    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(n_groups=2)
        else: self._config = config
        self.splitter = model_selection.LeavePGroupsOut(**self._config)

        self.splits = SpinBox(min=1, max=1000, step=1, text="number of groups")
        self.splits.button.setValue(self._config["n_groups"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
    
    def set_splitter(self):
        self._config["n_groups"] = self.splits.button.value()
        self.splitter = model_selection.LeavePGroupsOut(**self._config)

class LeaveOneOut(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)

    def set_config(self, config):
        self.clear_layout()

        self.set_splitter()
    
    def set_splitter(self):
        self.splitter = model_selection.LeaveOneOut()

class LeavePOut(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)

    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(p=2)
        else: self._config = config
        self.splitter = model_selection.LeavePOut(**self._config)

        self.splits = SpinBox(min=1, max=1000, step=1, text="number of samples")
        self.splits.button.setValue(self._config["p"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
    
    def set_splitter(self):
        self._config["p"] = self.splits.button.value()
        self.splitter = model_selection.LeavePOut(**self._config)

class RepeatedKFold(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(n_splits=5,n_repeats=10)
        else: self._config = config
        self.splitter = model_selection.RepeatedKFold(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of folds")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.repeats = SpinBox(min=1, max=1000, step=1, text="number of repeats")
        self.repeats.button.valueChanged.connect(self.set_splitter)
        self.repeats.button.setValue(self._config["n_repeats"])
        self.vlayout.addWidget(self.repeats)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["n_repeats"] = self.repeats.button.value()
        self.splitter = model_selection.RepeatedKFold(**self._config)

class RepeatedStratifiedKFold(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)

    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(n_splits=5,n_repeats=10)
        else: self._config = config
        self.splitter = model_selection.RepeatedStratifiedKFold(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of folds")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.repeats = SpinBox(min=1, max=1000, step=1, text="number of repeats")
        self.repeats.button.valueChanged.connect(self.set_splitter)
        self.repeats.button.setValue(self._config["n_repeats"])
        self.vlayout.addWidget(self.repeats)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["n_repeats"] = self.repeats.button.value()
        self.splitter = model_selection.RepeatedStratifiedKFold(**self._config)

class ShuffleSplit(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(n_splits=10,test_size=0.2)
        else: self._config = config
        self.splitter = model_selection.ShuffleSplit(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of splits")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.test_size = DoubleSpinBox(min=0, max=1, step=0.01, text="test size")
        self.test_size.button.valueChanged.connect(self.set_splitter)
        self.test_size.button.setValue(self._config["test_size"])
        self.vlayout.addWidget(self.test_size)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["test_size"] = self.test_size.button.value()
        self.splitter = model_selection.ShuffleSplit(**self._config)
    
class StratifiedKFold(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)

    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(n_splits=5,shuffle=False)
        else: self._config = config
        self.splitter = model_selection.StratifiedKFold(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of folds")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.shuffle = Toggle(text="shuffle")
        self.shuffle.button.checkedChanged.connect(self.set_splitter)
        self.shuffle.button.setChecked(self._config["shuffle"])
        self.vlayout.addWidget(self.shuffle)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["shuffle"] = self.shuffle.button.isChecked()
        self.splitter = model_selection.StratifiedKFold(**self._config)

class StratifiedShuffleSplit(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(n_splits=10,test_size=0.2)
        else: self._config = config
        self.splitter = model_selection.StratifiedShuffleSplit(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of splits")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.test_size = DoubleSpinBox(min=0, max=1, step=0.01, text="test size")
        self.test_size.button.valueChanged.connect(self.set_splitter)
        self.test_size.button.setValue(self._config["test_size"])
        self.vlayout.addWidget(self.test_size)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["test_size"] = self.test_size.button.value()
        self.splitter = model_selection.StratifiedShuffleSplit(**self._config)

class StratifiedGroupKFold(SplitterBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):
        self.clear_layout()

        if config == None: self._config = dict(n_splits=5,shuffle=False)
        else: self._config = config
        self.splitter = model_selection.StratifiedGroupKFold(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of folds")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.shuffle = Toggle(text="shuffle")
        self.shuffle.button.checkedChanged.connect(self.set_splitter)
        self.shuffle.button.setChecked(self._config["shuffle"])
        self.vlayout.addWidget(self.shuffle)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["shuffle"] = self.shuffle.button.isChecked()
        self.splitter = model_selection.StratifiedGroupKFold(**self._config)

class TrainTestSplitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setTitle("Feature (X)")
        self.node.input_sockets[1].setTitle("Label (Y)")
        self.node.output_sockets[0].setTitle("Train/Test")
        self.node.output_sockets[1].setTitle("Data")
        self.data_to_view = pd.DataFrame()
        self.exec()
        self._config = dict(splitter="K Fold",config=None)


    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)
        dialog.main_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMaximumSize)
        splitter = ComboBox(items=["group k fold","group shuffle split","k fold",
                                   "leave one group out", "leave p group out",
                                   "leave one out", "leave p out","repeated k fold",
                                   "repeated stratified k fold","shuffle split",
                                   "stratified k fold","stratified shuffle split",
                                   "stratified group k fold"], text="splitter")
        splitter.button.setCurrentText(self._config["splitter"])
        splitter.button.currentTextChanged.connect(lambda: stackedlayout.setCurrentIndex(splitter.button.currentIndex()))
        dialog.main_layout.addWidget(splitter)
        dialog.main_layout.addWidget(SeparateHLine())
        stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(stackedlayout)
        stackedlayout.addWidget(GroupKFold())
        stackedlayout.addWidget(GroupShuffleSplit())
        stackedlayout.addWidget(Kfold())
        stackedlayout.addWidget(LeaveOneGroupOut())
        stackedlayout.addWidget(LeavePGroupOut())
        stackedlayout.addWidget(LeaveOneOut())
        stackedlayout.addWidget(LeavePOut())
        stackedlayout.addWidget(RepeatedKFold())
        stackedlayout.addWidget(RepeatedStratifiedKFold())
        stackedlayout.addWidget(ShuffleSplit())
        stackedlayout.addWidget(StratifiedKFold())
        stackedlayout.addWidget(StratifiedShuffleSplit())
        stackedlayout.addWidget(StratifiedGroupKFold())
        stackedlayout.setCurrentIndex(splitter.button.currentIndex())
        stackedlayout.currentWidget().set_config(self._config["config"])

        if dialog.exec():
            self.splitter = stackedlayout.currentWidget().splitter
            self.splitter: Union[model_selection.BaseCrossValidator, model_selection.BaseShuffleSplit]
            self._config["splitter"] = splitter.button.currentText()
            self._config["config"] = stackedlayout.currentWidget()._config
            self.exec()

    def func(self):
        self.eval()
        result = list()

        try:
            if isinstance(self.node.input_sockets[0].socket_data, pd.DataFrame) and isinstance(self.node.input_sockets[1].socket_data, pd.DataFrame):
                X = self.node.input_sockets[0].socket_data
                Y = self.node.input_sockets[1].socket_data

                self.data_to_view = X.copy()
                self.data_to_view["Label Encoder"] = str()
                n_classes = Y.shape[1]   
                n_samples = Y.shape[0]
                for i in range(n_samples):
                    for j in range(n_classes):
                        self.data_to_view.iloc[i,-1] += str(Y.iloc[i,j])

                for fold, (train_idx, test_idx) in enumerate(self.splitter.split(X, Y)):

                    self.data_to_view.loc[train_idx.tolist(),f"Fold{fold+1}"] = "Train"
                    self.data_to_view.loc[test_idx.tolist(),f"Fold{fold+1}"] = "Test"     
                    result.append((train_idx, test_idx))                       

                logger.info(f"{self.name} run successfully.")
            else:
                X, Y = pd.DataFrame(), pd.DataFrame()
                self.data_to_view = pd.DataFrame()
                logger.warning(f"{self.name} Not enough input data, return an empty DataFrame.")

        except Exception as e:
            X, Y = pd.DataFrame(), pd.DataFrame()
            self.data_to_view = pd.DataFrame()
            logger.error(f"{self.name} {repr(e)}, return an empty DataFrame.")
       
        self.node.output_sockets[0].socket_data = [result, X, Y]
        self.node.output_sockets[1].socket_data = self.data_to_view
     
    def eval(self):
        # reset input sockets
        for socket in self.node.input_sockets:
            socket.socket_data = None
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
