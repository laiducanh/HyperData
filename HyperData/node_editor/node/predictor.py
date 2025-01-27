from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from config.settings import logger, GLOBAL_DEBUG
import pandas as pd

DEBUG = False

class Predictor (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Model")
        self.node.input_sockets[1].setSocketLabel("Features (X)")
        self.node.output_sockets[0].setSocketLabel("Data out")

        self.X, self.Y_pred = pd.DataFrame(), pd.DataFrame()
    
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection, preprocessing, linear_model
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            X = df.iloc[:,:4]
            Y = preprocessing.LabelEncoder().fit_transform(df.iloc[:,4])
            Y = pd.DataFrame(data=Y)
            model = linear_model.LogisticRegression()
            model.fit(X.to_numpy(), Y.to_numpy())
            self.node.input_sockets[0].socket_data = model
            self.node.input_sockets[1].socket_data = X
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try: 
            self.model: OneVsRestClassifier|OneVsOneClassifier = self.node.input_sockets[0].socket_data
            self.X = self.node.input_sockets[1].socket_data
            self.Y_pred = self.model.predict(self.X)

            self.Y_pred = pd.DataFrame(self.Y_pred,columns=["Prediction"])
            data = pd.concat([self.X, self.Y_pred], axis=1)

            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            logger.info(f"{self.name} {self.node.id}: run successfully.")

        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def eval(self):
        self.resetStatus()
        # reset socket data
        for socket in self.node.input_sockets:
            socket.socket_data = None
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
    
