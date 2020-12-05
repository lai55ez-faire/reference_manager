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
        languages = load(open("../static/languages.json", mode="r"))
        self.active_language = languages[languages["active_language"]]["main_window"]
        self.active_language_for_dialogs = languages[languages["active_language"]]["error_windowses"]

        try:
            self.references_list = load(open("../data/references.json", mode="r"))
        except FileNotFoundError:
            self.references_list = load(open("../data/references.json", mode="w"))
        except PermissionError:
            message_box = QMessageBox.question(self, self.active_language_for_dialogs\
                                               ["window_title"], self.active_language_for_dialogs\
                                               ["permission_error"], QMessageBox.Yes)

        super().__init__()
        self.initUI()

        print("Program launched!\n")

    def initUI(self):
        """Инициализация окна."""
        uic.loadUi("../ui_templates/main_window.ui", self)
        program_info = load(open("../static/program_info.json"))

        self.setFixedSize(500, 380)
        self.setStyleSheet(window)
        self.setWindowTitle(self.active_language["window_title"].format(program_info["program_name"]))

        self.referencesList.setStyleSheet(widget)
        self.update_references()

        self.deleteButton.setStyleSheet(button)
        self.deleteButton.setText(self.active_language["delete_button"])
        self.deleteButton.clicked.connect(self.delete_method)

        self.addButton.setStyleSheet(button)
        self.addButton.setText(self.active_language["add_button"])
        self.addButton.clicked.connect(self.add_method)

        self.openButton.setStyleSheet(button)
        self.openButton.setText(self.active_language["open_button"])
        self.openButton.clicked.connect(self.open_method)

        self.showInfoButton.setStyleSheet(button)
        self.showInfoButton.setText(self.active_language["show_program_info"])
        self.showInfoButton.clicked.connect(self.show_program_info)

        self.updateButton.setStyleSheet(button)
        self.updateButton.setText(self.active_language["update_button"])
        self.updateButton.clicked.connect(self.update_references)


    def update_references(self):
        self.references_list = load(open("../data/references.json", mode="r"))
        self.referencesList.clear()
        for reference_title in sorted(self.references_list.keys()):
            self.referencesList.addItem(f"{reference_title} ({self.references_list[reference_title]})")

    def delete_method(self):
        """Удаляет выбранные пользователем ссылки."""

        del self.references_list[sorted(self.references_list.keys())[self.referencesList.currentRow()]]

        open("../data/references.json", "w").write(dumps(self.references_list, sort_keys=True,
                                                             indent=2, separators=(",", ": ")))

        self.update_references()

    def add_method(self):
        """Открывает окно для добавления ссылки."""
        self.window = AddReference()
        self.window.show()

        self.window.closeEvent(self.update_references())

        print("A new reference added!")

    def open_method(self):
        """Открывает выбранные ссылки в браузере по умолчанию."""
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
