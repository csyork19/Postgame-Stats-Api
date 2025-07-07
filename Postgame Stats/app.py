from flask import Flask, request
from nba_api.stats.endpoints import BoxScoreDefensiveV2

import NbaPlayerStats
import TeamStats
import ShotChartUtil
import PostGameStatsUtil
from flask_cors import CORS
from descriptors.errors import handle_exceptions, require_json
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
import logging

logging.basicConfig(
    level=logging.DEBUG,  # or INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s [%(levelname)s] %(message)s',
)

logger = logging.getLogger(__name__)


@require_json
@handle_exceptions
@app.route('/api/nba/player/id', methods=['POST'])
def get_player_id():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving NBA player id for {player_name}")
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
    logger.info(f"retrieved NBA player id for {player_name}")
    return player_id


@require_json
@handle_exceptions
@app.route('/api/nba/player/seasonStats', methods=['POST'])
def get_player_season_stats():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving NBA player season stats - {player_name}")
    return NbaPlayerStats.get_player_stats(player_name)


@require_json
@handle_exceptions
@app.route('/api/nba/player/advancedSeasonStats', methods=['POST'])
def get_player_advanced_season_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA Advanced player season stats - {player_name} | {season} | {season_type}")
    return NbaPlayerStats.get_player_advanced_stats_for_season(player_name, season, season_type)


@require_json
@handle_exceptions
@app.route('/api/nba/player/advancedAverageSeasonStats', methods=['POST'])
def get_player_average_advanced_season_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA Advanced Average player season stats - {player_name} | {season} | {season_type}")
    return NbaPlayerStats.get_player_average_advanced_stats_for_season(player_name, season, season_type)


@require_json
@handle_exceptions
@app.route('/api/nba/player/perSeasonStats', methods=['POST'])
def get_player_any_season_stats():
    player_name = request.get_json()['playerName']
    year = request.get_json()['season']
    logger.info(f"retrieving NBA player stats per season - {player_name} | {year}")
    return NbaPlayerStats.get_player_stats_per_season(player_name, year)


@require_json
@handle_exceptions
@app.route('/api/nba/player/perSeasonAverages', methods=['POST'])
def get_nba_player_season_averages():
    player_name = request.get_json()['playerName']
    year = request.get_json()['season']
    logger.info(f"retrieving NBA player average stats per season - {player_name} | {year}")
    return NbaPlayerStats.get_player_stats_per_season(player_name, year)


@require_json
@handle_exceptions
@app.route('/api/nba/player/careerSeasonTotal', methods=['POST'])
def get_player_career_stats():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving NBA player career season total- {player_name}")
    return NbaPlayerStats.get_player_career_stats(player_name)


@require_json
@handle_exceptions
@app.route('/api/nba/player/playoffStats', methods=['POST'])
def get_player_playoff_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    logger.info(f"retrieving NBA player playoff stats- {player_name} | {season}")
    return NbaPlayerStats.get_player_playoff_stats(player_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/player/statsPerGame', methods=['POST'])
def get_player_stats_per_game():
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA player stats for game - {game_id}")
    return NbaPlayerStats.get_player_stats_by_game(game_id)


@require_json
@handle_exceptions
@app.route('/api/nba/player/shotChartCoordinates', methods=['POST'])
def get_player_short_chart_coordinates():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    logger.info(f"retrieving NBA player shot chart coordinates stats- {player_name} | {season}")
    return NbaPlayerStats.get_player_shot_chart_coordinates(player_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/player/hexmap', methods=['POST'])
def create_player_hexmap():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA player hexmap - {player_name} | {season} | {season_type} | {game_id}")
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
    logger.info(f"retrieving NBA player heatmap - {player_name} | {season} | {season_type} | {game_id}")
    return ShotChartUtil.create_player_heatmap(player_name, season, season_type, game_id)


@require_json
@handle_exceptions
@app.route('/api/nba/team/heatmap', methods=['POST'])
def create_team_heatmap():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA Team heatmap - {team_name} | {season} | {season_type} | {game_id}")
    return ShotChartUtil.create_team_heatmap(team_name, season, season_type, game_id)


@require_json
@handle_exceptions
@app.route('/api/nba/team/hexmap', methods=['POST'])
def create_team_hexmap():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA Team hexmap - {team_name} | {season} | {season_type} | {game_id}")
    return ShotChartUtil.create_team_hexmap_per_season(team_name, season, season_type, game_id)


@require_json
@handle_exceptions
@app.route('/api/nba/team/seasonStats', methods=['POST'])
def get_team_season_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    logger.info(f"retrieving NBA Team season stats - {team_name} | {season}")
    return TeamStats.get_team_season_stats(team_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/team/seasonAverages', methods=['POST'])
def get_team_season_average_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    logger.info(f"retrieving NBA Team season average stats - {team_name} | {season}")
    return TeamStats.get_team_season_stats(team_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/team/playoffStats', methods=['POST'])
def get_team_playoff_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    logger.info(f"retrieving NBA Team playoffs stats - {team_name} | {season}")
    return TeamStats.get_team_playoff_stats(team_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/team/playoffStatsAverage', methods=['POST'])
def get_team_playoff_average_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    logger.info(f"retrieving NBA Team playoffs average stats - {team_name} | {season}")
    return TeamStats.get_team_playoff_stats(team_name, season)


@require_json
@handle_exceptions
@app.route('/api/nba/team/finalsHexmap', methods=['POST'])
def create_team_playoff_finals_per_game_hexmap_shot_chart():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = request.get_json()['season']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA Team finals hexmap - {team_name} | {season} | {game_id}")
    return ShotChartUtil.create_team_playoffs_finals_per_game_hexmap_shot_chart(team_name, season, game_id)


@require_json
@handle_exceptions
@app.route('/api/wnba/player/id', methods=['POST'])
def get_wnba_player_id():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving WNBA player id - {player_name}")
    return PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(player_name)


@require_json
@handle_exceptions
@app.route('/api/wnba/player/seasonStats', methods=['POST'])
def get_wnba_player_season_stats():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving WNBA player id - {player_name}")
    return NbaPlayerStats.get_wnba_player_season_stats(player_name)


@require_json
@handle_exceptions
@app.route('/api/gleague/player/id', methods=['POST'])
def get_gleague_player_id():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving GLEAGUE player id - {player_name}")
    return PostGameStatsUtil.PostGameStatsUtil.get_gleague_player_id(player_name)


@require_json
@handle_exceptions
@app.route('/api/gleague/player/seasonStats', methods=['POST'])
def get_gleague_player_season_stats():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving GLEAGUE player season stats - {player_name}")
    return NbaPlayerStats.get_glegaue_player_season_stats(player_name)


if __name__ == '__main__':
    app.run()
