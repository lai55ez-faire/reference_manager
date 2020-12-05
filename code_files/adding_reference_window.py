from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic

from static.stylesheet_generator import *
from json import load, dumps

from sys import argv, exit


class AddReference(QWidget):
    def __init__(self):
        languages = load(open("../data/static_data/languages.json", mode="r"))
        self.active_language = languages[languages["active_language"]]["adding_reference_window"]

        super().__init__()
        self.init_UI()

        try:
            self.references_list = load(open("../data/references.json", mode="r"))
        except FileNotFoundError:
            message_box = QMessageBox.question(self, self.active_language_for_dialogs\
                                               ["window_title"], self.active_language_for_dialogs\
                                               ["file_not_found_error"], QMessageBox.Yes)
        except PermissionError:
            message_box = QMessageBox.question(self, self.active_language_for_dialogs\
                                               ["window_title"], self.active_language_for_dialogs\
                                               ["permission_error"], QMessageBox.Yes)

    def init_UI(self):
        uic.loadUi("../ui_templates/adding_reference_window.ui", self)
        self.setFixedSize(285, 115)
        self.setStyleSheet(window)

        self.referenceName.setStyleSheet(widget)
        self.referenceURL.setStyleSheet(widget)

        self.addButton.setStyleSheet(button)
        self.addButton.setText(self.active_language["add_reference_button"])
        self.addButton.clicked.connect(self.add_button)

        self.exitButton.setStyleSheet(button)
        self.exitButton.setText(self.active_language["exit_button"])
        self.exitButton.clicked.connect(self.exit_button)

    def add_button(self):
        new_reference = (self.referenceName.text(), self.referenceURL.text())
        self.references_list[new_reference[0]] = new_reference[1]

        open("../data/references.json", "w").write(dumps(self.references_list, sort_keys=True,
                                                         indent=2, separators=(",", ": ")))

        print("A new reference added!")

        self.close()

    def exit_button(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(argv)
    program = AddReference()
    program.show()
    exit(app.exec())
