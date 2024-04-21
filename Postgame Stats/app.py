from flask import Flask
from nba_api.stats.endpoints import playergamelog

app = Flask(__name__)


@app.route('/api/player/seasonStats', methods=['GET'])
def player_season_stats():
    # LeBron James' player ID
    lebron_id = '2544'

    # Fetching game logs for LeBron James for the latest season
    player_logs = playergamelog.PlayerGameLog(player_id=lebron_id)
    player_logs_df = player_logs.get_data_frames()[0]
    # json
    return player_logs_df.to_dict()

@app.route('/api/player/careerStats')
def player_career_stats():
    return "This is a test flask api setup!  :)"

@app.route('/api/player/careerAccolades')
def player_career_accolades():
    return "This is a test flask api setup!  :)"

@app.route('/api/player/playoffStats')
def player_playoff_stats():
    return "This is a test flask api setup!  :)"

@app.route('/api/team/seasonStats')
def team_season_stats():
    # Be sure to include any advanced stats
    return "This is a test flask api setup!  :)"

@app.route('/api/team/careerStats')
def team_career_stats():
    return "This is a test flask api setup!  :)"

@app.route('/api/team/careerAccolades')
def team_career_accolades():
    return "This is a test flask api setup!  :)"

@app.route('/api/team/playoffStats')
def team_playoff_stats():
    return "This is a test flask api setup!  :)"







if __name__ == '__main__':
    app.run()
