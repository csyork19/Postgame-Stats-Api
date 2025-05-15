from flask import Flask, request
import NbaPlayerStats
import TeamStats
import ShotChartUtil
import PostGameStatsUtil
from flask_cors import CORS
from descriptors.errors import handle_exceptions

app = Flask(__name__)
CORS(app)


@handle_exceptions
@app.route('/api/nba/player/id', methods=['POST'])
def player_id():
    global player_name
    if request.is_json:
        player_name = request.get_json()['playerName']
        return PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)


@handle_exceptions
@app.route('/api/wnba/player/id', methods=['POST'])
def wnba_player_id():
    global player_name
    if request.is_json:
        player_name = request.get_json()['playerName']
        return PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(player_name)


@handle_exceptions
@app.route('/api/wnba/player/seasonStats', methods=['POST'])
def wnba_player_season_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_wnba_player_season_stats(player_name)


@handle_exceptions
@app.route('/api/gleague/player/id', methods=['POST'])
def gleague_player_id():
    global player_name
    if request.is_json:
        player_name = request.get_json()['playerName']
        return PostGameStatsUtil.PostGameStatsUtil.get_gleague_player_id(player_name)


@handle_exceptions
@app.route('/api/gleague/player/seasonStats', methods=['POST'])
def gleague_player_season_stats():
    global player_name
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_glegaue_player_season_stats(player_name)


@handle_exceptions
@app.route('/api/nba/player/seasonStats', methods=['POST'])
def player_season_stats():
    global player_name
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_player_stats(player_name)


@handle_exceptions
@app.route('/api/nba/player/perSeasonStats', methods=['POST'])
def player_any_season_stats():
    global player_name
    if request.is_json:
        player_name = request.get_json()['playerName']
        year = request.get_json()['season']
        return NbaPlayerStats.get_player_stats_per_season(player_name, year)


@handle_exceptions
@app.route('/api/nba/player/perSeasonAverages', methods=['POST'])
def nba_player_season_averages():
    global player_name
    if request.is_json:
        player_name = request.get_json()['playerName']
        year = request.get_json()['season']
        return NbaPlayerStats.get_player_stats(player_name, year)


@handle_exceptions
@app.route('/api/nba/player/seasonAverages', methods=['POST'])
def player_season_average_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_player_season_average(player_name)


@handle_exceptions
@app.route('/api/nba/player/careerStats', methods=['POST'])
def player_career_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_player_career_stats(player_name)


@handle_exceptions
@app.route('/api/nba/player/playoffStats', methods=['POST'])
def player_playoff_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        return NbaPlayerStats.get_player_playoff_stats(player_name, season)


@handle_exceptions
@app.route('/api/nba/player/playoffStatsAverage', methods=['POST'])
def player_playoff_average_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        return NbaPlayerStats.get_player_playoff_stats(player_name, season)


@handle_exceptions
@app.route('/api/nba/player/statsPerGame', methods=['POST'])
def player_stats_pers_stats():
    if request.is_json:
        game_id = request.get_json()['gameId']
        return NbaPlayerStats.get_player_stats_by_game(game_id)


@handle_exceptions
@app.route('/api/nba/player/shotChartCoordinates', methods=['POST'])
def player_short_chart():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        return NbaPlayerStats.get_player_shot_chart_coordinates(player_name, season)


@handle_exceptions
@app.route('/api/nba/player/regularSeasonShotChart', methods=['POST'])
def player_regular_season_short_chart():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        ShotChartUtil.create_player_season_shot_chart_hexmap_heatmap(player_name, season)
        return "shot chart creation is successful"


@handle_exceptions
@app.route('/api/nba/player/regularSeasonHexmap', methods=['POST'])
def player_regular_season_hex_map():
    global player_name, season
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        return ShotChartUtil.create_hexmap_per_season(player_name, season)


@handle_exceptions
@app.route('/api/nba/player/leagueLeaders', methods=['POST'])
def player_league_leaders():
    if request.is_json:
        return PostGameStatsUtil.PostGameStatsUtil.get_league_leaders(request)


@handle_exceptions
@app.route('/api/nba/team/seasonStats', methods=['POST'])
def team_season_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_season_stats(team_name, season)


@handle_exceptions
@app.route('/api/nba/team/seasonAverages', methods=['POST'])
def team_season_average_stats():
    global team_name, season
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_season_stats(team_name, season)


@handle_exceptions
@app.route('/api/nba/team/playoffStats', methods=['POST'])
def team_playoff_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_playoff_stats(team_name, season)


@handle_exceptions
@app.route('/api/nba/team/playoffStatsAverage', methods=['POST'])
def team_playoff_average_stats():
    global team_name, season
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_playoff_stats(team_name, season)


if __name__ == '__main__':
    app.run()
