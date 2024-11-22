from flask import jsonify
from nba_api.stats.endpoints import playergamelog, playercareerstats
from nba_api.stats.static import players

import PostGameStatsUtil


def get_player_id(self):
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(self)
    return jsonify(int(player_id))

def get_player_stats(self):
    if self:
        desired_columns = [
            "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
            "FTA", "FTM", "FT_PCT", "GAME_DATE", "MATCHUP", "MIN", "OREB", "PF",
            "PLUS_MINUS", "PTS", "REB", "STL", "TOV", "WL"
        ]

        # Fetch the player game logs
        player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
        player_logs_df = player_logs.get_data_frames()[0]

        # Filter the DataFrame to only include the desired columns
        filtered_player_logs_df = player_logs_df[desired_columns]

        # Return the filtered DataFrame as a dictionary
        return filtered_player_logs_df.to_dict()
    return None

def get_player_season_average(self):
    player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
    player_logs_df = player_logs.get_data_frames()[0]

    # Define the columns you want to average
    columns_to_average = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV"
    ]

    # Filter the DataFrame to only include these columns
    filtered_df = player_logs_df[columns_to_average]
    averages = filtered_df.mean()
    averages = averages.round(3)
    return averages.to_dict()


def get_player_career_stats(self):
    if self:
        # player dictionary
        nba_players = players.get_players()
        player_dict = [player for player in nba_players if player['full_name'] == self][0]

        # career df
        career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
        career_df = career.get_data_frames()[0]
        return career_df.to_dict();
        # player_career = playercareerstats.PlayerCareerStats(
        #     player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
        # player_career_df = player_career.get_data_frames()[0]
        # return player_career_df.to_dict()


def get_player_playoff_stats(self, year):
    if self:
        player_logs = playergamelog.PlayerGameLog(
            player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self),
            season=year,
            season_type_all_star='Playoffs')
        player_logs_df = player_logs.get_data_frames()[0]
        return player_logs_df.to_dict()


def get_player_shot_chart_coordinates(self, year):
    if self:
        return PostGameStatsUtil.PostGameStatsUtil.get_player_season_shot_chart(self, year)
