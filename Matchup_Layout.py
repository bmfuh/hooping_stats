""" The purpose of this file is to create a gui
"""


import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QPalette, QColor


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matchup Layout")

        
        layout = QHBoxLayout()

        layout.addWidget(Color('grey'))
        layout.addWidget(Color('grey'))
        layout.addWidget(Color('grey'))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)




app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

