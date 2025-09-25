from flask import Blueprint, jsonify, request

import NFLStats
from decorators.errors import handle_exceptions
from decorators.jwt import jwt_required
from decorators.with_json import with_json

nfl_player_bp = Blueprint("nfl_player_bp", __name__, url_prefix="/api/nfl/player")


@nfl_player_bp.route('/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@with_json(required_fields=["playerName", "season", "seasonType"])
def get_nfl_player_season_stats() -> 'flask.Response':
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    seasonType = request.get_json()['seasonType']
    response = NFLStats.NFLPlayerStats.get_nfl_player_stats(player_name, season, seasonType)
    return response


@nfl_player_bp.route('/rushingSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@with_json(required_fields=["playerName", "season", "seasonType"])
def get_nfl_player_rushing_season_stats() -> 'flask.Response':
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    seasonType = request.get_json()['seasonType']
    response = NFLStats.NFLPlayerStats.get_nfl_player_rushing_stats(player_name, season, seasonType)
    return response


@nfl_player_bp.route('/receivingSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@with_json(required_fields=["playerName", "season", "seasonType"])
def get_nfl_player_receiving_season_stats() -> 'flask.Response':
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    seasonType = request.get_json()['seasonType']
    response = NFLStats.NFLPlayerStats.get_nfl_player_receiving_stats(player_name, season, seasonType)
    return response


@nfl_player_bp.route('/seasonPBPStats', methods=['POST'])
@jwt_required
@handle_exceptions
@with_json(required_fields=["teamName", "season"])
def get_nfl_pbp_team_season_stats() -> 'flask.Response':
    try:
        team_name = request.get_json()['teamName']
        season = request.get_json()['season']
        response = NFLStats.NFLTeamStats.get_nfl_pbp_team_stats(team_name, season)
        return response
    except Exception as e:
        return jsonify("Error retrieving NFL team season stats")
