import os

from flask import Flask, request, jsonify, send_file, send_from_directory
import NbaPlayerStats
import TeamStats
import ShotChartUtil
import PostGameStatsUtil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/nba/player/id', methods=['POST'])
def player_id():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_player_id(player_name)

@app.route('/api/nba/player/seasonStats', methods=['POST'])
def player_season_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_player_stats(player_name)


@app.route('/api/gleague/player/seasonStats', methods=['POST'])
def gleague_player_season_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return jsonify(PostGameStatsUtil.PostGameStatsUtil.get_gleague_player_id(player_name))

@app.route('/api/nba/player/seasonAverages', methods=['POST'])
def player_season_average_stats():
    if request.is_json:
        player_name = request.get_json()['playerName']
        return NbaPlayerStats.get_player_season_average(player_name)


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

@app.route('/api/nba/player/playoffStatsAverage', methods=['POST'])
def player_playoff_average_stats():
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

@app.route('/api/nba/player/regularSeasonShotChart', methods=['POST'])
def player_regular_season_short_chart():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        player_shot_chart_df, league_avg = ShotChartUtil.get_player_shotchartdetail(player_name, season)
        image_file = ShotChartUtil.shot_chart(player_shot_chart_df,player_name, season, title=str(player_name))
        file_url = f"http://127.0.0.1:5000/shotcharts/{player_name}_{season}_stats.png"
        SHOTCHARTS_DIR = os.path.join(os.path.dirname(__file__), 'shotcharts')
        return send_from_directory(SHOTCHARTS_DIR, f"{player_name}_{season}_stats.png")


@app.route('/api/nba/player/regularSeasonHeatmap', methods=['POST'])
def player_regular_season_heat_map():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        player_shot_chart_df, league_avg = ShotChartUtil.get_player_shotchartdetail(player_name, season)
        image_file = ShotChartUtil.heatmap(player_shot_chart_df, player_name, season, title=str(player_name))
        return image_file

@app.route('/api/nba/player/regularSeasonHexmap', methods=['POST'])
def player_regular_season_hex_map():
    if request.is_json:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        player_shot_chart_df, league_avg = ShotChartUtil.get_player_shotchartdetail(player_name, season)
        image_file = ShotChartUtil.hexmap_chart(player_shot_chart_df, league_avg, player_name, season, title=str(player_name))
        file_url = f"http://127.0.0.1:5000/shotcharts/{player_name}_{season}_stats.png"
        SHOTCHARTS_DIR = os.path.join(os.path.dirname(__file__), 'shotcharts')
        return send_from_directory(SHOTCHARTS_DIR, f"{player_name}_{season}_hexmap_chart.png")

@app.route('/api/nba/player/leagueLeaders', methods=['POST'])
def player_league_leaders():
    if request.is_json:
        return PostGameStatsUtil.PostGameStatsUtil.get_league_leaders(request)
        # player_name = request.get_json()['playerName']
        # return NbaPlayerStats.get_player_id(player_name)


@app.route
def team_player_leaders():
    if request.is_json:
        return 1

@app.route('/api/nba/team/seasonStats', methods=['POST'])
def team_season_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_season_stats(team_name, season)

@app.route('/api/nba/team/seasonAverages', methods=['POST'])
def team_season_average_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_season_stats(team_name, season)



@app.route('/api/nba/team/playoffStats', methods=['POST'])
def team_playoff_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_playoff_stats(team_name, season)


@app.route('/api/nba/team/playoffStatsAverage', methods=['POST'])
def team_playoff_average_stats():
    if request.is_json:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = request.get_json()['season']
        return TeamStats.get_team_playoff_stats(team_name, season)

if __name__ == '__main__':
    app.run()
