from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, IterativeImputer, KNNImputer
from ui.base_widgets.window import Dialog
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.text import LineEdit, EditableComboBox, Completer
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from config.settings import logger
from PyQt6.QtWidgets import QFileDialog, QDialog, QWidget, QVBoxLayout, QStackedLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

class NAEliminator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(axis='index',thresh='any',ignore_index=False)
    
    def initMenu(self):
        action = QAction("Execute card")
        action.triggered.connect(self.exec)
        self.menu.addAction(action)
        action = QAction("View output")
        action.triggered.connect(self.viewData)
        self.menu.addAction(action)
        action = QAction("Configuration")
        action.triggered.connect(self.config)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Show Comment")
        action.triggered.connect(self.comment.show)
        self.menu.addAction(action)
        action = QAction("Hide Comment")
        action.triggered.connect(self.comment.hide)
        self.menu.addAction(action)

    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)

        axis = ComboBox(items=["index","columns"], text="drop")
        axis.button.setCurrentText(self._config["axis"].title())
        dialog.textLayout.addWidget(axis)

        thresh = EditableComboBox(text='thresh')
        thresh.button.setCompleter(Completer(["any","all"]))
        thresh.button.setText(self._config['thresh'])
        dialog.textLayout.addWidget(thresh)

        ignore_index = Toggle(text='ignore index')
        ignore_index.button.setChecked(self._config['ignore_index'])
        dialog.textLayout.addWidget(ignore_index)

        if dialog.exec():
            self._config["axis"] = axis.button.currentText().lower()
            self._config["thresh"] = thresh.button.text()
            self._config["ignore_index"] = ignore_index.button.isChecked()
            self.exec()

    def func(self):
        try:
            if self._config["thresh"] in ["any","all"]:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.dropna(axis=self._config["axis"],
                                                          how=self._config["how"],
                                                          ignore_index=self._config["ignore_index"])
            else:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.dropna(axis=self._config["axis"],
                                                          thresh=int(self._config["how"]),
                                                          ignore_index=self._config["ignore_index"])
            logger.info(f"{self.name} run successfully.")
        except Exception as e: 
            self.node.output_sockets[0].socket_data = self.node.output_sockets[0].socket_data
            logger.error(f"{self.name} {repr(e)}, return the original DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data
                
    def eval(self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data

class NAImputer (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
    
        self._config = dict(imputer='univariate', m_strategy='mean', m_fill_value=None,
                            estimator=None, max_iter=10, tol=1e-3, u_strategy='mean', u_fill_value=None,
                            imputation_order='ascending', skip_complete=False,
                            n_neighbors=5, weights='uniform', )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)
        imputer = ComboBox(items=["univariate","multivariate","KNN"], text='imputer')
        imputer.button.setCurrentText(self._config['imputer'].title())
        imputer.button.currentTextChanged.connect(lambda: stacklayout.setCurrentIndex(imputer.button.currentIndex()))
        dialog.textLayout.addWidget(imputer)

        stacklayout = QStackedLayout()
        dialog.textLayout.addLayout(stacklayout)

        univariate_widget = QWidget()
        univariate_layout = QVBoxLayout()
        univariate_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        univariate_widget.setLayout(univariate_layout)
        stacklayout.addWidget(univariate_widget)
        u_strategy = ComboBox(items=["next valid observation", "last valid observation", "mean","median","most_frequent","constant"],text='strategy')
        u_strategy.button.currentTextChanged.connect(lambda s: u_fill_value.button.setEnabled(True) if s == 'Constant' 
                                                   else u_fill_value.button.setEnabled(False))
        u_strategy.button.setCurrentText(self._config['u_strategy'].title())
        univariate_layout.addWidget(u_strategy)
        u_fill_value = LineEdit(text='fill value')
        u_fill_value.button.setText(self._config['u_fill_value'])
        u_fill_value.button.setEnabled(True if u_strategy.button.currentText() == 'Constant' else False)
        univariate_layout.addWidget(u_fill_value)

        multivariate_widget = QWidget()
        multivariate_layout = QVBoxLayout()
        multivariate_widget.setLayout(multivariate_layout)
        stacklayout.addWidget(multivariate_widget)

        max_iter = SpinBox(min=1, max=1000, step=5, text='max iterations')
        max_iter.button.setValue(self._config['max_iter'])
        multivariate_layout.addWidget(max_iter)

        tol = DoubleSpinBox(min=1e-8,max=1,step=5e-8, text='tolerance')
        tol.button.setDecimals(8)
        tol.button.setValue(self._config['tol'])
        multivariate_layout.addWidget(tol)

        m_strategy = ComboBox(items=["mean","median","most_frequent","constant"],text='strategy')
        m_strategy.button.currentTextChanged.connect(lambda s: m_fill_value.button.setEnabled(True) if s == 'Constant' 
                                                   else m_fill_value.button.setEnabled(False))
        m_strategy.button.setCurrentText(self._config['m_strategy'].title())
        multivariate_layout.addWidget(m_strategy)
        m_fill_value = LineEdit(text='fill value')
        m_fill_value.button.setText(self._config['m_fill_value'])
        m_fill_value.button.setEnabled(True if m_strategy.button.currentText() == 'Constant' else False)
        multivariate_layout.addWidget(m_fill_value)

        imputation_order = ComboBox(items=['ascending', 'descending', 'roman', 'arabic', 'random'], text='imputation order')
        imputation_order.button.setCurrentText(self._config["imputation_order"].title())
        multivariate_layout.addWidget(imputation_order)

        skip_complete = Toggle(text='Skip complete')
        skip_complete.button.setChecked(self._config["skip_complete"])
        multivariate_layout.addWidget(skip_complete)

        knn_widget = QWidget()
        knn_layout = QVBoxLayout()
        knn_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        knn_widget.setLayout(knn_layout)
        stacklayout.addWidget(knn_widget)

        n_neighbors = SpinBox(min=0, max=1000, step=5, text='neighbors')
        n_neighbors.button.setValue(self._config["n_neighbors"])
        knn_layout.addWidget(n_neighbors)

        weights = ComboBox(items=['uniform','distance'], text='weights')
        weights.button.setCurrentText(self._config["weights"].title())
        knn_layout.addWidget(weights)

        if dialog.exec(): 
            self._config["imputer"] = imputer.button.currentText().lower()
            self._config["u_strategy"] = u_strategy.button.currentText().lower()
            self._config["u_fill_value"] = u_fill_value.button.text()
            self._config["m_strategy"] = m_strategy.button.currentText().lower()
            self._config["m_fill_value"] = m_fill_value.button.text()
            self._config["estimator"] = None
            self._config["max_iter"] = max_iter.button.value()
            self._config["tol"] = tol.button.value()
            self._config["imputation_order"] = imputation_order.button.currentText().lower()
            self._config["skip_complete"] = skip_complete.button.isChecked()
            self._config["n_neighbors"] = n_neighbors.button.value()
            self._config["weights"] = weights.button.currentText().lower()
            self.exec()

    def func(self):
        imputer = None
        try:
            if self._config['imputer'] == 'univariate':
                if self._config['u_strategy'] == 'next valid observation':
                    self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.fillna(method='ffill')
                elif self._config['u_strategy'] == 'last valid observation':
                    self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.fillna(method='bfill')
                else:
                    imputer = SimpleImputer(strategy=self._config['u_strategy'],
                                        fill_value=self._config['u_fill_value'])
            elif self._config['imputer'] == 'multivariate':
                imputer = IterativeImputer(max_iter=self._config['max_iter'],
                                        tol=self._config["tol"],
                                        initial_strategy=self._config["m_strategy"],
                                        fill_value=self._config["m_fill_value"],
                                        imputation_order=self._config['imputation_order'],
                                        skip_complete=self._config["skip complete"])
            elif self._config["imputer"] == "knn":
                imputer = KNNImputer(n_neighbors=self._config['n_neighbors'],
                                    weights=self._config["weights"])
            if imputer != None:
                columns = self.node.input_sockets[0].socket_data.columns
                self.node.output_sockets[0].socket_data = imputer.fit_transform(self.node.input_sockets[0].socket_data)
                self.node.output_sockets[0].socket_data = pd.DataFrame(self.node.output_sockets[0].socket_data, columns=columns)            
            
            logger.info(f"{self.name} run successfully.")

        except Exception as e:
            self.node.output_sockets[0].socket_data = self.node.output_sockets[0].socket_data
            logger.error(f"{self.name} {repr(e)}, return the original DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data        

    def eval(self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data

class DropDuplicate (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(keep='first',ignore_index=False)
    
    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)

        keep = ComboBox(items=["first","last","none"], text='keep')
        keep.button.setCurrentText(self._config["keep"].title())
        dialog.textLayout.addWidget(keep)

        ignore_index = Toggle(text='ignore index')
        ignore_index.button.setChecked(self._config["ignore_index"])
        dialog.textLayout.addWidget(ignore_index)

        if dialog.exec():
            self._config["keep"] = keep.button.currentText().lower()
            self._config["ignore_index"] = ignore_index.button.isChecked()
            self.exec()
    
    def exec(self):
        if self._config["keep"] == 'none': keep = False
        else: keep = self._config["keep"]
        try:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.drop_duplicates(keep=keep,ignore_index=self._config["ignore_index"])
            logger.info(f"{self.name} run successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = self.node.output_sockets[0].socket_data
            logger.error(f"{self.name} {repr(e)}, return the original DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data

    def eval(self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
