from node_editor.node.regressor.base import RegressorBase
from sklearn import ensemble
from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class Bagging(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_estimators=10,
            max_samples=1.0,
            max_features=1.0,
            bootstrap=True,
            bootstrap_features=False,
            oob_score=False,
        )
        else: self._config = config

        self.n_estimators = HTransparentSpinBox(
            label='Number of estimators',
            getter=lambda: self._config['n_estimators'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_samples = HTransparentDoubleSpinBox(
            label='Percentage samples',
            minimum=0, maximum=1, singleStep=0.1,
            getter=lambda: self._config['max_samples'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_features = HTransparentDoubleSpinBox(
            label='Percentage features',
            minimum=0, maximum=1, singleStep=0.1,
            getter=lambda: self._config['max_features'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
        self.bootstrap = HToggle(
            label='Bootstrap',
            label2='Whether samples are drawn with replacement',
            getter=lambda: self._config['bootstrap'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.bootstrap_features = HToggle(
            label='Bootstrap features',
            label2='Whether features are drawn with replacement',
            getter=lambda: self._config['bootstrap_features'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.oob_score = HToggle(
            label='Out-of-bag samples',
            label2='Whether to use out-of-bag samples to estimate the generalization error',
            getter=lambda: self._config['oob_score'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        self._config['n_estimators'] = self.n_estimators.get_value()
        self._config['max_samples'] = self.max_samples.get_value()
        self._config['max_features'] = self.max_features.get_value()
        self._config['bootstrap'] = self.bootstrap.get_value()
        self._config['bootstrap_features'] = self.bootstrap_features.get_value()
        self._config['oob_score'] = self.oob_score.get_value()
