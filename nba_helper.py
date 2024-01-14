import sys
import pandas
# from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QDockWidget, QTextEdit, QApplication, QListWidget, QVBoxLayout, QGridLayout, \
    QLabel, QWidget, QLineEdit, QTableWidget, QPushButton, QTableWidgetItem
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import players
from functools import partial


def display_stats(df, table):
    headers = list(df)
    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])
    table.setHorizontalHeaderLabels(headers)

    # getting data from df is computationally costly so convert it to array first
    df_array = df.values
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            table.setItem(row, col, QTableWidgetItem(str(df_array[row, col])))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        dockWidget = QDockWidget('Dock', self)
        other_dock_widget = QDockWidget('Dock2', self)
        self.middle_dock_widget = QTableWidget()
        left_dock_widget = QWidget(self)
        left_widget_layout = QGridLayout()
        left_dock_widget.setLayout(left_widget_layout)
        # other_dock_widget.setWidget(QLabel("Player Name"))

        self.p1_name = QLineEdit()
        self.p2_name = QLineEdit()
        search_btn = QPushButton("Search")

        left_widget_layout.addWidget(QLabel("Player Name"), 0, 0)
        left_widget_layout.addWidget(QLabel("Opponent Name"), 1, 0)
        left_widget_layout.addWidget(self.p1_name, 0, 1)
        left_widget_layout.addWidget(self.p2_name, 1, 1)
        left_widget_layout.addWidget(search_btn, 2, 0)

        # left_widget_layout.addWidget(QLabel("Opponent Name"),1,0)
        other_dock_widget.setWidget(left_dock_widget)

        self.textEdit = QTextEdit()
        self.textEdit.setFontPointSize(16)

        self.listWidget = QListWidget()
        self.listWidget.addItem('Google')
        self.listWidget.addItem('Facebook')
        self.listWidget.addItem('Microsoft')
        self.listWidget.addItem('Apple')
        self.listWidget.itemDoubleClicked.connect(self.get_list_item)

        search_btn.pressed.connect(partial(self.update_table, self.p1_name, self.p2_name))
        dockWidget.setWidget(self.listWidget)
        dockWidget.setFloating(False)

        self.setCentralWidget(self.middle_dock_widget)


        self.addDockWidget(Qt.LeftDockWidgetArea, other_dock_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)
    def update_table(self,p1_name,p2_name):
        result_df = player_vs_player(p1_name.text(), p2_name.text())
        display_stats(result_df,self.middle_dock_widget)
    def get_list_item(self):
        self.textEdit.setPlainText(self.listWidget.currentItem().text())


def player_vs_player(p1_name, p2_name) -> pandas.DataFrame:
    p1_id = players.find_players_by_full_name(p1_name)[0]['id']
    p2_id = players.find_players_by_full_name(p2_name)[0]['id']
    p1_gamelog = pandas.concat(playergamelog.PlayerGameLog(player_id=p1_id, season=SeasonAll.all).get_data_frames())
    p2_gamelog = pandas.concat(playergamelog.PlayerGameLog(player_id=p2_id, season=SeasonAll.all).get_data_frames())
    players_gamelog = pandas.concat([p1_gamelog, p2_gamelog], axis=0)

    players_gamelog["GAME_DATE"] = pandas.to_datetime(players_gamelog["GAME_DATE"], format="%b %d, %Y")
    players_gamelog = players_gamelog.query("GAME_DATE.dt.year in [2020, 2021, 2022, 2023]")
    new_log = players_gamelog.sort_values("Game_ID", inplace=False)
    matchups = new_log[new_log["Game_ID"].duplicated(keep=False)]
    matchups = matchups.replace(p1_id, p1_name)
    matchups = matchups.replace(p2_id,p2_name)

    return matchups



def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


main()
