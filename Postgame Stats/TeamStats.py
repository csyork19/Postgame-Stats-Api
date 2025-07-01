from flask import jsonify
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
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


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, Arc

# Draw NCAA court
def draw_ncaa_court(ax=None, color="black", lw=1, outer_lines=False):
    if ax is None:
        ax = plt.gca()

    # Court elements (in inches)
    hoop = Circle((250, 47.5), radius=7.5, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((220, 40), 60, 1, linewidth=lw, color=color)
    paint = Rectangle((190, 0), 120, 190, linewidth=lw, color=color, fill=False)
    free_throw_top = Arc((250, 190), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color)
    free_throw_bottom = Arc((250, 190), 120, 120, theta1=180, theta2=0, linestyle='dashed', linewidth=lw, color=color)
    restricted = Arc((250, 47.5), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    three_arc = Arc((250, 47.5), 442.92, 442.92, theta1=-12.4, theta2=192.4, linewidth=lw, color=color)

    elements = [hoop, backboard, paint, free_throw_top, free_throw_bottom, restricted, three_arc]
    if outer_lines:
        outer = Rectangle((0, 0), 500, 470, linewidth=lw, color=color, fill=False)
        elements.append(outer)

    for element in elements:
        ax.add_patch(element)

    return ax

# Normalize shots to inches and flip Y
def normalize_shots(x_vals, y_vals):
    x = np.array(x_vals)  # feet to inches
    y = np.array(y_vals)
    return x, y

# Load data
df = pd.read_csv('game_play_by_play.csv')
df.columns = df.columns.str.strip()

player_name = input("Enter player name: ")
player_data = df[df['play_desc'].str.contains(player_name, na=False)]
player_data = player_data.dropna(subset=['shot_x', 'shot_y'])

if not player_data.empty:
    x, y = normalize_shots(player_data['shot_x'], player_data['shot_y'])

    fig, ax = plt.subplots(figsize=(12, 10))
    draw_ncaa_court(ax, outer_lines=True)

    ax.scatter(x, y, c='red', edgecolors='black', alpha=0.7)
    plt.title(f"{player_name}'s NCAA Shot Chart")
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 470)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("#F5DEB3")
    plt.show()
else:
    print("No shots found for that player.")
