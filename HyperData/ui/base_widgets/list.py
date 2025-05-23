from PySide6.QtGui import QMouseEvent, QPixmap, QCursor, QEnterEvent, QColor, QDrag
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget, QListWidget, QAbstractItemView, QWidget
from PySide6.QtCore import QSize, Qt, QEvent, QMimeData, QPoint, Signal

class ListWidget (QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setIconSize(QSize(32, 32))
        #self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalScrollBar().setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
        self.horizontalScrollBar().setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    
    def enterEvent(self, event: QEnterEvent) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        return super().enterEvent(event)

    def leaveEvent(self, a0: QEvent) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        return super().leaveEvent(a0)

class Draggable_ListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragEnabled(True)
    
    def mousePressEvent(self, event:QMouseEvent):
        item = self.itemAt(event.pos())
        if item and item.text():

            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor("lightgray"))

            mimeData = QMimeData()
            mimeData.setText(item.text())

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)

            super().mousePressEvent(event)


class TreeWidget (QTreeWidget):
    sig_doubleClick = Signal(str)
    sig_onChange = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setIconSize(QSize(24, 24))
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalScrollBar().setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
        self.horizontalScrollBar().setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setHeaderHidden(True)

    def setData (self, data:dict):

        self.clear()

        items = []
        self.data = data
        for key, values in data.items():
            item = QTreeWidgetItem([key])            

            for value in values:
                child = QTreeWidgetItem([value])
                item.addChild(child)
            items.append(item)

        self.insertTopLevelItems(0, items)
        self.expandAll()
    
    def addItemWidget(self, item:QTreeWidgetItem, column:int, widget: QWidget, index=None):
        if not index: index = self.topLevelItemCount()
        child = QTreeWidgetItem(item)
        self.insertTopLevelItem(index, child)
        self.setItemWidget(child, column, widget)
    
    def mousePressEvent(self, event:QMouseEvent):
        # item = self.itemAt(event.pos())
        # if isinstance(item, QtWidgets.QTreeWidgetItem):
        #     if item.text(0) in self.data.keys():
        #         item.setExpanded(not item.isExpanded())

        super().mousePressEvent(event) 
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        item = self.itemAt(event.pos())
        if isinstance(item, QTreeWidgetItem): 
            self.sig_doubleClick.emit(str(item.data(0,0)))
        return super().mouseDoubleClickEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        return super().enterEvent(event)

    def leaveEvent(self, a0: QEvent) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        return super().leaveEvent(a0)

class TreeWidgetItem (QTreeWidgetItem):
    def __init__(self, treeview:QTreeWidget):
        super().__init__(treeview)

        self.setSizeHint(0, QSize(36,36))
        self.setExpanded(True)

class Draggable_TreeWidget (TreeWidget):   
    
    def mousePressEvent(self, event:QMouseEvent):
        item = self.itemAt(event.pos())
        if isinstance(item, QTreeWidgetItem):
            if item.text(0) not in self.data.keys():
                pixmap = QPixmap(16, 16)
                pixmap.fill(QColor("lightgray"))

                mimeData = QMimeData()
                mimeData.setText(item.text(0))

                drag = QDrag(self)
                drag.setMimeData(mimeData)
                drag.setHotSpot(QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))
                drag.setPixmap(pixmap)

                drag.exec(Qt.DropAction.MoveAction)
            
            
        super().mousePressEvent(event)

    

