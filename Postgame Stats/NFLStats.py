import nfl_data_py as nfl
import pandas as pd


class NFLPlayerStats:
    def get_nfl_player_stats(player_name, season, player_position):
        nfl_pbp_data = nfl.import_pbp_data([int(season)])
        nfl_player_stats = nfl_pbp_data[nfl_pbp_data[player_position] == player_name]
        filtered_nfl_player_stats = nfl_player_stats.groupby('passer').agg({
            'passing_yards': 'sum',
            'air_yards': 'sum',
            'yards_gained': 'sum',
            'qb_scramble': 'sum'
        }).reset_index()
        return filtered_nfl_player_stats.to_dict()


class NFLTeamStats:

    def get_nfl_team_stats(team_name, season):
        nfl_pbp_data = nfl.import_pbp_data([int(season)])
        nfl_home_team_stats = nfl_pbp_data[nfl_pbp_data['home_team'] == team_name]
        nfl_away_team_stats = nfl_pbp_data[nfl_pbp_data['away_team'] == team_name]
        nfl_team_season_stats = pd.concat([nfl_home_team_stats,nfl_away_team_stats])

        nfl_team_stat_columns = ['passing_yards', 'air_yards', 'yards_gained', 'qb_scramble']
        for column in nfl_team_stat_columns:
            nfl_team_season_stats[column] = pd.to_numeric(nfl_team_season_stats[column], errors='coerce')
        filtered_nfl_team_stats = nfl_team_season_stats[nfl_team_stat_columns].agg('sum').to_frame().T
        filtered_nfl_team_stats['team'] = team_name
        return filtered_nfl_team_stats.to_dict()
