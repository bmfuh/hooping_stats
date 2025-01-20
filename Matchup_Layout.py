""" The purpose of this file is to create a gui
focus on the first panel
change class color to information panel
offensive team selection is a drop down
all of the player selction are drop down but they go from left to right intsead of top to bottom like " offensive team player and defensive 
team player
all of the player selections should have a check box on the left hand side
large window in the middle should be a text box 
focus on getting all of the check boxes, dropdowns , text box and buttons in the right place.
"""
"""
testing """

#testing

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget,  QVBoxLayout, QHBoxLayout, QComboBox , QPushButton, QLabel,  QCheckBox, QLineEdit
from PySide6.QtGui import QPalette, QColor, Qt

class playerSelectionsSetup(QWidget):
     def __init__(self):
        super().__init__()

        checkbox = QCheckBox( self)

        self.playerSelection = QComboBox(self)
        self.playerSelection.setDisabled(True)
        self.playerSelection.addItem(" Player Selection ")


        self.layout = QHBoxLayout(self)
        self.layout.addWidget(checkbox)  # Add checkbox first (left side)
        self.layout.addWidget(self.playerSelection)  # Add dropdown second (right side)
        self.setLayout(self.layout)





        # self.layoutp = QVBoxLayout(self)
        # self.layoutp.addWidget(self.playerSelection)


    

        # checkbox = QCheckBox()
        # checkbox.setCheckState(Qt.CheckState.Checked)


        # checkbox.stateChanged.connect(self.show_state)




class informationPanel(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

        self.layout = QVBoxLayout(self)




        menu = QComboBox()
        menu.setDisabled(True)
        menu.addItem(" Offensive Team Selection ")
       

        self.layout.addWidget(QLabel(" Offensive Team Selection"))
        self.layout.addWidget(menu)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.layout.addStretch(1)

    def  addDropdown(self,additionalDropdown):
        self.layout.addWidget(QLabel(" Player Selection"))
        self.layout.addWidget(additionalDropdown)

          # Create a separate layout for Player Selections
        player_layout = QVBoxLayout()  # New layout for player selections
        for i in range(4):  # Adding 5 player selection dropdowns
            playerselectioninstance = playerSelectionsSetup()
            player_layout.addWidget(playerselectioninstance)

        self.layout.addLayout(player_layout) 


        menu2 = QComboBox()
        menu2.setDisabled(True)
        menu2.addItem(" Defensive Team Selection ")
       

        self.layout.addWidget(QLabel(" Defensive Team Selection"))
        self.layout.addWidget(menu2)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.layout.addStretch(1)


    def  addDropdown2(self,additionalDropdown):
        self.layout.addWidget(QLabel(" Player Selection"))
        self.layout.addWidget(additionalDropdown)

        player_layout2 = QVBoxLayout()
        for i in range(4):  # Adding 5 player selection dropdowns
            playerselectioninstance = playerSelectionsSetup()
            player_layout2.addWidget(playerselectioninstance)

        self.layout.addLayout(player_layout2) 


        switchButton = QPushButton(" Switch Sides ")
        self.layout.addWidget(switchButton)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

        self.textbox = QLineEdit()
        self.textbox.setFixedSize(200,100)
        self.layout.addWidget(self.textbox)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

        genButton = QPushButton(" Generate Information ")
        self.layout.addWidget(genButton)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

        





class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matchup Layout")

        playerselections = playerSelectionsSetup()
        infopanel = informationPanel("orange")
        

        infopanel.addDropdown(playerselections.playerSelection)


        infopanel.addDropdown2(playerselections.playerSelection)
        
       
        main_layout = QHBoxLayout()
        main_layout.addWidget(infopanel)



        # section1 = infopanel("orange")
        # section2 = informationPanel(" yellow")
        # section3 = informationPanel("brown")

       

        # main_layout.addWidget(section1)
        # # main_layout.addWidget(section2)
        # # main_layout.addWidget(section3)
        

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
#jkhkj
