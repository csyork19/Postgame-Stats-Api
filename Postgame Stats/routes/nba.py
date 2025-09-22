from flask import Blueprint

import NbaPlayerStats
import ShotChartUtil
import TeamStats
from PostGameStatsUtil import PostGameStatsUtil
from decorators.errors import handle_exceptions
from decorators.jwt import jwt_required
from decorators.safe_json import safe_json

nba_player_bp = Blueprint("nba_player_bp", __name__, url_prefix="/api/nba/player")
nba_team_bp = Blueprint("nba_team_bp", __name__, url_prefix="/api/nba/team")


@nba_player_bp.route("/id", methods=["POST"])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName"])
def get_player_id(request) -> 'flask.Response':
    player_name = request['playerName']
    response = PostGameStatsUtil.get_player_id(player_name)
    return response


@nba_player_bp.route('/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName"])
def get_player_season_stats(data) -> 'flask.Response':
    player_name = data['playerName']
    return NbaPlayerStats.get_player_stats(player_name)


@nba_player_bp.route('/advancedSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName", "season", "seasonType"])
def get_player_advanced_season_stats(data) -> 'flask.Response':
    player_name = data['playerName']
    season = data['season']
    season_type = data['seasonType']
    return NbaPlayerStats.get_player_advanced_stats_for_season(player_name, season, season_type)


@nba_player_bp.route('/advancedAverageSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName", "season", "seasonType"])
def get_player_average_advanced_season_stats(data) -> 'flask.Response':
    player_name = data['playerName']
    season = data['season']
    season_type = data['seasonType']
    return NbaPlayerStats.get_player_average_advanced_stats_for_season(player_name, season, season_type)


@nba_player_bp.route('/perSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName", "season"])
def get_player_any_season_stats(data) -> 'flask.Response':
    player_name = data['playerName']
    year = data['season']
    return NbaPlayerStats.get_player_stats_per_season(player_name, year)


@nba_player_bp.route('/perSeasonAverages', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName", "season"])
def get_nba_player_season_averages(data) -> 'flask.Response':
    player_name = data['playerName']
    year = data['season']
    return NbaPlayerStats.get_player_stats_per_season(player_name, year)


@nba_player_bp.route('/careerSeasonTotal', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName"])
def get_player_career_stats(data) -> 'flask.Response':
    player_name = data['playerName']
    return NbaPlayerStats.get_player_career_stats(player_name)


@nba_player_bp.route('/playoffStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName", "season"])
def get_player_playoff_stats(data) -> 'flask.Response':
    player_name = data['playerName']
    season = data['season']
    return NbaPlayerStats.get_player_playoff_stats(player_name, season)


@nba_player_bp.route('/statsPerGame', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["gameId"])
def get_player_stats_per_game(data) -> 'flask.Response':
    game_id = data['gameId']
    return NbaPlayerStats.get_player_stats_by_game(game_id)


@nba_player_bp.route('/shotChartCoordinates', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName", "season"])
def get_player_short_chart_coordinates(data) -> 'flask.Response':
    player_name = data['playerName']
    season = data['season']
    return NbaPlayerStats.get_player_shot_chart_coordinates(player_name, season)


@nba_player_bp.route('/hexmap', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName", "season", "seasonType", "gameId"])
def create_player_hexmap(data) -> 'flask.Response':
    player_name = data['playerName']
    season = data['season']
    season_type = data['seasonType']
    game_id = data['gameId']
    return ShotChartUtil.create_updated_player_regular_season_hexmap_shot_chart(player_name, season, season_type,
                                                                                game_id)


@nba_player_bp.route('/heatmap', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName", "season", "seasonType", "gameId"])
def create_player_heatmap(data) -> 'flask.Response':
    player_name = data['playerName']
    season = data['season']
    season_type = data['seasonType']
    game_id = data['gameId']
    return ShotChartUtil.create_player_heatmap(player_name, season, season_type, game_id)


@nba_team_bp.route('/heatmap', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season", "seasonType", "gameId"])
def create_team_heatmap(data) -> 'flask.Response':
    team_name = data['teamName']
    season = data['season']
    season_type = data['seasonType']
    game_id = data['gameId']
    return ShotChartUtil.create_team_heatmap(team_name, season, season_type, game_id)


@nba_team_bp.route('/hexmap', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season", "seasonType", "gameId"])
def create_team_hexmap(data) -> 'flask.Response':
    team_name = data['teamName']
    season = data['season']
    season_type = data['seasonType']
    game_id = data['gameId']
    return ShotChartUtil.create_team_hexmap_per_season(team_name, season, season_type, game_id)


@nba_team_bp.route('/defensiveHexmap', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season", "seasonType", "gameId"])
def create_team_defensive_hexmap(data) -> 'flask.Response':
    team_name = data['teamName']
    season = data['season']
    season_type = data['seasonType']
    game_id = data['gameId']
    return ShotChartUtil.create_team_defense_heatmap(team_name, season, season_type, game_id)


@nba_team_bp.route('/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season"])
def get_team_season_stats(data) -> 'flask.Response':
    team_name = data['teamName']
    season = data['season']
    return TeamStats.get_team_season_stats(team_name, season)


@nba_team_bp.route('/seasonAverages', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season"])
def get_team_season_average_stats(data) -> 'flask.Response':
    team_name = data['teamName']
    season = data['season']
    return TeamStats.get_team_season_stats(team_name, season)


@nba_team_bp.route('/playoffStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season"])
def get_team_playoff_stats(data) -> 'flask.Response':
    team_name = data['teamName']
    season = data['season']
    return TeamStats.get_team_playoff_stats(team_name, season)


@nba_team_bp.route('/playoffStatsAverage', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season"])
def get_team_playoff_average_stats(data) -> 'flask.Response':
    team_name = data['teamName']
    season = data['season']
    return TeamStats.get_team_playoff_stats(team_name, season)


@nba_team_bp.route('/finalsHexmap', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season", "gameId"])
def create_team_playoff_finals_per_game_hexmap_shot_chart(data) -> 'flask.Response':
    team_name = data['teamName']
    season = data['season']
    game_id = data['gameId']
    return ShotChartUtil.create_team_playoffs_finals_per_game_hexmap_shot_chart(team_name, season, game_id)
