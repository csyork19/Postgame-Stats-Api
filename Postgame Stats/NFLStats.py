
import nfl_data_py as nfl
import pandas as pd
import sqlite3



class NFLPlayerStats:
    def get_nfl_player_stats(player_name, season, season_type):
        global nfl_seasonal_data
        conn = sqlite3.connect('/Users/stormyork/Documents/NFL Information.db')
        query = """
                SELECT short_name FROM nfl_players WHERE LOWER(display_name) = LOWER(?)
                AND display_name IS NOT NULL AND display_name != ''
                """
        cur = conn.cursor()
        cur.execute(query, (player_name,))
        result = cur.fetchone()
        conn.close()
        short_name = result[0] if result else None

        # nfl_season_data_2000 = nfl.import_seasonal_data(2000, 'REG')
        # nfl_season_data_2001 = nfl.import_seasonal_data(2001, 'REG')
        # nfl_season_data_2002 = nfl.import_seasonal_data(2002, 'REG')
        # nfl_season_data_2003 = nfl.import_seasonal_data(2003, 'REG')
        # nfl_season_data_2004 = nfl.import_seasonal_data(2004, 'REG')
        # nfl_season_data_2005 = nfl.import_seasonal_data(2005, 'REG')
        # nfl_season_data_2006 = nfl.import_seasonal_data(2006, 'REG')
        # nfl_season_data_2007 = nfl.import_seasonal_data(2007, 'REG')
        # nfl_season_data_2008 = nfl.import_seasonal_data(2008, 'REG')
        # nfl_season_data_2009 = nfl.import_seasonal_data(2009, 'REG')
        # nfl_season_data_2010 = nfl.import_seasonal_data(2010, 'REG')
        # nfl_season_data_2011 = nfl.import_seasonal_data(2011, 'REG')
        # nfl_season_data_2012 = nfl.import_seasonal_data(2012, 'REG')
        # nfl_season_data_2013 = nfl.import_seasonal_data(2013, 'REG')
        # nfl_season_data_2014 = nfl.import_seasonal_data(2014, 'REG')
        # nfl_season_data_2015 = nfl.import_seasonal_data(2015, 'REG')
        # nfl_season_data_2016 = nfl.import_seasonal_data(2016, 'REG')
        # nfl_season_data_2017 = nfl.import_seasonal_data(2017, 'REG')
        # nfl_season_data_2018 = nfl.import_seasonal_data(2018, 'REG')
        # nfl_season_data_2019 = nfl.import_seasonal_data(2019, 'REG')
        # nfl_season_data_2020 = nfl.import_seasonal_data(2020, 'REG')
        # nfl_season_data_2021 = nfl.import_seasonal_data(2021, 'REG')
        # nfl_season_data_2022 = nfl.import_seasonal_data(2022, 'REG')
        # nfl_season_data_2023 = nfl.import_seasonal_data(2023, 'REG')
        # nfl_season_data_2024 = nfl.import_seasonal_data(2024, 'REG')

        nfl_seasonal_data = nfl.import_pbp_data([int(season)])
        nfl_season_data_2015 = nfl.import_seasonal_data([int(2000)], 'REG')
        test = "hello"

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
            if season != '2024':
                nfl_seasonal_data = nfl.import_pbp_data([int(season)])
            else:
                nfl_seasonal_data = get_player_season_data_from_db(nfl_player_id, season)
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

    def get_nfl_pbp_team_stats(team_name, season):
        nfl_pbp_data = nfl.import_pbp_data([int(season)])
        nfl_home_team_stats = nfl_pbp_data[nfl_pbp_data['home_team'] == team_name]
        nfl_away_team_stats = nfl_pbp_data[nfl_pbp_data['away_team'] == team_name]
        nfl_team_season_stats = pd.concat([nfl_home_team_stats, nfl_away_team_stats])
        return nfl_team_season_stats.to_dict()

    def get_nfl_team_stats(self, season_type):
        years = self

        nfl_seasonal_data = nfl.import_seasonal_data(years if isinstance(years, (list, range)) else [years],
                                                     season_type)
        return nfl_seasonal_data.to_dict()



        # nfl_team_stat_columns = ['passing_yards', 'air_yards', 'yards_gained', 'qb_scramble', 'shotgun', 'qb_dropback',
        #                          'qb_scramble', 'air_yards', 'yards_after_catch']
        # for column in nfl_team_stat_columns:
        #     nfl_team_season_stats[column] = pd.to_numeric(nfl_team_season_stats[column], errors='coerce')
        # filtered_nfl_team_stats = nfl_team_season_stats[nfl_team_stat_columns].sum(skipna=True).to_frame().T
        # filtered_nfl_team_stats['team'] = team_name
        # return filtered_nfl_team_stats.to_dict()
