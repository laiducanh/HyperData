from node_editor.node.regressor.base import RegressorBase
from sklearn import cross_decomposition
from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class PLS(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            n_components=2,
            scale=True,
            max_iter=500,
            algorithm='nipals'
        )
        else: self._config = config
        self.estimator = cross_decomposition.PLSCanonical(**self._config)

        self.n_components = HTransparentSpinBox(
            label='Number of components',
            getter=lambda: self._config['n_components'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.scale = HToggle(
            label='Scale',
            label2='Whether to scale features and labels',
            getter=lambda: self._config['scale'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_iter = HTransparentSpinBox(
            label='Maximum iterations',
            minimum=1, maximum=100000, singleStep=1000,
            getter=lambda: self._config['max_iter'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.algorithm = HTransparentComboBox(
            items=['nipals','svd'],
            label='Algorithm',
            getter=lambda: self._config['algorithm'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['n_components'] = self.n_components.get_value()
        self._config['max_iter'] = self.max_iter.get_value()
        self._config['scale'] = self.scale.get_value()
        self._config['algorithm'] = self.algorithm.get_value()
        self.estimator = cross_decomposition.PLSCanonical(**self._config)