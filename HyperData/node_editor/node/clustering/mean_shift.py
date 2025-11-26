from node_editor.node.clustering.base import MethodBase
from sklearn import cluster
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentSpinBox

class MeanShift(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            cluster_all=True,
            max_iter=300
        )
        else: self._config = config
        self.method = cluster.MeanShift(**self._config)

        self.cluster_all = HToggle(
            label='Cluster all',
            getter=lambda: self._config['cluster_all'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_iter = HTransparentSpinBox(
            label='Maximum iterations',
            getter=lambda: self._config['max_iter'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        
    def set_estimator(self):
        self._config.update(
            cluster_all = self.cluster_all.get_value(),
            max_iter = self.max_iter.get_value()
        )
        self.method = cluster.MeanShift(**self._config)
    
