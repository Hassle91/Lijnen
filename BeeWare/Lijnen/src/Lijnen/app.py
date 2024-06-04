"""
Program that calculated how to distribute medication over IV lines
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import lijnen

class Hessel(toga.App):
    def startup(self):
        
        main_box = toga.Box()

        lijnen.main_window()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return Hessel()
