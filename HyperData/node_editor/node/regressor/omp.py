from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model

class OrthogonalMatchingPursuit(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        self.estimator = linear_model.OrthogonalMatchingPursuit(**self._config)
        
    def set_estimator(self):
        self.estimator = linear_model.OrthogonalMatchingPursuit(**self._config)