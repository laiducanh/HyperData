from node_editor.node.classifier.classifier import ClassifierBase
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class AdaBoost(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_estimators=50,
            learning_rate=1.0,
        )
        else: self._config = config

        self.n_estimators = HTransparentSpinBox(
            label='Number of estimators',
            getter=lambda: self._config['n_estimators'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.learning_rate = HTransparentDoubleSpinBox(
            label='Learning rate',
            getter=lambda: self._config['learning_rate'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

    def set_estimator(self):
        self._config['n_estimators'] = self.n_estimators.get_value()
        self._config['learning_rate'] = self.learning_rate.get_value()