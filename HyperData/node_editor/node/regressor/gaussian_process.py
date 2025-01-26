from node_editor.node.regressor.base import RegressorBase
from sklearn import gaussian_process

class GaussianProcessRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = gaussian_process.GaussianProcessRegressor(**self._config)