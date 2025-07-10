import nfl_data_py as nfl


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

    def get_nfl_team_stats(self):
        return ""
