from flask import Flask, request

import NCAAStats
import NFLStats
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
    response = PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
    logger.info(f"retrieved NBA player id for {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/seasonStats', methods=['POST'])
def get_player_season_stats():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving NBA player season stats - {player_name}")
    response = NbaPlayerStats.get_player_stats(player_name)
    logger.info(f"retrieved NBA player season stats - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/advancedSeasonStats', methods=['POST'])
def get_player_advanced_season_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA Advanced player season stats - {player_name} | {season} | {season_type}")
    response = NbaPlayerStats.get_player_advanced_stats_for_season(player_name, season, season_type)
    logger.info(f"retrieved NBA Advanced player season stats - {player_name} | {season} | {season_type}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/advancedAverageSeasonStats', methods=['POST'])
def get_player_average_advanced_season_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA Advanced Average player season stats - {player_name} | {season} | {season_type}")
    response = NbaPlayerStats.get_player_average_advanced_stats_for_season(player_name, season, season_type)
    logger.info(f"retrieved NBA Advanced Average player season stats - {player_name} | {season} | {season_type}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/perSeasonStats', methods=['POST'])
def get_player_any_season_stats():
    player_name = request.get_json()['playerName']
    year = request.get_json()['season']
    logger.info(f"retrieving NBA player stats per season - {player_name} | {year}")
    response = NbaPlayerStats.get_player_stats_per_season(player_name, year)
    logger.info(f"retrieved NBA player stats per season - {player_name} | {year}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/perSeasonAverages', methods=['POST'])
def get_nba_player_season_averages():
    player_name = request.get_json()['playerName']
    year = request.get_json()['season']
    logger.info(f"retrieving NBA player average stats per season - {player_name} | {year}")
    response = NbaPlayerStats.get_player_stats_per_season(player_name, year)
    logger.info(f"retrieved NBA player average stats per season - {player_name} | {year}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/careerSeasonTotal', methods=['POST'])
def get_player_career_stats():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving NBA player career season total - {player_name}")
    response = NbaPlayerStats.get_player_career_stats(player_name)
    logger.info(f"retrieved NBA player career season total - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/playoffStats', methods=['POST'])
def get_player_playoff_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    logger.info(f"retrieving NBA player playoff stats - {player_name} | {season}")
    response = NbaPlayerStats.get_player_playoff_stats(player_name, season)
    logger.info(f"retrieved NBA player playoff stats - {player_name} | {season}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/statsPerGame', methods=['POST'])
def get_player_stats_per_game():
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA player stats for game - {game_id}")
    response = NbaPlayerStats.get_player_stats_by_game(game_id)
    logger.info(f"retrieved NBA player stats for game - {game_id}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/shotChartCoordinates', methods=['POST'])
def get_player_short_chart_coordinates():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    logger.info(f"retrieving NBA player shot chart coordinates - {player_name} | {season}")
    response = NbaPlayerStats.get_player_shot_chart_coordinates(player_name, season)
    logger.info(f"retrieved NBA player shot chart coordinates - {player_name} | {season}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/hexmap', methods=['POST'])
def create_player_hexmap():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA player hexmap - {player_name} | {season} | {season_type} | {game_id}")
    response = ShotChartUtil.create_updated_player_regular_season_hexmap_shot_chart(player_name, season, season_type,
                                                                                    game_id)
    logger.info(f"retrieved NBA player hexmap - {player_name} | {season} | {season_type} | {game_id}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/player/heatmap', methods=['POST'])
def create_player_heatmap():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA player heatmap - {player_name} | {season} | {season_type} | {game_id}")
    response = ShotChartUtil.create_player_heatmap(player_name, season, season_type, game_id)
    logger.info(f"retrieved NBA player heatmap - {player_name} | {season} | {season_type} | {game_id}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/team/heatmap', methods=['POST'])
def create_team_heatmap():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA team heatmap - {team_name} | {season} | {season_type} | {game_id}")
    response = ShotChartUtil.create_team_heatmap(team_name, season, season_type, game_id)
    logger.info(f"retrieved NBA team heatmap - {team_name} | {season} | {season_type} | {game_id}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/team/hexmap', methods=['POST'])
def create_team_hexmap():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA team hexmap - {team_name} | {season} | {season_type} | {game_id}")
    response = ShotChartUtil.create_team_hexmap_per_season(team_name, season, season_type, game_id)
    logger.info(f"retrieved NBA team hexmap - {team_name} | {season} | {season_type} | {game_id}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/team/defensiveHexmap', methods=['POST'])
def create_team_defensive_hexmap():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    season_type = request.get_json()['seasonType']
    game_id = request.get_json()['gameId']
    logger.info(f"retrieving NBA team hexmap - {team_name} | {season} | {season_type} | {game_id}")
    response = ShotChartUtil.create_team_defense_heatmap(team_name, season, season_type, game_id)
    logger.info(f"retrieved NBA team hexmap - {team_name} | {season} | {season_type} | {game_id}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/team/seasonStats', methods=['POST'])
def get_team_season_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = data['season']
    logger.info(f"retrieving NBA team season stats - {team_name} | {season}")
    response = TeamStats.get_team_season_stats(team_name, season)
    logger.info(f"retrieved NBA team season stats - {team_name} | {season}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/team/seasonAverages', methods=['POST'])
def get_team_season_average_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = data['season']
    logger.info(f"retrieving NBA team season average stats - {team_name} | {season}")
    response = TeamStats.get_team_season_stats(team_name, season)
    logger.info(f"retrieved NBA team season average stats - {team_name} | {season}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/team/playoffStats', methods=['POST'])
def get_team_playoff_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = data['season']
    logger.info(f"retrieving NBA team playoff stats - {team_name} | {season}")
    response = TeamStats.get_team_playoff_stats(team_name, season)
    logger.info(f"retrieved NBA team playoff stats - {team_name} | {season}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/team/playoffStatsAverage', methods=['POST'])
def get_team_playoff_average_stats():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = data['season']
    logger.info(f"retrieving NBA team playoff average stats - {team_name} | {season}")
    response = TeamStats.get_team_playoff_stats(team_name, season)
    logger.info(f"retrieved NBA team playoff average stats - {team_name} | {season}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nba/team/finalsHexmap', methods=['POST'])
def create_team_playoff_finals_per_game_hexmap_shot_chart():
    data = request.get_json()
    team_name = data.get('teamName', '')
    season = data['season']
    game_id = data['gameId']
    logger.info(f"retrieving NBA team finals hexmap - {team_name} | {season} | {game_id}")
    response = ShotChartUtil.create_team_playoffs_finals_per_game_hexmap_shot_chart(team_name, season, game_id)
    logger.info(f"retrieved NBA team finals hexmap - {team_name} | {season} | {game_id}")
    return response


@require_json
@handle_exceptions
@app.route('/api/wnba/player/id', methods=['POST'])
def get_wnba_player_id():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving WNBA player id - {player_name}")
    response = PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(player_name)
    logger.info(f"retrieved WNBA player id - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/wnba/player/seasonStats', methods=['POST'])
def get_wnba_player_season_stats():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving WNBA player season stats - {player_name}")
    response = NbaPlayerStats.get_wnba_player_season_stats(player_name)
    logger.info(f"retrieved WNBA player season stats - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/gleague/player/id', methods=['POST'])
def get_gleague_player_id():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving G League player id - {player_name}")
    response = PostGameStatsUtil.PostGameStatsUtil.get_gleague_player_id(player_name)
    logger.info(f"retrieved G League player id - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/gleague/player/seasonStats', methods=['POST'])
def get_gleague_player_season_stats():
    player_name = request.get_json()['playerName']
    logger.info(f"retrieving G League player season stats - {player_name}")
    response = NbaPlayerStats.get_glegaue_player_season_stats(player_name)
    logger.info(f"retrieved G League player season stats - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nfl/player/seasonStats', methods=['POST'])
def get_nfl_player_season_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    seasonType = request.get_json()['seasonType']
    logger.info(f"retrieving NFL player season stats - {player_name}")
    response = NFLStats.NFLPlayerStats.get_nfl_player_stats(player_name, season, seasonType)
    logger.info(f"retrieved NFL player season stats - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nfl/player/rushingSeasonStats', methods=['POST'])
def get_nfl_player_rushing_season_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    seasonType = request.get_json()['seasonType']
    logger.info(f"retrieving NFL rushing player season stats - {player_name}")
    response = NFLStats.NFLPlayerStats.get_nfl_player_rushing_stats(player_name, season, seasonType)
    logger.info(f"retrieved NFL rushing player season stats - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nfl/player/receivingSeasonStats', methods=['POST'])
def get_nfl_player_receiving_season_stats():
    player_name = request.get_json()['playerName']
    season = request.get_json()['season']
    seasonType = request.get_json()['seasonType']
    logger.info(f"retrieving NFL player receiving season stats - {player_name}")
    response = NFLStats.NFLPlayerStats.get_nfl_player_receiving_stats(player_name, season, seasonType)
    logger.info(f"retrieved NFL player receiving season stats - {player_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/nfl/team/seasonStats', methods=['POST'])
def get_nfl_team_season_stats():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    logger.info(f"retrieving NFL team season stats - {team_name}")
    response = NFLStats.NFLTeamStats.get_nfl_team_stats(team_name, season)
    logger.info(f"retrieved NFL team season stats - {team_name}")
    return response


@require_json
@handle_exceptions
@app.route('/api/ncaam/player/seasonStats', methods=['POST'])
def get_ncaa_player_season_stats():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    logger.info(f"retrieving NCAA Mens Player season stats - {team_name}")
    response = NCAAStats.NCAAPlayerStats.get_player_season_stats(team_name, season)
    logger.info(f"retrieved NCAA Mens Player season stats - {team_name}")
    return response

@require_json
@handle_exceptions
@app.route('/api/ncaam/team/seasonStats', methods=['POST'])
def get_ncaa_team_season_stats():
    team_name = request.get_json()['teamName']
    season = request.get_json()['season']
    logger.info(f"retrieving NCAA Mens Player season stats - {team_name}")
    response = NCAAStats.NCAATeamStats.get_team_season_stats(team_name, season)
    logger.info(f"retrieved NCAA Mens Player season stats - {team_name}")
    return response


if __name__ == '__main__':
    app.run()
