from node_editor.node.data_transformation.base import MethodBase
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.frame import VFrame

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

        fr = VFrame(self.vlayout)

        self.method = HTransparentComboBox(
            items=["yeo-johnson","box-cox"], 
            label="Method",
            getter=lambda: self._config["method"],
            layout=fr.vlayout
        )

        self.standardize = HToggle(
            label="Standardize",
            getter=lambda: self._config["standardize"],
            layout=fr.vlayout
        )
        
    def update_config(self):
        self._config.update(
            method = self.method.button.currentText(),
            standardize = self.standardize.button.isChecked()
        )
