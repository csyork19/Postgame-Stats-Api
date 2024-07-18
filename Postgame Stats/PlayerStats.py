import requests
from bs4 import BeautifulSoup
from nba_api.stats.endpoints import playergamelog, playercareerstats
from sportsipy.ncaab.teams import Teams

import PostGameStatsUtil

def get_cbb_player_stats(self):
    return get_espn_player_id(self)


def get_player_stats(self):
    if self:
        player_logs = playergamelog.PlayerGameLog(
            player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
        player_logs_df = player_logs.get_data_frames()[0]
        return player_logs_df.to_dict()
    return None


def get_player_career_stats(self):
    if self:
        player_career = playercareerstats.PlayerCareerStats(
            player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self))
        player_career_df = player_career.get_data_frames()[0]
        return player_career_df.to_dict()


def get_player_playoff_stats(self, year):
    if self:
        player_logs = playergamelog.PlayerGameLog(
            player_id=PostGameStatsUtil.PostGameStatsUtil.get_player_id(self),
            season=year,
            season_type_all_star='Playoffs')
        player_logs_df = player_logs.get_data_frames()[0]
        return player_logs_df.to_dict()


def get_player_shot_chart_coordinates(self, year):
    if self:
        return PostGameStatsUtil.PostGameStatsUtil.get_player_season_shot_chart(self, year)



def get_espn_player_id(player_name):
    try:
        # Iterate over all teams to find the player
        list_of_teams = Teams()
        for team in list_of_teams:
            roster = team.roster.players
            for player in roster:
                if player.name.lower() == player_name.lower():
                    print(f"Found player: {player.name}")
                    # Attempt to fetch ESPN ID from external source
                    return search_espn_for_player_id(player.name, team.name)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def search_espn_for_player_id(player_name, team_name):
    search_url = f"https://www.espn.com/search/_/q/{player_name.replace(' ', '%20')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example parsing, you will need to inspect ESPN's page structure for the actual HTML
    player_links = soup.find_all('a', href=True)
    for link in player_links:
        if '/player/' in link['href']:
            if player_name.lower() in link['href'].lower():
                espn_id = link['href'].split('/')[-1]
                return espn_id
    return None