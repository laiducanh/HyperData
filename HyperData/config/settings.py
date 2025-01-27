import string, itertools, matplotlib, os, logging, json
from PySide6.QtCore import QStandardPaths, QDir

GLOBAL_DEBUG = False

# list_name is replaced by column_labels
list_name =list(string.ascii_lowercase)
for j in [''.join(i) for i in itertools.product(string.ascii_lowercase, repeat = 2)]: list_name.append(j) # can handle maximum of 702 columns

from matplotlib import font_manager
font_lib = font_manager.get_font_names()
font_lib.append('sans-serif')

from matplotlib import lines
marker_lib = lines.Line2D.markers

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

color_lib = matplotlib.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = itertools.cycle(color_lib)
# linestyle_lib = dict()
# for ls in ["solid","dashed","dotted","dashdot"]:
#     linestyle_lib[matplotlib.lines._get_dash_pattern(ls)] = ls
linestyle_lib = {"-":"solid","--":"dashed","-.":"dashdot",":":"dotted"}

hatch_lib = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*','None']

encode = ['ascii',
 'big5',
 'big5hkscs',
 'cp037',
 'cp273',
 'cp424',
 'cp437',
 'cp500',
 'cp720',
 'cp737',
 'cp775',
 'cp850',
 'cp852',
 'cp855',
 'cp856',
 'cp857',
 'cp858',
 'cp860',
 'cp861',
 'cp862',
 'cp863',
 'cp864',
 'cp865',
 'cp866',
 'cp869',
 'cp874',
 'cp875',
 'cp932',
 'cp949',
 'cp950',
 'cp1006',
 'cp1026',
 'cp1125',
 'cp1140',
 'cp1250',
 'cp1251',
 'cp1252',
 'cp1253',
 'cp1254',
 'cp1255',
 'cp1256',
 'cp1257',
 'cp1258',
 'euc_jp',
 'euc_jis_2004',
 'euc_jisx0213',
 'euc_kr',
 'gb2312',
 'gbk',
 'gb18030',
 'hz',
 'iso2022_jp',
 'iso2022_jp_1',
 'iso2022_jp_2',
 'iso2022_jp_2004',
 'iso2022_jp_3',
 'iso2022_jp_ext',
 'iso2022_kr',
 'latin_1',
 'iso8859_2',
 'iso8859_3',
 'iso8859_4',
 'iso8859_5',
 'iso8859_6',
 'iso8859_7',
 'iso8859_8',
 'iso8859_9',
 'iso8859_10',
 'iso8859_11',
 'iso8859_13',
 'iso8859_14',
 'iso8859_15',
 'iso8859_16',
 'johab',
 'koi8_r',
 'koi8_t',
 'koi8_u',
 'kz1048',
 'mac_cyrillic',
 'mac_greek',
 'mac_iceland',
 'mac_latin2',
 'mac_roman',
 'mac_turkish',
 'ptcp154',
 'shift_jis',
 'shift_jis_2004',
 'shift_jisx0213',
 'utf_32',
 'utf_32_be',
 'utf_32_le',
 'utf_16',
 'utf_16_be',
 'utf_16_le',
 'utf_7',
 'utf_8',
 'utf_8_sig']

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
# configFile = "config.json.txt"
if os.path.exists(configFile):
    with open(configFile, "r") as file:
        raw_data = file.read()
        config = json.loads(raw_data)
else: config = {"theme":"Light", "dock area":"Left", "version":"0.9.21", "plot_tooltip":False, }

logFile = os.path.join(dataPathDir.absolutePath(),appName,"debug.txt")
logFile = "debug.txt"
logging.getLogger('matplotlib.font_manager').disabled = True
# Create and configure logger
logging.basicConfig(filename=logFile,format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)




   