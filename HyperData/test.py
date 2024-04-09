from ui.base_widgets.button import _Toggle, _PushButton, SegmentedWidget, _TransparentPushButton, _ComboBox, ComboBox, _ToolButton
from ui.base_widgets.text import BodyLabel, TitleLabel
from ui.base_widgets.line_edit import _LineEdit, _SearchBox, _CompleterLineEdit
from ui.base_widgets.spinbox import _SpinBox, _Slider
from ui.base_widgets.window import ProgressBar, Dialog
from ui.base_widgets.color import ColorPickerButton
from ui.base_widgets.list import Draggable_ListWidget, TreeWidget
from ui.base_widgets.menu import Menu
from ui.utils import icon
import sys, os, darkdetect
from PyQt6 import QtWidgets, QtCore, QtGui

# Subclass QMainWindow to customize your application's main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")
        central_widget = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self.central_layout)
        self.central_layout.addWidget(TitleLabel('title label'))
        button = SegmentedWidget()
        self.central_layout.addWidget(button)
        button = _TransparentPushButton()
        self.central_layout.addWidget(button)


        button = _CompleterLineEdit(items=['heelo','world'])
        button._addItems(['qpowiuncd','qwpicns'])
        self.central_layout.addWidget(button)

        button = ComboBox(items=["tiem 2","tiwm1", "qwpjic"])
        self.central_layout.addWidget(button)

        button = _ToolButton()
        button.setIcon(icon("axis-left.png"))
        # self.y_axis = Menu(parent=self)
        # self.axis_left = QtGui.QAction(icon=icon("axis-left.png"),text='Left Axis', parent=self)
        # self.axis_right = QtGui.QAction(icon=icon("axis-right.png"),text='Right Axis', parent=self)
        # self.y_axis.addActions([self.axis_left,self.axis_right])
        # button.setMenu(self.y_axis)
        self.central_layout.addWidget(button)

        layout = QtWidgets.QHBoxLayout()
        self.central_layout.addLayout(layout)

        layout.addWidget(_PushButton())
        layout.addWidget(_CompleterLineEdit())
       
        # Set the central widget of the Window.
        self.setCentralWidget(central_widget)


app = QtWidgets.QApplication(sys.argv)
string = str()
path = os.path.join("ui","qss","light")
for file in os.listdir(path):
    with open(os.path.join(path, file), 'r') as f:
        string += f.read()
print(string)
app.setStyleSheet(string)
window = MainWindow()
window.show()

app.exec()