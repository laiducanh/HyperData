from node_editor.node.regressor.base import RegressorBase
from sklearn import neighbors

class KNeighborsRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = neighbors.KNeighborsRegressor(**self._config)