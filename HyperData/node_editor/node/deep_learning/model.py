from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from keras import Model, metrics, callbacks
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.deep_learning.base import DLBase
from node_editor.node.deep_learning.report import Report
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.button import HToggle, TransparentPushButton
from config.settings import logger, GLOBAL_DEBUG

DEBUG = False

class ModelCompiler (DLBase):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            metrics = ['accuracy'],
            batch_size = 32,
            epochs = 3,
            shuffle = True,
            early_stop = True,
            es_patience = 5,
        )
        self.histories = []

        self.node.input_sockets[0].setSocketLabel("Data in")
        self.node.input_sockets[1].setSocketLabel("Optimizer")
        self.node.input_sockets[2].setSocketLabel("Loss function")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Estimator")
        self.node.output_sockets[2].setSocketLabel("Data out")

        self.score_btn = TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
    
    def config(self):
        dialog = Dialog(title="Configuration", parent=self.parent)
        dialog.setMinimumSize(600, 400)

        dialog.main_layout.addWidget(TitleLabel('Model Compiler'))
        dialog.main_layout.addWidget(SeparateHLine())

        batch_size = HTransparentSpinBox(
            label='Batch size',
            label2='Number of samples per gradient update',
            getter=lambda: self._config['batch_size'],
            layout=dialog.main_layout
        )

        epochs = HTransparentSpinBox(
            label="Epochs",
            label2='NUmber of epochs to train the model',
            getter=lambda: self._config['epochs'],
            layout=dialog.main_layout
        )

        shuffle = HToggle(
            label='Shuffle',
            label2='Whether to shuffle the training data before each epoch',
            getter=lambda: self._config['shuffle'],
            layout=dialog.main_layout
        )

        early_stop = HToggle(
            label='Early stop',
            label2='Early stopping based on validation loss',
            getter=lambda: self._config['early_stop'],
            layout=dialog.main_layout
        )

        es_patience = HTransparentSpinBox(
            label='Patience',
            label2='Number of epochs to wait before early stopping',
            getter=lambda: self._config['es_patience'],
            layout=dialog.main_layout
        )

        if dialog.exec():
            self._config.update(
                batch_size = batch_size.get_value(),
                epochs = epochs.get_value(),
                shuffle = shuffle.get_value(),
                early_stop = early_stop.get_value(),
                es_patience = es_patience.get_value()
            )
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()
    
    def func(self):
        try:
            # unpack data from input socket
            cv, X, Y, input_layer, output_layer = self.node.input_sockets[0].socket_data
            optimizer = self.node.input_sockets[1].socket_data
            loss = self.node.input_sockets[2].socket_data
            X = X.to_numpy()
            Y = Y.to_numpy()

            # compile model
            metrics = self._config['metrics']
            estimator = Model(input_layer, output_layer)
            estimator.compile(metrics=metrics,optimizer=optimizer,loss=loss)
            if self._config['early_stop']:
                early_stop = callbacks.EarlyStopping(
                    patience=self._config['es_patience'],
                    verbose=0
                )
            self.histories = []
      
            # fit model
            for fold, (train_idx, test_idx) in enumerate(cv):
                X_train, X_test = X[train_idx], X[test_idx]
                Y_train, Y_test = Y[train_idx], Y[test_idx]
                
                model = Model(input_layer, output_layer)
                model.compile(metrics=metrics,optimizer=optimizer,loss=loss)
                history = model.fit(
                    X_train, Y_train,
                    validation_data=(X_test, Y_test),
                    batch_size=self._config["batch_size"],
                    epochs=self._config["epochs"],
                    shuffle=self._config["shuffle"],
                    callbacks=[early_stop],
                )

                self.histories.append(history)
                
            # predict
            data = model.predict(X)

            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")
           
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = model
        self.node.output_sockets[1].socket_data = estimator
        self.node.output_sockets[2].socket_data = data.copy()
        self.data_to_view = data.copy()

    def score_dialog(self):
        dialog = Report(self.histories)
        dialog.exec()

    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = [None, None, None, None, None]
        self.node.input_sockets[1].socket_data = None
        self.node.input_sockets[2].socket_data = None
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[2].edges:
            self.node.input_sockets[2].socket_data = edge.start_socket.socket_data