import flask
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

import NCAAStats
import NFLStats
import NbaPlayerStats
import TeamStats
import ShotChartUtil
import PostGameStatsUtil
from decorators.errors import handle_exceptions, require_json
import sqlite3
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from decorators.jwt import jwt_required

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.DEBUG,  # or INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s [%(levelname)s] %(message)s',
)

SECRET_KEY = "my_dirty_little_secret"  # All American Rejects :)


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/nba/player/id', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_id() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        logger.info(f"retrieving NBA player id for {player_name}")
        response = PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
        logger.info(f"retrieved NBA player id for {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player id *****")
        return jsonify("Error retrieving player id")


@app.route('/api/nba/player/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        logger.info(f"retrieving NBA player season stats - {player_name}")
        response = NbaPlayerStats.get_player_stats(player_name)
        logger.info(f"retrieved NBA player season stats - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player season stats *****")
        return jsonify("Error retrieving player season stats")


@app.route('/api/nba/player/advancedSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_advanced_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        season_type = request.get_json()['seasonType']
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving NBA Advanced player season stats - {player_name} | {season} | {season_type}")
        response = NbaPlayerStats.get_player_advanced_stats_for_season(player_name, season, season_type)
        logger.info(f"retrieved NBA Advanced player season stats - {player_name} | {season} | {season_type}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player advanced season stats *****")
        return jsonify("Error retrieving player advanced season stats")


@app.route('/api/nba/player/advancedAverageSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_average_advanced_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        season_type = request.get_json()['seasonType']
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving NBA Advanced Average player season stats - {player_name} | {season} | {season_type}")
        response = NbaPlayerStats.get_player_average_advanced_stats_for_season(player_name, season, season_type)
        logger.info(f"retrieved NBA Advanced Average player season stats - {player_name} | {season} | {season_type}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player advanced average season stats *****")
        return jsonify("Error retrieving player advanced average season stats")


@app.route('/api/nba/player/perSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_any_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        year = request.get_json()['season']
        logger.info(f"retrieving NBA player stats per season - {player_name} | {year}")
        response = NbaPlayerStats.get_player_stats_per_season(player_name, year)
        logger.info(f"retrieved NBA player stats per season - {player_name} | {year}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player per season stats *****")
        return jsonify("Error retrieving player per season stats")


@app.route('/api/nba/player/perSeasonAverages', methods=['POST'])
@jwt_required
@handle_exceptions
def get_nba_player_season_averages() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        year = request.get_json()['season']
        logger.info(f"retrieving NBA player average stats per season - {player_name} | {year}")
        response = NbaPlayerStats.get_player_stats_per_season(player_name, year)
        logger.info(f"retrieved NBA player average stats per season - {player_name} | {year}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player per season averages *****")
        return jsonify("Error retrieving player per season averages")


@app.route('/api/nba/player/careerSeasonTotal', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_career_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        logger.info(f"retrieving NBA player career season total - {player_name}")
        response = NbaPlayerStats.get_player_career_stats(player_name)
        logger.info(f"retrieved NBA player career season total - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player career stats *****")
        return jsonify("Error retrieving player career stats")


@app.route('/api/nba/player/playoffStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_playoff_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        logger.info(f"retrieving NBA player playoff stats - {player_name} | {season}")
        response = NbaPlayerStats.get_player_playoff_stats(player_name, season)
        logger.info(f"retrieved NBA player playoff stats - {player_name} | {season}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player playoff stats *****")
        return jsonify("Error retrieving player playoff stats")


@app.route('/api/nba/player/statsPerGame', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_stats_per_game() -> 'flask.Response':
    try:
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving NBA player stats for game - {game_id}")
        response = NbaPlayerStats.get_player_stats_by_game(game_id)
        logger.info(f"retrieved NBA player stats for game - {game_id}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player per game stats *****")
        return jsonify("Error retrieving player per stats")


@app.route('/api/nba/player/shotChartCoordinates', methods=['POST'])
@jwt_required
@handle_exceptions
def get_player_short_chart_coordinates() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        logger.info(f"retrieving NBA player shot chart coordinates - {player_name} | {season}")
        response = NbaPlayerStats.get_player_shot_chart_coordinates(player_name, season)
        logger.info(f"retrieved NBA player shot chart coordinates - {player_name} | {season}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player shot chart coordinates *****")
        return jsonify("Error retrieving player shot chart coordinates")


@app.route('/api/nba/player/hexmap', methods=['POST'])
@jwt_required
@handle_exceptions
def create_player_hexmap() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        season_type = request.get_json()['seasonType']
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving NBA player hexmap - {player_name} | {season} | {season_type} | {game_id}")
        response = ShotChartUtil.create_updated_player_regular_season_hexmap_shot_chart(player_name, season,
                                                                                        season_type,
                                                                                        game_id)
        logger.info(f"retrieved NBA player hexmap - {player_name} | {season} | {season_type} | {game_id}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player hexmap *****")
        return jsonify("Error retrieving player hexmap")


@app.route('/api/nba/player/heatmap', methods=['POST'])
@jwt_required
@handle_exceptions
def create_player_heatmap() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        season_type = request.get_json()['seasonType']
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving NBA player heatmap - {player_name} | {season} | {season_type} | {game_id}")
        response = ShotChartUtil.create_player_heatmap(player_name, season, season_type, game_id)
        logger.info(f"retrieved NBA player heatmap - {player_name} | {season} | {season_type} | {game_id}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving player heatmap *****")
        return jsonify("Error retrieving player heatmap")


@app.route('/api/nba/team/heatmap', methods=['POST'])
@jwt_required
@handle_exceptions
def create_team_heatmap() -> 'flask.Response':
    try:
        team_name = request.get_json()['teamName']
        season = request.get_json()['season']
        season_type = request.get_json()['seasonType']
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving NBA team heatmap - {team_name} | {season} | {season_type} | {game_id}")
        response = ShotChartUtil.create_team_heatmap(team_name, season, season_type, game_id)
        logger.info(f"retrieved NBA team heatmap - {team_name} | {season} | {season_type} | {game_id}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving team heatmap *****")
        return jsonify("Error retrieving team heatmap")


@app.route('/api/nba/team/hexmap', methods=['POST'])
@jwt_required
@handle_exceptions
def create_team_hexmap() -> 'flask.Response':
    try:
        team_name = request.get_json()['teamName']
        season = request.get_json()['season']
        season_type = request.get_json()['seasonType']
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving NBA team hexmap - {team_name} | {season} | {season_type} | {game_id}")
        response = ShotChartUtil.create_team_hexmap_per_season(team_name, season, season_type, game_id)
        logger.info(f"retrieved NBA team hexmap - {team_name} | {season} | {season_type} | {game_id}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving team hexmap *****")
        return jsonify("Error retrieving team hexmap")


@app.route('/api/nba/team/defensiveHexmap', methods=['POST'])
@jwt_required
@handle_exceptions
def create_team_defensive_hexmap() -> 'flask.Response':
    try:
        team_name = request.get_json()['teamName']
        season = request.get_json()['season']
        season_type = request.get_json()['seasonType']
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving NBA team hexmap - {team_name} | {season} | {season_type} | {game_id}")
        response = ShotChartUtil.create_team_defense_heatmap(team_name, season, season_type, game_id)
        logger.info(f"retrieved NBA team hexmap - {team_name} | {season} | {season_type} | {game_id}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving team defensive hexmap *****")
        return jsonify("Error retrieving player team defensive hexmap")


@app.route('/api/nba/team/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_team_season_stats() -> 'flask.Response':
    try:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = data['season']
        logger.info(f"retrieving NBA team season stats - {team_name} | {season}")
        response = TeamStats.get_team_season_stats(team_name, season)
        logger.info(f"retrieved NBA team season stats - {team_name} | {season}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving team seasonStats *****")
        return jsonify("Error retrieving team seasonStats")


@app.route('/api/nba/team/seasonAverages', methods=['POST'])
@jwt_required
@handle_exceptions
def get_team_season_average_stats() -> 'flask.Response':
    try:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = data['season']
        logger.info(f"retrieving NBA team season average stats - {team_name} | {season}")
        response = TeamStats.get_team_season_stats(team_name, season)
        logger.info(f"retrieved NBA team season average stats - {team_name} | {season}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving team season averages *****")
        return jsonify("Error retrieving team season averages")


@app.route('/api/nba/team/playoffStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_team_playoff_stats() -> 'flask.Response':
    try:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = data['season']
        logger.info(f"retrieving NBA team playoff stats - {team_name} | {season}")
        response = TeamStats.get_team_playoff_stats(team_name, season)
        logger.info(f"retrieved NBA team playoff stats - {team_name} | {season}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving team playoff stats *****")
        return jsonify("Error retrieving team playoff stats")


@app.route('/api/nba/team/playoffStatsAverage', methods=['POST'])
@jwt_required
@handle_exceptions
def get_team_playoff_average_stats() -> 'flask.Response':
    try:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = data['season']
        logger.info(f"retrieving NBA team playoff average stats - {team_name} | {season}")
        response = TeamStats.get_team_playoff_stats(team_name, season)
        logger.info(f"retrieved NBA team playoff average stats - {team_name} | {season}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving team playoff stats average *****")
        return jsonify("Error retrieving team playoff stats average")


@app.route('/api/nba/team/finalsHexmap', methods=['POST'])
@jwt_required
@handle_exceptions
def create_team_playoff_finals_per_game_hexmap_shot_chart() -> 'flask.Response':
    try:
        data = request.get_json()
        team_name = data.get('teamName', '')
        season = data['season']
        game_id = data['gameId']
        logger.info(f"retrieving NBA team finals hexmap - {team_name} | {season} | {game_id}")
        response = ShotChartUtil.create_team_playoffs_finals_per_game_hexmap_shot_chart(team_name, season, game_id)
        logger.info(f"retrieved NBA team finals hexmap - {team_name} | {season} | {game_id}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving team finals hexmap *****")
        return jsonify("Error retrieving player team finals hexmap")


@app.route('/api/wnba/player/id', methods=['POST'])
@jwt_required
@handle_exceptions
def get_wnba_player_id() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        logger.info(f"retrieving WNBA player id - {player_name}")
        response = PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(player_name)
        logger.info(f"retrieved WNBA player id - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving wnba player id *****")
        return jsonify("Error retrieving wnba player id")


@app.route('/api/wnba/player/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_wnba_player_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        logger.info(f"retrieving WNBA player season stats - {player_name}")
        response = NbaPlayerStats.get_wnba_player_season_stats(player_name)
        logger.info(f"retrieved WNBA player season stats - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving wnba player season stats *****")
        return jsonify("Error retrieving wnba player season stats")


@app.route('/api/wnba/player/hexmap', methods=['POST'])
@jwt_required
@handle_exceptions
def get_wnba_player_hexmap() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        season_type = request.get_json()['seasonType']
        game_id = request.get_json()['gameId']
        logger.info(f"retrieving WNBA player hexmap - {player_name} | {season} | {season_type} | {game_id}")
        response = ShotChartUtil.create_wnba_player_heatmap(player_name, season, season_type, game_id)
        logger.info(f"retrieved WNBA player hexmap - {player_name} | {season} | {season_type} | {game_id}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving wnba player hexmap *****")
        return jsonify("Error retrieving wnba player hexmap")


@app.route('/api/gleague/player/id', methods=['POST'])
@jwt_required
@handle_exceptions
def get_gleague_player_id() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        logger.info(f"retrieving G League player id - {player_name}")
        response = PostGameStatsUtil.PostGameStatsUtil.get_gleague_player_id(player_name)
        logger.info(f"retrieved G League player id - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving gleague player id *****")
        return jsonify("Error retrieving gleague player id")


@app.route('/api/gleague/player/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_gleague_player_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        logger.info(f"retrieving G League player season stats - {player_name}")
        response = NbaPlayerStats.get_glegaue_player_season_stats(player_name)
        logger.info(f"retrieved G League player season stats - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving gleague player season stats *****")
        return jsonify("Error retrieving gleague player season stats")


@app.route('/api/nfl/player/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_nfl_player_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        seasonType = request.get_json()['seasonType']
        logger.info(f"retrieving NFL player season stats - {player_name}")
        response = NFLStats.NFLPlayerStats.get_nfl_player_stats(player_name, season, seasonType)
        logger.info(f"retrieved NFL player season stats - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving NFL player season stats *****")
        return jsonify("Error retrieving NFL player seasons stats")


@app.route('/api/nfl/player/rushingSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_nfl_player_rushing_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        seasonType = request.get_json()['seasonType']
        logger.info(f"retrieving NFL rushing player season stats - {player_name}")
        response = NFLStats.NFLPlayerStats.get_nfl_player_rushing_stats(player_name, season, seasonType)
        logger.info(f"retrieved NFL rushing player season stats - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving NFL player rushing season stats *****")
        return jsonify("Error retrieving NFL rushing season stats")


@app.route('/api/nfl/player/receivingSeasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_nfl_player_receiving_season_stats() -> 'flask.Response':
    try:
        player_name = request.get_json()['playerName']
        season = request.get_json()['season']
        seasonType = request.get_json()['seasonType']
        logger.info(f"retrieving NFL player receiving season stats - {player_name}")
        response = NFLStats.NFLPlayerStats.get_nfl_player_receiving_stats(player_name, season, seasonType)
        logger.info(f"retrieved NFL player receiving season stats - {player_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving NFL player receiving season stats *****")
        return jsonify("Error retrieving NFL player receiving season stats")


@app.route('/api/nfl/team/seasonPBPStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_nfl_pbp_team_season_stats() -> 'flask.Response':
    try:
        team_name = request.get_json()['teamName']
        season = request.get_json()['season']
        logger.info(f"retrieving NFL team season stats - {team_name}")
        response = NFLStats.NFLTeamStats.get_nfl_pbp_team_stats(team_name, season)
        logger.info(f"retrieved NFL team season stats - {team_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving NFL team season stats *****")
        return jsonify("Error retrieving NFL team season stats")


@app.route('/api/ncaam/team/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_nfl_team_season_stats() -> 'flask.Response':
    try:
        team_name = request.get_json()['teamName']
        season = request.get_json().get('season', [])
        if not isinstance(season, list):
            season = [season]
        logger.info(f"retrieving NFL team season stats - {team_name}")
        season_type = 'REG'
        response = NFLStats.NFLTeamStats.get_nfl_team_stats(season, season_type)
        logger.info(f"retrieved NFL team season stats - {team_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving NFL team season stats *****")
        return jsonify("Error retrieving NFL team season stats")


@app.route('/api/ncaam/team/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_ncaa_player_season_stats() -> 'flask.Response':
    try:
        team_name = request.get_json()['teamName']
        season = request.get_json().get('season', [])
        if not isinstance(season, list):
            season = [season]
        logger.info(f"retrieving NCAA Mens Player season stats - {team_name}")
        response = NCAAStats.NCAAPlayerStats.get_player_season_stats(team_name, season)
        logger.info(f"retrieved NCAA Mens Player season stats - {team_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving NCAA player  season stats *****")
        return jsonify("Error retrieving NCAA player season stats")


@app.route('/api/ncaam/team/seasonStats', methods=['POST'])
@jwt_required
@handle_exceptions
def get_ncaa_team_season_stats() -> 'flask.Response':
    try:
        team_name = request.get_json()['teamName']
        season = request.get_json()['season']
        logger.info(f"retrieving NCAA Mens Player season stats - {team_name}")
        response = NCAAStats.NCAATeamStats.get_team_season_stats(team_name, season)
        logger.info(f"retrieved NCAA Mens Player season stats - {team_name}")
        return response
    except Exception as e:
        logger.info(f"***** Error retrieving NCAA teams season stats *****")
        return jsonify("Error retrieving NCAA teams season stats")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
