from PySide6.QtWidgets import QLabel, QTextBrowser
import logging

class BodyLabel (QLabel):
    """ """

class InfoLabel (QLabel):
   """ """

class TitleLabel (QLabel):
    """ """

class TextEditLogger(logging.Handler):
    def __init__(self, widget: QTextBrowser):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)