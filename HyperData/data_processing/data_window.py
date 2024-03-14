from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTableView, QApplication, QLabel, QAbstractItemView,
                             QCompleter, QPushButton, QMainWindow, QScrollBar)
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtCore import QModelIndex, QSize, pyqtSignal, Qt, QAbstractTableModel, QVariant
import os, missingno, qfluentwidgets, math
from collections import Counter
import pandas as pd
import numpy as np
from config.settings import list_name
from ui.base_widgets.button import _PushButton, _ToolButton, _PrimaryPushButton
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.icons import Icon
from plot.canvas import Canvas

class TableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self.numRows=100    
        self.numColumns=100

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        index=QModelIndex
        """
        if not index.isValid():
            return
        
        if index.row()>=self.numRows or index.row()<0 or index.column()>=self.numColumns or index.column()<0:
            return 
        
        if role==Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        elif role==Qt.ItemDataRole.BackgroundRole:
            return QVariant(QGuiApplication.palette().base())
            
        return 
    
    def canFetchMore(self, index):
        """
        index=QModelIndex
        """
        if self.numRows<self._data.shape[0] or self.numColumns<self._data.shape[1]:
            return True
        else:
            return False
    def fetchMore(self, index):
        """
        Index=QModelIndex
        """
        maxFetch=20     #maximum number of rows/columns to grab at a time.
        
        remainderRows=self._data.shape[0]-self.numRows
        
        
        if maxFetch < remainderRows:
            self.beginInsertRows(QModelIndex(), self.numRows, self.numRows+maxFetch-1)
            self.endInsertRows()
            self.numRows+=maxFetch
        else:
            self.beginResetModel()
            self.numRows = self._data.shape[0]
            self.endResetModel()

        remainderColumns=self._data.shape[1]-self.numColumns
        
        if maxFetch<remainderColumns:
            self.beginInsertColumns(QModelIndex(), self.numColumns, self.numColumns+maxFetch-1)
            self.endInsertColumns()
            self.numColumns+=maxFetch
        else:
            self.beginResetModel()
            self.numColumns = self._data.shape[1]
            self.endResetModel()
        

    def rowCount(self, parent):
        if self.numRows < self._data.shape[0]:
            return self.numRows
        return self._data.shape[0]
        

    def columnCount(self, parent):
        if self.numColumns < self._data.shape[1]:
            return self.numColumns
        return self._data.shape[1]
    
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                pass
                #for i in range(self._data.shape[1]):
                return str(list_name[section]).capitalize()+"\n"+str(self._data.columns[section])
                #return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                #print(type(self._data.index[section]),self._data.index[section])
                if isinstance(self._data.index[section], int):
                    return str(self._data.index[section]+1)
                
                return str(self._data.index[section])
            
class TableView (QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Data")
        self.data = data
        self.parent = parent

        self.view = QTableView(parent)
        self.update_data(data)
        
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)
        #self.view.setStyleSheet("QWidget {background:white}")

        self.layout.addWidget(self.view)
        #view.setVerticalScrollBar(widget)
        
        self.clipboard = QApplication.clipboard()
        self.selected_values = list()

        self.initUI()
    
    def initUI (self):
        
        layout1 = QHBoxLayout()
        self.layout.addLayout(layout1)
        text = BodyLabel('Data types:')
        text.setFixedWidth(100)
        layout1.addWidget(text)
        self.data_type = BodyLabel()
        layout1.addWidget(self.data_type)
        self.copy_btn = _PrimaryPushButton()
        self.copy_btn.setIcon(Icon(os.path.join('copy.png')))
        self.copy_btn.setText('Copy to clipboard')
        #self.copy_btn.setToolTip('Copy to clipboard')
        self.copy_btn.setToolTipDuration(2000)
        self.copy_btn.clicked.connect(self.copy_func)
        layout1.addWidget(self.copy_btn)

        layout4 = QHBoxLayout()
        #layout4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(layout4)
        text = BodyLabel('Data points:')
        text.setFixedWidth(100)
        layout4.addWidget(text)
        self.data_point = BodyLabel()
        layout4.addWidget(self.data_point)
        text = BodyLabel('Missing:')
        text.setFixedWidth(100)
        layout4.addWidget(text)
        self.missing = BodyLabel()
        layout4.addWidget(self.missing)
        text = BodyLabel('Distinct:')
        text.setFixedWidth(100)
        layout4.addWidget(text)
        self.distinct = BodyLabel()
        layout4.addWidget(self.distinct)
        text = BodyLabel('Unique:')
        text.setFixedWidth(100)
        layout4.addWidget(text)
        self.unique = BodyLabel()
        layout4.addWidget(self.unique)

    def on_selection (self):

        # selected cell values
        _selectedRows = self.view.selectionModel().selectedRows()
        _selectedColumns = self.view.selectionModel().selectedColumns()
        _selectedIndexes=self.view.selectionModel().selectedIndexes()
        
        # filter the selectedRows and selectedColumns so they do not overlap
        selectedAll = False
        selectedRows = list()
        for i in _selectedRows:
            selectedRows.append(i.row())
        selectedColumns = list()
        for i in _selectedColumns:
            selectedColumns.append(i.column())
        selectedIndexes = list()
        for i in _selectedIndexes:
            try:
                if not i.row() in selectedRows and not i.column() in selectedColumns:
                    selectedIndexes.append(i)
            except:pass
        
        # check if all cells are selected
        if len(selectedRows) == self.data.shape[0] or len(selectedColumns) == self.data.shape[1]:
            selectedAll = True
        
        _datapoints = 0
        _missing = 0
        self.selected_values = list()
        
        for i in selectedRows:
            _datapoints += self.data.iloc[i].shape[0]
            _missing += self.data.iloc[i].isna().sum()
            if self.data.shape[0]*self.data.shape[1] < 1000*20000:
                for j in self.data.iloc[i]:
                    self.selected_values.append(j)
        for i in selectedColumns:
            _datapoints += self.data.iloc[:,i].shape[0]
            _missing += self.data.iloc[:,i].isna().sum()
            if self.data.shape[0]*self.data.shape[1] < 1000*20000:
                for j in self.data.iloc[:,i]:
                    self.selected_values.append(j)
        for i in selectedIndexes:
            _datapoints += 1
            try: _missing += 1 if pd.isna(float(i.data())) else 0
            except:pass
            if self.data.shape[0]*self.data.shape[1] < 1000*20000:
                self.selected_values.append(i.data())
        
        if selectedAll:
            _datapoints = self.data.shape[0]*self.data.shape[1]
            _missing = pd.isnull(self.data).sum().sum()
        
        _unique_values = list()
        for i in self.selected_values:
            if i not in _unique_values:
                _unique_values.append(i)
            else:
                _unique_values.remove(i)

        string = list()
        for value in self.selected_values:
            value = str(value)
            if value.isdigit():
                string.append('int')
            elif value.replace('.','',1).isdigit():
                string.append("float")
            elif value.lower() in ['true','false']:
                string.append('boolean')
            elif value == 'nan':
                string.append('nan')
            else:
                string.append("string")
                
        data_type = ", ".join(list(set(string)))
        
        self.data_type.setText(data_type)
        self.unique.setText(str(len(_unique_values)))
        self.distinct.setText(str(np.unique(self.selected_values).shape[0]))
        self.data_point.setText(str(_datapoints))
        self.missing.setText(str(_missing))
       
    
    def copy_func (self):
        string = [str(i) for i in self.selected_values]
        self.clipboard.setText(', '.join(string))
    
    def update_data (self, data):
        self.data = data
        self.model = TableModel(data, self.parent)
        self.view.setModel(self.model)
        self.view.selectionModel().selectionChanged.connect(self.on_selection)
            
class ExploreView (QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.view = QTableView(parent)
        self.layout.addWidget(self.view)
        self.canvas = Canvas()
        self.canvas.fig.subplots_adjust(left=0.12,right=0.9,top=0.8,bottom=0.1)
        #self.canvas.axes.set_visible(False)
        self.canvas.axesx2.set_axis_off()
        self.canvas.axesy2.set_axis_off()
        self.layout.addWidget(self.canvas)
        self.update_data(data)

    def update_data (self, data:pd.DataFrame):
        
        if data.empty:
            describe = pd.DataFrame()
            self.canvas.axes.cla()
            self.canvas.axes.set_axis_off()
            self.canvas.draw()
        else:
            self.canvas.axes.cla()
            self.canvas.axes.set_axis_on()
            missingno.matrix(df=data,fontsize=6,ax=self.canvas.axes)
            self.canvas.draw()
            describe = data.describe()
        
        self.model = TableModel(describe, self.parent)
        self.view.setModel(self.model)
        
class DataView (QMainWindow):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Data")
        layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        self.setWindowIcon(QIcon(os.path.join("data-window.png")))
        
        self.tableview = TableView(data, parent)
        layout.addWidget(self.tableview)

        self.explore = ExploreView(data, parent)
        layout.addWidget(self.explore)
    
    def update_data (self, data):
        self.tableview.update_data(data)
        self.explore.update_data(data)

class DataSelection (QMainWindow):
    sig = pyqtSignal(str)
    def __init__(self, data, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Data")
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        self.setWindowIcon(QIcon(os.path.join("UI","Icons","data-window.png")))
        
        self.tableview = TableView(data, parent)
        layout.addWidget(self.tableview)
        self.tableview.copy_btn.setText('Insert to input field')
        self.tableview.copy_btn.pressed.connect(self.btn_pressed)

    def update_data (self, data):
        self.tableview.update_data(data)
    
    def btn_pressed (self):
        string = [str(i) for i in self.tableview.selected_values]
        self.sig.emit(", ".join(string))
