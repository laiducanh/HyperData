from node_editor.node.clustering.base import MethodBase
from sklearn import cluster

class MeanShift(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        self._config = dict()
        self.method = cluster.MeanShift(**self._config)