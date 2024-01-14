from nba_api.stats.endpoints import playercareerstats
import typing
import nba_api.stats.static.players as player
import nba_api.stats.static.teams as team
from nba_api.stats.endpoints import playervsplayer
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import playercompare
import pandas as pd

# career = playercareerstats.PlayerCareerStats()
m = player.find_players_by_full_name("lebron james")[0]
k = player.find_players_by_full_name("kevin durant")[0]
z = player.get_players()
l = team.find_teams_by_full_name("phoenix suns")[0]
p1_id = m['id']
p2_id = k['id']
team_id = l['id']
# print(m)
# print(z[0])

print(p1_id)
print(p2_id)

t = playervsplayer.PlayerVsPlayer(p1_id, p2_id)
# p1_games = playergamelogs.PlayerGameLogs(player_id_nullable=p1_id,date_from_nullable=None, date_to_nullable=None).player_game_logs.data
# p2_games = playergamelogs.PlayerGameLogs(player_id_nullable=p2_id,date_from_nullable="2020-05-20", date_to_nullable="2022-06-30").player_game_logs.data
# g = playercompare.PlayerCompare(p1_id,p2_id).data
# print(g)
# df1 = pd.DataFrame(data=p1_games['data'], columns=p1_games['headers'])
# df2 = pd.DataFrame(data=p2_games['data'], columns=p2_games['headers'])
# df2 = pd.DataFrame(p2_games)
# print(p1_games)
# print(p2_games)
print(t.headers)
# print(df1)
# print(df2)
