from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic

from static.stylesheet_generator import *

from webbrowser import open_new_tab

from json import load, dumps
from sys import argv, exit

from adding_reference_window import AddReference
from info_window import InfoWindow


class MainWindow(QMainWindow):
    def __init__(self):
        languages = load(open("../static/languages.json", mode="r", encoding="utf-8"))
        settings_file = load(open("../data/settings.json", mode="r", encoding="utf-8"))

        self.active_language = languages[settings_file["active_language"]]["main_window"]
        self.active_language_for_dialogs = languages[settings_file["active_language"]]["error_windowses"]

        try:
            self.references_list = load(open("../data/references.json", mode="r", encoding="utf-8"))
        except FileNotFoundError:
            self.references_list = load(open("../data/references.json", mode="w", encoding="utf-8"))
        except PermissionError:
            message_box = QMessageBox.question(self, self.active_language_for_dialogs\
                                               ["window_title"], self.active_language_for_dialogs\
                                               ["permission_error"], QMessageBox.Yes)

        print("Program is launched!")
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("../ui_templates/main_window.ui", self)
        program_info = load(open("../static/program_info.json"))

        self.setFixedSize(500, 415)
        self.setStyleSheet(window)
        self.setWindowTitle(self.active_language["window_title"].format(program_info["program_name"]))

        self.referencesList.setStyleSheet(widget)
        self.update_references()

        self.initilise_button(self.deleteButton, "delete_button", self.delete_method)
        self.initilise_button(self.addButton, "add_button", self.add_method)
        self.initilise_button(self.openButton, "open_button", self.open_method)
        self.initilise_button(self.showInfoButton, "show_program_info", self.show_program_info)
        self.initilise_button(self.updateButton, "update_button", self.update_references)


    def initilise_button(self, object, key_in_language_file, function):
        object.setStyleSheet(button)
        object.setText(self.active_language[key_in_language_file])
        object.clicked.connect(function)

    def update_references(self):
        self.references_list = load(open("../data/references.json", mode="r", encoding="utf-8"))
        self.referencesList.clear()

        for reference_title in sorted(self.references_list.keys()):
            self.referencesList.addItem(f"{reference_title} ({self.references_list[reference_title]})")

        print("References list is updated.")

    def delete_method(self):
        del self.references_list[sorted(self.references_list.keys())[self.referencesList.currentRow()]]

        open("../data/references.json", "w", encoding="utf-8").\
            write(dumps(self.references_list, sort_keys=True,
                        indent=2, separators=(",", ": ")))

        self.update_references()

    def add_method(self):
        self.window = AddReference()
        self.window.show()



    def open_method(self):
        open_new_tab(self.references_list[sorted(self.references_list.keys())[self.referencesList.currentRow()]])

        print(f"\"{sorted(self.references_list.keys())[self.referencesList.currentRow()]}\" is opened!")

    def show_program_info(self):
        self.window = InfoWindow()
        self.window.show()


if __name__ == '__main__':
    app = QApplication(argv)
    program = MainWindow()
    program.show()
    exit(app.exec())
