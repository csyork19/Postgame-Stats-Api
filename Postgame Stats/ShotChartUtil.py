from io import BytesIO
import pandas as pd
import requests
from matplotlib.cm import ScalarMappable
from scipy.stats import percentileofscore
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import PostGameStatsUtil
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

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


def draw_court(ax=None, color="black", lw=1, shotzone=False, outer_lines=False):
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

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

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
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc, inner_circle, outer_circle,
                          corner_three_a_x, corner_three_b_x,
                          inner_line_1, inner_line_2, inner_line_3, inner_line_4, inner_line_5, inner_line_6]
    else:
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]

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


def hexbin_shot_chart(data, player_name, year, title="", cmap='coolwarm', gridsize=30,
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
    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(player_name)
    url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
    try:
        img = Image.open(BytesIO(requests.get(url).content)).convert("RGB")
        imagebox = OffsetImage(img, zoom=.5)
        ab = AnnotationBbox(imagebox, (xlim[0] + 500, ylim[1]), frameon=False)
        ax.add_artist(ab)
    except Exception as e:
        print(f"Could not load image for player {player_id}: {e}")
    pc = sized_hexbin(ax, hc1, hc2, cmap=plt.get_cmap(cmap), norm=norm)

    # ✅ Add the colorbar using that PatchCollection
    cbar = plt.colorbar(pc, ax=ax)
    cbar.set_label("Field Goal %", fontsize=12, labelpad=10)
    cbar.ax.tick_params(labelsize=10, length=0)
    cbar.outline.set_visible(False)

    ax.set_title(f'{player_name} {year} Hexbin Shot Chart', fontsize=18)
    ax.axis('off')

    file_name = f"shotcharts/{player_name}_{year}_hexbin.png"
    os.makedirs("shotcharts", exist_ok=True)
    plt.savefig(file_name, dpi=300)
    plt.title(f"{player_name} field goal percentage for {year}")
    plt.close()
    return file_name

def hexmap_chart(data, league_avg, title="", color="b",
                 xlim=(-250, 250), ylim=(422.5, -47.5), line_color="black",
                 court_color="#FFFFFF", court_lw=2, outer_lines=False,
                 flip_court=False, gridsize=None,
                 ax=None, despine=False, **kwargs):
    LA = (league_avg.loc[:, ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'FGA', 'FGM']]
          .groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'])
          .sum())
    LA['FGP'] = LA['FGM'] / LA['FGA']

    # Get player data: count makes and misses by zone
    player = data.groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_MADE_FLAG']).size().unstack(fill_value=0)

    # Rename columns explicitly
    player = player.rename(columns={0: 'Misses', 1: 'Makes'})  # 0 = missed, 1 = made
    player['FGA'] = player['Makes'] + player['Misses']
    player['FGP'] = player['Makes'] / player['FGA']
    # Group by location or hex bin beforehand

    player_vs_league = (player.loc[:, 'FGP'] - LA.loc[:, 'FGP']) * 100
    data = pd.merge(data, player_vs_league, on=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'], how='right')

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

    # draws the court
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    x = data['LOC_X']
    y = data['LOC_Y']

    # for diverging color map
    colors = [
        "#053061",  # Deep red (much worse)
        "#d6604d",  # Red (worse)
        "#f4a582",  # Light red-orange (slightly worse)
        "#00FF00",  # Neutral gray (about league average)
        "#4393c3",  # Light blue (slightly better)
        "#2166ac",  # Blue (better)
        "#b2182b",  # Deep blue (way better than average)
    ]

    cmap = ListedColormap(colors)
    # The 5 colors are separated by -9, -3, 0, 3, 9
    boundaries = [-np.inf, -9, -3, 0, 3, 9, np.inf]
    norm = BoundaryNorm(boundaries, cmap.N, clip=True)

    # first hexbin required for bincount
    # second hexbin for the coloring of each hexagons
    hexbin = ax.hexbin(x, y, gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425])
    hexbin2 = ax.hexbin(x, y, C=data['FGP'], gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425])
    sized_hexbin(ax, hexbin, hexbin2, cmap, norm)
    # Add colorbar legend for FG% difference vs. league average
    # Add legend colorbar for FG% difference

    # draw_custom_hex_legend(ax)
    # Define colormap and norm
    bounds = [-9, -6, -3, 0, 3, 6, 9]
    cmap = plt.get_cmap('coolwarm')  # or whatever colormap you're using
    norm = BoundaryNorm(bounds, cmap.N)

    # Create ScalarMappable and force it to have valid values
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(np.array(bounds))  # THIS IS CRUCIAL

    # Now create the colorbar safely
    cbar = plt.colorbar(sm, ax=ax, fraction=0.035, pad=0.04)

    cbar.set_label('FG% vs League Avg', fontsize=12, labelpad=10)
    cbar.ax.tick_params(labelsize=10)
    cbar.outline.set_visible(False)
    cbar.set_ticks([-9, -3, 0, 3, 9])
    cbar.set_ticklabels(['Much Worse', 'Worse', 'Avg', 'Better', 'Much Better'])

    # Set the spines to match the rest of court lines, makes outer_lines
    # somewhate unnecessary
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(str(player_name))
    url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
    try:
        img = Image.open(BytesIO(requests.get(url).content)).convert("RGB")
        imagebox = OffsetImage(img, zoom=.4)
        ab = AnnotationBbox(imagebox, (xlim[0], ylim[1] + 400), frameon=False)
        ax.add_artist(ab)
    except Exception as e:
        print(f"Could not load image for player {player_id}: {e}")

        # Save the chart dynamically
    save_directory = 'shotcharts'
    os.makedirs(save_directory, exist_ok=True)  # Ensure directory exists

    file_name = os.path.join(save_directory, f"{player_name}_{season}_hexmap_chart.png")
    plt.savefig(file_name, dpi=300)
    plt.close()  # Close the figure to release memory


def draw_custom_hex_legend(ax):
    # Colors (adjust to match your cmap)
    colors = ['#1f77b4', '#5fa2c7', '#d1e4f2', '#ffffcc', '#ffe699', '#f4b183', '#c00000']
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






player_name = "Tyrese Haliburton"
season = "2024-25"
# game_id = '0042400111'


shot_df, _ = get_player_shot_chart_detail(player_name, season)
shot_chart(shot_df, player_name, season)
chart_path = hexbin_shot_chart(shot_df, player_name, season)
hexbin_shot_chart(shot_df, player_name, season)
player_shotchart_df, league_avg = get_player_shot_chart_detail(player_name, season)

# df = get_player_sper_game_shot_chart(player_name,season,game_id)
# shot_chart(df, player_name, season)
hexmap_chart(player_shotchart_df, league_avg)


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

