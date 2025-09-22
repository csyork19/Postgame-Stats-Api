from datetime import time
from io import BytesIO
import requests
from scipy.stats import percentileofscore
from nba_api.stats.endpoints import playergamelog, playercareerstats
import seaborn as sns
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.patches import Circle, Rectangle, Arc
import Const
import PostGameStatsUtil
from matplotlib.patches import RegularPolygon
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import ListedColormap, BoundaryNorm
from PIL import Image
from nba_api.stats.endpoints import shotchartdetail
from tqdm import tqdm  # for progress bar
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
import pandas as pd
import time
import matplotlib.pyplot as plt
import os
from matplotlib.path import Path   # ✅ not pathlib.Path


sns.set_style('white')
sns.set_color_codes()
plt.switch_backend('Agg')
pd.options.display.max_columns = None

global player_id


def get_team_games(team_name: str, season_id: str) -> dict:
    nba_team_id = PostGameStatsUtil.PostGameStatsUtil.get_team_id(team_name)
    nba_game_finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=nba_team_id, season_nullable=season_id)
    nba_games = nba_game_finder.get_data_frames()[0]
    return nba_games[['GAME_ID', 'MATCHUP']]


def get_opponent_shots_against_team(team_name: str, season_id: str, season_type):
    nba_games = get_team_games(team_name, season_id)
    nba_team_id = PostGameStatsUtil.PostGameStatsUtil.get_team_id(team_name)
    all_opponent_shots = []
    for _, row in tqdm(nba_games.iterrows(), total=len(nba_games)):
        game_id = row['GAME_ID']
        shots = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=0,
            game_id_nullable=game_id,
            season_type_all_star=season_type,
            context_measure_simple="FGA"
        ).get_data_frames()[0]
        opponent_shots = shots[shots['TEAM_ID'] != nba_team_id]
        all_opponent_shots.append(opponent_shots)
    full_df = pd.concat(all_opponent_shots, ignore_index=True)
    return full_df


def get_nba_player_shot_chart_information(player_name: str, season_id: str, season_type: str, game_id: str):
    nba_player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
    career = playercareerstats.PlayerCareerStats(player_id=nba_player_id)
    career_df = career.get_data_frames()[0]
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']
    shot_chart_list = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=nba_player_id,
        season_type_all_star=season_type,
        season_nullable=season_id,
        game_id_nullable=game_id if game_id is not None else None,
        context_measure_simple="FGA").get_data_frames()
    return shot_chart_list[0], shot_chart_list[1], nba_player_id


def get_wnba_player_shot_chart_information(player_name: str, season_id: str, season_type: str, game_id: str):
    nba_player_id = PostGameStatsUtil.PostGameStatsUtil.get_wnba_player_id(player_name)
    career = playercareerstats.PlayerCareerStats(player_id=nba_player_id,
                                                 league_id_nullable="10")
    career_df = career.get_data_frames()[0]
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']
    shot_chart_list = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=nba_player_id,
        league_id='10',
        season_type_all_star=season_type,
        season_nullable=season_id,
        game_id_nullable=game_id if game_id is not None else None,
        context_measure_simple="FGA").get_data_frames()
    return shot_chart_list[0], shot_chart_list[1], nba_player_id


def get_team_shot_chart_updated(team_name: str, season_id: str, season_type: str, game_id: str):
    nba_team_id = PostGameStatsUtil.PostGameStatsUtil.get_team_id(team_name)
    shot_chart_list = shotchartdetail.ShotChartDetail(
        team_id=nba_team_id,
        player_id=0,  # Use 0 or omit this parameter
        season_type_all_star=season_type,
        season_nullable=season_id,
        game_id_nullable=game_id if game_id is not None else None,
        context_measure_simple="FGA"
    ).get_data_frames()
    return shot_chart_list[0], shot_chart_list[1]


def get_player_per_game_shot_chart(player_name: str, season_id: str, game_id: str):
    nba_player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
    career = playercareerstats.PlayerCareerStats(player_id=nba_player_id)
    career_df = career.get_data_frames()[0]
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']
    shot_chart_list = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=nba_player_id,
        season_type_all_star='Regular Season',
        season_nullable=season_id,
        game_id_nullable=game_id,
        context_measure_simple="FGA"
    ).get_data_frames()
    return shot_chart_list[0]


def get_nba_finals_player_shot_chart_information(player_name: str, season_id: str, game_id: str):
    nba_player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
    game_finder = leaguegamefinder.LeagueGameFinder(
        player_id_nullable=nba_player_id,
        season_type_nullable='Playoffs',
        season_nullable=season_id
    )
    all_games = game_finder.get_data_frames()[0]
    finals_games = all_games[all_games['GAME_ID'].str.contains('00424004')]
    finals_game_ids = finals_games['GAME_ID'].unique().tolist()
    team_id = finals_games.iloc[0]['TEAM_ID'] if not finals_games.empty else None
    if not team_id:
        raise ValueError(f"No Finals games found for {player_name} in {season_id}.")

    shot_chart = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=nba_player_id,
        season_type_all_star='Playoffs',
        season_nullable=season_id,
        context_measure_simple="FGA").get_data_frames()[0]
    shot_chart_finals = shot_chart[shot_chart['GAME_ID'].isin(finals_game_ids)]
    return shot_chart_finals


def get_nba_finals_team_per_game_shot_chart_information(team_name: str, season_id: str, game_id_prefix="004"):
    nba_team_id = PostGameStatsUtil.PostGameStatsUtil.get_team_id(team_name)
    game_finder = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=nba_team_id,
        season_type_nullable='Playoffs',
        season_nullable=season_id
    )
    all_games = game_finder.get_data_frames()[0]
    finals_games = all_games[all_games['GAME_ID'].str.startswith(game_id_prefix)]
    finals_game_ids = finals_games['GAME_ID'].unique().tolist()

    if not finals_game_ids:
        raise ValueError(f"No Finals games found for {team_name} in {season_id}.")

    shot_chart = shotchartdetail.ShotChartDetail(
        team_id=nba_team_id,
        player_id=0,  # 0 = all players (i.e., team)
        season_type_all_star='Playoffs',
        season_nullable=season_id,
        context_measure_simple="FGA"
    ).get_data_frames()[0]
    shot_chart_finals = shot_chart[shot_chart['GAME_ID'].isin(finals_game_ids)]
    grouped_by_game = {
        game_id: group_df.reset_index(drop=True)
        for game_id, group_df in shot_chart_finals.groupby("GAME_ID")
    }

    return grouped_by_game


def draw_nba_court(ax=None, color="white", lw=1, shotzone=False, outer_lines=False, flip=False):
    if ax is None:
        ax = plt.gca()
    OFFSET_Y = 95

    def adjust_y(y):
        if flip:
            return 422.5 - y + OFFSET_Y  # Flip around the court's midpoint and apply offset
        return y + OFFSET_Y  # Just apply offset

    hoop = Circle((0, adjust_y(0)), radius=7.5, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-30, adjust_y(-7.5)), 60, 1, linewidth=lw, color=color, fill=False)
    paint_outer = Rectangle((-80, adjust_y(-47.5)), 160, 190, linewidth=lw, color=color, fill=False)
    paint_inner = Rectangle((-60, adjust_y(-47.5)), 120, 190, linewidth=lw, color=color, fill=False)

    # Adjust arc angles based on flip
    if flip:
        free_throw_top = Arc((0, adjust_y(142.5)), 120, 120, theta1=180, theta2=360, linewidth=lw, color=color)
        free_throw_bottom = Arc((0, adjust_y(142.5)), 120, 120, theta1=0, theta2=180, linestyle='dashed', linewidth=lw,
                                color=color)
    else:
        free_throw_top = Arc((0, adjust_y(142.5)), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color)
        free_throw_bottom = Arc((0, adjust_y(142.5)), 120, 120, theta1=180, theta2=0, linestyle='dashed', linewidth=lw,
                                color=color)

    restricted = Arc((0, adjust_y(0)), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    corner_three_left = Rectangle((-220, adjust_y(-47.0)), 0, 140, linewidth=lw, color=color)
    corner_three_right = Rectangle((220, adjust_y(-47.0)), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, adjust_y(0)), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
    baseline = Rectangle((-250, adjust_y(-48)), 500, 0, linewidth=lw, color=color)

    court_elements = [hoop, backboard, paint_outer, paint_inner, free_throw_top, free_throw_bottom, restricted,
                      corner_three_left, corner_three_right, three_arc, baseline]

    if outer_lines:
        outer = Rectangle((-250, adjust_y(-47.5)), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer)

    for element in court_elements:
        ax.add_patch(element)

    return ax


def draw_shot_chart(data, player_name: str, year: str, title="", color="b", xlim=(-250, 250), ylim=(422.5, -47.5),
                    line_color="blue", court_color="black", court_lw=2, outer_lines=False, flip_court=True,
                    gridsize=None,
                    ax=None, despine=False, player_image_path='curry.png', **kwargs):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 11))  # Ensure it draws a figure
    else:
        fig = ax.figure

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_title(f'{player_name} {year} Shot Chart', fontsize=18)

    # Draw court
    draw_nba_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    # Separate data by make or miss
    x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']

    # Plot missed and made shots
    ax.scatter(x_missed, y_missed, c='r', marker="x", s=300, linewidths=3, **kwargs)
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='g', marker="o", s=100, linewidths=3, **kwargs)

    # Set spines
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        for spine in ["top", "bottom", "right", "left"]:
            ax.spines[spine].set_visible(False)

    add_player_image_to_shot_chart(ax, player_image_path, player_name, xlim, ylim)
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    file_name = os.path.join(save_directory, f"{player_name}_{year}_regular_season_shot_chart.png")
    fig.savefig(file_name, dpi=300)
    plt.close(fig)
    return file_name


def add_player_image_to_shot_chart(ax, player_image_path, player_name, xlim, ylim):
    if player_image_path and os.path.exists(player_image_path):
        player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
        url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
        try:
            img = Image.open(BytesIO(requests.get(url).content)).convert("RGB")
            imagebox = OffsetImage(img, zoom=.5)
            ab = AnnotationBbox(imagebox, (xlim[0] + 500, ylim[1]), frameon=False)
            ax.add_artist(ab)
        except Exception as e:
            print(f"Could not load image for player {player_id}: {e}")


from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
from scipy.stats import percentileofscore

def sized_hexbin(ax, hc, hc2, cmap, norm):
    offsets = hc.get_offsets()
    orgpath = hc.get_paths()[0]
    verts = orgpath.vertices
    values1 = hc.get_array()
    values2 = hc2.get_array()

    patches = []
    filtered_list = [v for v in values1 if v != 0]

    for offset, val in zip(offsets, values1):
        if int(val) == 0:
            continue

        pct = percentileofscore(filtered_list, val)
        if pct < 33.33:
            v1 = verts * 0.3 + offset
        elif pct > 69.99:
            v1 = verts + offset
        else:
            v1 = verts * 0.6 + offset

        # ✅ Correct: Path takes (vertices, codes)
        path = Path(v1, orgpath.codes)
        patch = PathPatch(path)
        patches.append(patch)

    pc = PatchCollection(patches, cmap=cmap, norm=norm)
    pc.set_array(values2)  # sets color mapping
    ax.add_collection(pc)

    hc.remove()
    hc2.remove()

    return pc


def hexmap_chart(nba_shot_data: any, nba_league_average_shots: any, nba_player_name: str, nba_season: str,
                 season_type: str, player_id: str, title="", color="b", xlim=(-250, 250), ylim=None, line_color="black",
                 court_color="#FFFFFF", court_lw=2, outer_lines=False, flip_court=True, gridsize=None, ax=None,
                 despine=False, **kwargs):
    # 1. Set default y-axis limits
    ylim = (470, -60)  # Original court orientation (hoop at y=0)

    # 2. Flip shot data if needed (to match court orientation)
    if flip_court:
        nba_shot_data = nba_shot_data.copy()
        nba_shot_data['LOC_Y'] = 422.5 - nba_shot_data['LOC_Y']

    # 3. Create figure and axis
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)

    # 4. Draw court (in original orientation, we'll flip the axis)
    draw_nba_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines, flip=False)

    # 5. Set axis range and aspect
    ax.set_xlim(xlim)
    if flip_court:
        ax.set_ylim(470, -60)  # Expanded limits to prevent cutoff (hoop at bottom)
    else:
        ax.set_ylim(470, -60)  # Original axis (hoop at bottom)
    ax.set_aspect('equal')

    # 6. Plot hex data
    nba_shot_data, player = get_player_data_and_calculate_league_average(nba_shot_data, nba_league_average_shots)
    boundaries, cmap = plot_nba_player_shot_chart_data_v2(ax, nba_shot_data, player)
    create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig)

    # 7. Style axes
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        for side in ["top", "bottom", "right", "left"]:
            ax.spines[side].set_visible(False)

    # 8. Player photo/stats overlays
    assist, blocks, fg, fg3, plus_minus, points, rebounds, season, steals = add_player_stats_to_shot_chart(
        nba_player_name, nba_season, season_type, player_id)
    add_player_image_to_chart(ax, player_id, xlim, ylim)
    add_project_logo_image_to_chart(ax, "right")
    add_shot_chart_header_info(assist, blocks, fg, fg3, fig, plus_minus, points, rebounds, season, steals,
                               nba_player_name, season_type, "black", "gray")

    # 9. Save chart
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    file_name = os.path.join(save_directory, f"{nba_player_name}_{season}_{season_type}_hexmap_chart.png")
    plt.savefig(file_name, dpi=300, bbox_inches=None, pad_inches=0)

    plt.close()
    return file_name


def team_hexmap_chart(data, league_avg, nba_team_name, nba_season, season_type, game_id, title="", color="b",
                      xlim=(-250, 250), ylim=None, line_color="black",
                      court_color="#FFFFFF", court_lw=2, outer_lines=False,
                      flip_court=True, gridsize=None,
                      ax=None, despine=False, **kwargs):
    import matplotlib.pyplot as plt
    import os

    # 1. Set default y-axis limits
    ylim = (470, -60)  # Original court orientation (hoop at y=0)

    # 2. Flip shot data if needed (to match court orientation)
    if flip_court:
        data = data.copy()
        data['LOC_Y'] = 422.5 - data['LOC_Y']

    # 3. Create figure and axis
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)

    # 4. Draw court (in original orientation, we'll flip the axis)
    draw_nba_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines, flip=False)

    # 5. Set axis range and aspect
    ax.set_xlim(xlim)
    if flip_court:
        ax.set_ylim(470, -60)  # Expanded limits to prevent cutoff (hoop at bottom)
    else:
        ax.set_ylim(470, -60)  # Original axis (hoop at bottom)
    ax.set_aspect('equal')

    # 6. Plot hex data
    data, player = get_player_data_and_calculate_league_average(data, league_avg)
    boundaries, cmap = plot_nba_player_shot_chart_data_v2(ax, data, player)
    create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig)

    # 7. Style axes
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        for side in ["top", "bottom", "right", "left"]:
            ax.spines[side].set_visible(False)

    assist, blocks, fg, fg3, team_id, points, rebounds, steals = add_team_stats_to_shot_chart(nba_team_name, nba_season,
                                                                                              season_type)
    add_team_image_to_chart(ax, nba_team_name, team_id, xlim, ylim)

    add_team_shot_chart_header_info(assist, blocks, fg, fg3, fig, points, rebounds, nba_season, steals,
                                    nba_team_name, season_type, "black")

    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    if game_id is not None:
        file_name = os.path.join(save_directory,
                                 f"{nba_team_name}_{nba_season}_{season_type}_{game_id}_hexmap_chart.png")
    else:
        file_name = os.path.join(save_directory,
                                 f"{nba_team_name}_{nba_season}_{season_type}_regular_season_hexmap_chart.png")

    plt.savefig(file_name, dpi=300, bbox_inches=None, pad_inches=0)
    plt.close()
    return file_name


def team_defense_hexmap_chart(data, league_avg, nba_team_name, nba_season, season_type, game_id, title="", color="b",
                              xlim=(-250, 250), ylim=None, line_color="black",
                              court_color="#FFFFFF", court_lw=2, outer_lines=False,
                              flip_court=True, gridsize=None,
                              ax=None, despine=False, **kwargs):
    # 1. Set default y-axis limits
    ylim = (470, -60)  # Original court orientation (hoop at y=0)

    # 2. Flip shot data if needed (to match court orientation)
    if flip_court:
        data = data.copy()
        data['LOC_Y'] = 422.5 - data['LOC_Y']

    # 3. Create figure and axis
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)

    # 4. Draw court (in original orientation, we'll flip the axis)
    draw_nba_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines, flip=False)

    # 5. Set axis range and aspect
    ax.set_xlim(xlim)
    if flip_court:
        ax.set_ylim(470, -60)  # Expanded limits to prevent cutoff (hoop at bottom)
    else:
        ax.set_ylim(470, -60)  # Original axis (hoop at bottom)
    ax.set_aspect('equal')

    # 6. Plot hex data
    data, player = get_team_defense_data_and_league_avg(data, league_avg)
    boundaries, cmap = plot_team_defense_shot_chart(ax, data, player)
    # create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig)

    # 7. Style axes
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        for side in ["top", "bottom", "right", "left"]:
            ax.spines[side].set_visible(False)

    fig.text(0.5, 0.96, f"{nba_team_name} {nba_season} Defensive {season_type} Performance. \n"
                        f"{nba_team_name} team defensive stats vs NBA League as a whole. ",
             ha='center', va='top', fontsize=16, fontweight='bold')
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    if game_id is not None:
        file_name = os.path.join(save_directory,
                                 f"{nba_team_name}_{nba_season}_{season_type}_{game_id}_defense hexmap_chart.png")
    else:
        file_name = os.path.join(save_directory,
                                 f"{nba_team_name}_{nba_season}_{season_type}_defense regular_season_hexmap_chart.png")

    plt.savefig(file_name, dpi=300, bbox_inches=None, pad_inches=0)
    plt.close()
    return file_name


def team_hexmap_playoff_chart(data, league_avg, nba_team_name, nba_season, title="", color="b",
                              xlim=(-250, 250), ylim=None, line_color="black",
                              court_color="#FFFFFF", court_lw=2, outer_lines=False,
                              flip_court=True, gridsize=None,
                              ax=None, despine=False, **kwargs):
    import matplotlib.pyplot as plt
    import os

    # 1. Set default y-axis limits
    ylim = (470, -60)  # Original court orientation (hoop at y=0)

    # 2. Flip shot data if needed (to match court orientation)
    if flip_court:
        data = data.copy()
        data['LOC_Y'] = 422.5 - data['LOC_Y']

    # 3. Create figure and axis
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)

    # 4. Draw court (in original orientation, we'll flip the axis)
    draw_nba_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines, flip=False)

    # 5. Set axis range and aspect
    ax.set_xlim(xlim)
    if flip_court:
        ax.set_ylim(470, -60)  # Expanded limits to prevent cutoff (hoop at bottom)
    else:
        ax.set_ylim(470, -60)  # Original axis (hoop at bottom)
    ax.set_aspect('equal')

    # 6. Plot hex data
    data, player = get_player_data_and_calculate_league_average(data, league_avg)
    boundaries, cmap = plot_nba_player_shot_chart_data_v2(ax, data, player)
    create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig)

    # 7. Style axes
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        for side in ["top", "bottom", "right", "left"]:
            ax.spines[side].set_visible(False)

    assist, blocks, fg, fg3, team_id, points, rebounds, steals = add_team_playoff_stats_to_shot_chart(nba_team_name,
                                                                                                      nba_season)
    add_team_image_to_chart(ax, nba_team_name, team_id, xlim, ylim)

    add_team_playoff_shot_chart_header_info(assist, blocks, fg, fg3, fig, points, rebounds, nba_season, steals,
                                            nba_team_name)

    # 9. Save chart
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    file_name = os.path.join(save_directory, f"{nba_team_name}_{nba_season}_playoff_hexmap_chart.png")
    plt.savefig(file_name, dpi=300, bbox_inches=None, pad_inches=0)

    plt.close()
    return file_name


def add_shot_chart_header_info(assist, blocks, fg, fg3, fig, plus_minus, points, rebounds, season, steals, player_name,
                               season_type, color, sub_color):
    top_row_y_val = 0.90
    bottom_row_y_val = 0.80
    x_spacing = 0.15  # a bit more spacing for label next to value
    x_start = 0.28
    horizontal_label_offset = 0.015  # distance to right of the value
    vertical_label_offset = -0.01
    stat_values = [points, fg, fg3, assist, blocks, rebounds, steals, plus_minus]
    stat_labels = ["PPG", "FG%", "3P%", "AST", "BLK", "REB", "STL", "+/-"]
    for i, (val, label) in enumerate(zip(stat_values, stat_labels)):
        row = 0 if i < 4 else 1
        col = i % 4
        x_val = x_start + col * x_spacing
        y_val = top_row_y_val if row == 0 else bottom_row_y_val
        x_label = x_val + horizontal_label_offset
        y_label = y_val + vertical_label_offset

        # Format value
        if isinstance(val, float):
            val_text = f"{val:.2f}".lstrip("0") if "%" in label else f"{val:.1f}"
        else:
            val_text = str(val)

        fig.text(x_val, y_val, val_text, fontsize=35, fontweight='bold', ha='right', va='center', color=color)
        fig.text(x_label, y_label, label, fontsize=10, color=sub_color, ha='left', va='center')
    # Optional stat block title
    fig.text(0.5, 0.96, f"{player_name} {season} {season_type} Performance",
             ha='center', va='top', fontsize=16, fontweight='bold', color=color)


def add_playoff_shot_chart_header_info(assist, blocks, fg, fg3, fig, plus_minus, points, rebounds, season, steals,
                                       player_name):
    top_row_y_val = 0.90
    bottom_row_y_val = 0.80
    x_spacing = 0.15  # a bit more spacing for label next to value
    x_start = 0.28
    horizontal_label_offset = 0.015  # distance to right of the value
    vertical_label_offset = -0.01
    stat_values = [points, fg, fg3, assist, blocks, rebounds, steals, plus_minus]
    stat_labels = ["PPG", "FG%", "3P%", "AST", "BLK", "REB", "STL", "+/-"]
    for i, (val, label) in enumerate(zip(stat_values, stat_labels)):
        row = 0 if i < 4 else 1
        col = i % 4
        x_val = x_start + col * x_spacing
        y_val = top_row_y_val if row == 0 else bottom_row_y_val
        x_label = x_val + horizontal_label_offset
        y_label = y_val + vertical_label_offset

        # Format value
        if isinstance(val, float):
            val_text = f"{val:.2f}".lstrip("0") if "%" in label else f"{val:.1f}"
        else:
            val_text = str(val)

        fig.text(x_val, y_val, val_text, fontsize=35, fontweight='bold', ha='right', va='center', color='black')
        fig.text(x_label, y_label, label, fontsize=10, color='gray', ha='left', va='center')
    # Optional stat block title
    fig.text(0.5, 0.96, f"{player_name} {season} Playoff Performance",
             ha='center', va='top', fontsize=16, fontweight='bold')


def add_team_shot_chart_header_info(assist, blocks, fg, fg3, fig, points, rebounds, season, steals,
                                    player_name, season_type, color):
    top_row_y_val = 0.90
    bottom_row_y_val = 0.80
    x_spacing = 0.15  # a bit more spacing for label next to value
    x_start = 0.28
    horizontal_label_offset = 0.015  # distance to right of the value
    vertical_label_offset = -0.01
    stat_values = [points, fg, fg3, assist, blocks, rebounds, steals]
    stat_labels = ["PPG", "FG%", "3P%", "AST", "BLK", "REB", "STL"]
    for i, (val, label) in enumerate(zip(stat_values, stat_labels)):
        row = 0 if i < 4 else 1
        col = i % 4
        x_val = x_start + col * x_spacing
        y_val = top_row_y_val if row == 0 else bottom_row_y_val
        x_label = x_val + horizontal_label_offset
        y_label = y_val + vertical_label_offset

        # Format value
        if isinstance(val, float):
            val_text = f"{val:.2f}".lstrip("0") if "%" in label else f"{val:.1f}"
        else:
            val_text = str(val)

        fig.text(x_val, y_val, val_text, fontsize=35, fontweight='bold', ha='right', va='center', color=color)
        fig.text(x_label, y_label, label, fontsize=10, color=color, ha='left', va='center')
    fig.text(0.5, 0.96, f"{player_name} {season} {season_type} Performance",
             ha='center', va='top', fontsize=16, fontweight='bold', color=color)


def add_team_playoff_shot_chart_header_info(assist, blocks, fg, fg3, fig, points, rebounds, season, steals,
                                            player_name):
    top_row_y_val = 0.90
    bottom_row_y_val = 0.80
    x_spacing = 0.15  # a bit more spacing for label next to value
    x_start = 0.28
    horizontal_label_offset = 0.015  # distance to right of the value
    vertical_label_offset = -0.01
    stat_values = [points, fg, fg3, assist, blocks, rebounds, steals]
    stat_labels = ["PPG", "FG%", "3P%", "AST", "BLK", "REB", "STL"]
    for i, (val, label) in enumerate(zip(stat_values, stat_labels)):
        row = 0 if i < 4 else 1
        col = i % 4
        x_val = x_start + col * x_spacing
        y_val = top_row_y_val if row == 0 else bottom_row_y_val
        x_label = x_val + horizontal_label_offset
        y_label = y_val + vertical_label_offset

        # Format value
        if isinstance(val, float):
            val_text = f"{val:.2f}".lstrip("0") if "%" in label else f"{val:.1f}"
        else:
            val_text = str(val)

        fig.text(x_val, y_val, val_text, fontsize=35, fontweight='bold', ha='right', va='center', color='black')
        fig.text(x_label, y_label, label, fontsize=10, color='gray', ha='left', va='center')
    # Optional stat block title
    fig.text(0.5, 0.96, f"{player_name} {season} Playoff Performance",
             ha='center', va='top', fontsize=16, fontweight='bold')


def add_playoff_finals_shot_chart_header_info(assist, blocks, fg, fg3, fig, plus_minus, points, rebounds, season,
                                              steals, player_name):
    top_row_y_val = 0.90
    bottom_row_y_val = 0.80
    x_spacing = 0.15  # a bit more spacing for label next to value
    x_start = 0.28
    horizontal_label_offset = 0.015  # distance to right of the value
    vertical_label_offset = -0.01
    stat_values = [points, fg, fg3, assist, blocks, rebounds, steals, plus_minus]
    stat_labels = ["PPG", "FG%", "3P%", "AST", "BLK", "REB", "STL", "+/-"]
    for i, (val, label) in enumerate(zip(stat_values, stat_labels)):
        row = 0 if i < 4 else 1
        col = i % 4
        x_val = x_start + col * x_spacing
        y_val = top_row_y_val if row == 0 else bottom_row_y_val
        x_label = x_val + horizontal_label_offset
        y_label = y_val + vertical_label_offset

        # Format value
        if isinstance(val, float):
            val_text = f"{val:.2f}".lstrip("0") if "%" in label else f"{val:.1f}"
        else:
            val_text = str(val)

        fig.text(x_val, y_val, val_text, fontsize=35, fontweight='bold', ha='right', va='center', color='black')
        fig.text(x_label, y_label, label, fontsize=10, color='gray', ha='left', va='center')
    # Optional stat block title
    fig.text(0.5, 0.96, f"{player_name} {season} Finals Playoff Performance",
             ha='center', va='top', fontsize=16, fontweight='bold')


def add_player_stats_to_shot_chart(nba_player_name, nba_season, season_type, playerId):
    season = nba_season
    if nba_player_name == 'Luka Doncic':
        player_id = 1629029
    else:
        player_id = playerId
    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV"]
    nba_player_logs = \
        playergamelog.PlayerGameLog(player_id=player_id, season=season,
                                    season_type_all_star=season_type).get_data_frames()[
            0]
    nba_player_season_average = nba_player_logs[nba_player_stat_columns].mean().round(2).to_dict()
    points = nba_player_season_average['PTS']
    fg = nba_player_season_average['FG_PCT']
    fg3 = nba_player_season_average['FG3_PCT']
    plus_minus = nba_player_season_average['PLUS_MINUS']
    assist = nba_player_season_average['AST']
    blocks = nba_player_season_average['BLK']
    rebounds = nba_player_season_average['REB']
    steals = nba_player_season_average['STL']
    return assist, blocks, fg, fg3, plus_minus, points, rebounds, season, steals


def add_team_stats_to_shot_chart(nba_team_name, nba_season, season_type):
    team_dict = [team for team in teams.get_teams() if team['full_name'] == nba_team_name][0]
    team_id = team_dict['id']

    nba_team_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PTS", "REB", "STL", "TOV"
    ]

    team_logs_df = teamgamelog.TeamGameLog(team_id=team_id, season=nba_season,
                                           season_type_all_star=season_type).get_data_frames()[0]

    # Convert column names if needed (some may be prefixed like "TEAM_")
    team_logs_df.columns = [col.replace("TEAM_", "") for col in team_logs_df.columns]

    team_season_average = team_logs_df[nba_team_stat_columns].mean().round(2).to_dict()

    points = team_season_average['PTS']
    fg = team_season_average['FG_PCT']
    fg3 = team_season_average['FG3_PCT']
    assist = team_season_average['AST']
    blocks = team_season_average['BLK']
    rebounds = team_season_average['REB']
    steals = team_season_average['STL']

    return assist, blocks, fg, fg3, team_id, points, rebounds, steals


def add_team_playoff_stats_to_shot_chart(nba_team_name, nba_season):
    team_dict = [team for team in teams.get_teams() if team['full_name'] == nba_team_name][0]
    team_id = team_dict['id']

    nba_team_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PTS", "REB", "STL", "TOV"
    ]

    team_logs_df = teamgamelog.TeamGameLog(team_id=team_id, season=nba_season,
                                           season_type_all_star='Playoffs').get_data_frames()[0]

    # Convert column names if needed (some may be prefixed like "TEAM_")
    team_logs_df.columns = [col.replace("TEAM_", "") for col in team_logs_df.columns]

    team_season_average = team_logs_df[nba_team_stat_columns].mean().round(2).to_dict()

    points = team_season_average['PTS']
    fg = team_season_average['FG_PCT']
    fg3 = team_season_average['FG3_PCT']
    assist = team_season_average['AST']
    blocks = team_season_average['BLK']
    rebounds = team_season_average['REB']
    steals = team_season_average['STL']

    return assist, blocks, fg, fg3, team_id, points, rebounds, steals


def get_player_playoff_stats_to_shot_chart(nba_player_name, nba_season):
    season = nba_season
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(str(nba_player_name))
    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV"]
    nba_player_logs = \
        playergamelog.PlayerGameLog(player_id=player_id, season=season,
                                    season_type_all_star='Playoffs').get_data_frames()[
            0]
    nba_player_season_average = nba_player_logs[nba_player_stat_columns].mean().round(2).to_dict()
    points = nba_player_season_average['PTS']
    fg = nba_player_season_average['FG_PCT']
    fg3 = nba_player_season_average['FG3_PCT']
    assist = nba_player_season_average['AST']
    blocks = nba_player_season_average['BLK']
    rebounds = nba_player_season_average['REB']
    plus_minus = nba_player_season_average['PLUS_MINUS']
    steals = nba_player_season_average['STL']
    return assist, blocks, fg, fg3, player_id, points, rebounds, season, steals, plus_minus


def get_player_finals_stats_to_shot_chart(nba_player_name, nba_season):
    season = nba_season
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(str(nba_player_name))
    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV", "Game_ID"]

    nba_player_logs = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season,
        season_type_all_star='Playoffs'
    ).get_data_frames()[0]

    # Filter for finals games (Game_ID contains "40")
    finals_games = nba_player_logs[nba_player_logs['Game_ID'].str.contains("00424004")]

    # Compute the mean only for those games
    nba_player_finals_average = finals_games[nba_player_stat_columns].mean(numeric_only=True).round(2).to_dict()

    points = nba_player_finals_average.get('PTS', 0)
    fg = nba_player_finals_average.get('FG_PCT', 0)
    fg3 = nba_player_finals_average.get('FG3_PCT', 0)
    plus_minus = nba_player_finals_average.get('PLUS_MINUS', 0)
    assist = nba_player_finals_average.get('AST', 0)
    blocks = nba_player_finals_average.get('BLK', 0)
    rebounds = nba_player_finals_average.get('REB', 0)
    steals = nba_player_finals_average.get('STL', 0)

    return assist, blocks, fg, fg3, player_id, plus_minus, points, rebounds, season, steals


def hexmap_playoff_chart(data, league_avg, nba_player_name, nba_season, title="", color="b",
                         xlim=(-250, 250), ylim=(422.5, -47.5), line_color="black",
                         court_color="#FFFFFF", court_lw=2, outer_lines=False,
                         flip_court=True, gridsize=None,
                         ax=None, despine=False, **kwargs):
    import matplotlib.pyplot as plt
    import os

    # 1. Set default y-axis limits
    ylim = (470, -60)  # Original court orientation (hoop at y=0)

    # 2. Flip shot data if needed (to match court orientation)
    if flip_court:
        data = data.copy()
        data['LOC_Y'] = 422.5 - data['LOC_Y']

    # 3. Create figure and axis
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)

    # 4. Draw court (in original orientation, we'll flip the axis)
    draw_nba_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines, flip=False)

    # 5. Set axis range and aspect
    ax.set_xlim(xlim)
    if flip_court:
        ax.set_ylim(470, -60)  # Expanded limits to prevent cutoff (hoop at bottom)
    else:
        ax.set_ylim(470, -60)  # Original axis (hoop at bottom)
    ax.set_aspect('equal')

    # 6. Plot hex data
    data, player = get_player_data_and_calculate_league_average(data, league_avg)
    boundaries, cmap = plot_nba_player_shot_chart_data_v2(ax, data, player)
    create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig)

    # 7. Style axes
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        for side in ["top", "bottom", "right", "left"]:
            ax.spines[side].set_visible(False)

    # 8. Player photo/stats overlays
    assist, blocks, fg, fg3, player_id, points, rebounds, season, steals, plus_minus = get_player_playoff_stats_to_shot_chart(
        nba_player_name, nba_season)
    add_player_image_to_chart(ax, player_id, xlim, ylim)
    add_local_image_bottom_right(ax, '')
    add_playoff_shot_chart_header_info(assist, blocks, fg, fg3, fig, plus_minus, points, rebounds, season, steals,
                                       nba_player_name)

    # 9. Save chart
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    file_name = os.path.join(save_directory, f"{nba_player_name}_{season}_hexmap_playoff_chart.png")
    plt.savefig(file_name, dpi=300, bbox_inches=None, pad_inches=0)

    plt.close()
    return file_name


def hexmap_finals_playoff_chart(data, league_avg, nba_player_name, nba_season, game_id, title="", color="b",
                                xlim=(-250, 250), ylim=(422.5, -47.5), line_color="black",
                                court_color="#FFFFFF", court_lw=2, outer_lines=False,
                                flip_court=True, gridsize=None,
                                ax=None, despine=False, **kwargs):
    import matplotlib.pyplot as plt
    import os

    # 1. Set default y-axis limits
    ylim = (470, -60)  # Original court orientation (hoop at y=0)

    # 2. Flip shot data if needed (to match court orientation)
    if flip_court:
        data = data.copy()
        data['LOC_Y'] = 422.5 - data['LOC_Y']

    # 3. Create figure and axis
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)

    # 4. Draw court (in original orientation, we'll flip the axis)
    draw_nba_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines, flip=False)

    # 5. Set axis range and aspect
    ax.set_xlim(xlim)
    if flip_court:
        ax.set_ylim(470, -60)  # Expanded limits to prevent cutoff (hoop at bottom)
    else:
        ax.set_ylim(470, -60)  # Original axis (hoop at bottom)
    ax.set_aspect('equal')

    # 6. Plot hex data
    data, player = get_player_data_and_calculate_league_average(data, league_avg)
    boundaries, cmap = plot_nba_player_shot_chart_data_v2(ax, data, player)
    create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig)

    # 7. Style axes
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        for side in ["top", "bottom", "right", "left"]:
            ax.spines[side].set_visible(False)

    # 8. Player photo/stats overlays
    assist, blocks, fg, fg3, player_id, plus_minus, points, rebounds, season, steals = (
        get_player_finals_stats_to_shot_chart(nba_player_name, nba_season))
    add_player_image_to_chart(ax, player_id, xlim, ylim)
    add_playoff_finals_shot_chart_header_info(assist, blocks, fg, fg3, fig, plus_minus, points, rebounds, season,
                                              steals, nba_player_name)

    # 9. Save chart
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    file_name = os.path.join(save_directory, f"{nba_player_name}_{season}_{game_id}_hexmap_finals_playoff_chart.png")
    plt.savefig(file_name, dpi=300, bbox_inches=None, pad_inches=0)

    plt.close()
    return file_name


def add_local_image_bottom_right(ax, local_image_path):
    try:
        img = Image.open(
            '/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/shotcharts/thunder.png').convert(
            "RGB")
        imagebox = OffsetImage(img, zoom=.2)

        # Bottom-right: x=1.05 (right), y=-0.05 (bottom)
        ab = AnnotationBbox(
            imagebox,
            (1.15, -0.15),  # slightly off the axes for margin
            xycoords='axes fraction',
            frameon=False,
            box_alignment=(1, 0)  # aligns image's top-left to the given point
        )
        ax.add_artist(ab)
    except Exception as e:
        print(f"Could not load local image: {e}")


def add_player_image_to_chart(ax, player_id, xlim, ylim):
    url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
    try:
        img = Image.open(BytesIO(requests.get(url).content)).convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            # If it's close to black, make it transparent
            if item[0] < 20 and item[1] < 20 and item[2] < 20:
                newData.append((0, 0, 0, 0))  # Transparent
            else:
                newData.append(item)

        img.putdata(newData)
        imagebox = OffsetImage(img, zoom=.6)
        # Coordinates in axes fraction (0 = left/bottom, 1 = right/top)
        ab = AnnotationBbox(imagebox, (-.10, .05), xycoords='axes fraction',
                            frameon=False, box_alignment=(0, 1))
        ax.add_artist(ab)
    except Exception as e:
        print(f"Could not load image for player {player_id}: {e}")


from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from io import BytesIO
import requests

from pathlib import Path
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def add_project_logo_image_to_chart(ax):
    # Build the path in a portable way
    image_path = Path.home() / "Documents" / "Personal Projects" / "Postgame-Stats-Api" / "Postgame Stats" / "project_logo" / "PGS Logo_profile_pic-white.jpg"

    try:
        # Open directly from local path
        img = Image.open(image_path).convert("RGBA")
        imagebox = OffsetImage(img, zoom=0.6)

        # Always place in bottom-right
        ab = AnnotationBbox(
            imagebox, (1.10, .05), xycoords='axes fraction',
            frameon=False, box_alignment=(1, 1)
        )

        ax.add_artist(ab)

    except Exception as e:
        print(f"Could not load project logo: {e}")



def plot_nba_player_shot_chart_data_v2(ax, data, player):
    # Transform shot data (hexes stay unchanged)
    OFFSET = 512
    x = data['LOC_X']
    y = -data['LOC_Y'] + OFFSET

    # Color setup
    colors = ["#00008C", "#4467C4", "#ADD8E6", "#FFFF00", "#FF5C00", "#ff0000"]
    cmap = ListedColormap(colors)
    boundaries = [-100, -9, -3, 0, 3, 9, 100]
    norm = BoundaryNorm(boundaries, cmap.N, clip=True)

    # Plot hexes
    extent = [-275, 275, -50, 425]
    hexbin = ax.hexbin(x, y, gridsize=40, cmap=cmap, norm=norm, extent=extent)
    hexbin2 = ax.hexbin(x, y, C=data['FGP_DIFF'], gridsize=40, cmap=cmap, norm=norm, extent=extent)
    sized_hexbin(ax, hexbin, hexbin2, cmap, norm)

    # Flip y-values function for label placement (must use with label's raw court y coordinates)
    def flip_y(y_val):
        return -y_val + OFFSET

    # Zone mapping uses raw court coordinates (y) that must be flipped when positioning labels
    zone_mapping = {
        ('Center(C)', 'Less Than 8 ft.'): ('Restricted Area', (0, 20)),
        ('Center(C)', '8-16 ft.'): ('In The Paint (Non-RA)', (0, 80)),
        ('Center(C)', '16-24 ft.'): ('Mid-Range (Center)', (0, 180)),
        ('Left Side Center(LC)', '16-24 ft.'): ('Mid-Range (Left)', (-100, 150)),
        ('Right Side Center(RC)', '16-24 ft.'): ('Mid-Range (Right)', (100, 150)),
        ('Left Side(L)', '24+ ft.'): ('Left Corner 3', (-220, 20)),
        ('Right Side(R)', '24+ ft.'): ('Right Corner 3', (220, 20)),
        ('Center(C)', '24+ ft.'): ('Above the Break 3 (Center)', (0, 280)),
        ('Left Side Center(LC)', '24+ ft.'): ('Above the Break 3 (Left)', (-150, 250)),
        ('Right Side Center(RC)', '24+ ft.'): ('Above the Break 3 (Right)', (150, 250)),
    }

    # FG% by zone
    zone_fgp = {}
    for (area, range_), (zone_name, _) in zone_mapping.items():
        if (area, range_) in player.index:
            fgp = player.loc[(area, range_), 'FGP'] * 100
            zone_fgp[zone_name] = {
                'FGP': fgp,
                'FGM': player.loc[(area, range_), 'Makes'],
                'FGA': player.loc[(area, range_), 'FGA']
            }

    # Draw FG% annotations with flipped y values to match hexbin coordinate system
    for (area, range_), (zone_name, (x_center, y_court)) in zone_mapping.items():
        if zone_name in zone_fgp and zone_fgp[zone_name]['FGA'] > 0:
            fgp = zone_fgp[zone_name]['FGP']
            y_center = flip_y(-y_court)  # Flip y coordinate here
            ax.text(x_center, -420 + y_center, f'{fgp:.0f}%', ha='center', va='center', fontsize=20, color='black',
                    weight='bold')
    return boundaries, cmap


def resolve_fgp_diff_column(data):
    if 'FGP_DIFF_x' in data.columns and 'FGP_DIFF_y' in data.columns:
        data['FGP_DIFF'] = data['FGP_DIFF_y']
        return data.drop(columns=['FGP_DIFF_x', 'FGP_DIFF_y'])
    elif 'FGP_DIFF_x' in data.columns:
        data['FGP_DIFF'] = data['FGP_DIFF_x']
        return data.drop(columns=['FGP_DIFF_x'])
    elif 'FGP_DIFF_y' in data.columns:
        data['FGP_DIFF'] = data['FGP_DIFF_y']
        return data.drop(columns=['FGP_DIFF_y'])
    return data


def plot_team_defense_shot_chart(ax, data, defense):
    # Coordinate shift for plotting
    OFFSET = 512
    x = data['LOC_X']
    y = -data['LOC_Y'] + OFFSET

    # Color map: negative = good defense, positive = bad defense (FG% above league average)
    colors = ["#00008C", "#4467C4", "#ADD8E6", "#FFFF00", "#FF5C00", "#ff0000"]
    cmap = ListedColormap(colors)
    boundaries = [-100, -9, -3, 0, 3, 9, 100]
    norm = BoundaryNorm(boundaries, cmap.N, clip=True)

    # Plot hexbins (C must be FG% difference vs league avg)

    data = resolve_fgp_diff_column(data)
    extent = [-275, 275, -50, 425]
    hexbin = ax.hexbin(x, y, gridsize=40, cmap=cmap, norm=norm, extent=extent)
    hexbin2 = ax.hexbin(x, y, C=data['FGP_DIFF'], gridsize=40, cmap=cmap, norm=norm, extent=extent)
    sized_hexbin(ax, hexbin, hexbin2, cmap, norm)

    # Helper to flip court y-coordinates
    def flip_y(y_val):
        return -y_val + OFFSET

    # Zones for annotations
    zone_mapping = {
        ('Center(C)', 'Less Than 8 ft.'): ('Restricted Area', (0, 20)),
        ('Center(C)', '8-16 ft.'): ('In The Paint (Non-RA)', (0, 80)),
        ('Center(C)', '16-24 ft.'): ('Mid-Range (Center)', (0, 180)),
        ('Left Side Center(LC)', '16-24 ft.'): ('Mid-Range (Left)', (-100, 150)),
        ('Right Side Center(RC)', '16-24 ft.'): ('Mid-Range (Right)', (100, 150)),
        ('Left Side(L)', '24+ ft.'): ('Left Corner 3', (-220, 20)),
        ('Right Side(R)', '24+ ft.'): ('Right Corner 3', (220, 20)),
        ('Center(C)', '24+ ft.'): ('Above the Break 3 (Center)', (0, 280)),
        ('Left Side Center(LC)', '24+ ft.'): ('Above the Break 3 (Left)', (-150, 250)),
        ('Right Side Center(RC)', '24+ ft.'): ('Above the Break 3 (Right)', (150, 250)),
    }

    # FG% by zone for opponents (i.e., defense)
    zone_fgp = {}
    for (area, range_), (zone_name, _) in zone_mapping.items():
        if (area, range_) in defense.index:
            fgp = defense.loc[(area, range_), 'FGP'] * 100
            zone_fgp[zone_name] = {
                'FGP': fgp,
                'FGM': defense.loc[(area, range_), 'Makes'],
                'FGA': defense.loc[(area, range_), 'FGA']
            }

    # Annotate with FG% allowed by the team (i.e., lower = better)
    for (area, range_), (zone_name, (x_center, y_court)) in zone_mapping.items():
        if zone_name in zone_fgp and zone_fgp[zone_name]['FGA'] > 0:
            fgp = zone_fgp[zone_name]['FGP']
            y_center = flip_y(-y_court)
            ax.text(x_center, -420 + y_center, f'{fgp:.0f}%', ha='center', va='center',
                    fontsize=20, color='black', weight='bold')

    return boundaries, cmap


def get_team_defense_data_and_league_avg(opponent_data, league_data):
    # --- Calculate league-wide FG% by zone ---
    league = (
        league_data
        .groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_MADE_FLAG'])
        .size()
        .unstack(fill_value=0)
        .rename(columns={0: 'Misses', 1: 'Makes'})
    )
    league['FGA'] = league['Makes'] + league['Misses']
    league['FGP'] = league['Makes'] / league['FGA']

    # --- Calculate FG% by opponents vs this team ---
    defense = (
        opponent_data
        .groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_MADE_FLAG'])
        .size()
        .unstack(fill_value=0)
        .rename(columns={0: 'Misses', 1: 'Makes'})
    )
    defense['FGA'] = defense['Makes'] + defense['Misses']
    defense['FGP'] = defense['Makes'] / defense['FGA']

    # --- Compute difference: team defense FG% vs league FG% ---
    fg_diff = (defense['FGP'] - league['FGP']) * 100  # Positive = worse defense, Negative = better

    # --- Merge FG_DIFF into shot-level opponent data for plotting ---
    merged = pd.merge(
        opponent_data,
        fg_diff.rename('FGP_DIFF'),
        on=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'],
        how='right'
    )

    return merged, defense


def get_player_data_and_calculate_league_average(data, league_avg):
    LA = (league_avg.loc[:, ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'FGA', 'FGM']]
          .groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'])
          .sum())
    LA['FGP'] = LA['FGM'] / LA['FGA']
    # Calculate player FG% by zone
    player = data.groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_MADE_FLAG']).size().unstack(fill_value=0)
    player = player.rename(columns={0: 'Misses', 1: 'Makes'})
    player['FGA'] = player['Makes'] + player['Misses']
    player['FGP'] = player['Makes'] / player['FGA']
    # Merge player vs league data
    player_vs_league = (player['FGP'] - LA['FGP']) * 100
    data = pd.merge(data, player_vs_league.rename('FGP_DIFF'), on=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'], how='right')
    return data, player


def get_team_defense_vs_league_avg(opponent_shot_data, league_avg_data):
    # 1. League-wide FG% by zone
    # 1. Calculate FGA and FGM for league from raw shots
    league_grouped = (
        league_avg_data
        .groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_MADE_FLAG'])
        .size()
        .unstack(fill_value=0)
        .rename(columns={0: 'Misses', 1: 'Makes'})
    )

    league_grouped['FGA'] = league_grouped['Makes'] + league_grouped['Misses']
    league_grouped['FGM'] = league_grouped['Makes']
    league_grouped['FGP'] = league_grouped['Makes'] / league_grouped['FGA']

    # 2. Opponent FG% against team by zone
    team_defense = (
        opponent_shot_data
        .groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_MADE_FLAG'])
        .size()
        .unstack(fill_value=0)
        .rename(columns={0: 'Misses', 1: 'Makes'})
    )

    team_defense['FGA'] = team_defense['Makes'] + team_defense['Misses']
    team_defense['FGP'] = team_defense['Makes'] / team_defense['FGA']

    # 3. Compare team defense FG% to league average
    team_defense['FGP_DIFF'] = (team_defense['FGP'] - league_grouped['FGP']) * 100

    # 4. Merge zone-based difference back into shot-level data (for plotting)
    merged = pd.merge(
        opponent_shot_data,
        team_defense['FGP_DIFF'].rename('FGP_DIFF'),
        on=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'],
        how='right'
    )

    return merged, team_defense


def add_team_image_to_chart(ax, nba_team_name, team_id, xlim, ylim):
    try:
        if Const.Constants.team_logo_images.__contains__(nba_team_name):
            nba_logo_name = Const.Constants.team_logo_images.get(nba_team_name)
            img = (Image.open(
                f'{nba_logo_name}').convert(
                "RGB"))
            img.show()
            imagebox = OffsetImage(img, zoom=.2)
            # Coordinates in axes fraction (0 = left/bottom, 1 = right/top)
            ab = AnnotationBbox(imagebox, (-.10, .15), xycoords='axes fraction',
                                frameon=False, box_alignment=(0, 1))
            ax.add_artist(ab)
    except Exception as e:
        print(f"Could not load image for player {team_id}: {e}")


# TODO: Update the LEGEND so that it is presentable
def create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig):
    # --- Efficiency (vertical color gradient) legend ---
    eff_legend_ax = fig.add_axes([0.45, 0.0, 0.1, 0.35])
    eff_legend_ax.axis('off')
    eff_legend_ax.set_facecolor('white')

    eff_colors = ["#00008C", "#4467C4", "#ADD8E6", "#FFFF00", "#FF5C00", "#ff0000"]
    eff_labels = ['Below AVG', '', '', '', '', 'Above AVG']
    hex_radius = 0.075
    spacing = 0.1
    y_start = .3

    for i, (color, label) in enumerate(zip(eff_colors, eff_labels)):
        y = y_start - i * spacing
        hexagon = RegularPolygon((0.3, y), numVertices=6, radius=hex_radius,
                                 orientation=0, facecolor=color, edgecolor='white')
        eff_legend_ax.add_patch(hexagon)

        if label:
            eff_legend_ax.text(0.6, y, label, ha='left', va='center', fontsize=8,
                               color='gray', fontweight='bold', fontfamily='Arial')

    eff_legend_ax.set_xlim(0, 1.5)
    eff_legend_ax.set_ylim(0, y_start + spacing)
    eff_legend_ax.text(0.3, y_start + spacing * 0.6, 'Efficiency', ha='left', va='bottom',
                       fontsize=12, color='gray', fontweight='bold', fontfamily='Arial')

    # --- Frequency (vertical growing-size hexes) legend ---
    freq_legend_ax = fig.add_axes([0.55, 0.0, 0.1, 0.35])  # Left of efficiency
    freq_legend_ax.axis('off')
    freq_legend_ax.set_facecolor('white')

    labels = ['Low', '', '', '', 'High']
    color_steps = len(labels)
    min_radius = 0.1
    max_radius = 0.2
    spacing = 0.81
    y_start = 3.5
    x_start = 0

    for i, label in enumerate(labels):
        radius = min_radius + (max_radius - min_radius) * (i / (color_steps - 1))

        boundary_value = boundaries[i + 1]
        normalized_value = (boundary_value - boundaries[0]) / (boundaries[-1] - boundaries[0])
        color = cmap(0.5)  # Mid-color for now

        x = x_start + i * spacing  # ← Change y-based spacing to x-based
        hexagon = RegularPolygon((x, 0.3), numVertices=6, radius=radius,
                                 orientation=np.radians(0), facecolor=color, edgecolor='white')
        freq_legend_ax.add_patch(hexagon)

        if label:
            freq_legend_ax.text(x, 0.6, label, ha='center', va='bottom', fontsize=8,
                                color='gray', fontweight='bold', fontfamily='Arial')

    freq_legend_ax.set_xlim(x_start - spacing, x_start + spacing * len(labels))
    freq_legend_ax.set_ylim(0, 1.0)

    freq_legend_ax.text(x_start, 0.9, 'Frequency', ha='left', va='bottom',
                        fontsize=12, color='gray', fontweight='bold', fontfamily='Arial')


def create_figure_and_axis(ax, flip_court, title, xlim, ylim):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 11))
    else:
        fig = ax.get_figure()
    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])
    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)
    ax.axis('off')
    return ax, fig


def draw_custom_hex_legend(ax):
    # Colors (adjust to match your cmap)
    colors = ["#053061", "#d6604d", "#f4a582", "#4393c3", "#2166ac", "#b2182b"]
    labels = ['Much Worse', 'Worse', 'Below Avg', 'Avg', 'Above Avg', 'Better', 'Much Better']

    # Draw colored hexagons
    for i, (color, label) in enumerate(zip(colors, labels)):
        hexagon = mpatches.RegularPolygon((i, 0.5), numVertices=6, radius=0.4, orientation=np.radians(30),
                                          facecolor=color, edgecolor='white')
        ax.add_patch(hexagon)
        ax.text(i, -0.2, label, ha='center', va='center', fontsize=8, color='white')

    # Frequency hexagons (gray)
    freqs = [0.2, 0.4, 0.6]
    x_start = len(labels) + 1.5
    for i, size in enumerate(freqs):
        hexagon = mpatches.RegularPolygon((x_start + i, 0.5), numVertices=6, radius=size,
                                          orientation=np.radians(30), facecolor='gray', edgecolor='white')
        ax.add_patch(hexagon)
    ax.text(x_start + 1, -0.2, "Low", ha='center', va='center', fontsize=8, color='white')
    ax.text(x_start + 2, -0.2, "High", ha='center', va='center', fontsize=8, color='white')

    ax.set_xlim(-1, x_start + 3)
    ax.set_ylim(-1, 1.5)
    ax.axis('off')
    ax.set_facecolor('#ea907a')  # match your chart background


def heatmap(data, player_name, season, season_type, player_id, title="", color="b", xlim=(-250, 250), ylim=None,
            line_color="white",
            court_color="white", court_lw=2, outer_lines=False, flip_court=False, gridsize=None, ax=None, despine=False,
            **kwargs):
    ylim = (470, -60)  # Original court orientation (hoop at y=0)

    # 2. Flip shot data if needed (to match court orientation)
    if flip_court:
        data = data.copy()
        data['LOC_Y'] = 422.5 - data['LOC_Y']

    # 3. Create figure and axis
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_facecolor("black")

    ax.set_title(title, fontsize=18)

    draw_nba_court(ax, color=court_color, lw=court_lw, outer_lines=outer_lines)

    x_offset = 0  # try tweaking these values
    y_offset = 95  # start with small adjustments like -10, -15, or +10

    x = data['LOC_X'] + x_offset
    y = data['LOC_Y'] + y_offset

    sns.kdeplot(x=x, y=y, fill=True, cmap='twilight', ax=ax, **kwargs)

    # Shot dots
    ax.scatter(x, y, facecolors='w', s=2, linewidths=0.1, **kwargs)

    # NOW draw the court lines on top
    draw_nba_court(ax, color="white", lw=2, outer_lines=False)

    # Set the spines to match the rest of court lines, makes outer_lines
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        # 8. Player photo/stats overlays
    assist, blocks, fg, fg3, plus_minus, points, rebounds, season, steals = add_player_stats_to_shot_chart(
        player_name, season, season_type, player_id)
    add_player_image_to_chart(ax, player_id, xlim, ylim)
    add_shot_chart_header_info(assist, blocks, fg, fg3, fig, plus_minus, points, rebounds, season, steals, player_name,
                               season_type, "white", "white")
    save_directory = 'shotcharts'
    file_name = os.path.join(save_directory, f"{player_name}_{season}_{season_type}heatmap_season_chart.png")
    plt.savefig(file_name, facecolor='black')
    plt.close()


def heatmap_team(data, team_name, season, season_type, title="", color="b", xlim=(-250, 250), ylim=None,
                 line_color="white", court_color="white", court_lw=2, outer_lines=False, flip_court=False,
                 gridsize=None,
                 ax=None, despine=False, **kwargs):
    ylim = (470, -60)  # Original court orientation (hoop at y=0)

    if flip_court:
        data = data.copy()
        data['LOC_Y'] = 422.5 - data['LOC_Y']

    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)
    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_facecolor("black")
    ax.set_title(title, fontsize=18)

    draw_nba_court(ax, color=court_color, lw=court_lw, outer_lines=outer_lines)

    x_offset = 0
    y_offset = 95

    x = data['LOC_X'] + x_offset
    y = data['LOC_Y'] + y_offset

    sns.kdeplot(x=x, y=y, fill=True, cmap='twilight', ax=ax, **kwargs)

    ax.scatter(x, y, facecolors='w', s=2, linewidths=0.1, **kwargs)

    draw_nba_court(ax, color="white", lw=2, outer_lines=False)

    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    assist, blocks, fg, fg3, team_id, points, rebounds, steals = add_team_stats_to_shot_chart(team_name, season,
                                                                                              season_type)
    add_team_image_to_chart(ax, team_name, team_id, xlim, ylim)
    add_team_shot_chart_header_info(assist, blocks, fg, fg3, fig, points, rebounds, season, steals, team_name,
                                    season_type, "white")

    save_directory = 'shotcharts'
    file_name = os.path.join(save_directory, f"{team_name}_{season}_{season_type} heatmap_season_chart.png")
    plt.savefig(file_name, facecolor='black')
    plt.close()


def create_team_hexmap_per_season(team_name, season, season_type, game_id):
    team_shotchart_df, team_league_avg = get_team_shot_chart_updated(team_name, season, season_type, game_id)
    team_hexmap_chart(team_shotchart_df, team_league_avg, team_name, season, season_type, game_id)
    # create_team_defense_heatmap(team_name, team_league_avg, season, season_type)
    return f"Hexmap created for {team_name} for season: {season}"


def create_player_heatmap(player_name, season, season_type, game_id):
    shot_df, league_avg, player_id = get_nba_player_shot_chart_information(player_name, season, season_type, game_id)
    heatmap(shot_df, player_name, season, season_type, player_id)
    return f"{season_type} Heat Map created for {player_name} for season: {season} during the {season_type}."

def create_wnba_player_heatmap(player_name, season, season_type, game_id):
    wnba_shot_chart_df, league_avg, player_id = get_wnba_player_shot_chart_information(player_name, season, season_type, game_id)
    heatmap(wnba_shot_chart_df, player_name, season, season_type, player_id)
    return f"{season_type} Heat Map created for {player_name} for season: {season} during the {season_type}."


def create_team_heatmap(team_name, season, season_type, game_id):
    team_shot_chart_df, team_league_avg = get_team_shot_chart_updated(team_name, season, season_type, game_id)
    heatmap_team(team_shot_chart_df, team_name, season, season_type)
    return f"{season_type} Heat Map created for {team_name} for season: {season}"


def create_updated_player_regular_season_hexmap_shot_chart(player_name, season, season_type, game_id):
    shot_df, league_avg, player_id = get_nba_player_shot_chart_information(player_name, season, season_type, game_id)
    hexmap_chart(shot_df, league_avg, player_name, season, season_type, player_id)
    return f"{season_type} Hex Map created for {player_name} for season: {season}"


def create_team_playoffs_finals_per_game_hexmap_shot_chart(player_name, season, game_id):
    team_finals_shot_chart_df = get_nba_finals_team_per_game_shot_chart_information(player_name, season, game_id)
    player_playoff_shotchart_df, playoff_leage_avg = get_nba_finals_team_per_game_shot_chart_information(player_name,
                                                                                                         season)
    hexmap_finals_playoff_chart(team_finals_shot_chart_df, playoff_leage_avg, player_name, season, game_id)
    return f"Hex Map finals playoff created for {player_name} during season: {season} for game id {game_id}"


def get_all_shots_across_league(season, season_type='Regular Season', sleep_time=1.2):
    all_teams = teams.get_teams()
    all_shots = []

    print(f"Fetching shot data for all NBA teams in {season} {season_type}...")

    for team in all_teams:
        team_id = team['id']
        team_name = team['full_name']
        print(f"Getting shots for {team_name}...")

        try:
            shots = shotchartdetail.ShotChartDetail(
                team_id=team_id,
                player_id=0,
                season_nullable=season,
                season_type_all_star=season_type,
                context_measure_simple="FGA"
            ).get_data_frames()[0]

            all_shots.append(shots)
            time.sleep(sleep_time)  # Respect rate limits

        except Exception as e:
            print(f"Failed for {team_name}: {e}")

    if all_shots:
        league_df = pd.concat(all_shots, ignore_index=True)
        print(f"Collected {len(league_df)} total shots from all teams.")
        return league_df
    else:
        print("No shot data collected.")
        return pd.DataFrame()


def create_team_defense_heatmap(team_name, team_avg, season, season_type):
    # 1. Get opponent shots against the team for the full season
    opponent_data = get_opponent_shots_against_team(team_name, season, season_type)

    # 2. Get league-wide shot data (pre-cached or call another function)
    league_data = get_all_shots_across_league(season, season_type)  # <- implement or load this externally

    # 3. Calculate FG% difference between opponents vs league avg
    defense_data, zone_stats = get_team_defense_vs_league_avg(opponent_data, league_data)

    # 4. Generate heatmap or hexbin chart
    team_defense_hexmap_chart(defense_data, league_data, team_name, season, season_type, None)

    return f"{season_type} Defensive Heat Map created for {team_name} for season: {season}"
