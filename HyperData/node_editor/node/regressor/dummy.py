from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from node_editor.node.regressor.base import RegressorBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import dummy

DEBUG = False

class Dummy(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            strategy='prior',
            quantile=0.5
        )
        else: self._config = config
        self.estimator = dummy.DummyRegressor(**self._config)
        
        self.strategy = HTransparentComboBox(
            items=['mean','median','quantile'],
            label='Strategy',
            label2='Strategy to use to generate predictions',
            getter=lambda: self._config['strategy'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.quantile = HTransparentDoubleSpinBox(
            label='Quantile',
            label2='The quantile to predict using the quantile strategy',
            minimum=0, maximum=1, singleStep=0.1,
            getter=lambda: self._config['quantile'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

    def set_estimator(self):
        self._config["strategy"] = self.strategy.button.currentText()
        self._config['quantile'] = self.quantile.button.value()
        self.estimator = dummy.DummyRegressor(**self._config)