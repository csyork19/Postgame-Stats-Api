from flask import Flask, request
from nba_api.stats.endpoints import playergamelog, leagueleaders, playercareerstats
import PlayerStats

import pandas as pd

app = Flask(__name__)


@app.route('/api/player/seasonStats', methods=['POST'])
def player_season_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
        return PlayerStats.get_player_stats(player_name)
    return "test"



@app.route('/api/player/careerStats', methods=['POST'])
def player_career_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
        return PlayerStats.get_player_career_stats(player_name)

@app.route('/api/player/careerAccolades', methods=['POST'])
def player_career_accolades():
    return "This is a test flask api setup!  :)"

# THIS IS ON A YEARLY BASIS
@app.route('/api/player/playoffStats', methods=['POST'])
def player_playoff_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
        return PlayerStats.get_player_playoff_stats(player_name)
    return "This is a test flask api setup!  :)"

@app.route('/api/team/seasonStats', methods=['POST'])
def team_season_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
    # Be sure to include any advanced stats
    return "This is a test flask api setup!  :)"

@app.route('/api/team/careerStats', methods=['POST'])
def team_career_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
    return "This is a test flask api setup!  :)"

@app.route('/api/team/careerAccolades', methods=['POST'])
def team_career_accolades():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
    return "This is a test flask api setup!  :)"

@app.route('/api/team/playoffStats', methods=['POST'])
def team_playoff_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
    return "This is a test flask api setup!  :)"







if __name__ == '__main__':
    app.run()
