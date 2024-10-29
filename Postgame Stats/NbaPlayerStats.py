from nba_api.stats.endpoints import playergamelog, playercareerstats
import PostGameStatsUtil


def get_player_stats(self):
    if self:
        player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
        player_logs_df = player_logs.get_data_frames()[0]
        return player_logs_df.to_dict()
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
    return averages.to_dict()


def get_player_career_stats(self):
    if self:
        player_career = playercareerstats.PlayerCareerStats(
            player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
        player_career_df = player_career.get_data_frames()[0]
        return player_career_df.to_dict()


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
