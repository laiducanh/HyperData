from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from keras import Model, losses, optimizers, metrics
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.deep_learning.base import DLBase
from config.settings import logger, GLOBAL_DEBUG

DEBUG = True

class DLModel (DLBase):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            optimizer = optimizers.Adam(),
            loss = losses.BinaryCrossentropy(),
            metrics = metrics.Accuracy(),
            batch_size = 1,
            epochs = 3,
            shuffle = True,
        )

        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Estimator")
        self.node.output_sockets[2].setSocketLabel("Data out")
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            pass

        try:
            # unpack data from input socket
            cv, X, Y, input_layer, output_layer = self.node.input_sockets[0].socket_data
            X = X.to_numpy()
            Y = Y.to_numpy()
            # compile model
            
            model = Model(input_layer, output_layer)
            estimator = Model(input_layer, output_layer)
            
            model.compile(
                optimizer=self._config["optimizer"],
                loss=self._config["loss"],
                metrics=self._config["metrics"],
            )
            estimator.compile(
                optimizer=self._config["optimizer"],
                loss=self._config["loss"],
                metrics=self._config["metrics"],
            )
            
            # fit model
            for fold, (train_idx, test_idx) in enumerate(cv):
                X_train, X_test = X[train_idx], X[test_idx]
                Y_train, Y_test = Y[train_idx], Y[test_idx]
                
                model.fit(
                    X_train, Y_train,
                    validation_data=(X_test, Y_test),
                    batch_size=self._config["batch_size"],
                    epochs=self._config["epochs"],
                    shuffle=self._config["shuffle"]
                )
            # predict
            data = model.predict(X)
            
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")
           
        except Exception as e:
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = model
        self.node.output_sockets[1].socket_data = estimator
        self.node.output_sockets[2].socket_data = data.copy()
        self.data_to_view = data.copy()

    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = [None, None, None, None, None]
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data