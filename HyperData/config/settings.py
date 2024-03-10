import string, itertools, matplotlib, os, logging, qfluentwidgets
from PyQt6.QtCore import Qt, QStandardPaths, QDir, QSettings
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from ui.base_widgets.button import ComboBox

DEBUG = True

# list_name is replaced by column_labels
list_name =list(string.ascii_lowercase)
for j in [''.join(i) for i in itertools.product(string.ascii_lowercase, repeat = 2)]: list_name.append(j) # can handle maximum of 702 columns

from matplotlib import font_manager
font_lib = font_manager.get_font_names()
font_lib.append('sans-serif')

marker_lib = matplotlib.lines.Line2D.markers

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

color_lib = matplotlib.rcParams["axes.prop_cycle"].by_key()["color"]

linestyle_lib = {'-': 'Solid','--': 'Dashed','-.': 'DashDot',':': 'Dotted','None': 'None',}

hatch_lib = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']

### Initialize setting and logging profiles
dataPath = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
dataPathDir = QDir(dataPath)
if not dataPathDir.exists():
    # create the directory (including parent directories if they don't exist);
    # that the argument of mkpath is relative to the QDir's object path, so
    # using '.' means that it will create the actual dataPath
    dataPathDir.mkpath('.')  

appName = 'HyperData'
configFile = os.path.join(dataPathDir.absolutePath(),appName,"config.ini")
if DEBUG: configFile = "config.ini"
config = QSettings(configFile, QSettings.Format.IniFormat)

logFile = os.path.join(dataPathDir.absolutePath(),appName,"log.txt")
if DEBUG: logFile = "DEBUG.txt"
logging.getLogger('matplotlib.font_manager').disabled = True
# Create and configure logger
logging.basicConfig(filename=logFile,format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Initialize configuration when starting up
if config.value("theme") == "Auto":
    qfluentwidgets.setTheme(qfluentwidgets.Theme.AUTO)
elif config.value("theme") == "Light":
    qfluentwidgets.setTheme(qfluentwidgets.Theme.LIGHT)
elif config.value("theme") == "Dark":
    qfluentwidgets.setTheme(qfluentwidgets.Theme.DARK)        
else:
    qfluentwidgets.setTheme(qfluentwidgets.Theme.AUTO)
    config.setValue("theme", "Auto")

class SettingsWindow (QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        theme = ComboBox(items=["Auto","Light","Dark"], text='Theme')
        theme.button.setCurrentText(config.value("theme"))
        layout.addWidget(theme)
        theme.button.currentTextChanged.connect(self.setTheme)  

        layout.addWidget(QPushButton('abc',self))

    def setTheme(self, theme:str):
        config.setValue("theme", theme)
        if theme == "Auto":
            qfluentwidgets.setTheme(qfluentwidgets.Theme.AUTO)
        elif theme == "Light":
            qfluentwidgets.setTheme(qfluentwidgets.Theme.LIGHT)
        elif theme == "Dark":
            qfluentwidgets.setTheme(qfluentwidgets.Theme.DARK)     
                  