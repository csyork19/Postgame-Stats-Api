from flask import jsonify
from nba_api.stats.endpoints import TeamGameLogs
from nba_api.stats.static import teams


def get_team_season_stats(self, year):
    nba_teams = teams.get_teams()

    # Find the team ID based on the team name
    team_id = None
    for team in nba_teams:
        if team['full_name'].lower() == self.lower():
            team_id = team['id']
            break

    if team_id is None:
        return jsonify({'error': 'Team not found'}), 404

    return TeamGameLogs(
        league_id_nullable='00',  # nba 00, g_league 20, wnba 10
        team_id_nullable=team_id,
        season_nullable=year,
        season_type_nullable='Regular Season'  # Regular Season, Playoffs, Pre Season
    ).get_data_frames()[0].to_dict(orient="records")


def get_team_playoff_stats(self, year):
    nba_teams = teams.get_teams()

    # Find the team ID based on the team name
    team_id = None
    for team in nba_teams:
        if team['full_name'].lower() == self.lower():
            team_id = team['id']
            break

    if team_id is None:
        return jsonify({'error': 'Team not found'}), 404

    # Fetch the game logs for the team
    playoff_season_team_stats = TeamGameLogs(
        league_id_nullable='00',  # nba 00, g_league 20, wnba 10
        team_id_nullable=team_id,
        season_nullable=year,
        season_type_nullable='Playoffs'  # Regular Season, Playoffs, Pre Season
    )


    return playoff_season_team_stats.get_data_frames()[0].to_dict(orient="records")





