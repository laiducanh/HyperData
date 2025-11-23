from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import naive_bayes

DEBUG = False

class GaussianNB(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        self.estimator = naive_bayes.GaussianNB(**self._config)

    def set_estimator(self):
        self.estimator = naive_bayes.GaussianNB(**self._config)

class MultinomialNB(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        self.estimator = naive_bayes.MultinomialNB(**self._config)

    def set_estimator(self):
        self.estimator = naive_bayes.MultinomialNB(**self._config)

class ComplementNB(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        self.estimator = naive_bayes.ComplementNB(**self._config)

    def set_estimator(self):
        self.estimator = naive_bayes.ComplementNB(**self._config)

class BernoulliNB(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        self.estimator = naive_bayes.BernoulliNB(**self._config)

    def set_estimator(self):
        self.estimator = naive_bayes.BernoulliNB(**self._config)

class CategoricalNB(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
        self.estimator = naive_bayes.CategoricalNB(**self._config)

    def set_estimator(self):
        self.estimator = naive_bayes.CategoricalNB(**self._config)