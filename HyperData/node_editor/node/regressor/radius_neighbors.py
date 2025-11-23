from node_editor.node.regressor.base import RegressorBase
from sklearn import neighbors
from ui.base_widgets.button import HTransparentComboBox, HToggle, HGroupRadioButton
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class RadiusNeighbors(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            radius=1.0,
            weights='uniform',
            algorithm='auto',
            leaf_size=30,
            metric='minkowski',
        )
        else: self._config = config
        self.estimator = neighbors.RadiusNeighborsRegressor(**self._config)

        self.radius = HTransparentDoubleSpinBox(
            label='Radius',
            label2='Range of parameter space',
            getter=lambda: self._config['radius'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.weights = HGroupRadioButton(
            label='Weight function',
            items=['uniform','distance'],
            getter=lambda: self._config['weights'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.algorithm = HTransparentComboBox(
            items=['auto','ball_tree','kd_tree','brute'],
            label='Algorithm',
            getter=lambda: self._config['algorithm'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.leaf_size = HTransparentSpinBox(
            label='Leaf size',
            getter=lambda: self._config['leaf_size'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.metric_ = HTransparentComboBox(
            label='Metric',
            label2='Use for distance computation',
            items=['cityblock','cosine','euclidean','haversine','l1','l2',
                   'manhattan','nan_euclidean','minkowski'],
            getter=lambda: self._config['metric'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['radius'] = self.radius.get_value()
        self._config['weights'] = self.weights.get_value()
        self._config['algorithm'] = self.algorithm.get_value()
        self._config['leaf_size'] = self.leaf_size.get_value()
        self._config['metric'] = self.metric_.get_value()
        self.estimator = neighbors.RadiusNeighborsRegressor(**self._config)