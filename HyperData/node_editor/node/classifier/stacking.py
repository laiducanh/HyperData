from node_editor.node.classifier.classifier import ClassifierBase
from sklearn import ensemble

class Stacking(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        
    def set_estimator(self):
        
        self.estimator = ensemble.StackingClassifier(**self._config)