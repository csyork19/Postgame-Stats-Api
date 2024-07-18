from flask import Flask, request, jsonify
from nba_api.stats.endpoints import leagueleaders
import PlayerStats
import TeamStats
from flask_cors import CORS
from nba_api.stats.endpoints import TeamGameLogs
from nba_api.stats.static import teams

app = Flask(__name__)
CORS(app)


@app.route('/api/cbb/player/seasonStats', methods=['POST'])
def cbb_player_season_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return PlayerStats.get_cbb_player_stats(player_name)
        #return "test"


@app.route('/api/cbb/player/careerStats')
def cbb_player_career_stats():
    if request.is_json:
        return "test"


@app.route('/api/cbb/player/conferenceTournamentStats')
def cbb_player_conf_tourn_stats():
    if request.is_json:
        return "test"


@app.route('/api/cbb/player/marchMadnessStats')
def cbb_player_mrch_madnss_stats():
    if request.is_json:
        return "test"


@app.route('/api/player/seasonStats', methods=['POST'])
def player_season_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return PlayerStats.get_player_stats(player_name)


@app.route('/api/player/careerStats', methods=['POST'])
def player_career_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return PlayerStats.get_player_career_stats(player_name)


@app.route('/api/player/playoffStats', methods=['POST'])
def player_playoff_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        return PlayerStats.get_player_playoff_stats(player_name, season)


@app.route('/api/player/shotChartCoordinates', methods=['POST'])
def player_short_chart():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        return PlayerStats.get_player_shot_chart_coordinates(player_name, season)


@app.route('/api/team/seasonStats', methods=['POST'])
def team_season_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_season_stats(team_name, season)
    # Be sure to include any advanced stats
    return "This is a test flask api setup!  :)"


@app.route('/api/team/playoffStats', methods=['POST'])
def team_playoff_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_playoff_stats(team_name, season)


if __name__ == '__main__':
    app.run()
