from flask import Flask, request
import NbaPlayerStats
import TeamStats
import ShotChartUtil
import PostGameStatsUtil
import ExceptionHandler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/nba/player/id', methods=['POST'])
def player_id():
    global player_name
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            return PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(f"Error retrieving NBA player id for {player_name}")
    else:
        return ExceptionHandler.PostGameStatsException("Please send a JSON request and try again.")


@app.route('/api/wnba/player/id', methods=['POST'])
def wnba_player_id():
    global player_name
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            return PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(player_name)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(f"Error retrieving WNBA player id for {player_name}")
    else:
        return ExceptionHandler.PostGameStatsException("Please send a JSON request and try again.")


@app.route('/api/wnba/player/seasonStats', methods=['POST'])
def wnba_player_season_stats():
    global player_name
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            return NbaPlayerStats.get_wnba_player_season_stats(player_name)
        except Exception as ex:
            app.logger.info('%s EXCEPTION OCCURRED RETRIEVING PLAYER STATS', ex)
            return ExceptionHandler.PostGameStatsException(f"Error retrieving NBA player id for {player_name}")
    else:
        return ExceptionHandler.PostGameStatsException("Please send a JSON request and try again.")


@app.route('/api/gleague/player/id', methods=['POST'])
def gleague_player_id():
    global player_name
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            return PostGameStatsUtil.PostGameStatsUtil.get_gleague_player_id(player_name)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(f"Error retrieving GLEAGUE player id for {player_name}")
    else:
        return ExceptionHandler.PostGameStatsException("Please send a JSON request and try again.")


@app.route('/api/gleague/player/seasonStats', methods=['POST'])
def gleague_player_season_stats():
    global player_name
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            return NbaPlayerStats.get_glegaue_player_season_stats(player_name)
        except Exception as ex:
            app.logger.info('%s EXCEPTION OCCURRED RETRIEVING PLAYER STATS', ex)
            return ExceptionHandler.PostGameStatsException(f"Error retrieving NBA player id for {player_name}")
    else:
        return ExceptionHandler.PostGameStatsException("Please send a JSON request and try again.")


@app.route('/api/nba/player/seasonStats', methods=['POST'])
def player_season_stats():
    global player_name
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            return NbaPlayerStats.get_player_stats(player_name)
        except Exception as ex:
            app.logger.info('%s EXCEPTION OCCURRED RETRIEVING PLAYER STATS', ex)
            return ExceptionHandler.PostGameStatsException(f"Error retrieving NBA player id for {player_name}")
    else:
        return ExceptionHandler.PostGameStatsException("Please send a JSON request and try again.")

@app.route('/api/nba/player/perSeasonStats', methods=['POST'])
def player_any_season_stats():
    global player_name
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            year = request.get_json()['season']
            return NbaPlayerStats.get_player_stats_per_season(player_name, year)
        except Exception as ex:
            app.logger.info('%s EXCEPTION OCCURRED RETRIEVING PLAYER STATS', ex)
            return ExceptionHandler.PostGameStatsException(f"Error retrieving NBA player id for {player_name}")
    else:
        return ExceptionHandler.PostGameStatsException("Please send a JSON request and try again.")


@app.route('/api/nba/player/perSeasonAverages', methods=['POST'])
def nba_player_season_averages():
    global player_name
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            year = request.get_json()['season']
            return NbaPlayerStats.get_player_stats(player_name, year)
        except Exception as ex:
            app.logger.info('%s EXCEPTION OCCURRED RETRIEVING PLAYER STATS', ex)
            return ExceptionHandler.PostGameStatsException(f"Error retrieving NBA player id for {player_name}")
    else:
        return ExceptionHandler.PostGameStatsException("Please send a JSON request and try again.")

@app.route('/api/nba/player/seasonAverages', methods=['POST'])
def player_season_average_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']

        try:
            return NbaPlayerStats.get_player_season_average(player_name)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player Season Averages for {player_name}")


@app.route('/api/nba/player/careerStats', methods=['POST'])
def player_career_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']

        try:
            return NbaPlayerStats.get_player_career_stats(player_name)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player Career Stats for {player_name}")


@app.route('/api/nba/player/playoffStats', methods=['POST'])
def player_playoff_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']

        try:
            return NbaPlayerStats.get_player_playoff_stats(player_name, season)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player Playoff Stats for {player_name} during the {season} season.")


@app.route('/api/nba/player/playoffStatsAverage', methods=['POST'])
def player_playoff_average_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']

        try:
            return NbaPlayerStats.get_player_playoff_stats(player_name, season)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player Playoff Stats Averages for {player_name} during the {season} season.")

@app.route('/api/nba/player/statsPerGame', methods=['POST'])
def player_stats_pers_stats():
    if request.is_json:
        game_id = request.get_json()['gameId']

        try:
              return NbaPlayerStats.get_player_stats_by_game(game_id)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player Career Stats for {player_name}")


@app.route('/api/nba/player/shotChartCoordinates', methods=['POST'])
def player_short_chart():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']

        try:
            return NbaPlayerStats.get_player_shot_chart_coordinates(player_name, season)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player Shot Chart Coordinates for {player_name} during the {season} season.")


@app.route('/api/nba/player/regularSeasonShotChart', methods=['POST'])
def player_regular_season_short_chart():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']

        try:
            ShotChartUtil.create_player_season_shot_chart_hexmap_heatmap(player_name, season)
            return "shot chart creation is successful"
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player Regular Season Shot Chart Coordinates for {player_name} during the {season} season.")

#
# @app.route('/api/nba/player/regularSeasonHeatmap', methods=['POST'])
# def player_regular_season_heat_map():
#     global player_name, season
#     if request.is_json:
#         try:
#             player_name = request.get_json()['playerName']
#             season = request.get_json()['season']
#             player_shot_chart_df, league_avg = ShotChartUtil.get_player_shotchartdetail(player_name, season)
#             image_file = ShotChartUtil.heatmap(player_shot_chart_df, player_name, season, title=str(player_name))
#             return image_file
#         except Exception as ex:
#             return ExceptionHandler.PostGameStatsException(
#                 f"Error retrieving NBA Player Regular Season Heatmao for {player_name} during the {season} season.")
#
#
@app.route('/api/nba/player/regularSeasonHexmap', methods=['POST'])
def player_regular_season_hex_map():
    global player_name, season
    if request.is_json:
        try:
            player_name = request.get_json()['playerName']
            season = request.get_json()['season']
            return ShotChartUtil.create_hexmap_per_season(player_name,season)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player Regular Season Hexmap for {player_name} during the {season} season.")


@app.route('/api/nba/player/leagueLeaders', methods=['POST'])
def player_league_leaders():
    if request.is_json:
        try:
            return PostGameStatsUtil.PostGameStatsUtil.get_league_leaders(request)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Player League Leaders during the {season} season.")


@app.route('/api/nba/team/seasonStats', methods=['POST'])
def team_season_stats():
    if request.is_json:
        try:
            data = request.get_json()
            team_name = data.get('teamName', '')
            season = request.get_json()['season']
            return TeamStats.get_team_season_stats(team_name, season)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Team Season Stats for {team_name} during the {season} season.")


@app.route('/api/nba/team/seasonAverages', methods=['POST'])
def team_season_average_stats():
    global team_name, season
    if request.is_json:
        try:
            data = request.get_json()
            team_name = data.get('teamName', '')
            season = request.get_json()['season']
            return TeamStats.get_team_season_stats(team_name, season)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Team Season Averages for {team_name} during the {season} season.")


@app.route('/api/nba/team/playoffStats', methods=['POST'])
def team_playoff_stats():
    if request.is_json:
        try:
            data = request.get_json()
            team_name = data.get('teamName', '')
            season = request.get_json()['season']
            return TeamStats.get_team_playoff_stats(team_name, season)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Team Playoff Stats for {team_name} during the {season} season.")


@app.route('/api/nba/team/playoffStatsAverage', methods=['POST'])
def team_playoff_average_stats():
    global team_name, season
    if request.is_json:
        try:
            data = request.get_json()
            team_name = data.get('teamName', '')
            season = request.get_json()['season']
            return TeamStats.get_team_playoff_stats(team_name, season)
        except Exception as ex:
            return ExceptionHandler.PostGameStatsException(
                f"Error retrieving NBA Team Playoff Stats Averages for {team_name} during the {season} season.")


if __name__ == '__main__':
    app.run()
