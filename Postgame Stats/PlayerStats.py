from nba_api.stats.endpoints import leagueleaders, playergamelog, playercareerstats


class PlayerStats:

    def get_player_stats(player_name):
        return "test"

    def get_player_career_stats(player_name):
        return "test"


def get_player_stats(player_name):
    if player_name:
        # Process the extracted data (Here, we just echo it back)
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
        players_id = player_df[player_df['PLAYER'] == player_name]['PLAYER_ID'].iloc[0]

        player_logs = playergamelog.PlayerGameLog(player_id=players_id)
        player_logs_df = player_logs.get_data_frames()[0]
        return player_logs_df.to_dict()
    return None

def get_player_career_stats(player_name):
    if player_name:
        # Process the extracted data (Here, we just echo it back)
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
        players_id = player_df[player_df['PLAYER'] == player_name]['PLAYER_ID'].iloc[0]

        player_career = playercareerstats.PlayerCareerStats(player_id=players_id)
        player_career_df = player_career.get_data_frames()[0]
        # Extracting the seasons of player of choice
        seasons_played = player_career_df['SEASON_ID'].unique()
        return player_career_df.to_dict()

def get_player_playoff_stats(player_name):
    if player_name:
        # Process the extracted data (Here, we just echo it back)
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
        players_id = player_df[player_df['PLAYER'] == player_name]['PLAYER_ID'].iloc[0]

        player_logs = playergamelog.PlayerGameLog(player_id=players_id,season='2023-24',season_type_all_star='Playoffs')
        player_logs_df = player_logs.get_data_frames()[0]
        return player_logs_df.to_dict()
