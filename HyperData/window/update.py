import requests, time, sys, webbrowser
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import TitleLabel, BodyLabel
from config.settings import GLOBAL_DEBUG, logger, config

DEBUG = False

class UpdateDialog(Dialog):
    def __init__(self, title = "Update", parent=None):
        super().__init__(title, parent)
        self.new_update = False
        self.request()
    
    def request(self):
        try:
            data_requested = requests.get("https://app.box.com/index.php?rm=box_download_shared_file&shared_name=b3198y2bh6lgyxoyxk8trnjvvqd4p1wz&file_id=f_1261375080213").text
            self.newest_version = data_requested.splitlines()[0]
            self.download = data_requested.splitlines()[1]

            if self.newest_version != config["version"]: 
                self.new_update = True
                self.ok_btn.setText("Download")
                self.ok_btn.pressed.connect(self.download_update)
                self.main_layout.addWidget(TitleLabel('Update Available'))
                self.main_layout.addWidget(BodyLabel(f"There is an update available. Newest version: {self.newest_version}."))
            else:
                self.main_layout.addWidget(TitleLabel('Up To Date'))
                self.main_layout.addWidget(BodyLabel(f"There are no updates available. Newest version: {self.newest_version}."))
            
            self.main_layout.addWidget(BodyLabel(f"Last check: {time.ctime()}"))
        except Exception as e:
            logger.exception(e)

    def download_update(self):
        try:
            if sys.platform == 'win32':
                webbrowser.open_new_tab(self.download)
        except Exception as e:
            logger.exception(e)
