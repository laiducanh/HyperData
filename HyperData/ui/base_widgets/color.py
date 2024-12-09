import os
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QColorDialog, QVBoxLayout, 
                             QGridLayout)
from PyQt6.QtGui import (QColor, QEnterEvent, QPainter, QIcon)
from PyQt6.QtCore import QEvent, pyqtSignal, Qt, QRectF, QSize
from PyQt6.QtSvg import QSvgRenderer
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import _PushButton, _TransparentPushButton, HButton
from ui.base_widgets.menu import Menu
from ui.base_widgets.frame import SeparateHLine
from config.settings import color_lib

PALETTES = {
    # Matplotlib default
    "matplotlib": color_lib,
    # bokeh paired 12
    'paired12':['#000000', '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', '#ffffff'],
    # d3 category 10
    'category10':['#000000', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ffffff'],
    # 17 undertones https://lospec.com/palette-list/17undertones
    '17undertones': ['#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49', '#458352','#dcd37b', 
                     '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b', '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff'],
    # distinguishable colors
    '32 colors': ["#FF0000","#FF8600","#FFF700","#1DFF00","#00FFEE","#0019FF","#FF00FF","#000000",
                  "#FF5050","#FFAC50","#FFFA50","#64FF50","#50FFF3","#5061FF","#FF50FF","#505050",
                  "#FFA0A0","#FFD2A0","#FFFCA0","#ABFFA0","#A0FFF9","#A0AAFF","#FFA0FF","#A0A0A0",
                  "#FFF0F0","#FFF8F0","#FFFFF0","#F2FFF0","#F0FFFE","#F0F2FF","#FFF0FF","#F0F0F0"],
    # basic colors
    'basic colors': ["#000000","#aa0000","#005500","#aa5500","#00aa00","#aaaa00","#00ff00","#aaff00",
                     "#00007f","#aa007f","#00557f","#aa557f","#00aa7f","#aaaa7f","#00ff7f","#aaff7f",
                     "#0000ff","#aa00ff","#0055ff","#aa55ff","#00aaff","#aaaaff","#00ffff","#aaffff",
                     "#550000","#ff0000","#555500","#ff5500","#55aa00","#ffaa00","#55ff00","#ffff00",
                     "#55007f","#ff007f","#55557f","#ff557f","#55aa7f","#ffaa7f","#55ff7f","#ffff7f",
                     "#5500ff","#ff00ff","#5555ff","#ff55ff","#55aaff","#ffaaff","#55ffff","#ffffff"]
}


class _PaletteButton(_PushButton):
    def __init__(self, color, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(25, 25)
        self.setColor(color)
        self.isHover = False

    def setColor(self, color):
        """ set the color of card """
        self.color = QColor(color)
        self.update()
    
    def enterEvent(self, a0: QEnterEvent) -> None:
        self.isHover = True
        return super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:
        self.isHover = False
        return super().leaveEvent(a0)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if self.isHover:
            painter.setOpacity(0.83)

        # draw color
        painter.setBrush(self.color)
        painter.setPen(QColor(0, 0, 0, 13))
        painter.drawRoundedRect(self.rect(), 4, 4)

class _PaletteBase(QWidget):

    selected = pyqtSignal(object)

    def _emit_color(self, color):
        self.selected.emit(color)

class _PaletteLinearBase(_PaletteBase):
    def __init__(self, colors, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(colors, str):
            if colors in PALETTES:
                colors = PALETTES[colors]
        
        palette = self.layoutvh()

        for c in colors:
            b = _PaletteButton(c)
            b.pressed.connect(
                lambda c=c: self._emit_color(c)
            )
            palette.addWidget(b)

        self.setLayout(palette)

class PaletteHorizontal(_PaletteLinearBase):
    layoutvh = QHBoxLayout

class PaletteVertical(_PaletteLinearBase):
    layoutvh = QVBoxLayout

class PaletteGrid(_PaletteBase):
    sig_openDialog = pyqtSignal()
    def __init__(self, colors, n_columns, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout(self)

        if isinstance(colors, str):
            if colors in PALETTES:
                colors = PALETTES[colors]

        palette = QGridLayout()
        
        row, col = 0, 0

        for c in colors:
            b = _PaletteButton(c)
            b.pressed.connect(
                lambda c=c: self._emit_color(c)
            )
            palette.addWidget(b, row, col)
            col += 1
            if col == n_columns:
                col = 0
                row += 1
        
        layout.addLayout(palette)

        layout.addWidget(SeparateHLine())
        
        add = _TransparentPushButton()
        add.setText("More colors")
        add.setIcon('add.png')
        add.setIconSize(QSize(15,15))
        add.clicked.connect(self.sig_openDialog.emit)
        layout.addWidget(add)
        
        
        #self.setFixedSize(QSize(int(35*n_columns),int(35*(row+1))))
        
        # add = _TransparentPushButton()
        
        # add.setIcon('add.png')
        # add.setIconSize(QSize(20,20))
        # add.clicked.connect(self.sig_openDialog.emit)
        # palette.addWidget(add)
        # add.setFixedSize(QSize(70,30))
        
        # self.setLayout(palette)
        # self.setFixedSize(QSize(int(78*n_columns),int(42*(row+1))))



class PaletteMenu (Menu):
    def __init__(self, colors, n_columns=8, *args, **kwargs):
        super().__init__()
        self._palette = PaletteGrid(colors=colors, n_columns=n_columns, *args, **kwargs)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self._palette)

class ColorPickerButton (_PushButton):
    colorChanged = pyqtSignal(str)
    def __init__(self, color: QColor, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(96, 32)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.isHover = False

        if color: self.setColor(color)
        else: self.setColor("black")

        self._menu = PaletteMenu(colors='basic colors',parent=self)
        self._menu._palette.selected.connect(self.__onColorChanged)
        self._menu._palette.sig_openDialog.connect(self.__showColorDialog)
        self.setMenu(self._menu)

    def __showColorDialog(self):
        """ show color dialog """
        dialog = QColorDialog(self.color, self.window())
        dialog.colorSelected.connect(self.__onColorChanged)
        dialog.exec()
        
    def __onColorChanged(self, color):
        """ color changed slot """
        self.setColor(color)
        if isinstance(color, QColor): color = color.name()
        self.colorChanged.emit(color)
        self._menu.close()

    def setColor(self, color):
        """ set color """
        if not color: color = 'white'
        self.color = QColor(color)
        self.update()
    
    def enterEvent(self, a0: QEnterEvent) -> None:
        self.isHover = True
        return super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:
        self.isHover = False
        return super().leaveEvent(a0)
    
    def _drawDropDownIcon(self, painter:QPainter, rect):
        # determine whether the self.color is dark or light
        _pc = QColor(self.color)
        brightness = 0.2126*_pc.getRgb()[0]+ \
                     0.7152*_pc.getRgb()[1]+ \
                     0.0722*_pc.getRgb()[2]
        if brightness >= 128:
            icon = os.path.join("ui","icons","black","ChevronDown_black.svg")
        else:
            icon = os.path.join("ui","icons","white","ChevronDown_white.svg")
        renderer = QSvgRenderer(icon)
        renderer.render(painter, rect)
        
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        
        # darker self.color to get edge color
        _pc = QColor(self.color)
        pc = QColor(int(_pc.getRgb()[0]*0.5),
                    int(_pc.getRgb()[1]*0.5),
                    int(_pc.getRgb()[2]*0.5))
        painter.setPen(pc)
        
        if self.isHover:
            painter.setOpacity(0.83)

        # fill background with self.color
        painter.setBrush(QColor(self.color))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 5, 5)
        rect = QRectF(self.width()-22, self.height() /
                      2-5, 10, 10)
        self._drawDropDownIcon(painter, rect)  

class ColorDropdown (HButton):
    def __init__(self, text:str=None, text2:str=None, color=None,parent=None):
        super().__init__(text, text2, parent)

        self.button = ColorPickerButton(color, parent=parent)
        self.butn_layout.addWidget(self.button)

        