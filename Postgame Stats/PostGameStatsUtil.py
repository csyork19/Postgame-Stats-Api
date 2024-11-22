import json
import pandas as pd
from flask import jsonify
from nba_api.stats.endpoints import leagueleaders, shotchartdetail, CommonAllPlayers


class PostGameStatsUtil:
    def get_player_id(self):
        top_700 = leagueleaders.LeagueLeaders(season='2023-24',season_type_all_star='Regular Season',
                                              stat_category_abbreviation='PTS').get_data_frames()[0][:600]

        # Correct column names for grouping
        avg_stats_columns = ['MIN']
        top_700_avg = top_700.groupby(['PLAYER', 'PLAYER_ID'])[avg_stats_columns].mean()

        df = top_700_avg.reset_index()[['PLAYER', 'PLAYER_ID']]
        # Find the player ID for the given player name
        player_df = df[['PLAYER', 'PLAYER_ID']]
        players_id = player_df[player_df['PLAYER'] == self]['PLAYER_ID'].iloc[0]
        return players_id

    def get_player_season_shot_chart(self, season):
        shot_json1 = shotchartdetail.ShotChartDetail(
            team_id=0,  # can input the id# but 0, will return all
            player_id=PostGameStatsUtil.get_player_id(self),  # can input the id# but 0, will return all
            context_measure_simple='FGA',  # also 'PTS' has ONLY makes
            season_nullable=season,
            season_type_all_star='Regular Season')  # can incldue (Pre Season, Playoffs, All Star)

        # Load data into a Python dictionary
        shot_data1 = json.loads(shot_json1.get_json())

        # Get the relevant data from our dictionary
        relevant_data1 = shot_data1['resultSets'][0]

        # Get the headers and row data
        headers = relevant_data1['headers']
        rows = relevant_data1['rowSet']

        # Create pandas DataFrame
        nba_shot_data1 = pd.DataFrame(rows)
        nba_shot_data1.columns = headers
        # Assuming nba_shot_data1 is a pandas DataFrame
        filtered_data = nba_shot_data1[['LOC_X', 'LOC_Y']].to_dict()
        return filtered_data


    def get_wnba_player_id(self):
        common_all_players = CommonAllPlayers(
            is_only_current_season=0,  # 1 active, 0 not active
            league_id='10',  # nba 00, g_league 20, wnba 10
            season='2023-24'  # change year(s) if needed
        )

        df_common_players = common_all_players.get_data_frames()[0]
        df_player_names = df_common_players['DISPLAY_FIRST_LAST']
        # Loop through the data frame of players and search for the requested player name
        player_id = ''
        for player in df_player_names:
            if player == self:
                player_info = df_common_players[df_common_players['DISPLAY_FIRST_LAST'] == player]
                person_id = player_info['PERSON_ID'].iloc[0]
                return person_id

    def get_gleague_player_id(self):
        common_all_players = CommonAllPlayers(
            is_only_current_season=0,  # 1 active, 0 not active
            league_id='20',  # nba 00, g_league 20, wnba 10
            season='2023-24'  # change year(s) if needed
        )

        df_common_players = common_all_players.get_data_frames()[0]
        df_player_names = df_common_players['DISPLAY_FIRST_LAST']

        top_700 = leagueleaders.LeagueLeaders(season='2023-24', season_type_all_star='Regular Season',
                                              stat_category_abbreviation='PTS', league_id='00').get_data_frames()[0][:600]
        # Loop through the data frame of players and search for the requested player name
        player_id = ''
        for player in df_player_names:
            if player == self:
                player_info = df_common_players[df_common_players['DISPLAY_FIRST_LAST'] == player]
                person_id = player_info['PERSON_ID'].iloc[0]
                return top_700.to_dict()


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

        # Display top players for each category
        # for stat, players in top_stats.items():
        #     print(f"Top 5 players for {stat}:")
        #     print(players)
        #     print()



