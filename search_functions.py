import pandas
from nba_api.stats.endpoints import playervsplayer, matchupsrollup, playergamelog, boxscorematchupsv3
from nba_api.stats.endpoints import playercareerstats
import typing
import nba_api.stats.static.players as player
import nba_api.stats.static.teams as team
from nba_api.stats.endpoints.boxscorematchupsv3 import BoxScoreMatchupsV3
# import nba_api.stats.endpoints.boxscorematchupsv3 as boxmatchup
from nba_api.stats.endpoints import playervsplayer, matchupsrollup, teamvsplayer
from nba_api.stats.library.parameters import SeasonAll, Season, SeasonType, PerModeSimple
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import playercompare
import pandas as pd


def get_player_id(player_name):
    player_id = None
    try:
        player_id = player.find_players_by_full_name(player_name)[0]['id']
    except:
        print("Couldn't find that player's ID")
    return player_id


def get_team_id(team_name):
    team_id = None

    try:
        team_id = team.find_teams_by_full_name(team_name)[0]['id']
    except:
        print("Couldn't find that team's ID")
    return team_id

def get_team_name_from_name(team_name):
    full_team_name = None

    try:
        full_team_name = team.find_teams_by_full_name(team_name)[0][team_name]
    except:
        print("Couldn't find that team's full name")
    return full_team_name
def get_team_name_from_id(team_id):
    team_name = None

    try:
        team_name = team.find_team_name_by_id(team_id)[0]["full_name"]
    except:
        print("Couldn't find that team's name")
    return team_name

def get_player_vs_player_game_ids(p1_id, p2_id, years: list, season=None):
    """

    :param years:
    :param p1_id: player 1's id
    :param p2_id: player 2's id
    :return: all the game ids that these two played against each other
    """
    p1_gamelog = pandas.concat(playergamelog.PlayerGameLog(player_id=p1_id, season=SeasonAll.all).get_data_frames())
    p2_gamelog = pandas.concat(playergamelog.PlayerGameLog(player_id=p2_id, season=SeasonAll.all).get_data_frames())
    players_gamelog = pandas.concat([p1_gamelog, p2_gamelog],
                                    axis=0)

    # TODO: query the players game log and return the games that they faced each other
    players_gamelog["GAME_DATE"] = pandas.to_datetime(players_gamelog["GAME_DATE"], format="%b %d, %Y")
    players_gamelog = players_gamelog.query(f"GAME_DATE.dt.year in {years}")
    new_log = players_gamelog.sort_values("Game_ID", inplace=False)

    # To find the games that they played each other in, use duplicated to identify which games they were both in.
    matchups = new_log[new_log["Game_ID"].duplicated(keep=False)]
    game_ids = matchups["Game_ID"].drop_duplicates()

    # TODO: Maybe I should return the game ids as a list or set
    return list(game_ids)


def get_player_vs_team_game_ids(p_id, team_abbreviation, season=None):
    gamelog = pandas.concat(playergamelog.PlayerGameLog(player_id=p_id,season=SeasonAll.all).get_data_frames())
    matchups = gamelog[gamelog["MATCHUP"].str.contains(team_abbreviation)]
    game_ids = matchups["Game_ID"]

    # print("Done")
    return list(game_ids)
    # gamelog = pandas.concat(teamvsplayer.TeamVsPlayer(vs_player_id=p_id, team_id=team_id).get_data_frames())

def get_player_offensive_performance_on_game_ids(p_id, game_id):

    matchups = pandas.concat(boxscorematchupsv3.BoxScoreMatchupsV3(game_id=game_id).get_data_frames())
    matchups = matchups[matchups["personIdOff"] == p_id]
    print("done")

def get_player_defensive_performance_on_game_ids(p_id, game_id):

    matchups = pandas.concat(boxscorematchupsv3.BoxScoreMatchupsV3(game_id=game_id).get_data_frames())
    matchups = matchups[matchups["personIdDef"] == p_id]

def player_vs_player(p1_id, p2_id):
    """0

    :param p1_id: player 1's id
    :param p2_id: player 2's id
    :return: dataset of the time's that player one has played against player two
    """
    pass


def main():
    p1_id = get_player_id("Lebron James")
    p2_id = get_player_id("Kevin Durant")
    team_id = get_team_id("Lakers")
    # team_name = Los_Anz
    # test = get_player_vs_player_game_ids(p1_id, p2_id, [2020,2021,2022,2023])
    test2 = get_player_vs_team_game_ids(p1_id,"TOR")
    test3 = get_player_offensive_performance_on_game_ids(p1_id, test2[0])
    print(test2)


main()
