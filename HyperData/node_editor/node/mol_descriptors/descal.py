import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.node.mol_descriptors.descal_dict import desc_total
from data_processing.data_window import MolDataView
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import PushButton, HTransparentComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel, TitleLabel
from ui.base_widgets.list import TreeWidget, QTreeWidgetItem
from ui.base_widgets.line_edit import SearchBox
from PySide6.QtWidgets import QHeaderView, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal

DEBUG = False

class _SearchBox(SearchBox):
    def __init__(self, data_lookup = None, parent=None, *args, **kwargs):
        super().__init__(data_lookup, parent, *args, **kwargs)

    def search_func(self):
        matches = []
        root = self.lookup.invisibleRootItem()
        stack = [root]
        while stack:
            parent = stack.pop()
            for i in range(parent.childCount()):
                item = parent.child(i)
                for col in range(self.lookup.columnCount()):
                    if self.text().lower() in item.text(col).lower():
                        matches.append(item)
                        break
                stack.append(item)
        for i in range(self.lookup.topLevelItemCount()):
            item = self.lookup.topLevelItem(i)
            for j in range(item.childCount()):
                if item.child(j) in matches:
                    item.child(j).setHidden(False)
                else:
                    item.child(j).setHidden(True)

class _TreeWidget(TreeWidget):
    selectedChange = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setHeaderHidden(False)
        self.setHeaderLabels(['Code','Description','Tags'])
        # self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.itemChanged.connect(self.onChanged)
        self.itemPressed.connect(self.onPressed)

        self.selected = []
        self.total_items = 0

    def setData(self, data:dict, selected:list):
        self.clear()
        self.total_items = 0
        self.data = data
        for group, group_values in data.items():
            item = QTreeWidgetItem([group,'',''])   
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            for code, desc in group_values.items():
                child = QTreeWidgetItem([code, desc[0],''])
                child.setFlags(child.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.addChild(child)
                self.total_items += 1
                if code in selected:
                    child.setCheckState(0, Qt.CheckState.Checked)        
                    self.selected.append(code)
                else:
                    child.setCheckState(0, Qt.CheckState.Unchecked)
            self.invisibleRootItem().addChild(item)

        self.expandAll()
        self.header().resizeSections(QHeaderView.ResizeMode.ResizeToContents)
    
    def onPressed(self, item:QTreeWidgetItem, column):
        state = item.checkState(0)
        if state == Qt.CheckState.Unchecked:
            item.setCheckState(0, Qt.CheckState.Checked)
        else:
            item.setCheckState(0, Qt.CheckState.Unchecked)

    def onChanged(self, item:QTreeWidgetItem, column):

        self.blockSignals(True)
        state = item.checkState(0)

        # Propagate to children
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, state)

        # Update parent if exists
        parent = item.parent()
        if parent is not None:
            checked, unchecked = 0, 0
            for i in range(parent.childCount()):
                cstate = parent.child(i).checkState(0)
                if cstate == Qt.CheckState.Checked:
                    checked += 1
                elif cstate == Qt.CheckState.Unchecked:
                    unchecked += 1
            if checked == parent.childCount():
                parent.setCheckState(0, Qt.CheckState.Checked)
            elif unchecked == parent.childCount():
                parent.setCheckState(0, Qt.CheckState.Unchecked)
            else:
                parent.setCheckState(0, Qt.CheckState.PartiallyChecked)

        self.blockSignals(False)

        # update number of selected items
        self.selected = []
        for i in range(self.topLevelItemCount()):
            for j in range(self.topLevelItem(i).childCount()):
                item = self.topLevelItem(i).child(j)
                if item.checkState(0) == Qt.CheckState.Checked:
                    self.selected.append(item.text(0))

        self.selectedChange.emit()
    
    def selectAll(self):
        for i in range(self.topLevelItemCount()):
            for j in range(self.topLevelItem(i).childCount()):
                self.topLevelItem(i).child(j).setCheckState(0, Qt.CheckState.Checked)
        return super().selectAll()

    def clearSelection(self):
        for i in range(self.topLevelItemCount()):
            for j in range(self.topLevelItem(i).childCount()):
                self.topLevelItem(i).child(j).setCheckState(0, Qt.CheckState.Unchecked)
        return super().clearSelection()
    
class DescCal(NodeContentWidget):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.view = MolDataView(self.data_to_view, parent)
        self._config = dict(
            descriptors = [],
            source = None
        )
    
    def config(self):
        dialog = Dialog(title="Configuration", parent=self.parent)
        dialog.setMinimumSize(600, 400)

        dialog.main_layout.addWidget(TitleLabel('Molecular Descriptors'))
        dialog.main_layout.addWidget(SeparateHLine())

        source = HTransparentComboBox(
            items=list(self.node.input_sockets[0].socket_data.columns),
            label='Source',
            label2='Column to read molecules',
            getter=lambda: self._config["source"],
            layout=dialog.main_layout
        )

        hlayout = QHBoxLayout()
        dialog.main_layout.addLayout(hlayout)

        self.num_selected = BodyLabel()
        hlayout.addWidget(self.num_selected)

        hlayout.addStretch()
        selectAll = PushButton('Select All')
        hlayout.addWidget(selectAll)

        deselectAll = PushButton('Deselect All')
        hlayout.addWidget(deselectAll)

        self.tree = _TreeWidget(self.parent)
        self.tree.setData(desc_total, self._config["descriptors"])
        self.tree.selectedChange.connect(self.update_selected)
        self.update_selected()
        selectAll.pressed.connect(self.tree.selectAll)
        deselectAll.pressed.connect(self.tree.clearSelection)
        dialog.main_layout.addWidget(self.tree)

        search_box = _SearchBox()
        search_box.set_TreeView(self.tree)
        search_box.setPlaceholderText("Filter descriptors")
        dialog.main_layout.addWidget(search_box)

        if dialog.exec():
            self._config.update(
                descriptors=self.tree.selected,
                source=source.get_value()
            )
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()
    
    def update_selected(self):
        self.num_selected.setText(f"Selected: {len(self.tree.selected)}/{self.tree.total_items}")

    def func(self, *args, **kwargs):       
        try:
            data = self.node.input_sockets[0].socket_data.copy()
            for index in data.index:
                mol = data.loc[index, self._config['source']]
                for desc in self._config["descriptors"]:
                    for values in desc_total.values():
                        if desc in values:
                            func = values[desc][-1]
                            data.loc[index, desc] = func(mol)

            # write log
            logger.info(f"{self.name} {self.node.id}: compute molecular descriptors successfully.")
            # change progressbar's color
            self.progress.changeColor('success')
        except Exception as e:
            data = self.node.input_sockets[0].socket_data.copy()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: fail, return the original DataFrame.") 
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()

    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data