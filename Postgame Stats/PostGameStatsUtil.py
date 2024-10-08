import json
import pandas as pd
from nba_api.stats.endpoints import leagueleaders, shotchartdetail, TeamGameLogs, CommonAllPlayers, LeagueLeaders



class PostGameStatsUtil:
    def get_player_id(self):
        top_500 = leagueleaders.LeagueLeaders(
            season='2023-24',
            season_type_all_star='Regular Season',
            stat_category_abbreviation='PTS'
        ).get_data_frames()[0][:600]

        # Correct column names for grouping
        avg_stats_columns = ['MIN']
        top_600_avg = top_500.groupby(['PLAYER', 'PLAYER_ID'])[avg_stats_columns].mean()

        df = top_600_avg.reset_index()[['PLAYER', 'PLAYER_ID']]
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
