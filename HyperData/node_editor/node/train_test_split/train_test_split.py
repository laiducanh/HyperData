from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import model_selection
from ui.base_widgets.window import Dialog
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import Toggle
from config.settings import logger, GLOBAL_DEBUG

DEBUG = False

class TrainTestSplitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Feature (X)")
        self.node.input_sockets[1].setSocketLabel("Label (Y)")
        self.node.output_sockets[0].setSocketLabel("Splitter")
        self.node.output_sockets[1].setSocketLabel("Train")
        self.node.output_sockets[2].setSocketLabel("Test")
        self.data_to_view = pd.DataFrame()
        self._config = dict(
            test_size = 0.25,
            shuffle = True,
        )

    def config(self):
        dialog = Dialog("Configuration", self.parent)

        test_size = DoubleSpinBox(min=0, max=1, step=0.01, text="Test size")
        test_size.button.setValue(self._config["test_size"])
        dialog.main_layout.addWidget(test_size)

        shuffle = Toggle(text="Shuffle")
        shuffle.button.setChecked(self._config["shuffle"])
        dialog.main_layout.addWidget(shuffle)
        

        if dialog.exec():
            self._config["test_size"] = test_size.button.value()
            self._config["shuffle"] = shuffle.button.isChecked()
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
                
                X_train, X_test = model_selection.train_test_split(X, **self._config)
                result.append((X_train.index.tolist(), X_test.index.tolist())) 

                data.loc[X_train.index.tolist(),"Fold 1"] = "Train"
                data.loc[X_test.index.tolist(),"Fold 1"] = "Test"   

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
        self.node.output_sockets[1].socket_data = data[data["Fold 1"] == "Train"].drop(columns="Fold 1")
        self.node.output_sockets[2].socket_data = data[data["Fold 1"] == "Test"].drop(columns="Fold 1")
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
