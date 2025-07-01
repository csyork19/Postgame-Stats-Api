from flask import Flask, request
import NbaPlayerStats
import TeamStats
import ShotChartUtil
import PostGameStatsUtil
from flask_cors import CORS
from descriptors.errors import handle_exceptions, require_json

app = Flask(__name__)
CORS(app)


@require_json
@handle_exceptions
@app.route('/api/nba/player/id', methods=['POST'])
def get_player_id():
    player_name = request.get_json()['playerName']
    return PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)


@require_json
@handle_exceptions
@app.route('/api/nba/player/seasonStats', methods=['POST'])
def get_player_season_stats():
    player_name = request.get_json()['playerName']
    return NbaPlayerStats.get_player_stats(player_name)


@require_json
@handle_exceptions
@app.route('/api/nba/player/perSeasonStats', methods=['POST'])
def get_player_any_season_stats():
    player_name = request.get_json()['playerName']
    year = request.get_json()['season']
    return NbaPlayerStats.get_player_stats_per_season(player_name, year)


@require_json
@handle_exceptions
@app.route('/api/nba/player/perSeasonAverages', methods=['POST'])
def get_nba_player_season_averages():
    player_name = request.get_json()['playerName']
    year = request.get_json()['season']
    return NbaPlayerStats.get_player_stats_per_season(player_name, year)


@require_json
@handle_exceptions
@app.route('/api/nba/player/careerStats', methods=['POST'])
def get_player_career_stats():
    player_name = request.get_json()['playerName']
    return NbaPlayerStats.get_player_career_stats(player_name)


@require_json
@handle_exceptions
@app.route('/api/nba/player/playoffStats', methods=['POST'])
def get_player_playoff_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    return NbaPlayerStats.get_player_playoff_stats(player_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/player/statsPerGame', methods=['POST'])
def get_player_stats_per_game():
    game_id = request.get_json()['gameId']
    return NbaPlayerStats.get_player_stats_by_game(game_id)


@require_json
@handle_exceptions
@app.route('/api/nba/player/shotChartCoordinates', methods=['POST'])
def get_player_short_chart_coordinates():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    return NbaPlayerStats.get_player_shot_chart_coordinates(player_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/player/hexmap', methods=['POST'])
def create_player_hexmap():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    return ShotChartUtil.create_updated_player_regular_season_hexmap_shot_chart(player_name, season, season_type,
                                                                                game_id)

@require_json
@handle_exceptions
@app.route('/api/nba/player/heatmap', methods=['POST'])
def create_player_heatmap():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    return ShotChartUtil.create_player_heatmap(player_name, season, season_type, game_id)


@require_json
@handle_exceptions
@app.route('/api/nba/team/heatmap', methods=['POST'])
def create_team_heatmap():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    return ShotChartUtil.create_team_heatmap(team_name, season, season_type, game_id)


@require_json
@handle_exceptions
@app.route('/api/nba/team/hexmap', methods=['POST'])
def create_team_hexmap():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    return ShotChartUtil.create_team_hexmap_per_season(team_name, season, season_type, game_id)


@require_json
@handle_exceptions
@app.route('/api/nba/team/seasonStats', methods=['POST'])
def get_team_season_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    return TeamStats.get_team_season_stats(team_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/team/seasonAverages', methods=['POST'])
def get_team_season_average_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    return TeamStats.get_team_season_stats(team_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/team/playoffStats', methods=['POST'])
def get_team_playoff_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    return TeamStats.get_team_playoff_stats(team_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/team/playoffStatsAverage', methods=['POST'])
def get_team_playoff_average_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    return TeamStats.get_team_playoff_stats(team_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/team/finalsHexmap', methods=['POST'])
def create_team_playoff_finals_per_game_hexmap_shot_chart():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    game_id = request.get_json()['gameId']
    return ShotChartUtil.create_team_playoffs_finals_per_game_hexmap_shot_chart(team_name, season, game_id)


@require_json
@handle_exceptions
@app.route('/api/wnba/player/id', methods=['POST'])
def get_wnba_player_id():
    player_name = request.get_json()['playerName']
    return PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(player_name)


@require_json
@handle_exceptions
@app.route('/api/wnba/player/seasonStats', methods=['POST'])
def get_wnba_player_season_stats():
    player_name = request.get_json()['playerName']
    return NbaPlayerStats.get_wnba_player_season_stats(player_name)


@require_json
@handle_exceptions
@app.route('/api/gleague/player/id', methods=['POST'])
def get_gleague_player_id():
    player_name = request.get_json()['playerName']
    return PostGameStatsUtil.PostGameStatsUtil.get_gleague_player_id(player_name)


@require_json
@handle_exceptions
@app.route('/api/gleague/player/seasonStats', methods=['POST'])
def get_gleague_player_season_stats():
    player_name = request.get_json()['playerName']
    return NbaPlayerStats.get_glegaue_player_season_stats(player_name)


if __name__ == '__main__':
    app.run()
