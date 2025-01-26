from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsSocket
from node_editor.node.misc.executor import Executor
from node_editor.node.misc.looper import Looper
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import _TransparentComboBox, PushButton, _TransparentToolButton, _TransparentPushButton
from ui.base_widgets.line_edit import LineEdit, Completer, TextEdit
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.frame import SeparateHLine
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QSize, Signal

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6

class UserDefine (NodeContentWidget):
    sig_redraw = Signal()
    def __init__(self, node=None, parent=None):
        super().__init__(node, parent)

        self._config = dict(title="user define card")
        self.socket_in, self.socket_out = list(), list()

    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)
        socket_in = self.socket_in
        socket_out = self.socket_out
        self.socket_in, self.socket_out = list(), list()
        btn_in, btn_out = list(), list()

        def changeTitle (title):
            self.node.title = title
            self.node.setTitle()
        title = LineEdit(text='Card Title')
        title.button.setText(self._config['title'])
        dialog.main_layout.addWidget(title)

        dialog.main_layout.addWidget(SeparateHLine())

        socket_layout = QHBoxLayout()
        socket_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        dialog.main_layout.addLayout(socket_layout)

        input_socket = QVBoxLayout()
        input_socket.setAlignment(Qt.AlignmentFlag.AlignTop)
        input_socket.setSpacing(4)
        input_socket.addWidget(BodyLabel("Input"))
        socket_layout.addLayout(input_socket)

        add_socket_in = _TransparentPushButton()
        add_socket_in.setIcon("add.png")
        add_socket_in.clicked.connect(lambda: addSocketIn(len(self.socket_in), 1))
        input_socket.addWidget(add_socket_in)

        output_socket = QVBoxLayout()
        output_socket.setSpacing(4)
        output_socket.setAlignment(Qt.AlignmentFlag.AlignTop)
        output_socket.addWidget(BodyLabel("Output"))
        socket_layout.addLayout(output_socket)

        add_socket_out = _TransparentPushButton()
        add_socket_out.setIcon("add.png")
        add_socket_out.clicked.connect(lambda: addSocketOut(len(self.socket_out), 3))
        output_socket.addWidget(add_socket_out)
            
        def addSocketIn(index, socket_type):
            if len(self.socket_in) < 3: # maximum sockets = 3
                createButtonIn(index, socket_type)
                self.node.addSocket(index=index, socket_type=socket_type)
                self.sig_redraw.emit() # fire signal to redraw connection cards
        
        def removeSocketIn(button:_TransparentComboBox):
            index = btn_in.index(button)
            button.parent().deleteLater()
            self.socket_in.pop(index)
            btn_in.remove(button)
            redrawSockets()
        
        def updateSocketIn(index, socket_type):
            socket_type = MULTI_IN if socket_type == "multiple in" else SINGLE_IN
            self.socket_in[index] = socket_type
            self.node.removeSocket(index, socket_type)
            self.node.addSocket(index, socket_type)
        
        def createButtonIn(index, socket_type):
            layout = QHBoxLayout()
            layout.setContentsMargins(0,0,0,0)
            layout.setSpacing(0)
            widget = QWidget()
            widget.setLayout(layout)
            input_socket.insertWidget(index+1, widget)

            button = _TransparentComboBox(items=["single in", "multiple in"])
            button.setCurrentText("multiple in" if socket_type==MULTI_IN else "single in")
            self.socket_in.append(socket_type)
            btn_in.append(button)
            button.currentTextChanged.connect(lambda text: updateSocketIn(index, text))
            layout.addWidget(button)

            remove_btn = _TransparentToolButton(parent=widget)
            remove_btn.setIcon("close.png")
            remove_btn.setIconSize(QSize(12,12))
            remove_btn.clicked.connect(lambda: removeSocketIn(button))
            layout.addWidget(remove_btn)
        
        def addSocketOut(index, socket_type):
            if len(self.socket_out) < 3: # maximum sockets = 3
                createButtonOut(index, socket_type)
                self.node.addSocket(index=index, socket_type=socket_type)
                self.sig_redraw.emit() # fire signal to redraw connection cards
        
        def removeSocketOut(button:_TransparentComboBox):
            index = btn_out.index(button)
            button.parent().deleteLater()
            self.socket_out.pop(index)
            btn_out.remove(button)
            redrawSockets()
        
        def updateSocketOut(index, socket_type):
            socket_type = MULTI_OUT if socket_type == "multiple out" else SINGLE_OUT
            self.socket_out[index] = socket_type
            self.node.removeSocket(index, socket_type)
            self.node.addSocket(index, socket_type)
        
        def createButtonOut(index, socket_type):
            layout = QHBoxLayout()
            layout.setContentsMargins(0,0,0,0)
            layout.setSpacing(0)
            widget = QWidget()
            widget.setLayout(layout)
            output_socket.insertWidget(index+1, widget)

            button = _TransparentComboBox(items=["single out", "multiple out"])
            button.setCurrentText("multiple out" if socket_type==MULTI_OUT else "single out")
            self.socket_out.append(socket_type)
            btn_out.append(button)
            button.currentTextChanged.connect(lambda text: updateSocketOut(index, text))
            layout.addWidget(button)

            remove_btn = _TransparentToolButton(parent=widget)
            remove_btn.setIcon("close.png")
            remove_btn.setIconSize(QSize(12,12))
            remove_btn.clicked.connect(lambda: removeSocketOut(button))
            layout.addWidget(remove_btn)
            
        def redrawSockets():
            for obj in self.node.childItems():
                if isinstance(obj, NodeGraphicsSocket):
                    if obj.socket_type not in [PIPELINE_IN, PIPELINE_OUT]:
                        self.node.removeSocket(socket=obj)
            for index, socket_type in enumerate(self.socket_in):
                self.node.addSocket(index=index,socket_type=socket_type)
            for index, socket_type in enumerate(self.socket_out):
                self.node.addSocket(index=index,socket_type=socket_type)
            self.sig_redraw.emit() # fire signal to redraw connection cards

        for ind, socket_type in enumerate(socket_in):
            createButtonIn(ind, socket_type)
        for ind, socket_type in enumerate(socket_out):
            createButtonOut(ind, socket_type)
        
        if dialog.exec(): 
            self._config["title"] = title.button.text()
            changeTitle(self._config["title"])
    
    def exec(self):
        self.sig.emit()