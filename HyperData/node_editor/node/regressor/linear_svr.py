from node_editor.node.regressor.base import RegressorBase
from sklearn import svm

class LinearSVR(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = svm.LinearSVR(**self._config)