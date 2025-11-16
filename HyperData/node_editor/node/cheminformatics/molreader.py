from rdkit import Chem
import os
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.base.node_graphics_content import NodeContentWidget
from data_processing.data_window import MolDataView
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine, VFrame
from ui.base_widgets.text import TitleLabel

DEBUG = False

class MolReader(NodeContentWidget):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.view = MolDataView(self.data_to_view, parent)
        self._config = {
            "source": None,
            "format": "SMILES",
            "addHs": True
        }

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.setMinimumSize(600, 200)
        dialog.main_layout.addWidget(TitleLabel("Molecule Reader"))
        dialog.main_layout.addWidget(SeparateHLine())
        fr = VFrame(dialog.main_layout)

        if self._config["source"] is None:
            self._config["source"] = self.node.input_sockets[0].socket_data.columns[0]
        source = HTransparentComboBox(
            items=list(self.node.input_sockets[0].socket_data.columns),
            label='Source',
            label2='Column to read molecules',
            getter=lambda: self._config["source"],
            layout=fr.vlayout
        )
        fmt = HTransparentComboBox(
            items=['SMILES','InChI','SMARTS','FASTA','HELM',
                   'SDF','PDB','MOL','MOL2','XYZ'],
            label="Format",
            getter=lambda: self._config["format"],
            layout=fr.vlayout
        )
        addHs = HToggle(
            label='Add hydrogens',
            label2='Only apply to string code, e.g., SMILES, InChI, Smarts, FASTA, HELM',
            getter=lambda: self._config["addHs"],
            layout=fr.vlayout
        )

        if dialog.exec(): 
            self._config["source"] = source.get_value()
            self._config["format"] = fmt.get_value()
            self._config["addHs"] = addHs.get_value()
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()
    
    def string_to_mol(self, string:str, fmt:str):
        if fmt == 'SMILES':
            mol = Chem.MolFromSmiles(str(string))
        elif fmt == 'InChI':
            mol = Chem.MolFromInchi(str(string))
        elif fmt == 'SMARTS':
            mol = Chem.MolFromSmarts(str(string))
        elif fmt == 'FASTA':
            mol = Chem.MolFromFASTA(str(string))
        elif fmt == 'HELM':
            mol = Chem.MolFromHELM(str(string))
        elif fmt == 'SDF':
            # read the first conformation in .sdf file
            mol = Chem.SDMolSupplier(os.path.abspath(string))[0]
        elif fmt == 'PDB':
            mol = Chem.MolFromPDBFile(os.path.abspath(string))
        elif fmt == 'MOL':
            mol = Chem.MolFromMolFile(os.path.abspath(string))
        elif fmt == 'MOL2':
            mol = Chem.MolFromMol2File(os.path.abspath(string))
        elif fmt == 'XYZ':
            mol = Chem.MolFromXYZFile(os.path.abspath(string))
        if fmt in ['SMILES','InChI','SMARTS','FASTA','HELM']:
            if self._config["addHs"] and mol is not None:
                mol = Chem.AddHs(mol, addCoords=True)
        return mol
    
    def func(self):
        try:
            data = self.node.input_sockets[0].socket_data.copy()
            if self._config["source"] is None:
                source = self.node.input_sockets[0].socket_data.columns[0]
            else:
                source = self._config["source"]
            fmt = self._config["format"]
            source = data[source]
            mols = []
            for string in source:
                mol = self.string_to_mol(string, fmt)
                if mol is None:
                    raise Exception(f'Cannot read {fmt} for input: {string}')
                mols.append(mol)
            data['_molread'] = mols
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: read molecules from DataFrame successfully.")

        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: fail, return an empty DataFrame.") 
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
        self.view.data = data.copy()        
    
    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data