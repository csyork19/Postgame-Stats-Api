from flask import Flask, request
from nba_api.stats.endpoints import playergamelog, leagueleaders
import pandas as pd

app = Flask(__name__)


@app.route('/api/player/seasonStats', methods=['POST'])
def player_season_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']

        # Check if name is populated
        if player_name:
            # Process the extracted data (Here, we just echo it back)
            top_500 = leagueleaders.LeagueLeaders(
                season='2023-24',
                season_type_all_star='Regular Season',
                stat_category_abbreviation='PTS'
            ).get_data_frames()[0][:600]

            # Correct column names for grouping
            avg_stats_columns = ['MIN']
            top_600_avg = top_500.groupby(['PLAYER', 'PLAYER_ID'])[avg_stats_columns].mean()

            df = top_600_avg.reset_index()[['PLAYER', 'PLAYER_ID']]
            # Find the player ID for the given player name
            player_df = df[['PLAYER', 'PLAYER_ID']]
            players_id = player_df[player_df['PLAYER'] == player_name]['PLAYER_ID'].iloc[0]

            player_logs = playergamelog.PlayerGameLog(player_id=players_id)
            player_logs_df = player_logs.get_data_frames()[0]
            return player_logs_df.to_dict()

    return "test"



@app.route('/api/player/careerStats', methods=['POST'])
def player_career_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
    return "This is a test flask api setup!  :)"

@app.route('/api/player/careerAccolades', methods=['POST'])
def player_career_accolades():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
    return "This is a test flask api setup!  :)"

@app.route('/api/player/playoffStats', methods=['POST'])
def player_playoff_stats():
    if request.is_json:
        # Get player name
        player_name = request.get_json()['playerName']
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
