from flask import jsonify, Blueprint

import NbaPlayerStats
from PostGameStatsUtil import PostGameStatsUtil
from decorators.errors import handle_exceptions
from decorators.jwt import jwt_required
from decorators.safe_json import safe_json

gleague_player_bp = Blueprint("gleague_player_bp", __name__, url_prefix="/api/gleague/player")


@gleague_player_bp.route('/id', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName"])
def get_gleague_player_id(request) -> 'flask.Response':
    player_name = request['playerName']
    response = PostGameStatsUtil.get_gleague_player_id(player_name)
    return response


@gleague_player_bp.route('/api/gleague/player/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["playerName"])
def get_gleague_player_season_stats(request) -> 'flask.Response':
    player_name = request['playerName']
    response = NbaPlayerStats.get_glegaue_player_season_stats(player_name)
    return response
