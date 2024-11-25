from flask import jsonify
from nba_api.stats.endpoints import playergamelog, playercareerstats
from nba_api.stats.static import players

import PostGameStatsUtil


def get_player_id(self):
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(self)
    return jsonify(int(player_id))

def get_player_stats(self):
    # Fetch the player game logs
    nba_player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
    nba_player_logs_df = nba_player_logs.get_data_frames()[0]

    nba_player_stat_columns = [
         "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "GAME_DATE", "MATCHUP", "MIN", "OREB", "PF",
        "PLUS_MINUS", "PTS", "REB", "STL", "TOV", "WL"
    ]

    return nba_player_logs_df[nba_player_stat_columns].to_dict()

def get_player_season_average(self):
    nba_player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
    nba_player_logs_df = nba_player_logs.get_data_frames()[0]

    # Define the columns you want to average
    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV"
    ]

    # Filter the DataFrame to only include these columns
    filtered_df = nba_player_logs_df[nba_player_stat_columns].mean().round(2).to_dict()
    return filtered_df

def get_player_career_stats(self):
    nba_players = players.get_players()
    nba_player_dict = [player for player in nba_players if player['full_name'] == self][0]
    return playercareerstats.PlayerCareerStats(player_id=nba_player_dict['id']).get_data_frames()[0].to_dict()

def get_player_playoff_stats(self, year):
    return playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self),
                                       season=year,
                                       season_type_all_star='Playoffs').get_data_frames()[0].to_dict()

def get_player_shot_chart_coordinates(self, year):
    return PostGameStatsUtil.PostGameStatsUtil.get_player_season_shot_chart(self, year)
