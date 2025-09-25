from flask import Blueprint

import NCAAStats
from decorators.errors import handle_exceptions
from decorators.jwt import jwt_required
from decorators.safe_json import safe_json

ncaa_mens_team_bp = Blueprint("ncaa_mens_player_bp", __name__, url_prefix="/api/ncaa/team/")


@ncaa_mens_team_bp.route('/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
@safe_json(required_fields=["teamName", "season"])
def get_ncaa_team_season_stats(request) -> 'flask.Response':
    team_name = request['teamName']
    season = request['season']
    response = NCAAStats.NCAATeamStats.get_team_season_stats(team_name, season)
    return response
