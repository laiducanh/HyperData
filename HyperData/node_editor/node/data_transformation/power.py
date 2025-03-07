from node_editor.node.data_transformation.base import MethodBase
from ui.base_widgets.button import ComboBox, Toggle

class Power(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            method = "yeo-johnson",
            standardize = True
        )
        else: self._config = config

        self.method = ComboBox(items=["yeo-johnson","box-cox"], text="Method")
        self.method.button.setCurrentText(self._config["method"])
        self.vlayout.addWidget(self.method)

        self.standardize = Toggle(text="Standardize")
        self.standardize.button.setChecked(self._config["standardize"])
        self.vlayout.addWidget(self.standardize)
        
    def update_config(self):
        self._config.update(
            method = self.method.button.currentText(),
            standardize = self.standardize.button.isChecked()
        )
