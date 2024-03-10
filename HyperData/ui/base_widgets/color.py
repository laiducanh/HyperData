import qfluentwidgets
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QFrame, QApplication
from PyQt6.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QBrush, QAction, QPalette
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.palette import PaletteMenu

class ColorDialog (QWidget):
    colorChanged = pyqtSignal(QColor)

    def __init__(self, color=QColor(255, 0, 0), title: str='color', parent=None, enableAlpha=False):
        """
        Parameters
        ----------
        color: `QColor` | `GlobalColor` | str
            initial color

        title: str
            the title of dialog

        parent: QWidget
            parent widget

        enableAlpha: bool
            whether to enable the alpha channel
        """
        super().__init__(parent)
        self.enableAlpha = enableAlpha
        if not enableAlpha:
            color = QColor(color)
            color.setAlpha(255)

        self.oldColor = QColor(color)
        self.color = QColor(color)

        self.scrollArea = QScrollArea(self)
        self.scrollWidget = QWidget(self.scrollArea)

        self.buttonGroup = QFrame(self)
        self.yesButton = qfluentwidgets.PushButton(self.tr('OK'), self.buttonGroup)
        self.cancelButton = qfluentwidgets.PushButton(self.tr('Cancel'), self.buttonGroup)

        self.titleLabel = qfluentwidgets.BodyLabel(title, self.scrollWidget)
        self.huePanel = qfluentwidgets.dialog_box.color_dialog.HuePanel(color, self.scrollWidget)
        self.newColorCard = qfluentwidgets.dialog_box.color_dialog.ColorCard(color, self.scrollWidget, enableAlpha)
        self.oldColorCard = qfluentwidgets.dialog_box.color_dialog.ColorCard(color, self.scrollWidget, enableAlpha)
        self.brightSlider = qfluentwidgets.dialog_box.color_dialog.BrightnessSlider(color, self.scrollWidget)

        self.editLabel = qfluentwidgets.BodyLabel(self.tr('Edit Color'), self.scrollWidget)
        self.redLabel = qfluentwidgets.BodyLabel(self.tr('Red'), self.scrollWidget)
        self.blueLabel = qfluentwidgets.BodyLabel(self.tr('Blue'), self.scrollWidget)
        self.greenLabel = qfluentwidgets.BodyLabel(self.tr('Green'), self.scrollWidget)
        self.opacityLabel = qfluentwidgets.BodyLabel(self.tr('Opacity'), self.scrollWidget)
        self.hexLineEdit = qfluentwidgets.dialog_box.color_dialog.HexColorLineEdit(color, self.scrollWidget, enableAlpha)
        self.redLineEdit = qfluentwidgets.dialog_box.color_dialog.ColorLineEdit(self.color.red(), self.scrollWidget)
        self.redLineEdit.setFixedWidth(80)
        self.greenLineEdit = qfluentwidgets.dialog_box.color_dialog.ColorLineEdit(self.color.green(), self.scrollWidget)
        self.greenLineEdit.setFixedWidth(80)
        self.blueLineEdit = qfluentwidgets.dialog_box.color_dialog.ColorLineEdit(self.color.blue(), self.scrollWidget)
        self.blueLineEdit.setFixedWidth(80)
        self.opacityLineEdit = qfluentwidgets.dialog_box.color_dialog.OpacityLineEdit(self.color.alpha(), self.scrollWidget)

        self.vBoxLayout = QVBoxLayout(self)

        self.__initWidget()

    def __initWidget(self):
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setViewportMargins(48, 24, 0, 24)
        self.scrollArea.setWidget(self.scrollWidget)

        self.setMaximumSize(488, 600+40*self.enableAlpha)
        self.resize(488, 600+40*self.enableAlpha)
        self.scrollWidget.resize(440, 500+40*self.enableAlpha)
        self.buttonGroup.setFixedSize(486, 81)
        self.yesButton.setFixedWidth(216)
        self.cancelButton.setFixedWidth(216)

        #self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 80))
        #self.setMaskColor(QColor(0, 0, 0, 76))

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.huePanel.move(0, 46)
        self.newColorCard.move(288, 46)
        self.oldColorCard.move(288, self.newColorCard.geometry().bottom()+1)
        self.brightSlider.move(0, 324)

        self.editLabel.move(0, 385)
        self.redLineEdit.move(0, 426)
        self.greenLineEdit.move(120, 426)
        self.blueLineEdit.move(260, 426)
        self.redLabel.move(90, 434)
        self.greenLabel.move(210, 434)
        self.blueLabel.move(350, 434)
        self.hexLineEdit.move(150, 381)

        if self.enableAlpha:
            self.opacityLineEdit.move(0, 560)
            self.opacityLabel.move(144, 567)
        else:
            self.opacityLineEdit.hide()
            self.opacityLabel.hide()

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.scrollArea, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignmentFlag.AlignBottom)

        self.yesButton.move(24, 25)
        self.cancelButton.move(250, 25)

    def setColor(self, color, movePicker=True):
        """ set color """
        self.color = QColor(color)
        self.brightSlider.setColor(color)
        self.newColorCard.setColor(color)
        self.hexLineEdit.setColor(color)
        self.redLineEdit.setText(str(color.red()))
        self.blueLineEdit.setText(str(color.blue()))
        self.greenLineEdit.setText(str(color.green()))
        if movePicker:
            self.huePanel.setColor(color)

    def __onHueChanged(self, color):
        """ hue changed slot """
        self.color.setHsv(
            color.hue(), color.saturation(), self.color.value(), self.color.alpha())
        self.setColor(self.color)

    def __onBrightnessChanged(self, color):
        """ brightness changed slot """
        self.color.setHsv(
            self.color.hue(), self.color.saturation(), color.value(), color.alpha())
        self.setColor(self.color, False)

    def __onRedChanged(self, red):
        """ red channel changed slot """
        self.color.setRed(int(red))
        self.setColor(self.color)

    def __onBlueChanged(self, blue):
        """ blue channel changed slot """
        self.color.setBlue(int(blue))
        self.setColor(self.color)

    def __onGreenChanged(self, green):
        """ green channel changed slot """
        self.color.setGreen(int(green))
        self.setColor(self.color)

    def __onOpacityChanged(self, opacity):
        """ opacity channel changed slot """
        self.color.setAlpha(int(int(opacity)/100*255))
        self.setColor(self.color)

    def __onHexColorChanged(self, color):
        """ hex color changed slot """
        self.color.setNamedColor("#" + color)
        self.setColor(self.color)

    def __onYesButtonClicked(self):
        """ yes button clicked slot """
        
        if self.color != self.oldColor:
            self.colorChanged.emit(self.color)
        self.close()

    def updateStyle(self):
        """ update style sheet """
        self.setStyle(QApplication.style())
        self.titleLabel.adjustSize()
        self.editLabel.adjustSize()
        self.redLabel.adjustSize()
        self.greenLabel.adjustSize()
        self.blueLabel.adjustSize()
        self.opacityLabel.adjustSize()

    def showEvent(self, e):
        self.updateStyle()
        super().showEvent(e)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        self.cancelButton.clicked.connect(self.close)
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

        self.huePanel.colorChanged.connect(self.__onHueChanged)
        self.brightSlider.colorChanged.connect(self.__onBrightnessChanged)

        self.redLineEdit.valueChanged.connect(self.__onRedChanged)
        self.blueLineEdit.valueChanged.connect(self.__onBlueChanged)
        self.greenLineEdit.valueChanged.connect(self.__onGreenChanged)
        self.hexLineEdit.valueChanged.connect(self.__onHexColorChanged)
        self.opacityLineEdit.valueChanged.connect(self.__onOpacityChanged)

class ColorPicker (QWidget):
    def __init__(self, title:str, text:str=None, color:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if color == None:
            color = 'white'
        
        if text != None:
            layout.addWidget(BodyLabel(text.title()))

        self.button = qfluentwidgets.ColorPickerButton(color=color, title=title, parent=parent)
        layout.addWidget(self.button)


class _ColorDropdown (qfluentwidgets.SplitPushButton):
    colorChanged = pyqtSignal(str)
    def __init__(self, color=qfluentwidgets.themeColor(),parent=None):
        super().__init__()

        self.menu = PaletteMenu(colors='matplotlib',parent=self)
        self.menu._palette.selected.connect(self.colorSelected)
        self.menu._palette.sig_openDialog.connect(self.buttonClicked)
        self.dropDownClicked.connect(self.execMenu)
        self.button.clicked.connect(self.buttonClicked)
        self.color = color
        self.parent = parent
    
    def execMenu (self):
        self.menu.exec(self.mapToGlobal(self.dropButton.pos()))
    
    def buttonClicked(self):
        self.menu.close()
        dialog = qfluentwidgets.ColorDialog(color=self.color,title='ablc',parent=self.parent)
        dialog.colorChanged.connect(self.colorSelected)
        dialog.exec()
    
    def colorSelected (self, color):
        self.menu.close()
        self.color = QColor(color)
        self.colorChanged.emit(color)
        self.update()
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        pc = QColor(255, 255, 255, 10) if qfluentwidgets.isDarkTheme() else QColor(234, 234, 234)
        painter.setPen(pc)

        color = QColor(self.color)

        painter.setBrush(color)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 5, 5)
        return super().paintEvent(a0)

class ColorDropdown (QWidget):
    def __init__(self, text:str=None,color=None,parent=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(qfluentwidgets.BodyLabel(text))
        
        self.button = _ColorDropdown(parent=parent)
        layout.addWidget(self.button)

        