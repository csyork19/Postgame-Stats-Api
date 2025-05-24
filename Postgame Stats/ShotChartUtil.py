from io import BytesIO
import pandas as pd
import requests
from scipy.stats import percentileofscore
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail, playergamelog
from nba_api.stats.endpoints import playercareerstats
import seaborn as sns
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import PostGameStatsUtil
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Rectangle, Arc

sns.set_style('white')
sns.set_color_codes()
plt.switch_backend('Agg')
pd.options.display.max_columns = None


def get_player_sper_game_shot_chart(player_name, season_id, game_id):
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']
    shot_chart_list = shotchartdetail.ShotChartDetail(team_id=team_id,
                                                      player_id=player_dict['id'],
                                                      season_type_all_star='Regular Season',
                                                      season_nullable=season_id,
                                                      game_id_nullable=game_id,
                                                      context_measure_simple="FGA").get_data_frames()
    return shot_chart_list[0]


def get_player_shot_chart_detail(player_name, season_id):
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']
    shot_chart_list = shotchartdetail.ShotChartDetail(team_id=team_id,
                                                      player_id=player_dict['id'],
                                                      season_type_all_star='Regular Season',
                                                      season_nullable=season_id,
                                                      context_measure_simple="FGA").get_data_frames()
    return shot_chart_list[0], shot_chart_list[1]

def get_player_playoff_shot_chart_detail(player_name, season_id):
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']
    shot_chart_list = shotchartdetail.ShotChartDetail(team_id=team_id,
                                                      player_id=player_dict['id'],
                                                      season_type_all_star='Playoffs',
                                                      season_nullable=season_id,
                                                      context_measure_simple="FGA").get_data_frames()
    return shot_chart_list[0], shot_chart_list[1]





def draw_court_v2(ax=None, color="black", lw=1, shotzone=False, outer_lines=False, flip=False):
    if ax is None:
        ax = plt.gca()

    # Flip y-values if needed
    def flip_y(y):
        return 422.5 - y if flip else y

    def create_rect(x, y, width, height):
        return Rectangle((x, flip_y(y)), width, -height if flip else height, linewidth=lw, color=color, fill=False)

    def create_arc(xy, width, height, theta1, theta2, dashed=False):
        # Flip angles if flipping vertically
        if flip:
            theta1, theta2 = (360 - theta2) % 360, (360 - theta1) % 360
        return Arc((xy[0], flip_y(xy[1])), width, height,
                   theta1=theta1, theta2=theta2,
                   linewidth=lw, color=color, linestyle='dashed' if dashed else 'solid')

    def create_circle(center, radius):
        return Circle((center[0], flip_y(center[1])), radius=radius, linewidth=lw, color=color, fill=False)

    court_elements = [
        create_circle((0, 0), 7.5),  # Hoop
        create_rect(-30, -12.5, 60, 0),  # Backboard
        create_rect(-80, -47.5, 160, 190),  # Outer box
        create_rect(-60, -47.5, 120, 190),  # Inner box
        create_arc((0, 142.5), 120, 120, 0, 180),  # Top free-throw arc
        create_arc((0, 142.5), 120, 120, 180, 0, dashed=True),  # Bottom free-throw arc
        create_arc((0, 0), 80, 80, 0, 180),  # Restricted arc
        create_rect(-220, -47.5, 0, 140),  # Left corner 3
        create_rect(220, -47.5, 0, 140),  # Right corner 3
        create_arc((0, 0), 475, 475, 22, 158)
    ]

    if shotzone:
        court_elements += [
            create_circle((0, 0), 80),
            create_circle((0, 0), 160),
            create_rect(-250, 92.5, 30, 0),
            create_rect(220, 92.5, 30, 0),
            create_rect(40, 69.28, 80, 0),
            create_rect(-40, 69.28, 80, 0),
            create_rect(53.20, 150.89, 290, 0),
            create_rect(-53.20, 150.89, 290, 0),
            create_rect(130.54, 92.5, 80, 0),
            create_rect(-130.54, 92.5, 80, 0),
        ]

    if outer_lines:
        court_elements.append(create_rect(-250, -47.5, 500, 470))

    for element in court_elements:
        ax.add_patch(element)

    return ax



def draw_court(ax=None, color="black", lw=1, shotzone=False, outer_lines=False, flip=False):
    if ax is None:
        ax = plt.gca()

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color,
                         fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color,
                            linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three point line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)



    # Draw shot zone Lines
    # Based on Advanced Zone Mode
    if shotzone == True:
        inner_circle = Circle((0, 0), radius=80, linewidth=lw, color='black', fill=False)
        outer_circle = Circle((0, 0), radius=160, linewidth=lw, color='black', fill=False)
        corner_three_a_x = Rectangle((-250, 92.5), 30, 0, linewidth=lw, color=color)
        corner_three_b_x = Rectangle((220, 92.5), 30, 0, linewidth=lw, color=color)

        # 60 degrees
        inner_line_1 = Rectangle((40, 69.28), 80, 0, linewidth=lw, color=color)
        # 120 degrees
        inner_line_2 = Rectangle((-40, 69.28), 80, 0, linewidth=lw, color=color)

        # Assume x distance is also 40 for the endpoint
        inner_line_3 = Rectangle((53.20, 150.89), 290, 0, linewidth=lw, color=color)
        inner_line_4 = Rectangle((-53.20, 150.89), 290, 0, linewidth=lw, color=color)

        # Assume y distance is also 92.5 for the endpoint
        inner_line_5 = Rectangle((130.54, 92.5), 80, 0, linewidth=lw, color=color)
        inner_line_6 = Rectangle((-130.54, 92.5), 80, 0, linewidth=lw, color=color)

        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, inner_circle, outer_circle,
                          corner_three_a_x, corner_three_b_x,
                          inner_line_1, inner_line_2, inner_line_3, inner_line_4, inner_line_5, inner_line_6]
    else:
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax


def shot_chart(data, player_name, year, title="", color="b",
               xlim=(-250, 250), ylim=(422.5, -47.5), line_color="blue",
               court_color="black", court_lw=2, outer_lines=False,
               flip_court=True, gridsize=None,
               ax=None, despine=False,
               player_image_path='curry.png',  # ← New parameter
               **kwargs):
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
    draw_court_v2(ax, color=line_color, lw=court_lw, outer_lines=outer_lines, flip=True)

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

def shot_chart_v2(data, player_name, year, title="", color="b",
               xlim=(-250, 250), ylim=(422.5, -47.5), line_color="blue",
               court_color="black", court_lw=2, outer_lines=False,
               flip_court=True, gridsize=None,
               ax=None, despine=False,
               player_image_path='curry.png',  # ← New parameter
               **kwargs):
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
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

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


def sized_hexbin(ax, hc, hc2, cmap, norm):
    offsets = hc.get_offsets()
    orgpath = hc.get_paths()[0]
    verts = orgpath.vertices
    values1 = hc.get_array()
    values2 = hc2.get_array()
    ma = values1.max()
    patches = []

    for offset, val in zip(offsets, values1):
        filtered_list = list(filter(lambda num: num != 0, values1))
        if (int(val) == 0):
            continue
        elif (percentileofscore(filtered_list, val) < 33.33):
            v1 = verts * 0.3 + offset
        elif (percentileofscore(filtered_list, val) > 69.99):
            v1 = verts + offset
        else:
            v1 = verts * 0.6 + offset

        path = Path(v1, orgpath.codes)
        patch = PathPatch(path)
        patches.append(patch)

    pc = PatchCollection(patches, cmap=cmap, norm=norm)
    # sets color
    # so hexbin with C=data['FGP']
    pc.set_array(values2)
    ax.add_collection(pc)
    hc.remove()
    hc2.remove()
    return pc  # ✅ This is key for colorbar to work!


def hexbin_shot_chart(data, nba_player_name, year, title="", cmap='coolwarm', gridsize=30,
                      xlim=(-250, 250), ylim=(422.5, -47.5),
                      ax=None, court_color='black', line_color='blue'):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 11))

    ax.set_xlim(xlim[::-1])
    ax.set_ylim(ylim[::-1])
    ax.set_facecolor('white')

    draw_court(ax, color=line_color, lw=2, outer_lines=True)

    # Create a mask for made/missed
    made_mask = data['EVENT_TYPE'] == 'Made Shot'

    # FG% per location: need total attempts (C1), and makes (C2)
    hc1 = ax.hexbin(data['LOC_X'], data['LOC_Y'], gridsize=gridsize,
                    extent=(xlim[0], xlim[1], ylim[1], ylim[0]),
                    cmap=cmap, mincnt=1)

    hc2 = ax.hexbin(data[made_mask]['LOC_X'], data[made_mask]['LOC_Y'], gridsize=gridsize,
                    extent=(xlim[0], xlim[1], ylim[1], ylim[0]),
                    cmap=cmap, mincnt=1)

    norm = plt.Normalize(0, 1)  # Normalizing FG% color range (0-100%)
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(nba_player_name)
    url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
    try:
        img = Image.open(BytesIO(requests.get(url).content)).convert("RGB")
        imagebox = OffsetImage(img, zoom=.3)
        ab = AnnotationBbox(imagebox, (xlim[0] + 500, ylim[1]), frameon=False)
        ax.add_artist(ab)
    except Exception as e:
        print(f"Could not load image for player {player_id}: {e}")
    pc = sized_hexbin(ax, hc1, hc2, cmap=plt.get_cmap(cmap), norm=norm)

    # ✅ Add the colorbar using that PatchCollection
    cbar = plt.colorbar(pc, ax=ax)
    cbar.set_label("Field Goal %", fontsize=18, labelpad=10)
    cbar.ax.tick_params(labelsize=10, length=0)
    cbar.outline.set_visible(False)

    ax.set_title(f'{nba_player_name} {year} Hexbin Shot Chart', fontsize=18)
    ax.axis('off')

    file_name = f"shotcharts/{nba_player_name}_{year}_hexbin.png"
    os.makedirs("shotcharts", exist_ok=True)
    plt.savefig(file_name, dpi=300)
    plt.title(f"{nba_player_name} field goal percentage for {year}")
    plt.close()
    return file_name


def hexmap_chart(data, league_avg, nba_player_name,nba_season,title="", color="b",
                 xlim=(-250, 250), ylim=(422.5, -47.5), line_color="black",
                 court_color="#FFFFFF", court_lw=2, outer_lines=False,
                 flip_court=False, gridsize=None,
                 ax=None, despine=False, **kwargs):
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)
    draw_court_v2(ax, color=line_color, lw=court_lw, outer_lines=outer_lines,flip=True)
    data, player = get_player_data_and_calculate_league_average(data, league_avg)
    boundaries, cmap = plot_nba_player_shot_chart_data_v2(ax, data, player)
    create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig)

    # Set spines
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    # Add player image
    season = nba_season
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(str(nba_player_name))
    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV"]

    nba_player_logs = playergamelog.PlayerGameLog(player_id=player_id,season=season,season_type_all_star='Playoffs').get_data_frames()[0]
    nba_player_season_average = nba_player_logs[nba_player_stat_columns].mean().round(2).to_dict()
    points = nba_player_season_average['PTS']
    fg = nba_player_season_average['FG_PCT']
    fg3 = nba_player_season_average['FG3_PCT']
    plus_minus = nba_player_season_average['PLUS_MINUS']
    assist = nba_player_season_average['AST']
    blocks = nba_player_season_average['BLK']
    rebounds = nba_player_season_average['REB']
    steals = nba_player_season_average['STL']

    add_player_image_to_chart(ax, player_id, xlim, ylim)

    top_row_y_val = 0.90
    bottom_row_y_val = 0.80
    x_spacing = 0.15  # a bit more spacing for label next to value
    x_start = 0.38

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
    fig.text(0.5, 0.96, f"{season} Regular Season Performance",
             ha='center', va='top', fontsize=16, fontweight='bold')

    # Save the chart
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    file_name = os.path.join(save_directory, f"{nba_player_name}_{season}_hexmap_chart.png")
    plt.savefig(file_name, dpi=300)
    plt.close()
    return file_name

def hexmap_playoff_chart(data, league_avg, nba_player_name,title="", color="b",
                 xlim=(-250, 250), ylim=(422.5, -47.5), line_color="black",
                 court_color="#FFFFFF", court_lw=2, outer_lines=False,
                 flip_court=False, gridsize=None,
                 ax=None, despine=False, **kwargs):
    ax, fig = create_figure_and_axis(ax, flip_court, title, xlim, ylim)
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)
    data, player = get_player_data_and_calculate_league_average(data, league_avg)
    boundaries, cmap = plot_nba_player_shot_chart_data(ax, data, player)
    create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig)

    # Set spines
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    # Add player image
    season = "2024-25"
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(str(nba_player_name))
    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV"]

    nba_player_logs = playergamelog.PlayerGameLog(player_id=player_id,season=season,  season_type_all_star='Playoffs').get_data_frames()[0]
    nba_player_season_average = nba_player_logs[nba_player_stat_columns].mean().round(2).to_dict()
    points = nba_player_season_average['PTS']
    fg = nba_player_season_average['FG_PCT']
    fg3 = nba_player_season_average['FG3_PCT']
    plus_minus = nba_player_season_average['PLUS_MINUS']
    assist = nba_player_season_average['AST']
    blocks = nba_player_season_average['BLK']
    rebounds = nba_player_season_average['REB']
    steals = nba_player_season_average['STL']

    add_player_image_to_chart(ax, player_id, xlim, ylim)

    # Coordinates depend on your court dimensions – adjust as needed
    stat_x = 130  # near the right side outside the court
    stat_y = 50  # vertical position

    # Horizontal and vertical positioning
    # Two-line stat layout
    top_row_y_val = 0.90
    top_row_y_label = 0.85
    bottom_row_y_val = 0.80
    bottom_row_y_label = 0.75
    x_spacing = 0.1
    x_start = 0.35

    stat_values = [points, fg, fg3, assist, blocks, rebounds, steals, plus_minus]
    stat_labels = ["PPG", "FG%", "3P%", "AST", "BLK", "REB", "STL", "+/-"]

    for i, (val, label) in enumerate(zip(stat_values, stat_labels)):
        row = 0 if i < 4 else 1
        col = i % 4
        x = x_start + col * x_spacing
        y_val = top_row_y_val if row == 0 else bottom_row_y_val
        y_label = top_row_y_label if row == 0 else bottom_row_y_label

        # Format value
        if isinstance(val, float):
            val_text = f"{val:.2f}".lstrip("0") if "%" in label else f"{val:.1f}"
        else:
            val_text = str(val)

        fig.text(x, y_val, val_text, fontsize=25, fontweight='bold', ha='center', va='center', color='black')
        fig.text(x, y_label, label, fontsize=10, color='gray', ha='center', va='center')

    # Optional section header
    fig.text(0.5, 0.96, f"{season} Regular Season Performance",
             ha='center', va='top', fontsize=16, fontweight='bold')

    # Save the chart
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)
    file_name = os.path.join(save_directory, f"{nba_player_name}_{season}_hexmap_playoff_chart.png")
    plt.savefig(file_name, dpi=300)
    plt.close()
    return file_name



def plot_nba_player_shot_chart_data(ax, data, player):
    x = data['LOC_X']
    y = data['LOC_Y']
    colors = ["#00008C", "#4467C4", "#ADD8E6", "#FFFF00", "#FF5C00", "#ff0000"]
    cmap = ListedColormap(colors)
    boundaries = [-100, -9, -3, 0, 3, 9, 100]
    norm = BoundaryNorm(boundaries, cmap.N, clip=True)
    hexbin = ax.hexbin(x, y, gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425])
    hexbin2 = ax.hexbin(x, y, C=data['FGP_DIFF'], gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425])
    sized_hexbin(ax, hexbin, hexbin2, cmap, norm)
    # Define shot zones with separate regions
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
    # Calculate FG% for each zone
    zone_fgp = {}
    for (area, range_), (zone_name, _) in zone_mapping.items():
        if (area, range_) in player.index:
            fgp = player.loc[(area, range_), 'FGP'] * 100
            zone_fgp[zone_name] = {'FGP': fgp, 'FGM': player.loc[(area, range_), 'Makes'],
                                   'FGA': player.loc[(area, range_), 'FGA']}
    # Add FG% text to the chart
    for (area, range_), (zone_name, (x_center, y_center)) in zone_mapping.items():
        if zone_name in zone_fgp and zone_fgp[zone_name]['FGA'] > 0:
            fgp = zone_fgp[zone_name]['FGP']
            ax.text(x_center, y_center, f'{fgp:.0f}%', ha='center', va='center', fontsize=20, color='black',
                    weight='bold')
    return boundaries, cmap

from matplotlib.colors import ListedColormap, BoundaryNorm

def plot_nba_player_shot_chart_data_v2(ax, data, player):
    flip = True  # Set this to False if you don't want a flipped court

    def flip_y(val):
        return 422.5 - val if flip else val

    # Flip y if needed
    x = data['LOC_X']
    y = data['LOC_Y'].apply(flip_y) if flip else data['LOC_Y']

    colors = ["#00008C", "#4467C4", "#ADD8E6", "#FFFF00", "#FF5C00", "#ff0000"]
    cmap = ListedColormap(colors)
    boundaries = [-100, -9, -3, 0, 3, 9, 100]
    norm = BoundaryNorm(boundaries, cmap.N, clip=True)

    extent = [-275, 275, flip_y(425), flip_y(-50)] if flip else [-275, 275, -50, 425]

    hexbin = ax.hexbin(x, y, gridsize=40, cmap=cmap, norm=norm, extent=extent)
    hexbin2 = ax.hexbin(x, y, C=data['FGP_DIFF'], gridsize=40, cmap=cmap, norm=norm, extent=extent)

    sized_hexbin(ax, hexbin, hexbin2, cmap, norm)

    # Define shot zones with adjusted y-coordinates
    zone_mapping = {
        ('Center(C)', 'Less Than 8 ft.'): ('Restricted Area', (0, flip_y(20))),
        ('Center(C)', '8-16 ft.'): ('In The Paint (Non-RA)', (0, flip_y(80))),
        ('Center(C)', '16-24 ft.'): ('Mid-Range (Center)', (0, flip_y(180))),
        ('Left Side Center(LC)', '16-24 ft.'): ('Mid-Range (Left)', (-100, flip_y(150))),
        ('Right Side Center(RC)', '16-24 ft.'): ('Mid-Range (Right)', (100, flip_y(150))),
        ('Left Side(L)', '24+ ft.'): ('Left Corner 3', (-220, flip_y(20))),
        ('Right Side(R)', '24+ ft.'): ('Right Corner 3', (220, flip_y(20))),
        ('Center(C)', '24+ ft.'): ('Above the Break 3 (Center)', (0, flip_y(280))),
        ('Left Side Center(LC)', '24+ ft.'): ('Above the Break 3 (Left)', (-150, flip_y(250))),
        ('Right Side Center(RC)', '24+ ft.'): ('Above the Break 3 (Right)', (150, flip_y(250))),
    }

    # Calculate FG% for each zone
    zone_fgp = {}
    for (area, range_), (zone_name, _) in zone_mapping.items():
        if (area, range_) in player.index:
            fgp = player.loc[(area, range_), 'FGP'] * 100
            zone_fgp[zone_name] = {
                'FGP': fgp,
                'FGM': player.loc[(area, range_), 'Makes'],
                'FGA': player.loc[(area, range_), 'FGA']
            }

    # Draw FG% annotations
    for (area, range_), (zone_name, (x_center, y_center)) in zone_mapping.items():
        if zone_name in zone_fgp and zone_fgp[zone_name]['FGA'] > 0:
            fgp = zone_fgp[zone_name]['FGP']
            ax.text(x_center, y_center, f'{fgp:.0f}%', ha='center', va='center',
                    fontsize=20, color='black', weight='bold')

    return boundaries, cmap



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


def add_player_image_to_chart(ax, player_id, xlim, ylim):
    url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
    try:
        img = Image.open(BytesIO(requests.get(url).content)).convert("RGB")
        imagebox = OffsetImage(img, zoom=.5)
        # Coordinates in axes fraction (0 = left/bottom, 1 = right/top)
        ab = AnnotationBbox(imagebox, (0, 1.15), xycoords='axes fraction',
                            frameon=False, box_alignment=(0, 1))
        ax.add_artist(ab)
    except Exception as e:
        print(f"Could not load image for player {player_id}: {e}")


def create_shot_average_and_shot_frequency_legend(boundaries, cmap, fig):
    legend_ax = fig.add_axes([0.3, 0.05, 0.4, 0.05])  # Adjusted size for smaller hexagons
    legend_ax.axis('off')
    legend_ax.set_facecolor('white')
    # Custom growing-size hexagon legend (bottom-right corner)
    from matplotlib.patches import RegularPolygon
    import math
    # Add new axes for legend in the bottom-right
    grow_legend_ax = fig.add_axes([0.75, 0.02, 0.2, 0.05])  # [left, bottom, width, height]
    grow_legend_ax.axis('off')
    grow_legend_ax.set_facecolor('white')
    # Define color labels and hex sizes
    labels = ['Low', '', '', '', 'High']
    color_steps = len(labels)
    min_radius = 0.1
    max_radius = 0.4
    # Compute spacing and plot hexes with growing sizes
    spacing = 0  # We'll calculate as we go
    x = 0  # Start x position
    for i, label in enumerate(labels):
        # Size increases linearly from min to max
        radius = min_radius + (max_radius - min_radius) * (i / (color_steps - 1))

        # Color based on boundaries
        boundary_value = boundaries[i + 1]
        normalized_value = (boundary_value - boundaries[0]) / (boundaries[-1] - boundaries[0])
        color = cmap(0.5)  # 0.5 gives you a neutral/mid color from the colormap

        # Draw hexagon
        hexagon = RegularPolygon((x, 0.5), numVertices=6, radius=radius,
                                 orientation=np.radians(30), facecolor=color, edgecolor='white')
        grow_legend_ax.add_patch(hexagon)

        # Add label if not empty
        if label:
            grow_legend_ax.text(x, 0, label, ha='center', va='center', fontsize=8, color='gray')



        # Move x for next hex (approximate horizontal distance)
        x += radius * 2 * math.cos(math.pi / 6) + 0.05  # spacing between hexes
    # Add text label below the hex legend
    grow_legend_ax.text(2 * x / len(labels), -0.4, 'Frequency', ha='center', va='center',
                            fontsize=14, color='gray', fontstyle='normal', fontweight='normal',
                            fontfamily='Arial')
    grow_legend_ax.set_xlim(-0.5, x + 0.5)
    grow_legend_ax.set_ylim(-0.5, 1)
    # Add frequency gradient legend (Less — More)
    freq_legend_ax = fig.add_axes([0.127, 0.02, 0.2, 0.05])  # Positioned bottom left with more room
    freq_legend_ax.axis('off')
    freq_legend_ax.set_facecolor('#FBCEB1')
    # Define frequency gradient colors (light to dark)
    freq_colors = ["#00008C", "#4467C4", "#ADD8E6", "#FFFF00", "#FF5C00", "#ff0000"]
    freq_labels = ['Below AVG', '', '', '', '', 'Above AVG']
    hex_radius = 0.4
    spacing = hex_radius * 2 * math.sqrt(3)
    for i, (color, label) in enumerate(zip(freq_colors, freq_labels)):
        x = i * spacing
        hexagon = RegularPolygon((x, 0.5), numVertices=6, radius=hex_radius,
                                 orientation=np.radians(30), facecolor=color, edgecolor='white')
        freq_legend_ax.add_patch(hexagon)
        if label:
            freq_legend_ax.text(x, 0, label, ha='center', va='center', fontsize=8, color='gray',
                                fontstyle='normal', fontweight='bold', fontfamily='Arial')
            freq_legend_ax.text(2.5 * spacing, -0.4, 'Efficiency', ha='center', va='center',
                                fontsize=16, color='gray', fontweight='normal', fontfamily='Arial')
    freq_legend_ax.set_xlim(-0.5, x + spacing)
    freq_legend_ax.set_ylim(-0.5, 1)


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


def shot_zones(data, league_avg, title="", color="b",
               xlim=(-250, 250), ylim=(422.5, -47.5), line_color="black",
               court_color="white", court_lw=2, outer_lines=False,
               flip_court=False, ax=None, despine=False, **kwargs):
    if ax is None:
        ax = plt.gca()
        ax.set_facecolor(court_color)

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    draw_court(ax, color=line_color, lw=court_lw, shotzone=True, outer_lines=outer_lines)

    LA = (league_avg.loc[:, ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'FGA', 'FGM']]
          .groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'])
          .sum())
    LA['FGP'] = 1.0 * LA['FGM'] / LA['FGA']
    player = data.groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_MADE_FLAG']).size().unstack(fill_value=0)
    player['FGP'] = 1.0 * player.loc[:, 1] / player.sum(axis=1)
    player_vs_league = (player.loc[:, 'FGP'] - LA.loc[:, 'FGP']) * 100

    data = pd.merge(data, player_vs_league, on=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'], how='right')
    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='b', s=100, linewidths=3, **kwargs)

    # Set the spines to match the rest of court lines, makes outer_lines
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)


def heatmap(data, title="", color="b",
            xlim=(-250, 250), ylim=(422.5, -47.5), line_color="white",
            court_color="white", court_lw=2, outer_lines=False,
            flip_court=False, gridsize=None,
            ax=None, despine=False, **kwargs):
    if ax is None:
        ax = plt.gca()

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    x = data['LOC_X']
    y = data['LOC_Y']

    sns.kdeplot(x=x, y=y, fill=True, cmap='inferno', ax=ax, **kwargs)

    # Shot dots
    ax.scatter(x, y, facecolors='w', s=2, linewidths=0.1, **kwargs)

    # NOW draw the court lines on top
    draw_court(ax, color="white", lw=2, outer_lines=False)

    # Set the spines to match the rest of court lines, makes outer_lines
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    save_directory = 'shotcharts'
    file_name = os.path.join(save_directory, f"{player_name}_{season}_heatmap_season_chart.png")
    plt.savefig(file_name)
    plt.close()


player_name = "Kyrie Irving"
season = "2023-24"
# game_id = '0042400111'


shot_df, _ = get_player_shot_chart_detail(player_name, season)
shot_df_playoff, _ = get_player_playoff_shot_chart_detail(player_name, season)
shot_chart(shot_df, player_name, season)
chart_path = hexbin_shot_chart(shot_df, player_name, season)
hexbin_shot_chart(shot_df, player_name, season)
player_shotchart_df, league_avg = get_player_shot_chart_detail(player_name, season)
player_playoff_shotchart_df, playoff_leage_avg = get_player_playoff_shot_chart_detail(player_name,season)

# df = get_player_sper_game_shot_chart(player_name,season,game_id)
# shot_chart(df, player_name, season)
hexmap_chart(player_shotchart_df, league_avg, player_name, season)
hexmap_playoff_chart(player_playoff_shotchart_df, playoff_leage_avg, player_name)


heatmap(player_shotchart_df)


def create_hexmap_per_season(player_name, season):
    player_shot_chart_df, league_avg = get_player_shot_chart_detail(player_name, season)
    hexmap_chart(player_shot_chart_df, league_avg)
    return f"Hexmap created for {player_name} for season: {season}"


def create_hexmap_per_game(player_name, season, game_id):
    df = get_player_sper_game_shot_chart(player_name, season, game_id)
    player_shotchart_df, league_avg = get_player_shot_chart_detail(player_name, season)
    shot_chart(df, player_name, season)
    hexmap_chart(df, league_avg)
    return f"Hexmap created for {player_name} for game id: {game_id}"


def create_shot_chart_per_game(player_name, season, game_id):
    df = get_player_sper_game_shot_chart(player_name, season, game_id)
    shot_chart(df, player_name, season)
    return f"Shot Chart created for {player_name} for game id: {game_id}"


def create_shot_chart_per_season(player_name, season):
    player_shot_chart_df = get_player_shot_chart_detail(player_name, season)
    shot_chart(player_shot_chart_df, player_name, season)
    plt.show()
    return f"Shot Chart created for {player_name} for season: {season}"


def create_heat_map_per_season(player_name, season):
    player_shot_chart_df = get_player_shot_chart_detail(player_name, season)
    heatmap(player_shot_chart_df, player_name, season)
    plt.show()
    return f"Heat Map created for {player_name} for season: {season}"


def create_player_season_shot_chart_hexmap_heatmap(player_name, year):
    player_shotchart_df, league_avg = get_player_shot_chart_detail(player_name, year)
    hexmap_chart(player_shotchart_df, league_avg, title=str(player_name) + " Hex Chart " + str(year))
    heatmap(player_shotchart_df, player_name, year)
    return f"Hex Map and Heat Map created for {player_name} for season: {season}"
