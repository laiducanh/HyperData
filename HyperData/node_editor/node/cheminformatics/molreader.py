import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.data.data import DataReader
from data_processing.data_window import MolDataView
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel, BodyLabel
from PySide6.QtCore import QFileSystemWatcher

DEBUG = False

class MolReader(DataReader):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
    
        self.view = MolDataView(pd.DataFrame(), parent)