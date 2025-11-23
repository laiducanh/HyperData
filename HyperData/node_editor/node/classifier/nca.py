from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import neighbors

DEBUG = False

class NCA(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            init='auto',
            max_iter=50,
        )
        else: self._config = config
        self.estimator = neighbors.NeighborhoodComponentsAnalysis(**self._config)

        self.init_ = HTransparentComboBox(
            items=['Auto','PCA','LDA','Identity','Random'],
            label='Initialization method',
            label2='Initialization of the linear transformation',
            getter=lambda: self._config['init'],
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
        self._config["init"] = self.init_.get_value()
        self._config["max_iter"] = self.max_iter.get_value()
        self.estimator = neighbors.NeighborhoodComponentsAnalysis(**self._config)