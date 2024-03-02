import qfluentwidgets, os

class Icon (qfluentwidgets.FluentIconBase):
    def __init__ (self,fileName:str):
        super().__init__()
        self.fileName = fileName
    
    def path(self, theme=qfluentwidgets.Theme.AUTO):
        return os.path.join('UI','Icons',qfluentwidgets.getIconColor(theme),self.fileName)

class Action (qfluentwidgets.Action):
    """ """