from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from keras import Input, utils
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.deep_learning.base import DLBase
from config.settings import logger, GLOBAL_DEBUG

DEBUG = True

class InputLayer (DLBase):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Train/Test")

        self._config = dict(
            name = f"{self.name}_{self.node.id}"
        )
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection, preprocessing
            import numpy as np
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            X = df.iloc[:,:4]
            random_state = np.random.RandomState(0)
            n_samples, n_features = data.data.shape
            #X = np.concatenate([data.data, random_state.randn(n_samples, 200 * n_features)], axis=1)
            X = pd.DataFrame(X)
            Y = preprocessing.LabelEncoder().fit_transform(df.iloc[:,4])
            Y = pd.DataFrame(data=Y)
            split = model_selection.ShuffleSplit(n_splits=5, test_size=0.2).split(X, Y)
            result = list()
            for fold, (train_idx, test_idx) in enumerate(split):
                result.append((train_idx, test_idx))
            self.node.input_sockets[0].socket_data = [result, X, Y]
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            # unpack data from input socket
            cv, X, Y = self.node.input_sockets[0].socket_data
            # create layer
            layer = Input(shape=(X.shape[1],),**self._config)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")
           
        except Exception as e:
            cv, X, Y, layer = None, None, None, None
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = [cv, X, Y, layer, layer]

    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data