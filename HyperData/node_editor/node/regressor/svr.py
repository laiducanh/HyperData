from node_editor.node.regressor.base import RegressorBase
from sklearn import svm

class SVR(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = svm.SVR(**self._config)