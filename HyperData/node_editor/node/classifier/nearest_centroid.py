from ui.base_widgets.button import HTransparentComboBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import neighbors

DEBUG = False

class NearestCentroid(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if config == None: self._config = dict(metric="euclidean")
        else: self._config = config
        self.estimator = neighbors.NearestCentroid(**self._config)

        self.metric_ = HTransparentComboBox(items=["euclidean","manhattan"], label="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)
        
    def set_estimator(self):
        self._config["metric"] = self.metric_.button.currentText()
        
        self.estimator = neighbors.NearestCentroid(**self._config)