
import nfl_data_py as nfl
import pandas as pd
import sqlite3



class NFLPlayerStats:
    def get_nfl_player_stats(player_name, season, player_position):
        nfl_players = nfl.import_players()
        nfl_players_name = nfl_players['display_name']
        name_map = {}

        def save_nfl_players_to_db(nfl_players, db_path='/Users/stormyork/Documents/NFL Information.db'):
            conn = sqlite3.connect(db_path)
            nfl_players.to_sql('nfl_players', conn, if_exists='replace', index=False)
            conn.close()

        save_nfl_players_to_db(nfl_players)
        #nfl_pbp_data = nfl.import_pbp_data([int(season)])

        # for player in nfl_players_name.items():
        #     name = player[1]
        #     if name is not None:
        #         full_name = name
        #         abbr_name = None
        #         for index, row in nfl_players.iterrows():
        #             short_name = row['short_name'] if pd.notna(row['short_name']) else None
        #             display_name = row['display_name'] if pd.notna(row['display_name']) else None
        #             if short_name is not None and display_name is not None and player_name == display_name:
        #                 nfl_player = short_name
        #                 abbr_name = nfl_player
        #                 full_name = display_name
        #                 break
        #
        #         name_map[full_name] = abbr_name
        #         break

        conn = sqlite3.connect('/Users/stormyork/Documents/NFL Information.db')
        query = """
               SELECT short_name
               FROM nfl_players
               WHERE LOWER(display_name) = LOWER(?)
                 AND display_name IS NOT NULL
                 AND display_name != ''
            """
        cur = conn.cursor()
        cur.execute(query, (player_name,))
        result = cur.fetchone()
        conn.close()
        short_name = result[0] if result else None


        # TODO: Add player name map to a DB
        # TODO: Add nfl season data to a DB
        # TODO: Query the information from the DB
        # nfl_seasonal_data = nfl.import_seasonal_data([int(season)], "REG")

        def get_player_season_data_from_db(nfl_player_id, season,
                                           db_path='/Users/stormyork/Documents/NFL Information.db'):
            conn = sqlite3.connect(db_path)
            query = """
                SELECT *
                FROM nfl_seasonal_data
                WHERE player_id = ?
                  AND season = ?
            """
            df = pd.read_sql_query(query, conn, params=(nfl_player_id, season))
            conn.close()
            return df.to_dict()



        # Get player ID from PBP data

        # Select player id from PBP where fantasy_player_name column equals a variable I provide


        mapped_name = short_name
        conn = sqlite3.connect('/Users/stormyork/Documents/NFL Information.db')
        query = """
            SELECT id
            FROM NFL_2024_PBP
            WHERE LOWER(fantasy_player_name) = LOWER(?)
              AND fantasy_player_name IS NOT NULL
              AND fantasy_player_name != ''
            ORDER BY id ASC
            LIMIT 1
        """
        cur = conn.cursor()
        cur.execute(query, (mapped_name,))
        result = cur.fetchone()
        conn.close()
        nfl_player_id = result[0] if result else None

        if nfl_player_id:
            nfl_seasonal_data = get_player_season_data_from_db(nfl_player_id, season)
            # player_season_data = nfl_seasonal_data[nfl_seasonal_data['player_id'] == nfl_player_id]
        else:
            player_season_data = None
            print(f"Player ID not found for {player_name}")
        return nfl_seasonal_data

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
