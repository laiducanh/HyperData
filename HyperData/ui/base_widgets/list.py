import qfluentwidgets
from PyQt6 import QtCore, QtWidgets, QtGui

class Draggable_ListWidget(qfluentwidgets.ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setIconSize(QtCore.QSize(32, 32))
        #self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.setDragEnabled(True)
    
    def mousePressEvent(self, event:QtGui.QMouseEvent):
        item = self.itemAt(event.pos())
        if item and item.text():

            pixmap = QtGui.QPixmap(16, 16)
            pixmap.fill(QtGui.QColor("lightgray"))

            mimeData = QtCore.QMimeData()
            mimeData.setText(item.text())

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QtCore.QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))
            drag.setPixmap(pixmap)

            drag.exec(QtCore.Qt.DropAction.MoveAction)

            super().mousePressEvent(event)


class TreeWidget (qfluentwidgets.TreeWidget):
    sig_doubleClick = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setIconSize(QtCore.QSize(24, 24))
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.setHeaderHidden(True)

    def setData (self, data:dict):

        self.clear()

        items = []
        self.data = data
        for key, values in data.items():
            item = QtWidgets.QTreeWidgetItem([key])            

            for value in values:
                child = QtWidgets.QTreeWidgetItem([value])
                item.addChild(child)
            items.append(item)

        self.insertTopLevelItems(0, items)
        self.expandAll()
    
    def mousePressEvent(self, event:QtGui.QMouseEvent):
        item = self.itemAt(event.pos())
        if isinstance(item, QtWidgets.QTreeWidgetItem):
            if item.text(0) in self.data.keys():
                item.setExpanded(not item.isExpanded())

        super().mousePressEvent(event) 
    
    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent | None) -> None:
        item = self.itemAt(event.pos())
        if isinstance(item, QtWidgets.QTreeWidgetItem): 
            self.sig_doubleClick.emit(str(item.data(0,0)))
        return super().mouseDoubleClickEvent(event)

class Draggable_TreeWidget (TreeWidget):   
    
    def mousePressEvent(self, event:QtGui.QMouseEvent):
        item = self.itemAt(event.pos())
        if isinstance(item, QtWidgets.QTreeWidgetItem):
            if item.text(0) not in self.data.keys():
                pixmap = QtGui.QPixmap(16, 16)
                pixmap.fill(QtGui.QColor("lightgray"))

                mimeData = QtCore.QMimeData()
                mimeData.setText(item.text(0))

                drag = QtGui.QDrag(self)
                drag.setMimeData(mimeData)
                drag.setHotSpot(QtCore.QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))
                drag.setPixmap(pixmap)

                drag.exec(QtCore.Qt.DropAction.MoveAction)
            
            
        super().mousePressEvent(event)



