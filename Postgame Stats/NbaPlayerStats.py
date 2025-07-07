import pandas as pd
from nba_api.stats.endpoints import playergamelog, playercareerstats, BoxScoreAdvancedV2
from nba_api.stats.static import players
from nba_api.stats.endpoints import BoxScoreTraditionalV2

import PostGameStatsUtil


def get_glegaue_player_season_stats(self):
    gleague_player_logs = playergamelog.PlayerGameLog(
        player_id=PostGameStatsUtil.PostGameStatsUtil.get_gleague_player_id(self))
    gleague_player_logs_df = gleague_player_logs.get_data_frames()[0]
    return gleague_player_logs_df.to_dict(orient="records")


def get_wnba_player_season_stats(self):
    wnba_player_logs = playergamelog.PlayerGameLog(
        player_id=PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(self),
        league_id_nullable='10'
    )

    wnba_player_logs_df = wnba_player_logs.get_data_frames()[0]
    return wnba_player_logs_df.to_dict(orient="records")


def get_player_stats_by_game(game_id):
    box_score = BoxScoreTraditionalV2(game_id=game_id)
    boxscore_stats_df = box_score.player_stats.get_data_frame()

    desired_columns = [
        "PLAYER_NAME", "TEAM_ABBREVIATION", "MIN", "PTS", "REB", "AST", "STL", "BLK", "TOV", "FGM", "FGA", "FG_PCT",
        "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "PLUS_MINUS"
    ]
    return boxscore_stats_df[desired_columns].to_dict(orient="records")


def get_player_advanced_stats_for_season(player_name, season, season_type):
    nba_player_logs = playergamelog.PlayerGameLog(
        player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name),
        season=season)
    nba_player_logs_df = nba_player_logs.get_data_frames()[0]
    list_of_player_advanced_stats = []
    advanced_player_stats_logs = nba_player_logs_df["Game_ID"].tolist()
    # Pull data for each game and extract the dataframe
    for game_id in advanced_player_stats_logs:
        response = BoxScoreAdvancedV2(game_id=game_id)
        df = response.get_data_frames()[0]
        player_df = df[df['PLAYER_NAME'] == player_name]
        if not player_df.empty:
            list_of_player_advanced_stats.append(player_df)

    # Combine all game stats into one dataframe
    combined_df = pd.concat(list_of_player_advanced_stats, ignore_index=True)
    desired_columns = [
        "GAME_ID",
        "TEAM_ID",
        "TEAM_ABBREVIATION",
        "TEAM_CITY",
        "PLAYER_ID",
        "PLAYER_NAME",
        "START_POSITION",
        "COMMENT",
        "MIN",
        "E_OFF_RATING",
        "OFF_RATING",
        "E_DEF_RATING",
        "DEF_RATING",
        "E_NET_RATING",
        "NET_RATING",
        "AST_PCT",
        "AST_TOV",
        "AST_RATIO",
        "OREB_PCT",
        "DREB_PCT",
        "REB_PCT",
        "TM_TOV_PCT",
        "EFG_PCT",
        "TS_PCT",
        "USG_PCT",
        "E_USG_PCT",
        "E_PACE",
        "PACE",
        "PACE_PER40",
        "POSS",
        "PIE"
    ]
    filtered_df = combined_df[desired_columns]
    return filtered_df.to_dict(orient="records")

def get_player_average_advanced_stats_for_season(player_name, season, season_type):
    nba_player_logs = playergamelog.PlayerGameLog(
        player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name),
        season=season)
    nba_player_logs_df = nba_player_logs.get_data_frames()[0]
    list_of_player_advanced_stats = []
    advanced_player_stats_logs = nba_player_logs_df["Game_ID"].tolist()
    # Pull data for each game and extract the dataframe
    for game_id in advanced_player_stats_logs:
        response = BoxScoreAdvancedV2(game_id=game_id)
        df = response.get_data_frames()[0]
        player_df = df[df['PLAYER_NAME'] == player_name]
        if not player_df.empty:
            list_of_player_advanced_stats.append(player_df)

    # Combine all game stats into one dataframe
    combined_df = pd.concat(list_of_player_advanced_stats, ignore_index=True)

    # Step 2: Define the list of columns to average
    fields_to_average = [
        "MIN",
        "E_OFF_RATING", "OFF_RATING",
        "E_DEF_RATING", "DEF_RATING",
        "E_NET_RATING", "NET_RATING",
        "AST_PCT", "AST_TOV", "AST_RATIO",
        "OREB_PCT", "DREB_PCT", "REB_PCT",
        "TM_TOV_PCT", "EFG_PCT", "TS_PCT",
        "USG_PCT", "E_USG_PCT",
        "E_PACE", "PACE", "PACE_PER40", "POSS"
    ]

    # Step 3: Calculate average of each column
    averages = combined_df[fields_to_average].mean(numeric_only=True)

    # Step 4: Convert to a dictionary (optional, for JSON or response)
    average_dict = averages.to_dict()

    return average_dict






def get_player_advanced_stats_by_game(player_name):
    box_score = BoxScoreTraditionalV2(player_name)
    boxscore_stats_df = box_score.player_stats.get_data_frame()

    desired_columns = [
        "PLAYER_NAME", "TEAM_ABBREVIATION", "MIN", "PTS", "REB", "AST", "STL", "BLK", "TOV", "FGM", "FGA", "FG_PCT",
        "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "PLUS_MINUS"
    ]
    return boxscore_stats_df[desired_columns].to_dict(orient="records")


def get_player_stats(self):
    nba_player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
    nba_player_logs_df = nba_player_logs.get_data_frames()[0]

    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "GAME_DATE", "MATCHUP", "MIN", "OREB", "PF",
        "PLUS_MINUS", "PTS", "REB", "STL", "TOV", "WL"
    ]

    return nba_player_logs_df[nba_player_stat_columns].to_dict(orient="records")


def get_player_stats_per_season(self, year):
    nba_player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self),
                                                  season=year)
    nba_player_logs_df = nba_player_logs.get_data_frames()[0]

    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "GAME_DATE", "MATCHUP", "MIN", "OREB", "PF",
        "PLUS_MINUS", "PTS", "REB", "STL", "TOV", "WL"
    ]

    return nba_player_logs_df[nba_player_stat_columns].to_dict(orient="records")


def get_wnba_player_stats(self):
    global wnba_player_stats
    wnba_player_stats = None

    wnba_nba_player_logs = (playergamelog.PlayerGameLog(
        player_id=PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(self)).get_data_frames())[0]

    wnba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "GAME_DATE", "MATCHUP", "MIN", "OREB", "PF",
        "PLUS_MINUS", "PTS", "REB", "STL", "TOV", "WL"
    ]

    wnba_player_stats = wnba_nba_player_logs[wnba_player_stat_columns].to_dict(orient="records")
    return wnba_player_stats


def get_player_season_average(self):
    global nba_player_season_average
    nba_player_season_average = None

    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV"]

    nba_player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.
                                                  PostGameStatsUtil.get_player_id(self)).get_data_frames()[0]

    if nba_player_logs.get_data_frames()[0] is None:
        raise Exception("test")

    nba_player_season_average = nba_player_logs[nba_player_stat_columns].mean().round(2).to_dict()
    return nba_player_season_average


def get_player_career_stats(self):
    nba_players = players.get_players()
    nba_player_dict = [player for player in nba_players if player['full_name'] == self][0]
    return playercareerstats.PlayerCareerStats(player_id=nba_player_dict['id']).get_data_frames()[0].to_dict(
        orient="records")


def get_player_playoff_stats(self, year):
    return playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self),
                                       season=year,
                                       season_type_all_star='Playoffs').get_data_frames()[0].to_dict()


def get_player_shot_chart_coordinates(self, year):
    return PostGameStatsUtil.PostGameStatsUtil.get_player_season_shot_chart(self, year)
