from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import dummy

DEBUG = False

class Dummy(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            strategy='prior',
        )
        else: self._config = config
        self.estimator = dummy.DummyClassifier(**self._config)
        
        self.strategy = HTransparentComboBox(
            items=['most_frequent','prior','stratified','uniform'],
            label='Strategy',
            label2='Strategy to use to generate predictions',
            getter=lambda: self._config['strategy'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

    def set_estimator(self):
        self._config["strategy"] = self.strategy.button.currentText()
        self.estimator = dummy.DummyClassifier(**self._config)