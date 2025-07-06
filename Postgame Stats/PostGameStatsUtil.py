import json
import sqlite3

import pandas as pd
from nba_api.stats.endpoints import leagueleaders, shotchartdetail, CommonAllPlayers
from nba_api.stats.static import players


class PostGameStatsUtil:
    def get_player_id(self):
        db_path = "/Users/stormyork/Documents/NBA Information.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Case-insensitive match
        cur.execute("""
            SELECT player_id
            FROM nba_players_2
            WHERE LOWER(full_name) = LOWER(?)
        """, (self,))

        result = cur.fetchone()
        conn.close()
        return str(result[0])


    def get_player_season_shot_chart(self, season):
        shot_chart_data = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=PostGameStatsUtil.get_player_id(self),
            context_measure_simple='FGA',
            season_nullable=season,
            season_type_all_star='Regular Season')

        player_shot_info_data = json.loads(shot_chart_data.get_json())
        player_shot_data = player_shot_info_data['resultSets'][0]

        # Get the headers and row data
        headers = player_shot_data['headers']
        rows = player_shot_data['rowSet']

        player_shot_chart = pd.DataFrame(rows)
        player_shot_chart.columns = headers
        return player_shot_chart[['LOC_X', 'LOC_Y']].to_dict()

    def get_wnba_player_id(self):
        wnba_players = CommonAllPlayers(
            is_only_current_season=1,  # 1 active, 0 not active
            league_id='10',  # nba 00, g_league 20, wnba 10
            season='2024-25'  # change year(s) if needed
        ).get_data_frames()[0]

        sorted_wnba_players = wnba_players['DISPLAY_FIRST_LAST']

        for player in sorted_wnba_players:
            if player == self:
                player_info = wnba_players[wnba_players['DISPLAY_FIRST_LAST'] == player]
                person_id = player_info['PERSON_ID'].iloc[0]
                return str(person_id)

    def get_gleague_player_id(self):
        gleague_players = CommonAllPlayers(
            is_only_current_season=1,  # 1 active, 0 not active
            league_id='20',  # nba 00, g_league 20, wnba 10
            season='2024-25'  # change year(s) if needed
        ).get_data_frames()[0]

        sorted_gleague_players = gleague_players['DISPLAY_FIRST_LAST']

        for player in sorted_gleague_players:
            if player == self:
                player_info = gleague_players[gleague_players['DISPLAY_FIRST_LAST'] == player]
                person_id = player_info['PERSON_ID'].iloc[0]
                return str(person_id)


def get_league_leaders(self):
    top_700 = leagueleaders.LeagueLeaders(season='2023-24', season_type_all_star='Regular Season',
                                          stat_category_abbreviation='PTS').get_data_frames()[0][:600]

    df_points_leaders = None
    df_rebounds_leaders = None
    df_blocks_leaders = None

    stats_columns = ["REB", "PTS", "STL", "BLK", "AST"]
    top_stats = {}

    # Loop through each stat, sort, and extract top 5 players
    for stat in stats_columns:
        # Sort by the current stat in descending order
        top_players = top_700.sort_values(by=stat, ascending=False).head(5)
        # Add the result to the dictionary
        top_stats[stat] = top_players[["PLAYER", stat]]  # Include player names and the stat

    df = pd.DataFrame([top_stats])
    return df.to_json(orient='records')
