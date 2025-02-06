from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox
from sklearn import decomposition

class IncrementalPCA(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_components = None,
            whiten = False,
        )
        else: self._config = config
        self.method = decomposition.IncrementalPCA(**self._config)

        self.n_components = SpinBox(text="Number of components")
        self.n_components.button.setValue(self._config["n_components"])
        self.n_components.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_components)

        self.whiten = Toggle(text="Whitening")
        self.whiten.button.setChecked(self._config["whiten"])
        self.whiten.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.whiten)
        
    def set_estimator(self):
        self._config.update(
            n_components = self.n_components.button.value(),
            whiten = self.whiten.button.isChecked(),
        )
        self.method = decomposition.IncrementalPCA(**self._config)