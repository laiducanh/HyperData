from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTableView, QFileDialog,
                               QApplication, QMainWindow, QDialog, QLabel)
from PySide6.QtGui import QIcon, QGuiApplication, QPixmap, QImage
from PySide6.QtCore import QModelIndex, Signal, Qt, QAbstractTableModel, QSortFilterProxyModel
import os, missingno
from time import gmtime, strftime
import pandas as pd
import numpy as np
from io import BytesIO
from rdkit import Chem
from rdkit.Chem import Draw
from config.settings import list_name, GLOBAL_DEBUG, logger
from ui.base_widgets.button import (HDropDownPushButton, PrimaryPushButton, HComboBox, HToggle, 
                                    ComboBox, TransparentPushButton, TransparentToolButton, 
                                    ToolButton, ToggleToolButton, CheckBox)
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.line_edit import SearchBox
from ui.base_widgets.menu import Menu, Action
from ui.base_widgets.window import Dialog, FileDialog
from ui.base_widgets.frame import Frame
from ui.utils import get_path
from plot.canvas import ExplorerCanvas
from data_processing.utlis import check_float, check_integer

DEBUG = False

class TableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._data = data.astype('object')
        self.arrays = self._data.to_numpy()
        self.numRows = 100
        self.numColumns = 100
   
    def data(self, index:QModelIndex, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return
        
        if index.row()>=self.numRows or index.row()<0 or index.column()>=self.numColumns or index.column()<0:
            return 
        
        value = self.arrays[index.row(), index.column()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            return value
            
        return 
      
    def canFetchMore(self, index:QModelIndex):

        if self.numRows<self._data.shape[0] or self.numColumns<self._data.shape[1]:
            return True
        return False
    
    def fetchMore(self, index:QModelIndex):

        maxFetch=20     #maximum number of rows/columns to grab at a time.
        
        remainderRows=self._data.shape[0]-self.numRows
        
        if maxFetch < remainderRows:
            self.beginInsertRows(QModelIndex(), self.numRows, self.numRows+maxFetch-1)
            self.numRows += maxFetch
            self.endInsertRows()
        else:
            self.beginResetModel()
            self.numRows = self._data.shape[0]
            self.endResetModel()

        remainderColumns=self._data.shape[1]-self.numColumns
        
        if maxFetch < remainderColumns:
            self.beginInsertColumns(QModelIndex(), self.numColumns, self.numColumns+maxFetch-1)
            self.numColumns += maxFetch
            self.endInsertColumns()
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
    
    def getArray(self) -> np.ndarray:
        return self.arrays
           
class TableView(QWidget):
    def __init__(self, data: pd.DataFrame, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Data")
        self.model = TableModel(data, parent)
        self.filter = QSortFilterProxyModel()
        self.filter.setFilterKeyColumn(-1) # filter all columns.
        self.filter.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.data = data
        
        self.clipboard = QApplication.clipboard()
        self.selected_values = list()

        self.initUI()
    
    def initUI(self):

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        frame = Frame()
        self.hlayout = QHBoxLayout(frame)
        self.vlayout.addWidget(frame)
        header = ToggleToolButton(icon='header.png')
        header.setToolTip('Toggle header')
        header.setChecked(True)
        header.toggled.connect(self.toggle_header)
        self.hlayout.addWidget(header)
        self.savedata = ToolButton(icon='save.png')
        self.savedata.setToolTip('Export data as csv')
        self.savedata.clicked.connect(self.save_data)
        self.hlayout.addWidget(self.savedata)
        self.search_box = SearchBox()
        self.search_box.setPlaceholderText('Search from data')
        self.search_box.textChanged.connect(lambda string: self.filter.setFilterFixedString(string))
        self.hlayout.addWidget(self.search_box)
        self.time_update = BodyLabel()
        self.hlayout.addWidget(self.time_update)

        self.view = QTableView(self.parent())
        self.update_data(self.data)
        self.vlayout.addWidget(self.view)
        
        layout1 = QHBoxLayout()
        self.vlayout.addLayout(layout1)
        text = BodyLabel('Data types:')
        text.setFixedWidth(100)
        layout1.addWidget(text)
        self.data_type = BodyLabel()
        layout1.addWidget(self.data_type)
        self.copy_btn = PrimaryPushButton()
        #self.copy_btn.setIcon(Icon(os.path.join('copy.png')))
        self.copy_btn.setText('Copy to clipboard')
        #self.copy_btn.setToolTip('Copy to clipboard')
        self.copy_btn.setToolTipDuration(2000)
        self.copy_btn.clicked.connect(self.copy_func)
        layout1.addWidget(self.copy_btn)

        layout4 = QHBoxLayout()
        #layout4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vlayout.addLayout(layout4)
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
     
        data = self.model.getArray()

        # selected cell values
        selectedIndexes=self.view.selectionModel().selectedIndexes()
        
        selectedAll = False
        # check if all cells are selected
        if len(selectedIndexes) == data.size: 
            selectedAll = True
        
        _datapoints = 0
        _missing = 0
        self.selected_values = np.array([])
        
        if selectedAll:
            _datapoints = data.size
            self.selected_values = data.copy()
        elif selectedIndexes:
            _datapoints = len(selectedIndexes)
            for i in selectedIndexes:
                self.selected_values = np.append(self.selected_values, i.data())
        
        self.selected_values = self.selected_values.astype(str)
        _values, _count = np.unique(self.selected_values, return_counts=True)
        _unique_values = _values[_count == 1]

        string = list()
        for value in self.selected_values.flatten():
            if value.lower() in ['true','false']:
                string.append('boolean')
            elif value == 'nan':
                string.append('nan')
            elif check_integer(value):
                string.append('int')
            elif check_float(value):
                string.append("float")
            else:
                string.append("string")

        _missing = string.count("nan")
        data_type = ", ".join(list(set(string)))
        
        self.data_type.setText(data_type)
        self.unique.setText(str(len(_unique_values)))
        self.distinct.setText(str(np.unique(self.selected_values).shape[0]))
        self.data_point.setText(str(_datapoints))
        self.missing.setText(str(_missing))
       
    def copy_func (self):
        string = [str(i) for i in self.selected_values]
        self.clipboard.setText(', '.join(string))
    
    def update_data (self, data: pd.DataFrame):
        self.data = data
        self.model = TableModel(data, self.parent())
        self.filter.setSourceModel(self.model)
        self.view.setModel(self.filter)
        self.view.selectionModel().selectionChanged.disconnect() # disconnect the previous connection
        self.view.selectionModel().selectionChanged.connect(self.on_selection)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.time_update.setText(f"Updated: {time}")
    
    def save_data(self):
        dialog = FileDialog(
            caption="Save as",
            directory='untitled.csv',
            filter="""Comma-separated values (*.csv);;Microsoft excel (*.xlsx)""",
            acceptMode=QFileDialog.AcceptMode.AcceptSave,
        )
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            ext = os.path.splitext(path)[1]
            if ext == ".xlsx":
                self.data.to_excel(path)
            elif ext == ".csv":
                self.data.to_csv(path)
            else:
                self.data.to_csv(f"{path}.csv")
    
    def toggle_header(self, checked:bool):
        self.view.horizontalHeader().setVisible(checked)
        self.view.verticalHeader().setVisible(checked)          
            
class ExploreView(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)

        self.univar_plot = ["histogram","boxplot","density","kde"]
        self.bivar_plot = ["line","scatter","bar","area","hexbin"]
        self.multivar_plot = ["heatmap","correlation","covariance"]
        self.nan_plot = ["NaNs matrix","NaNs bar"]

        self.grouplist = []
        
        self.initUI()
        self.initMenu()
        self.update_data(data)
    
    def initUI(self):
        self.vlayout = QVBoxLayout(self)
        self.describe_layout = QHBoxLayout()
        self.describe_layout.setContentsMargins(0,0,0,0)
        self.vlayout.addLayout(self.describe_layout)
        self.groupby = HToggle(label="Group by")
        self.groupby.button.checkedChanged.connect(self.update_describe)
        self.groupby.button.checkedChanged.connect(lambda c: self.groupby2.setEnabled(c))
        self.describe_layout.addWidget(self.groupby)
        self.groupby2 = TransparentPushButton()
        self.groupby2.setEnabled(False)
        self.groupby2.setText("Choose group" if not self.grouplist else str(self.grouplist))
        self.groupby2.pressed.connect(self.groupbyDialog)
        self.describe_layout.addWidget(self.groupby2)
        self.describe_layout.addStretch()
        self.view = QTableView(self.parent())
        self.vlayout.addWidget(self.view)
        self.plot_widget = QWidget()
        self.plot_selection = QHBoxLayout(self.plot_widget)
        self.plot_selection.setContentsMargins(0,0,0,0)
        self.plot_selection.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vlayout.addWidget(self.plot_widget)
        self.btn = HDropDownPushButton(label='Plot type', parent=self)
        self.btn.button.setFixedWidth(150)
        self.plot_selection.addWidget(self.btn)
        menu = self.initMenu()
        self.btn.button.setMenu(menu)
        self.btn.button.setText("NaNs matrix")
        self.varx = HComboBox(label="X")
        self.plot_selection.addWidget(self.varx)
        self.vary = HComboBox(label="Y")
        self.plot_selection.addWidget(self.vary)
        self.plot_btn = PrimaryPushButton(parent=self)
        self.plot_btn.setText("Apply")
        self.plot_btn.pressed.connect(self.update_plot)
        self.plot_selection.addWidget(self.plot_btn)
        self.canvas = ExplorerCanvas()
        self.vlayout.addWidget(self.canvas)
    
    def initMenu(self):
        menu = Menu(parent=self)
        menu_univar = Menu("Univariate analysis", self)
        for i in self.univar_plot:
            action = Action(text=i, parent=self)
            action.triggered.connect(lambda _, s=i: self.btn.button.setText(s))
            action.triggered.connect(self.update_selection)
            menu_univar.addAction(action)
        menu.addMenu(menu_univar)
        menu_bivar = Menu("Bivariate analysis", self)
        for i in self.bivar_plot:
            action = Action(text=i, parent=self)
            action.triggered.connect(lambda _, s=i: self.btn.button.setText(s))
            action.triggered.connect(self.update_selection)
            menu_bivar.addAction(action)
        menu.addMenu(menu_bivar)
        menu_multivar = Menu("Multivariate analysis", self)
        for i in self.multivar_plot:
            action = Action(text=i, parent=self)
            action.triggered.connect(lambda _, s=i: self.btn.button.setText(s))
            action.triggered.connect(self.update_selection)
            menu_multivar.addAction(action)
        menu.addMenu(menu_multivar)
        menu_nan = Menu("Missing values", self)
        for i in self.nan_plot:
            action = Action(text=i, parent=self)
            action.triggered.connect(lambda _, s=i: self.btn.button.setText(s))
            action.triggered.connect(self.update_selection)
            menu_nan.addAction(action)
        menu.addMenu(menu_nan)
        return menu

    def groupbyDialog(self):
        class GroupWidget(QWidget):
            def __init__(self, parent:Dialog, cols:list=[], group:str=None):
                super().__init__(parent)

                idx = parent.main_layout.count()-1
                parent.main_layout.insertWidget(idx, self)

                self.hlayout = QHBoxLayout(self)
                self.hlayout.setContentsMargins(0,0,0,0)

                self.col = ComboBox(parent=parent)
                self.col.addItems(cols)
                self.col.setCurrentText(group)
                self.hlayout.addWidget(self.col)

                delete = TransparentToolButton(parent=parent)
                delete.setIcon("delete.png")
                delete.pressed.connect(self.onDelete)
                self.hlayout.addWidget(delete)

            def onDelete(self):
                self.parent().main_layout.removeWidget(self)
                self.deleteLater()
                QApplication.processEvents()
                self.parent().adjustSize()

        def add(group=None):
            GroupWidget(dialog, self.data.columns, group)

        dialog = Dialog("Group by", self.parent())

        add_btn = TransparentPushButton(parent=self)
        add_btn.setIcon("add.png")
        add_btn.pressed.connect(add)
        dialog.main_layout.addWidget(add_btn)

        for group in self.grouplist:
            add(group)

        if dialog.exec():
            self.grouplist = []
            for widget in dialog.findChildren(GroupWidget):
                widget : GroupWidget
                self.grouplist.append(widget.col.currentText())
            self.groupby2.setText(str(self.grouplist))
            self.update_describe()

    def update_selection(self):
        try:
            # save current text for later
            _varx = self.varx.button.currentText()
            _vary = self.vary.button.currentText()

            # update x and y variables for plot
            self.varx.button.clear()
            self.vary.button.clear()

            plottype = self.btn.button.text()

            self.varx.button.addItems(self.data.columns)
            self.vary.button.addItems(self.data.columns)

            # set previous text if possible
            self.varx.button.setCurrentText(_varx)
            self.vary.button.setCurrentText(_vary)
            
            # self.varx.button.currentTextChanged.connect(self.update_plot)
            # self.vary.button.currentTextChanged.connect(self.update_plot)

            if plottype in self.univar_plot:
                self.varx.setVisible(True)
                self.vary.setVisible(False)
            elif plottype in self.bivar_plot:
                self.varx.setVisible(True)
                self.vary.setVisible(True)
            elif plottype in self.multivar_plot + self.nan_plot:
                self.varx.setVisible(False)
                self.vary.setVisible(False)
            
            #self.update_plot()
        except Exception as e:
            logger.exception(e)

    def update_data (self, data:pd.DataFrame):
        self.data = data
        self.update_describe()
        self.update_selection()
        self.update_plot()
    
    def update_describe(self):
        if self.data.empty:
            describe = pd.DataFrame()
        elif self.groupby.button.isChecked() and self.grouplist != []:
            describe = self.data.groupby(self.grouplist).describe()
        else:
            describe = self.data.describe()
        
        self.model = TableModel(describe, self.parent())
        self.view.setModel(self.model)
    
    def update_plot(self):
        try:
            plottype = self.btn.button.text()
            
            varx = self.varx.button.currentText()
            vary = self.vary.button.currentText()
            
            if self.data.empty:
                self.canvas.figure.clear()
            else:
                self.canvas.figure.clear()
                ax = self.canvas.figure.add_subplot()
                
                if plottype == "NaNs matrix": missingno.matrix(df=self.data,fontsize=10,sparkline=False,ax=ax)
                elif plottype == "NaNs bar": missingno.bar(df=self.data,fontsize=10,ax=ax)
                elif plottype == "histogram": self.data.hist(varx, ax=ax)
                elif plottype == "boxplot": self.data.boxplot(varx, ax=ax)
                elif plottype == "density": self.data[varx].plot.density(ax=ax)
                elif plottype == "kde": self.data[varx].plot.kde(ax=ax)
                elif plottype == "line": self.data.plot.line(varx, vary, ax=ax)
                elif plottype == "scatter": self.data.plot.scatter(varx, vary, ax=ax)
                elif plottype == "bar": self.data.plot.bar(varx, vary, ax=ax)
                elif plottype == "area": self.data.plot.area(varx, vary, ax=ax)
                elif plottype == "hexbin": self.data.plot.hexbin(varx, vary, ax=ax)
                elif plottype == "heatmap": ax.imshow(self.data.select_dtypes(include="number"), aspect="auto")
                elif plottype == "correlation": ax.imshow(self.data.corr(numeric_only=True), aspect="auto")
                elif plottype == "covariance": ax.imshow(self.data.cov(numeric_only=True), aspect="auto")
                
            #     xticks = []
            #     for ind, label in enumerate(ax.get_xticklabels()):
            #         # keep the maximum number of xticks = 10
            #         if ind % np.ceil(len(ax.get_xticklabels())/5):
            #             xticks.append("")
            #         else: xticks.append(label)
            #     ax.set_xticks(ax.get_xticks(), xticks)
            self.canvas.figure.tight_layout()
            self.canvas.draw_idle() 
            
        except Exception as e:
            logger.exception(e)

class MolTableView(TableView):
    selection_onChange = Signal(int)
    def __init__(self, data, parent=None):
        super().__init__(data, parent)

        self.view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
    
    def initUI(self):

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        frame = Frame()
        self.hlayout = QHBoxLayout(frame)
        self.vlayout.addWidget(frame)
        header = ToggleToolButton(icon='header.png')
        header.setToolTip('Toggle header')
        header.setChecked(True)
        header.toggled.connect(self.toggle_header)
        self.hlayout.addWidget(header)
        self.savedata = ToolButton(icon='save.png')
        self.savedata.setToolTip('Export data as csv')
        self.savedata.clicked.connect(self.save_data)
        self.hlayout.addWidget(self.savedata)
        self.search_box = SearchBox()
        self.search_box.setPlaceholderText('Search from data')
        self.search_box.textChanged.connect(lambda string: self.filter.setFilterFixedString(string))
        self.hlayout.addWidget(self.search_box)
        self.time_update = BodyLabel()
        self.hlayout.addWidget(self.time_update)

        self.view = QTableView(self.parent())
        self.update_data(self.data)
        self.vlayout.addWidget(self.view)
        
    def on_selection(self):
        selectedRow = self.view.selectionModel().selectedRows()[0]
        self.selection_onChange.emit(selectedRow.row())

class MolView(QWidget):
    def __init__(self, parent=None):
        ''' mols is a list of molecular representations '''
        super().__init__(parent=parent)

        self.mol = None # current visualized molecule
        self.initUI()
    
    def initUI(self):
        self.vlayout = QVBoxLayout(self)

        self.hlayout1 = QHBoxLayout()
        self.vlayout.addLayout(self.hlayout1)
        self.implicitHs = CheckBox(
            text='Implitcit hydrogens',
            setter=self.update_image,
            layout=self.hlayout1
        )
        self.stereo = CheckBox(
            text='Stereocenters',
            setter=self.update_image,
            layout=self.hlayout1
        )
        self.hlayout2 = QHBoxLayout()
        self.vlayout.addLayout(self.hlayout2)
        self.atIdx = CheckBox(
            text='Atom Indices',
            setter=self.update_image,
            layout=self.hlayout2
        )
        self.bondIdx = CheckBox(
            text='Bond Indices',
            setter=self.update_image,
            layout=self.hlayout2
        )
        
        self.image2D = QLabel()
        self.vlayout.addWidget(self.image2D)
    
    def _remove_nonpolarHs(self):
        ''' Remove nonpolar hydrogens '''
        remove_ids = []
        for atom in self.mol.GetAtoms():
            if atom.GetAtomicNum() == 1:
                neighbor = atom.GetNeighbors()[0]
                if neighbor.GetAtomicNum() == 6:
                    remove_ids.append(atom.GetIdx())
        editable = Chem.EditableMol(self.mol)
        for idx in sorted(remove_ids, reverse=True):
            editable.RemoveAtom(idx)
        mol = editable.GetMol()
        Chem.SanitizeMol(mol)
        return mol
            
    def update_image(self):
        pixmap = self.mol_to_image()
        self.image2D.setPixmap(pixmap)
        self.image2D.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image2D.setFixedSize(pixmap.size())
    
    def mol_to_image(self, size=(500,500)) -> QPixmap:
        try:
            drawop = Draw.MolDrawOptions()
            drawop.addAtomIndices=self.atIdx.isChecked()
            drawop.addBondIndices=self.bondIdx.isChecked()
            drawop.addStereoAnnotation=self.stereo.isChecked()
            mol = self.mol
            if not self.implicitHs.isChecked():
                mol = self._remove_nonpolarHs()
            pil_img = Draw.MolToImage(mol, size, bgcolor=(255,255,255), options=drawop)
            buffer = BytesIO()
            pil_img.save(buffer, format='PNG')
            buffer.seek(0)
            qmig = QImage.fromData(buffer.read(), 'PNG')
            pixmap = QPixmap.fromImage(qmig)

        except Exception as e:
            pixmap = QPixmap(*size)
            pixmap.fill(Qt.GlobalColor.white)

        return pixmap
    
    def update_mol(self, mol:Chem.Mol):
        self.mol = mol
        self.update_image()
        
class DataView(QMainWindow):
    def __init__(self, data, parent=None):
        super().__init__(parent)
    
        self.setWindowTitle("Data")
        self.setWindowIcon(QIcon(os.path.join(get_path(),"ui","icons","data-window.png")))
        # screen = QGuiApplication.primaryScreen().geometry().getRect()
        #self.setMinimumSize(int(screen[2]*0.5), int(screen[3]*0.5))

        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.setCentralWidget(widget)
        
        self.tableview = TableView(data, parent)
        layout.addWidget(self.tableview)

        self.explore = ExploreView(data, parent)
        layout.addWidget(self.explore)
    
    def update_data (self, data):
        self.tableview.update_data(data)
        self.explore.update_data(data)

class MolDataView(QMainWindow):
    def __init__(self, data, parent=None):
        super().__init__(parent)
    
        self.setWindowTitle("Data")
        self.setWindowIcon(QIcon(os.path.join(get_path(),"ui","icons","data-window.png")))
        self.data = data

        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.setCentralWidget(widget)
        
        self.tableview = MolTableView(data, parent)
        self.tableview.selection_onChange.connect(self.selection_onChange)
        layout.addWidget(self.tableview)

        self.explore = MolView(parent)
        layout.addWidget(self.explore)

        
    def update_data(self, data):
        self.data = data
        self.tableview.update_data(data)
    
    def selection_onChange(self, idx:int):
        self.explore.update_mol(self.data.iloc[idx,-1])

class DataSelection(QDialog):
    sig = Signal(str)
    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        
        self.setWindowTitle("Data")
        layout = QVBoxLayout(self)
        self.setWindowIcon(QIcon(os.path.join(get_path(),"ui","icons","data-window.png")))
        screen = QGuiApplication.primaryScreen().geometry().getRect()
        self.setMinimumSize(int(screen[2]*0.5), int(screen[3]*0.5))
        
        self.tableview = TableView(data, parent)
        layout.addWidget(self.tableview)
        self.tableview.copy_btn.setText('Insert to input field')
        self.tableview.copy_btn.pressed.connect(self.btn_pressed)

    def update_data (self, data):
        self.tableview.update_data(data)
    
    def btn_pressed (self):
        string = [str(i) for i in self.tableview.selected_values]
        self.sig.emit(", ".join(string))