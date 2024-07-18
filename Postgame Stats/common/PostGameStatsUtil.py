from nba_api.stats.endpoints import leagueleaders


class PostGameStatsUtil:
    def get_player_id(player_name):
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
        return players_id
