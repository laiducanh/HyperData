import os
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QColorDialog, QVBoxLayout, 
                             QGridLayout)
from PyQt6.QtGui import (QColor, QEnterEvent, QPainter, QIcon)
from PyQt6.QtCore import QEvent, pyqtSignal, Qt, QRectF, QSize
from PyQt6.QtSvg import QSvgRenderer
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import _PushButton, _TransparentPushButton
from ui.base_widgets.menu import Menu
from config.settings import color_lib

PALETTES = {
    # Matplotlib default
    "matplotlib": color_lib,
    # bokeh paired 12
    'paired12':['#000000', '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', '#ffffff'],
    # d3 category 10
    'category10':['#000000', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ffffff'],
    # 17 undertones https://lospec.com/palette-list/17undertones
    '17undertones': ['#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49', '#458352','#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b', '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff']
}


class _PaletteButton(_PushButton):
    def __init__(self, color, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(70, 30)
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
        
        add = _TransparentPushButton()
        
        add.setIcon(QIcon(os.path.join('UI','Icons','add.png')))
        add.setIconSize(QSize(20,20))
        add.clicked.connect(self.sig_openDialog.emit)
        palette.addWidget(add)
        add.setFixedSize(QSize(70,30))
        
        self.setLayout(palette)
        self.setFixedSize(QSize(int(78*n_columns),int(42*(row+1))))

class PaletteMenu (Menu):
    def __init__(self, colors, n_columns=5, *args, **kwargs):
        super().__init__()
        self._palette = PaletteGrid(colors=colors, n_columns=n_columns, *args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(self._palette)

class ColorPickerButton (_PushButton):
    colorChanged = pyqtSignal(str)
    def __init__(self, color: QColor, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(96, 32)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.isHover = False

        self.setColor(color)

        self._menu = PaletteMenu(colors='matplotlib',parent=self)
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
        icon = os.path.join("ui","icons","black","ChevronDown_black.svg")
        renderer = QSvgRenderer(icon)
        renderer.render(painter, rect)
        
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        pc = QColor(234, 234, 234)
        painter.setPen(pc)
        color = QColor(self.color)
        
        if self.isHover:
            painter.setOpacity(0.83)
    
        painter.setBrush(color)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 5, 5)
        rect = QRectF(self.width()-22, self.height() /
                      2-5, 10, 10)
        self._drawDropDownIcon(painter, rect)  

class ColorDropdown (QWidget):
    def __init__(self, text:str=None,color=None,parent=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(BodyLabel(text))
        
        self.button = ColorPickerButton(color, parent=parent)
        layout.addWidget(self.button)

        