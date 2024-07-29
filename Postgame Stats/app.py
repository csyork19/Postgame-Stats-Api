from flask import Flask, request
from nba_api.stats.endpoints import PlayerGameLogs

import NbaPlayerStats
import TeamStats
import WnbaPlayerStats
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/nba/player/seasonStats', methods=['POST'])
def player_season_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_player_stats(player_name)


@app.route('/api/nba/player/careerStats', methods=['POST'])
def player_career_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_player_career_stats(player_name)


@app.route('/api/nba/player/playoffStats', methods=['POST'])
def player_playoff_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        return NbaPlayerStats.get_player_playoff_stats(player_name, season)


@app.route('/api/nba/player/shotChartCoordinates', methods=['POST'])
def player_short_chart():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        return NbaPlayerStats.get_player_shot_chart_coordinates(player_name, season)


@app.route('/api/nba/team/seasonStats', methods=['POST'])
def team_season_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_season_stats(team_name, season)
    # Be sure to include any advanced stats
    return "This is a test flask api setup!  :)"


@app.route('/api/nba/team/playoffStats', methods=['POST'])
def team_playoff_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_playoff_stats(team_name, season)


@app.route('/api/wnba/player/seasonStats', methods=['POST'])
def get_wnba_player_season_stats():
    if request.is_json:
        data = request.get_json()
        player_name = data.get('playerName')
        season = request.get_json('season')
        return WnbaPlayerStats.get_wnba_player_stats(player_name)

@app.route('/api/cbb/player/seasonStats', methods=['POST'])
def cbb_player_season_stats():
    player_game_logs = PlayerGameLogs(
        season_nullable='2022-23',  # change year(s) if needed
        season_type_nullable='Regular Season'  # Regular Season, Playoffs, Pre Season
    )
    return player_game_logs


@app.route('/api/cbb/player/careerStats')
def cbb_player_career_stats():
    if request.is_json:
        return "test"


@app.route('/api/cbb/player/conferenceTournamentStats')
def cbb_player_conf_tourn_stats():
    if request.is_json:
        return "test"


@app.route('/api/cbb/player/marchMadnessStats')
def cbb_player_march_madness_stats():
    if request.is_json:
        return "test"


if __name__ == '__main__':
    app.run()
