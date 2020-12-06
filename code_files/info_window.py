from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDialog, QInputDialog
from PyQt5 import uic

from static.stylesheet_generator import *
from json import load

from sys import argv, exit


class InfoWindow(QWidget):
    def __init__(self):
        languages = load(open("../static/languages.json", mode="r"))
        settings_file = load(open("../data/settings.json", mode="r"))

        self.active_language = languages[settings_file["active_language"]]["info_window"]

        super().__init__()
        self.init_UI()

    def init_UI(self):
        uic.loadUi("../ui_templates/info_window.ui", self)
        self.setFixedSize(400, 316)
        self.setStyleSheet(window)

        program_info = load(open("../static/program_info.json", mode="r"))

        self.info.setStyleSheet(widget)
        self.info.setText(self.active_language["text"].format(program_info["program_name"], \
        program_info["version"], program_info["author"]))

        self.okButton.setStyleSheet(button)
        self.okButton.setText(self.active_language["ok_button"])
        self.okButton.clicked.connect(self.ok_button)

    def ok_button(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(argv)
    program = InfoWindow()
    program.show()
    exit(app.exec())
