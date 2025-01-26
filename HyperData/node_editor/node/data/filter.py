from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, encode, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox
from ui.base_widgets.line_edit import Completer, TextEdit, CompleterLineEdit

DEBUG = False

class DataFilter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            axis="columns",
            type="items",
            apply=str()
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        def func1():
            try:
                if axis.button.currentText().lower() == "columns":
                    labels.button.setCompleter(Completer([str(i) for i in self.node.input_sockets[0].socket_data.columns])) 
                else:
                    labels.button.setCompleter(Completer([str(i) for i in self.node.input_sockets[0].socket_data.index])) 
            except: pass

        axis = ComboBox(items=["columns","index"], text="Filter by")
        axis.button.setCurrentText(self._config["axis"])
        axis.button.currentTextChanged.connect(func1)
        dialog.main_layout.addWidget(axis)

        type = ComboBox(items=["items","contains","regular expression"], text="filter type")
        type.button.setCurrentText(self._config["type"])
        dialog.main_layout.addWidget(type)

        def func2 ():
            if type.button.currentText().lower() == "items":
                if apply.button.toPlainText() == '':
                    string = list()
                else:
                    string = apply.button.toPlainText().split(",")
                string.append(labels.button.currentText())
                apply.button.setText(",".join(string))
            else:
                apply.button.setText(labels.button.currentText())
            labels.button.clear()

        labels = CompleterLineEdit(text="labels")
        labels.button.lineedit.returnPressed.connect(func2)
        func1()
        dialog.main_layout.addWidget(labels)

        apply = TextEdit(text="Keep labels")
        apply.button.setText(",".join(self._config["apply"]))
        dialog.main_layout.addWidget(apply)

        

        if dialog.exec():
            self._config["axis"] = axis.button.currentText()
            self._config["type"] = type.button.currentText()
            self._config["apply"] = apply.button.toPlainText().split(",")
            self.exec()
    

    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            if self._config["type"] == "items":
                data = self.node.input_sockets[0].socket_data.filter(
                    axis=self._config["axis"],
                    items=self._config["apply"]
                )
            elif self._config["type"] == "contains":
                data = self.node.input_sockets[0].socket_data.filter(
                    axis=self._config["axis"],
                    like=self._config["apply"][0]
                )
            elif self._config["type"] == "regular expression":
                data = self.node.input_sockets[0].socket_data.filter(
                    axis=self._config["axis"],
                    regex=self._config["apply"][0]
                )
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else: logger.info(f"{self.name} {self.node.id}: filtered data successfully.")

        except Exception as e:
            data = self.node.input_sockets[0].socket_data
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return the original DataFrame.") 
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def eval(self):
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data