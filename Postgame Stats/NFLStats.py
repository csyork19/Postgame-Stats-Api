import sqlite3

import nfl_data_py as nfl
import pandas as pd


class NFLPlayerStats:
    def get_nfl_player_stats(player_name, season, player_position):
        nfl_pbp_data = nfl.import_pbp_data([int(season)])
        nfl_seasonal_data = nfl.import_seasonal_data([int(season)], "REG")
        # db_path = "/Users/stormyork/Documents/NFL Information.db"
        # conn = sqlite3.connect(db_path)
        # cur = conn.cursor()
        #
        # query = """
        #        SELECT
        #            MIN(fantasy_player_id) AS fantasy_player_id,
        #            SUM(passing_yards) AS total_passing_yards,
        #            SUM(air_yards) AS total_air_yards,
        #            SUM(rushing_yards) AS total_rushing_yards,
        #            SUM(receiving_yards) AS total_receiving_yards
        #        FROM NFL_2024_PBP
        #        WHERE id = (
        #            SELECT id
        #            FROM NFL_2024_PBP
        #            WHERE LOWER(fantasy_player_name) = LOWER(?)
        #              AND fantasy_player_name IS NOT NULL
        #              AND fantasy_player_name != ''
        #            ORDER BY id ASC
        #            LIMIT 1
        #        )
        #    """
        #
        # df = pd.read_sql_query(query, conn, params=(player_name))
        # conn.close()
        # # result = cur.fetchone()
        # # conn.close()
        # return df



        fantasy_map = {}
        # for row in nfl_pbp_data.items():
        #     fantasy_id = row['fantasy_player_id']
        #     fantasy_player = row['fantasy']
        #     if fantasy_id is not None and fantasy_player is not None:
        #         if not fantasy_map[fantasy_id]:
        #             fantasy_map[fantasy_id] = fantasy_player # B. Young

        nfl_players = nfl.import_players()
        nfl_players_name = nfl_players['display_name']
        name_map = {}

        for player in nfl_players_name.items():
            name = player[1]
            if name is not None:
                full_name = name
                abbr_name = None
                for index, row in nfl_players.iterrows():
                    short_name = row['short_name'] if pd.notna(row['short_name']) else None
                    display_name = row['display_name'] if pd.notna(row['display_name']) else None
                    if short_name is not None and display_name is not None and player_name == display_name:
                        nfl_player = short_name
                        abbr_name = nfl_player
                        full_name = display_name
                        break

                name_map[full_name] = abbr_name
                break

        nfl_seasonal_data = nfl.import_seasonal_data([int(season)], "REG")

        # Get player ID from PBP data
        nfl_player_id = None
        for _, row in nfl_pbp_data.iterrows():
            if row['fantasy_player_name'] == name_map.get(player_name):
                nfl_player_id = row['id']  # or 'id' if that’s the correct column
                break  # stop once found

        # Filter the seasonal data for this player
        if nfl_player_id:
            player_season_data = nfl_seasonal_data[nfl_seasonal_data['player_id'] == nfl_player_id]
        else:
            player_season_data = None
            print(f"Player ID not found for {player_name}")
        # nfl_player_stats = nfl_pbp_data[nfl_pbp_data['fantasy_player_name'] == name_map.get(player_name)]
        # nfl_player_id = nfl_pbp_data[nfl_pbp_data['id'] == name_map.get(player_name)]
        #
        # nfl_passer_player_id = nfl_pbp_data[nfl_pbp_data['passer_player_id']]
        # nfl_rusher_player_id = nfl_pbp_data[nfl_pbp_data['rusher_player_id']]
        # nfl_receiver_player_id = nfl_pbp_data[nfl_pbp_data['receiver_player_id']]
        #
        #
        # filtered_nfl_player_stats = nfl_player_stats.groupby(player_position).agg({
        #     'passing_yards': 'sum',
        #     'air_yards': 'sum',
        #     'yards_gained': 'sum',
        #     'qb_scramble': 'sum',
        #     'fantasy_player_id': 'first'
        # }).reset_index()
        # fantasy_player_id = filtered_nfl_player_stats['fantasy_player_id']
        #
        # return filtered_nfl_player_stats.to_dict()

        return player_season_data.to_dict()

    def get_nfl_player_receiving_stats(player_name, season, player_position):
        nfl_pbp_data = nfl.import_pbp_data([int(season)])
        nfl_receiving_player_stats = nfl_pbp_data[nfl_pbp_data[player_position] == player_name]
        filtered_nfl_player_stats = nfl_receiving_player_stats.groupby(player_position).agg({
            'receiving_yards': 'sum'}).reset_index()
        return filtered_nfl_player_stats.to_dict()

    def get_nfl_player_rushing_stats(player_name, season, player_position):
        nfl_pbp_data = nfl.import_pbp_data([int(season)])
        nfl_rushing_player_stats = nfl_pbp_data[nfl_pbp_data[player_position] == player_name]
        filtered_nfl_player_stats = nfl_rushing_player_stats.groupby(player_position).agg({
            'rushing_yards': 'sum'}).reset_index()
        return filtered_nfl_player_stats.to_dict()


class NFLTeamStats:

    def get_nfl_team_stats(team_name, season):
        nfl_pbp_data = nfl.import_pbp_data([int(season)])
        nfl_home_team_stats = nfl_pbp_data[nfl_pbp_data['home_team'] == team_name]
        nfl_away_team_stats = nfl_pbp_data[nfl_pbp_data['away_team'] == team_name]
        nfl_team_season_stats = pd.concat([nfl_home_team_stats, nfl_away_team_stats])

        nfl_team_stat_columns = ['passing_yards', 'air_yards', 'yards_gained', 'qb_scramble', 'shotgun', 'qb_dropback',
                                 'qb_scramble', 'air_yards', 'yards_after_catch']
        for column in nfl_team_stat_columns:
            nfl_team_season_stats[column] = pd.to_numeric(nfl_team_season_stats[column], errors='coerce')
        filtered_nfl_team_stats = nfl_team_season_stats[nfl_team_stat_columns].sum(skipna=True).to_frame().T
        filtered_nfl_team_stats['team'] = team_name
        return filtered_nfl_team_stats.to_dict()
