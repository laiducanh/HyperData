from node_editor.node.regressor.base import RegressorBase
from sklearn import neighbors

class RadiusNeighborsRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = neighbors.RadiusNeighborsRegressor(**self._config)