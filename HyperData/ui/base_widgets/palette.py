from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QPixmap, QColor, QPainter, QBrush, QIcon
from config.settings import settings
from ui.base_widgets.button import _PushButton, _ToolButton
from ui.base_widgets.menu import Menu
import qfluentwidgets, os

color_lib = settings.value('color lib')

PALETTES = {
    # Matplotlib default
    'matplotlib': color_lib,
    # bokeh paired 12
    'paired12':['#000000', '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', '#ffffff'],
    # d3 category 10
    'category10':['#000000', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ffffff'],
    # 17 undertones https://lospec.com/palette-list/17undertones
    '17undertones': ['#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49', '#458352','#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b', '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff']
}


class _PaletteButton(_PushButton):
    def __init__(self, color, parent=None, enableAlpha=False):
        super().__init__()
        self.setFixedSize(70, 30)
        self.setColor(color)
        self.enableAlpha = enableAlpha
        self.titledPixmap = self._createTitledBackground()

    def _createTitledBackground(self):
        pixmap = QPixmap(8, 8)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)

        c = 255 if qfluentwidgets.common.style_sheet.isDarkTheme() else 0
        color = QColor(c, c, c, 26)
        painter.fillRect(4, 0, 4, 4, color)
        painter.fillRect(0, 4, 4, 4, color)
        painter.end()
        return pixmap

    def setColor(self, color):
        """ set the color of card """
        self.color = QColor(color)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        # draw tiled background
        if self.enableAlpha:
            painter.setBrush(QBrush(self.titledPixmap))
            painter.setPen(QColor(0, 0, 0, 13))
            painter.drawRoundedRect(self.rect(), 4, 4)

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

    def __init__(self, colors, n_columns=5, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        
        add = qfluentwidgets.TransparentToolButton()
        
        add.setIcon(QIcon(os.path.join('UI','Icons','add.png')))
        add.setIconSize(QSize(20,20))
        palette.addWidget(add)
        add.setFixedSize(QSize(70,30))

        
        
        self.setLayout(palette)
        self.setFixedSize(QSize(int(78*n_columns),int(42*(row+1))))

class PaletteGrid_Layout (QVBoxLayout):
    sig = pyqtSignal(str)
    def __init__(self, colors, n_columns=5, *args, **kwargs):
        super().__init__()
        palette = PaletteGrid(colors)
        self.addWidget(palette)
        palette.selected.connect(self.selectedColor)
    def selectedColor (self,color):
        self.sig.emit(color)

class PaletteMenu (Menu):
    def __init__(self, colors, text, n_columns=5, *args, **kwargs):
        super().__init__()
        self._palette = PaletteGrid(colors=colors)
        
        self.hBoxLayout.addChildWidget(self._palette)
        self._title = text

        margins = self.contentsMargins()
        _height = int(self._palette.size().height())
        _width = int(self._palette.size().width())
        self.view.setContentsMargins(0,0,0,0)
        self.hBoxLayout.setContentsMargins(0,0,0,0)
        
        self.view.setFixedSize(_width,_height)
        self.adjustSize()
