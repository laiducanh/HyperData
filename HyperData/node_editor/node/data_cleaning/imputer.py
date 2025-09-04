from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.experimental import enable_iterative_imputer # is required to load sklear.impute
from sklearn.impute import SimpleImputer, IterativeImputer, KNNImputer
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HPrimaryComboBox, HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentSpinBox, HTransparentDoubleSpinBox
from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.frame import Frame
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

DEBUG = False

class NAImputer (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            imputer='univariate', 
            m_strategy='mean', 
            m_fill_value=None,
            sample_posterior = False,
            max_iter=10, 
            tol=1e-3, 
            u_strategy='mean', 
            u_fill_value=None,
            imputation_order='ascending', 
            skip_complete=False,
            n_neighbors=5,
            weights='uniform',
        )

        self.node.input_sockets[0].setSocketLabel("Data")
        self.node.input_sockets[1].setSocketLabel("Estimator")
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.setMinimumSize(600, 400)
        imputer = HPrimaryComboBox(
            items=["univariate","multivariate","KNN"], 
            label='Imputer',
            getter=lambda: self._config["imputer"],
            setter=lambda: stacklayout.setCurrentIndex(imputer.button.currentIndex()),
            layout=dialog.main_layout
        )

        stacklayout = QStackedLayout()
        dialog.main_layout.addLayout(stacklayout)

        univariate_widget = Frame()
        univariate_layout = QVBoxLayout()
        univariate_layout.setContentsMargins(0,0,0,0)
        univariate_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        univariate_widget.setLayout(univariate_layout)
        stacklayout.addWidget(univariate_widget)
        u_strategy = HTransparentComboBox(items=["next valid observation", "last valid observation", "mean","median","most_frequent","constant"],label='Strategy')
        u_strategy.button.setMinimumWidth(300)
        u_strategy.button.setCurrentText(self._config['u_strategy'])
        univariate_layout.addWidget(u_strategy)
        u_fill_value = HLineEdit(label='Fill value')
        u_fill_value.button.setText(self._config['u_fill_value'])
        u_fill_value.button.setEnabled(True if u_strategy.button.currentText() == 'constant' else False)
        u_strategy.button.currentTextChanged.connect(lambda s: u_fill_value.button.setEnabled(True) if s == 'constant' 
                                                   else u_fill_value.button.setEnabled(False))
        univariate_layout.addWidget(u_fill_value)

        multivariate_widget = Frame()
        multivariate_layout = QVBoxLayout()
        multivariate_layout.setContentsMargins(0,0,0,0)
        multivariate_widget.setLayout(multivariate_layout)
        stacklayout.addWidget(multivariate_widget)

        sample_posterior = HToggle(label="Sample posterior")
        sample_posterior.button.setChecked(self._config["sample_posterior"])
        multivariate_layout.addWidget(sample_posterior)

        max_iter = HTransparentSpinBox(minimum=1, maximum=1000, singleStep=5, label='Max iterations')
        max_iter.button.setValue(self._config['max_iter'])
        multivariate_layout.addWidget(max_iter)

        tol = HTransparentDoubleSpinBox(minimum=1e-8,maximum=1,singleStep=5e-8, label='Tolerance')
        tol.button.setDecimals(8)
        tol.button.setValue(self._config['tol'])
        multivariate_layout.addWidget(tol)

        m_strategy = HTransparentComboBox(items=["mean","median","most_frequent","constant"],label='Strategy')
        m_strategy.button.currentTextChanged.connect(lambda s: m_fill_value.button.setEnabled(True) if s == 'Constant' 
                                                   else m_fill_value.button.setEnabled(False))
        m_strategy.button.setCurrentText(self._config['m_strategy'])
        multivariate_layout.addWidget(m_strategy)
        m_fill_value = HLineEdit(label='Fill value')
        m_fill_value.button.setText(self._config['m_fill_value'])
        m_fill_value.button.setEnabled(True if m_strategy.button.currentText() == 'Constant' else False)
        multivariate_layout.addWidget(m_fill_value)

        imputation_order = HTransparentComboBox(items=['ascending', 'descending', 'roman', 'arabic', 'random'], label='Imputation order')
        imputation_order.button.setCurrentText(self._config["imputation_order"])
        multivariate_layout.addWidget(imputation_order)

        skip_complete = HToggle(label='Skip complete')
        skip_complete.button.setChecked(self._config["skip_complete"])
        multivariate_layout.addWidget(skip_complete)

        knn_widget = Frame()
        knn_layout = QVBoxLayout()
        knn_layout.setContentsMargins(0,0,0,0)
        knn_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        knn_widget.setLayout(knn_layout)
        stacklayout.addWidget(knn_widget)

        n_neighbors = HTransparentSpinBox(minimum=0, maximum=1000, singleStep=5, label='Neighbors')
        n_neighbors.button.setValue(self._config["n_neighbors"])
        knn_layout.addWidget(n_neighbors)

        weights = HTransparentComboBox(items=['uniform','distance'], label='Weights')
        weights.button.setCurrentText(self._config["weights"])
        knn_layout.addWidget(weights)

        stacklayout.setCurrentIndex(imputer.button.currentIndex())

        if dialog.exec(): 
            self._config["imputer"] = imputer.button.currentText()
            self._config["u_strategy"] = u_strategy.button.currentText()
            self._config["u_fill_value"] = u_fill_value.button.text()
            self._config["m_strategy"] = m_strategy.button.currentText()
            self._config["m_fill_value"] = m_fill_value.button.text()
            self._config["sample_posterior"] = sample_posterior.button.isChecked()
            self._config["max_iter"] = max_iter.button.value()
            self._config["tol"] = tol.button.value()
            self._config["imputation_order"] = imputation_order.button.currentText()
            self._config["skip_complete"] = skip_complete.button.isChecked()
            self._config["n_neighbors"] = n_neighbors.button.value()
            self._config["weights"] = weights.button.currentText()
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()

    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            # randomly introduce some missing values
            df = df.mask(np.random.random(df.shape) < 0.2)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            imputer = None
            estimator = self.node.input_sockets[1].socket_data

            # Prepare imputer
            if self._config["imputer"] == 'univariate':
                if self._config['u_strategy'] == 'next valid observation':
                    data = self.node.input_sockets[0].socket_data.fillna(method='ffill')
                elif self._config['u_strategy'] == 'last valid observation':
                    data = self.node.input_sockets[0].socket_data.fillna(method='bfill')
                else:
                    imputer = SimpleImputer(
                        strategy=self._config['u_strategy'],
                        fill_value=self._config['u_fill_value']
                    )
            elif self._config["imputer"] == 'multivariate':
                imputer = IterativeImputer(
                    estimator=estimator,
                    sample_posterior=self._config["sample_posterior"],
                    max_iter=self._config['max_iter'],
                    tol=self._config["tol"],
                    initial_strategy=self._config["m_strategy"],
                    fill_value=self._config["m_fill_value"],
                    imputation_order=self._config['imputation_order'],
                    skip_complete=self._config["skip_complete"]
                )
            elif self._config["imputer"] == "knn":
                imputer = KNNImputer(
                    n_neighbors=self._config['n_neighbors'],
                    weights=self._config["weights"]
                )

            # Impute data
            if imputer:
                columns = self.node.input_sockets[0].socket_data.columns
                data = imputer.fit_transform(self.node.input_sockets[0].socket_data)
                data = pd.DataFrame(data, columns=columns)   

            # change progressbar's color
            self.progress.changeColor('success')       
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else: logger.info(f"{self.name} {self.node.id}: impute NaNs successfully.")

        except Exception as e:
            data = self.node.input_sockets[0].socket_data
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: fail, return the original DataFrame.")
            logger.exception(e)
    
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy() 

    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = None
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data