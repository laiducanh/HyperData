from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from keras import Model, metrics, callbacks
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.deep_learning.base import DLBase
from node_editor.node.deep_learning.report import Report
from node_editor.node.deep_learning.optimizer import Optimizer
from node_editor.node.deep_learning.loss import Loss
from ui.base_widgets.window import Dialog
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.button import HToggle, TransparentPushButton, SegmentedWidget
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout

DEBUG = False

class TrainConfig(QWidget):
    def __init__(self, config:dict, parent=None):
        super().__init__(parent=parent)

        self.vlayout = QVBoxLayout(self)
        self._config = config

        self.batch_size = HTransparentSpinBox(
            label='Batch size',
            label2='Number of samples per gradient update',
            getter=lambda: self._config['batch_size'],
            setter=self.set_config,
            layout=self.vlayout
        )

        self.epochs = HTransparentSpinBox(
            label="Epochs",
            label2='NUmber of epochs to train the model',
            getter=lambda: self._config['epochs'],
            setter=self.set_config,
            layout=self.vlayout
        )

        self.shuffle = HToggle(
            label='Shuffle',
            label2='Whether to shuffle the training data before each epoch',
            getter=lambda: self._config['shuffle'],
            setter=self.set_config,
            layout=self.vlayout
        )

        self.early_stop = HToggle(
            label='Early stop',
            label2='Early stopping based on validation loss',
            getter=lambda: self._config['early_stop'],
            setter=self.set_config,
            layout=self.vlayout
        )

        self.es_patience = HTransparentSpinBox(
            label='Patience',
            label2='Number of epochs to wait before early stopping',
            getter=lambda: self._config['es_patience'],
            setter=self.set_config,
            layout=self.vlayout
        )

        self.restore_best_weights = HToggle(
            label='Restore best weights',
            label2='Whether to restore model weights from the epoch with the best value of the monitored quantity',
            getter=lambda: self._config['restore_best_weights'],
            setter=self.set_config,
            layout=self.vlayout
        )
    
    def set_config(self):
        self._config.update(
            batch_size = self.batch_size.get_value(),
            epochs = self.epochs.get_value(),
            shuffle = self.shuffle.get_value(),
            early_stop = self.early_stop.get_value(),
            es_patience = self.es_patience.get_value(),
            restore_best_weights = self.restore_best_weights.get_value()
        )

class ModelCompiler (DLBase):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = {
            "train": dict(
                metrics = ['accuracy'],
                batch_size = 32,
                epochs = 3,
                shuffle = True,
                early_stop = True,
                es_patience = 5,
                restore_best_weights = False,
            ),
            "optimizer": dict(
                optimizer = 'RMSprop',
                config = dict()
            ),
            "loss": dict(
                loss = "Binary cross-entropy",
                config = dict()
            )
        }
            
        self.histories = []

        self.node.input_sockets[0].setSocketLabel("Data in")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Estimator")
        self.node.output_sockets[2].setSocketLabel("Data out")

        self.score_btn = TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
    
    def config(self):
        dialog = Dialog(title="Model Compiler", parent=self.parent)
        dialog.setMinimumSize(600, 400)

        segment_widget = SegmentedWidget()
        dialog.main_layout.addWidget(segment_widget)

        segment_widget.addButton(text='Training', func=lambda: stackedlayout.setCurrentIndex(0))
        segment_widget.addButton(text='Optimizer', func=lambda: stackedlayout.setCurrentIndex(1))
        segment_widget.addButton(text='Loss', func=lambda: stackedlayout.setCurrentIndex(2))
        segment_widget.setCurrentIndex(0)

        stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(stackedlayout)

        train = TrainConfig(self._config['train'])
        stackedlayout.addWidget(train)

        optimizer = Optimizer(self._config['optimizer'])
        stackedlayout.addWidget(optimizer)

        loss = Loss(self._config['loss'])
        stackedlayout.addWidget(loss)

        if dialog.exec():
            self._config['train'] = train._config
            self._config['optimizer'] = optimizer._config
            self._config['loss'] = loss._config
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()
    
    def func(self):
        try:
            # unpack data from input socket
            cv, X, Y, input_layer, output_layer = self.node.input_sockets[0].socket_data
            X = X.to_numpy()
            Y = Y.to_numpy()

            # compile model
            metrics = self._config['train']['metrics']
            batch_size = self._config['train']['batch_size']
            epochs = self._config['train']['epochs']
            shuffle = self._config['train']['shuffle']
            optimizer = Optimizer(self._config['optimizer']).set_optimizer()
            loss = Loss(self._config['loss']).set_loss()
            estimator = Model(input_layer, output_layer)
            estimator.compile(
                metrics=metrics,
                optimizer=optimizer,
                loss=loss
            )
            early_stop = self._config['train']['early_stop']
            patience = self._config['train']['es_patience']
            restore_best_weights = self._config['train']['restore_best_weights']
            if early_stop:
                early_stop = callbacks.EarlyStopping(
                    patience=patience,
                    restore_best_weights=restore_best_weights,
                    verbose=0
                )
            else:
                early_stop = None
            self.histories = []
      
            # fit model
            for fold, (train_idx, test_idx) in enumerate(cv):
                X_train, X_test = X[train_idx], X[test_idx]
                Y_train, Y_test = Y[train_idx], Y[test_idx]
                
                model = Model(input_layer, output_layer)
                model.compile(
                    metrics=metrics,
                    optimizer=optimizer,
                    loss=loss
                )
                history = model.fit(
                    X_train, Y_train,
                    validation_data=(X_test, Y_test),
                    batch_size=batch_size,
                    epochs=epochs,
                    shuffle=shuffle,
                    callbacks=early_stop,
                )

                if early_stop is not None:
                    if early_stop.stopped_epoch > 0:
                        logger.info(f'Early stopping at epoch {early_stop.stopped_epoch+1}')
                    if early_stop.restore_best_weights and early_stop.best_weights is not None:
                        logger.info(f"Restoring model weights from the end of the best epoch: {early_stop.best_epoch+1}")

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
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
