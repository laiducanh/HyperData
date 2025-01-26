from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model

class BayesianRidgeRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.BayesianRidge(**self._config)