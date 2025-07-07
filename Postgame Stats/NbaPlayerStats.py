import pandas as pd
from nba_api.stats.endpoints import playergamelog, playercareerstats, BoxScoreAdvancedV2
from nba_api.stats.static import players
from nba_api.stats.endpoints import BoxScoreTraditionalV2

import Const
import PostGameStatsUtil

global wnba_player_stats
global nba_player_season_average
wnba_player_stats = None
nba_player_season_average = None


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
    return boxscore_stats_df[Const.Constants.player_stats].to_dict(orient="records")


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
    filtered_df = combined_df[Const.Constants.get_advanced_player_stats]
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

    combined_df = pd.concat(list_of_player_advanced_stats, ignore_index=True)
    averages = combined_df[Const.Constants.fields_to_average].mean(numeric_only=True)
    return averages.to_dict()


def get_player_advanced_stats_by_game(player_name):
    box_score = BoxScoreTraditionalV2(player_name)
    box_score_stats_df = box_score.player_stats.get_data_frame()
    return box_score_stats_df[Const.Constants.advanced_stats_columns].to_dict(orient="records")


def get_player_stats(self):
    nba_player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
    nba_player_logs_df = nba_player_logs.get_data_frames()[0]
    return nba_player_logs_df[Const.Constants.nba_player_stat_columns].to_dict(orient="records")


def get_player_stats_per_season(self, year):
    nba_player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self),
                                                  season=year)
    nba_player_logs_df = nba_player_logs.get_data_frames()[0]
    return nba_player_logs_df[Const.Constants.nba_player_stat_columns].to_dict(orient="records")


def get_wnba_player_stats(self):
    wnba_nba_player_logs = (playergamelog.PlayerGameLog(
        player_id=PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(self)).get_data_frames())[0]
    wnba_player_stats = wnba_nba_player_logs[Const.Constants.wnba_player_stat_columns].to_dict(orient="records")
    return wnba_player_stats


def get_player_season_average(self):
    nba_player_logs = playergamelog.PlayerGameLog(player_id=PostGameStatsUtil.
                                                  PostGameStatsUtil.get_player_id(self)).get_data_frames()[0]
    if nba_player_logs.get_data_frames()[0] is None:
        raise Exception("test")
    nba_player_season_average = nba_player_logs[Const.Constants.nba_player_stat_avg_columns].mean().round(2).to_dict()
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
