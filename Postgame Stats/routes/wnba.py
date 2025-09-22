from flask import Blueprint

import NbaPlayerStats
import ShotChartUtil
from PostGameStatsUtil import PostGameStatsUtil
from decorators.errors import handle_exceptions
from decorators.jwt import jwt_required
from decorators.safe_json import safe_json

wnba_player_bp = Blueprint("wnba_player_bp", __name__, url_prefix="/api/wnba/player")


@wnba_player_bp.route('/api/wnba/player/id', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName"])
def get_wnba_player_id(request) -> 'flask.Response':
    player_name = request['playerName']
    response = PostGameStatsUtil.get_wnba_player_id(player_name)
    return response


@wnba_player_bp.route('/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName"])
def get_wnba_player_season_stats(request) -> 'flask.Response':
    player_name = request['playerName']
    response = NbaPlayerStats.get_wnba_player_season_stats(player_name)
    return response


@wnba_player_bp.route('/hexmap', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName","season", "seasonType", "gameId"])
def get_wnba_player_hexmap(request) -> 'flask.Response':
    player_name = request['playerName']
    season = request['season']
    season_type = request['seasonType']
    game_id = request['gameId']
    response = ShotChartUtil.create_wnba_player_heatmap(player_name, season, season_type, game_id)
    return response

