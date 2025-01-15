""" The purpose of this file is to create a gui
"""
"""
testing """

#testing

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget,  QVBoxLayout, QHBoxLayout, QComboBox , QPushButton, QLabel
from PySide6.QtGui import QPalette, QColor


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

        self.layout = QVBoxLayout()


        menu = QComboBox()
        menu.addItem(" Player Selection ")
        menu.addItem(" Player Selection ")
        menu.addItem(" Player Selection ")
        menu.addItem(" Player Selection ")
        menu.addItem(" Player Selection ")

        self.layout.addWidget(QLabel(" Offensive Team Selection"))
        self.layout.addWidget(menu)

        self.layout.addStretch()

        self.setLayout(self.layout)
        self.layout.addStretch(1)

        menu2 = QComboBox()
        menu2.addItem(" Player Selection ")
        menu2.addItem(" Player Selection ")
        menu2.addItem(" Player Selection ")
        menu2.addItem(" Player Selection ")
        menu2.addItem(" Player Selection ")

        self.layout.addWidget(QLabel(" Defensive  Team Selection"))
        self.layout.addWidget(menu2)

        self.layout.addStretch(1)

        self.setLayout(self.layout)

        self.layout.addStretch(1)

        button = QPushButton(" Switch Sides ")
        self.layout.addWidget(button)

        self.layout.addStretch(1)

    



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matchup Layout")

        main_layout = QHBoxLayout()

        section1 = Color("orange")
        section2 = Color(" yellow")
        section3 = Color("brown")

        main_layout.addWidget(section1)
        main_layout.addWidget(section2)
        main_layout.addWidget(section3)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        


app = QApplication([])
window = MainWindow()
window.show()
app.exec()

