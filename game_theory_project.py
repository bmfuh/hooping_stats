import sys
from functools import partial

import pandas
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QTableWidget, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QLabel, QTextEdit, QListWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QComboBox, QRadioButton, \
    QCheckBox, QTreeWidget, QTreeWidgetItem, QListWidgetItem
from nba_api.stats.endpoints import TeamDashLineups, playerdashboardbygamesplits
from nba_api.stats.library.parameters import Season, SeasonAll, SeasonTypePlayoffs, SeasonType
from nba_api.stats.endpoints import LeagueDashLineups
import nba_api.stats.static.players as player
import nba_api.stats.static.teams as team


def display_stats(df, table: QTableWidget):
    headers = list(df)
    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])
    table.setHorizontalHeaderLabels(headers)

    df_array = df.values
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            table.setItem(row, col, QTableWidgetItem(str(df_array[row, col])))


def display_stats_tree(df, tree: QTreeWidget):
    tree.setColumnCount(df.shape[1])
    tree.setHeaderLabels(list(df))
    tree.clear()
    for each_value in df.values:
        item = QTreeWidgetItem()
        for i in range(len(list(df))):
            item.setText(i, str(each_value[i]))
        tree.addTopLevelItem(item)
    tree.hideColumn(0)
    tree.hideColumn(1)


def all_team_options():
    all_teams = []
    for each_team in team.get_teams():
        all_teams.append(each_team['full_name'])

    return all_teams


def all_year_options(start_year, end_year):
    all_years = []
    for i in range(start_year, end_year):
        all_years.append(str(i) + "-" + str(i + 1)[2:])

    return all_years


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        left_dock_layout = QVBoxLayout()
        left_dock_widget = QWidget(self)

        right_dock_layout = QVBoxLayout()
        right_dock_widget = QWidget(self)

        left_dock_widget.setLayout(left_dock_layout)
        right_dock_widget.setLayout(right_dock_layout)

        left_dock = QDockWidget('Dock2', self)
        right_dock = QDockWidget('Dock', self)

        left_up_dock_layout = QHBoxLayout()
        left_dock_layout.addLayout(left_up_dock_layout)

        # Upper left of left dock
        left_up_left_dock_layout = QVBoxLayout()
        left_up_dock_layout.addLayout(left_up_left_dock_layout)

        # Team QLineEdit for left side
        left_up_left_team_layout = QHBoxLayout()
        left_up_left_dock_layout.addLayout(left_up_left_team_layout)  # holds team label and QLineEdit
        left_up_left_team_layout.addWidget(QLabel("Team"))
        # self.left_team_name = QLineEdit()
        # self.left_team_name.setPlaceholderText("Enter a team name")
        self.left_team_name = QComboBox()
        self.left_team_name.addItems(all_team_options())
        left_up_left_team_layout.addWidget(self.left_team_name)

        # Year and ComboBox for left side
        left_up_left_year_layout = QHBoxLayout()
        left_up_left_dock_layout.addLayout(left_up_left_year_layout)  # Holds the year and combobox
        left_up_left_year_layout.addWidget(QLabel("Year"))
        self.left_team_year = QComboBox()  # TODO: Populate combobox options
        self.left_team_year.addItems(all_year_options(2016, 2024))
        left_up_left_year_layout.addWidget(self.left_team_year)

        # Regular season & playoff check box (Left Side)
        left_up_left_choice_layout = QHBoxLayout()
        left_up_left_dock_layout.addLayout(left_up_left_choice_layout)  # Holds the choice of reg season vs playoffs
        self.left_up_left_reg_cb = QCheckBox("Regular Season")
        left_up_left_choice_layout.addWidget(self.left_up_left_reg_cb)
        self.left_up_left_playoff_cb = QCheckBox("PlayOffs")
        left_up_left_choice_layout.addWidget(self.left_up_left_playoff_cb)

        # Filter Button (left)
        self.left_up_left_filter_btn = QPushButton("Filter")
        left_up_left_dock_layout.addWidget(self.left_up_left_filter_btn)

        # QTree Widget to handle the results
        self.left_up_left_tree = QTreeWidget()
        left_up_left_dock_layout.addWidget(self.left_up_left_tree)

        self.left_up_left_filter_btn.pressed.connect(
            partial(self.filter_search_results, self.left_team_name.currentText, self.left_team_year.currentText,
                    self.left_up_left_reg_cb.isChecked, self.left_up_left_playoff_cb.isChecked, self.left_up_left_tree))

        # Upper right of right dock
        left_up_right_dock_layout = QVBoxLayout()
        left_up_dock_layout.addLayout(left_up_right_dock_layout)

        # Team QLineEdit for right side
        left_up_right_team_layout = QHBoxLayout()
        left_up_right_dock_layout.addLayout(left_up_right_team_layout)
        left_up_right_team_layout.addWidget(QLabel("Team"))
        # self.right_team_name = QLineEdit()
        # self.right_team_name.setPlaceholderText("Enter a team name")
        self.right_team_name = QComboBox()
        self.right_team_name.addItems(all_team_options())
        left_up_right_team_layout.addWidget(self.right_team_name)

        # Year and ComboBox for right side
        left_up_right_year_layout = QHBoxLayout()
        left_up_right_dock_layout.addLayout(left_up_right_year_layout)  # Holds the year and combobox
        left_up_right_year_layout.addWidget(QLabel("Year"))
        self.right_team_year = QComboBox()  # TODO: Populate combobox options
        self.right_team_year.addItems(all_year_options(2016, 2024))
        left_up_right_year_layout.addWidget(self.right_team_year)

        # Regular season & playoff check box (Right side)
        left_up_right_choice_layout = QHBoxLayout()
        left_up_right_dock_layout.addLayout(left_up_right_choice_layout)  # Holds the choice of reg season vs playoffs
        self.left_up_right_reg_cb = QCheckBox("Regular Season")
        left_up_right_choice_layout.addWidget(self.left_up_right_reg_cb)
        self.left_up_right_playoff_cb = QCheckBox("PlayOffs")
        left_up_right_choice_layout.addWidget(self.left_up_right_playoff_cb)

        # Filter Button (right)
        self.left_up_right_filter_btn = QPushButton("Filter")
        left_up_right_dock_layout.addWidget(self.left_up_right_filter_btn)

        # QTree Widget to handle the results
        self.left_up_right_tree = QTreeWidget()
        left_up_right_dock_layout.addWidget(self.left_up_right_tree)

        self.left_up_right_filter_btn.pressed.connect(
            partial(self.filter_search_results, self.right_team_name.currentText, self.right_team_year.currentText,
                    self.left_up_right_reg_cb.isChecked, self.left_up_right_playoff_cb.isChecked,
                    self.left_up_right_tree))

        # Here's the bottom half of the left dock
        left_bottom_dock_layout = QHBoxLayout()
        left_dock_layout.addLayout(left_bottom_dock_layout)

        # Bottom left of left dock
        left_bottom_left_dock_layout = QVBoxLayout()
        left_bottom_dock_layout.addLayout(left_bottom_left_dock_layout)

        left_bottom_left_dock_layout.addWidget(QLabel("Strategy 1"))  # Used to see widget area
        self.left_bottom_left_strategy_list = QListWidget()
        left_bottom_left_dock_layout.addWidget(self.left_bottom_left_strategy_list)  # TODO: Fill up list with headers

        self.load_strategies(self.left_bottom_left_strategy_list)

        # Bottom right of left dock
        lefT_bottom_right_dock_layout = QVBoxLayout()
        left_bottom_dock_layout.addLayout(lefT_bottom_right_dock_layout)
        lefT_bottom_right_dock_layout.addWidget(QLabel("Strategy 2"))  # Used to see widget area
        self.left_bottom_right_strategy_list = QListWidget()
        lefT_bottom_right_dock_layout.addWidget(self.left_bottom_right_strategy_list)  # TODO: Fill up list with headers

        self.load_strategies(self.left_bottom_right_strategy_list)

        # Bottom of the left dock
        self.calculate_results_pb = QPushButton("Calculate Results")
        left_dock_layout.addWidget(self.calculate_results_pb)

        # Top of the Right Dock
        right_dock_up_layout = QGridLayout()
        right_dock_layout.addLayout(right_dock_up_layout)

        self.team_one_label = QLabel("Team 1")
        self.team_two_label = QLabel("Team 2")
        self.strategy_one_label = QLabel("Strategy 1")
        self.strategy_one_label_copy = QLabel("Strategy 1")
        self.strategy_two_label = QLabel("Strategy 2")
        self.strategy_two_label_copy = QLabel("Strategy 1")

        self.s1_t1_t2 = QLabel("?")  # this would be the top left grid position
        self.s1_t1_s2_t2 = QLabel("?")  # this would be the bottom left grid position

        self.s2_t1_s1_t2 = QLabel("?")  # This would be the top right grid position
        self.s2_t1_t2 = QLabel("?")  # This would be the bottom right grid position

        right_dock_up_layout.addWidget(self.team_one_label, 0, 2)  # TODO: Get actual team 1 selected
        right_dock_up_layout.addWidget(self.team_two_label, 2, 0)  # TODO: Get actual team 2 selected

        right_dock_up_layout.addWidget(self.strategy_one_label, 1, 2)  # TODO: Get team 1 strat 1
        right_dock_up_layout.addWidget(self.strategy_two_label, 1, 3)  # TODO: Get team 1 strat 2

        right_dock_up_layout.addWidget(self.strategy_one_label_copy, 2, 1)  # TODO: Get team 2 strat 1
        right_dock_up_layout.addWidget(self.strategy_two_label_copy, 3, 1)  # TODO: Get team 2 strat 2

        right_dock_up_layout.addWidget(self.s1_t1_t2, 2, 2)  # Top Left
        right_dock_up_layout.addWidget(self.s2_t1_s1_t2, 2, 3)  # Top Right

        right_dock_up_layout.addWidget(self.s1_t1_s2_t2, 3, 2)  # Bottom Left
        right_dock_up_layout.addWidget(self.s2_t1_t2, 3, 3)  # Bottom Right

        right_dock_bottom_layout = QVBoxLayout()
        right_dock_layout.addLayout(right_dock_bottom_layout)

        self.summary_text = QTextEdit()
        right_dock_bottom_layout.addWidget(self.summary_text)

        stat_breakdown_label = QLabel("Statistical Breakdown")
        stat_breakdown_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        right_dock_bottom_layout.addWidget(stat_breakdown_label)
        right_dock_bottom_summary_layout = QHBoxLayout()
        right_dock_bottom_layout.addLayout(right_dock_bottom_summary_layout)

        right_dock_bottom_left_layout = QVBoxLayout()
        self.right_bottom_left_summary_tree = QTreeWidget()
        right_dock_bottom_left_layout.addWidget(
            self.right_bottom_left_summary_tree)  # Shows the players stat averages for that year

        right_dock_bottom_right_layout = QVBoxLayout()
        self.right_bottom_right_summary_tree = QTreeWidget()
        right_dock_bottom_right_layout.addWidget(
            self.right_bottom_right_summary_tree)  # Shows the players stat averages for that year

        right_dock_bottom_summary_layout.addLayout(right_dock_bottom_left_layout)
        right_dock_bottom_summary_layout.addLayout(right_dock_bottom_right_layout)

        right_dock.setWidget(right_dock_widget)
        left_dock.setWidget(left_dock_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, left_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, right_dock)

        self.calculate_results_pb.pressed.connect(self.calculate_results)
        # left_dock_layout.addWidget()

        # self.setCentralWidget(QTableWidget())
        # self.setLayout(left_dock_layout)

    def get_list_item(self):
        self.textEdit.setPlainText(self.listWidget.currentItem().text())

    def calculate_results(self):
        self.right_bottom_left_summary_tree.clear()
        self.right_bottom_right_summary_tree.clear()
        # When the calculate results button is pushed it should take the information from the left side
        # Then it should filter the stuff on the right side to show what's going on.

        self.team_one_label.setText(self.left_team_name.currentText())
        self.team_two_label.setText(self.right_team_name.currentText())

        if self.left_bottom_left_strategy_list.currentItem():
            self.strategy_one_label.setText(self.left_bottom_left_strategy_list.currentItem().text())
            self.strategy_one_label_copy.setText(self.left_bottom_left_strategy_list.currentItem().text())
        if self.left_bottom_right_strategy_list.currentItem():
            self.strategy_two_label.setText(self.left_bottom_right_strategy_list.currentItem().text())
            self.strategy_two_label_copy.setText(self.left_bottom_right_strategy_list.currentItem().text())
        # Strategy comparison headers will be the player one id, strategy name, player two id, then strategy name
        bottom_left_summary_headers = [self.team_one_label.text(), self.strategy_one_label.text(),
                                       self.team_two_label.text(), self.strategy_one_label.text()]
        bottom_right_summary_headers = [self.team_one_label.text(), self.strategy_two_label.text(),
                                        self.team_two_label.text(), self.strategy_two_label.text()]
        # Grab the top left tree and top right tree player_ids and split them into two lists
        if self.left_up_left_tree.currentItem() and self.left_up_right_tree.currentItem():
            team_one_player_ids = self.left_up_left_tree.currentItem().text(1)[1:-1].split("-")
            team_two_player_ids = self.left_up_right_tree.currentItem().text(1)[1:-1].split("-")

            team_one_strategy_one_result = 0
            team_one_strategy_two_result = 0
            team_two_strategy_one_result = 0
            team_two_strategy_two_result = 0

            for i in range(len(team_one_player_ids)):

                if self.left_up_left_reg_cb:
                    player_one = playerdashboardbygamesplits.PlayerDashboardByGameSplits(
                        player_id=team_one_player_ids[i],
                        season=self.left_team_year.currentText(),
                        season_type_playoffs=SeasonType.regular)

                    player_one_name = player.find_player_by_id(team_one_player_ids[i])['full_name']
                elif self.left_up_left_playoff_cb:
                    player_one = playerdashboardbygamesplits.PlayerDashboardByGameSplits(
                        player_id=team_one_player_ids[i],
                        season=self.left_team_year.currentText(),
                        season_type_playoffs=SeasonTypePlayoffs.playoffs)
                    player_one_name = player.find_player_by_id(team_one_player_ids[i])['full_name']

                if self.left_up_right_reg_cb:
                    player_two = playerdashboardbygamesplits.PlayerDashboardByGameSplits(
                        player_id=team_two_player_ids[i],
                        season=self.right_team_year.currentText(),
                        season_type_playoffs=SeasonType.regular)
                    player_two_name = player.find_player_by_id(team_two_player_ids[i])['full_name']

                elif self.left_up_right_playoff_cb:
                    player_two = playerdashboardbygamesplits.PlayerDashboardByGameSplits(
                        player_id=team_two_player_ids[i],
                        season=self.right_team_year.currentText(),
                        season_type_playoffs=SeasonTypePlayoffs.playoffs)
                    player_two_name = player.find_player_by_id(team_two_player_ids[i])['full_name']

                strategy_one_index = player_one.data_sets[0].data['headers'].index(self.strategy_one_label.text())
                strategy_two_index = player_two.data_sets[0].data['headers'].index(self.strategy_two_label.text())

                strategy_one_value_p1 = player_one.data_sets[0].data['data'][0][strategy_one_index]
                strategy_one_value_p2 = player_two.data_sets[0].data['data'][0][strategy_one_index]
                strategy_two_value_p1 = player_two.data_sets[0].data['data'][0][strategy_two_index]
                strategy_two_value_p2 = player_two.data_sets[0].data['data'][0][strategy_two_index]

                if strategy_one_value_p1 > strategy_one_value_p2:
                    # team_one gets a point for their strategy one result
                    team_one_strategy_one_result += 1
                elif strategy_one_value_p1 < strategy_one_value_p2:
                    # team two gets a point for their strategy one result
                    team_two_strategy_one_result += 1

                if strategy_two_value_p1 > strategy_two_value_p2:
                    # team one gets a point for their strategy two result
                    team_one_strategy_two_result += 1
                elif strategy_two_value_p1 < strategy_two_value_p2:
                    # Team two gets a point for their strategy two result
                    team_two_strategy_two_result += 1

                strategy_one_summary_item = QTreeWidgetItem(
                    [player_one_name, str(strategy_one_value_p1), player_two_name, str(strategy_one_value_p2)])
                strategy_two_summary_item = QTreeWidgetItem(
                    [player_one_name, str(strategy_two_value_p1), player_two_name, str(strategy_two_value_p2)])

                self.right_bottom_left_summary_tree.addTopLevelItem(strategy_one_summary_item)
                self.right_bottom_right_summary_tree.addTopLevelItem(strategy_two_summary_item)
            print()
            # Update the labels for the nash equilibria table
            self.s1_t1_t2.setText(f"{team_one_strategy_one_result} / {team_two_strategy_one_result}") # top left
            self.s2_t1_s1_t2.setText(f"{team_one_strategy_two_result} / {team_two_strategy_one_result}") # top right
            self.s1_t1_s2_t2.setText(f"{team_one_strategy_one_result} / {team_two_strategy_two_result}") # bottom left
            self.s2_t1_t2.setText(f"{team_one_strategy_two_result} / {team_two_strategy_two_result}") # bottom right

            # Finish the program by saying which should use which
            text = f""

            if team_one_strategy_one_result > team_two_strategy_one_result: # if the first result is greater than second result
                text += f"The {self.team_one_label.text()} should use this {self.strategy_one_label.text()} strategy against the {self.team_two_label.text()} {self.strategy_one_label.text()} strategy if they want to win\n"
            elif team_one_strategy_one_result < team_two_strategy_one_result:
                text += f"The {self.team_two_label.text()} should use this {self.strategy_one_label.text()} strategy the {self.team_one_label.text()} {self.strategy_one_label.text()} strategy if they want to win\n"
            else:
                text += f"Neither team had any advantage with this {self.strategy_one_label.text()} strategy...\n"

            if team_one_strategy_two_result > team_two_strategy_one_result:
                text += f"The {self.team_one_label.text()} should use this {self.strategy_two_label.text()} strategy against the {self.team_two_label.text()} {self.strategy_one_label.text()} strategy if they want to win\n"
            elif team_one_strategy_two_result < team_two_strategy_one_result:
                text += f"The {self.team_two_label.text()} should use this {self.strategy_one_label.text()} strategy against the {self.team_two_label.text()} {self.strategy_two_label.text()} strategy if they want to win\n"
            else:
                text += f"Neither team had any advantage with this {self.strategy_one_label.text()} vs {self.strategy_two_label.text()} strategy\n"

            if team_one_strategy_one_result > team_two_strategy_two_result:
                text += f"The {self.team_one_label.text()} should use this {self.strategy_one_label.text()} strategy against the {self.team_two_label.text()} {self.strategy_two_label.text()} strategy if they want to win\n"
            elif team_one_strategy_one_result < team_two_strategy_two_result:
                text += f"The {self.team_two_label.text()} should use this {self.strategy_two_label.text()} strategy against the {self.team_one_label.text()} {self.strategy_one_label.text()} strategy if they want to win\n"
            else:
                text += f"Neither team had any advantage with this {self.strategy_one_label.text()} vs {self.strategy_two_label.text()} strategy\n"

            if team_one_strategy_two_result < team_two_strategy_two_result: # if the second result is greater than the first result
                text += f"The {self.team_one_label.text()} should use this {self.strategy_two_label.text()} strategy against the {self.team_two_label.text()} {self.strategy_two_label.text()} strategy if they want to win\n"
            elif team_one_strategy_two_result < team_two_strategy_two_result:
                text += f"The {self.team_two_label.text()} should use this {self.strategy_two_label.text()} strategy against the {self.team_two_label.text()} {self.strategy_two_label.text()} strategy if they want to win\n"
            else:
                text += f"Neither team had any advantage with this {self.strategy_two_label.text()} strategy...\n"

            self.summary_text.setText("Based on the results: \n" + text)
        self.right_bottom_left_summary_tree.setHeaderLabels(bottom_left_summary_headers)

        self.right_bottom_right_summary_tree.setHeaderLabels(bottom_right_summary_headers)

        print()

    def filter_search_results(self, team_name, year, reg, playoff, tree: QTreeWidget):

        reg = reg()
        playoff = playoff()
        team_name = team_name()
        year = year()
        # Use the team, year, and regular season / playoff checkboxes to filter the tree results
        team_id = team.find_teams_by_full_name(team_name)[0]['id']
        if reg and playoff:
            lineups_per_year = TeamDashLineups(team_id=team_id, season=year)
        elif reg and not playoff:
            lineups_per_year = TeamDashLineups(team_id=team_id, season=year, season_type_all_star=SeasonType.regular)
        elif not reg and playoff:
            lineups_per_year = TeamDashLineups(team_id=team_id, season=year,
                                               season_type_all_star=SeasonTypePlayoffs.playoffs)
        else:
            return
        headers = TeamDashLineups(team_id=team_id).data_sets[-1].data['headers']
        lineups_per_year = lineups_per_year.data_sets[-1].data['data']
        df = pandas.DataFrame.from_dict(lineups_per_year)
        df.columns = headers
        # df = df.drop(columns=['GROUP_SET', 'GROUP_ID'], axis=1)
        display_stats_tree(df, tree)

    def load_strategies(self, strategy_list: QListWidget):
        strategy_list.addItems(HEADERS)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


# Needed to load strategies first then call to main()
team_id_temp = team.find_teams_by_full_name("phoenix suns")[0]['id']
HEADERS = TeamDashLineups(team_id=team_id_temp).data_sets[-1].data['headers']
HEADERS = HEADERS[3:]
main()
