import string, itertools, matplotlib, os, logging, qfluentwidgets, json
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtCore import Qt, QStandardPaths, QDir, QSettings, QSize

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

linestyle_lib = dict()
for ls in ["solid","dashed","dotted","dashdot"]:
    linestyle_lib[matplotlib.lines._get_dash_pattern(ls)] = ls

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
configFile = os.path.join(dataPathDir.absolutePath(),appName,"config.json.txt")
if DEBUG: configFile = "config.json.txt"
if os.path.exists(configFile):
    with open(configFile, "r") as file:
        raw_data = file.read()
        config = json.loads(raw_data)
        print(config)
else: config = {"theme":"Auto","theme color":qfluentwidgets.themeColor().name(),"dock area":"left",}

logFile = os.path.join(dataPathDir.absolutePath(),appName,"log.txt")
if DEBUG: logFile = "DEBUG.txt"
logging.getLogger('matplotlib.font_manager').disabled = True
# Create and configure logger
logging.basicConfig(filename=logFile,format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)




   