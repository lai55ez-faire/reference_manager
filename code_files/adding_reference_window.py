from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic

from static.stylesheet_generator import *
from json import load, dumps

from sys import argv, exit


class AddReference(QWidget):
    def __init__(self):
        languages = load(open("../static/languages.json", mode="r", encoding="utf-8"))
        settings_file = load(open("../data/settings.json", mode="r", encoding="utf-8"))

        self.active_language = languages[settings_file["active_language"]]["adding_reference_window"]

        super().__init__()
        self.init_UI()

        try:
            self.references_list = load(open("../data/references.json", mode="r", encoding="utf-8"))
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

        self.initilise_button(self.addButton, "add_reference_button", self.add_button)
        self.initilise_button(self.exitButton, "exit_button", self.exit_button)

    def initilise_button(self, object, key_in_language_file, function):
        object.setStyleSheet(button)
        object.setText(self.active_language[key_in_language_file])
        object.clicked.connect(function)

    def add_button(self):
        new_reference = (self.referenceName.text(), self.referenceURL.text())
        self.references_list[new_reference[0]] = new_reference[1]

        open("../data/references.json", "w", encoding="utf-8").write \
            (dumps(self.references_list, sort_keys=True,
                   indent=2, separators=(",", ": ")))

        print(f"\"{self.referenceName.text()}\" reference added!")

        self.close()

    def exit_button(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(argv)
    program = AddReference()
    program.show()
    exit(app.exec())
