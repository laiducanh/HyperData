from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import discriminant_analysis

DEBUG = False

class LDA(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        self.estimator = discriminant_analysis.LinearDiscriminantAnalysis(**self._config)
        
    def set_estimator(self):
        self.estimator = discriminant_analysis.LinearDiscriminantAnalysis(**self._config)

class QDA(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        self.estimator = discriminant_analysis.QuadraticDiscriminantAnalysis(**self._config)
        
    def set_estimator(self):
        self.estimator = discriminant_analysis.QuadraticDiscriminantAnalysis(**self._config)