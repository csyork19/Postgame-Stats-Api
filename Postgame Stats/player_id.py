from nba_api.stats.endpoints import leagueleaders
import pandas as pd

from nba_api.stats.endpoints import playercareerstats


# Take the first name and last name of the player
# def get_player_id_for_name(firstname, lastname):

try:
    # Pull data for the top 500 scorers
    top_500 = leagueleaders.LeagueLeaders(
        season='2023-24',
        season_type_all_star='Regular Season',
        stat_category_abbreviation='PTS'
    ).get_data_frames()[0][:600]

    # Correct column names for grouping
    avg_stats_columns = ['MIN']
    top_500_avg = top_500.groupby(['PLAYER', 'PLAYER_ID'])[avg_stats_columns].mean()

    df = top_500_avg.reset_index()[['PLAYER', 'PLAYER_ID']]
    # Find the player ID for the given player name
    player_df = top_500_avg[['PLAYER', 'PLAYER_ID']]
    player_id = player_df[player_df['PLAYER'] == player_name]['PLAYER_ID'].iloc[0]

    # Fetching career statistics for Player of Choice using his player ID
    player_career = playercareerstats.PlayerCareerStats(player_id='202681')
    player_career_df = player_career.get_data_frames()[0]
    # Extracting the seasons of player of choice
    seasons_played = player_career_df['SEASON_ID'].unique()
    print(seasons_played.tolist())

    # Create a DataFrame for the player with only player name and player id
    player_data = pd.DataFrame({'Player Name': [player_name], 'Player ID': [player_id]})
    print(player_data)

    # Inspect the first few rows of the averaged stats
    # print(top_500_avg)




except Exception as e:
    print(f"An error occurred: {e}")