import sqlite3

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


class NCAAPlayerStats:
    def get_player_season_stats(self: str, game_id: str) -> str:
        return "NOT IMPLEMENTED"


class NCAATeamStats:
    def get_team_season_stats(self: str, year: str) -> dict:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        conn = sqlite3.connect('/Users/stormyork/Documents/NCAA Information.db')
        query = """
                      SELECT team_id
                      FROM ncaam_team_info
                      WHERE LOWER(team_name) = LOWER(?)
                   """
        cur = conn.cursor()
        cur.execute(query, (self,))
        result = cur.fetchone()
        conn.close()
        ncaa_mens_team_id = result[0] if result else None

        players = []
        if ncaa_mens_team_id:
            ncaa_mens_team_stats_url = f"https://www.espn.com/mens-college-basketball/team/stats/_/id/{ncaa_mens_team_id}/season/{year}"
            ncaa_mens_team_stats_response = requests.get(ncaa_mens_team_stats_url, headers=headers)
            ncaa_player_soup = BeautifulSoup(ncaa_mens_team_stats_response.text, "html.parser")
            rows = ncaa_player_soup.select(".Table__Scroller table tbody tr")
            names = ncaa_player_soup.select(".Table--fixed-left .Table__TBODY a.AnchorLink")

            # Loop through rows and collect stats
            players = {}
            for name_tag, row in zip(names, rows):
                cells = row.find_all("span", {"data-testid": "statCell"})
                if len(cells) >= 11:  # Ensure it's a stat row and all stats are present
                    player_name = name_tag.text.strip()
                    if player_name not in players:
                        stats = {
                            'gp': int(float(cells[0].text.strip() or 0)),
                            'min': float(cells[1].text.strip() or 0),
                            'pts': float(cells[2].text.strip() or 0),
                            'reb': float(cells[3].text.strip() or 0),
                            'ast': float(cells[4].text.strip() or 0),
                            'stl': float(cells[5].text.strip() or 0),
                            'blk': float(cells[6].text.strip() or 0),
                            'to': float(cells[7].text.strip() or 0),
                            'fg%': float(cells[8].text.strip() or 0),
                            'ft%': float(cells[9].text.strip() or 0),
                            '3p%': float(cells[10].text.strip() or 0),
                        }
                        players[player_name] = stats
        ncaa_team_season_stats = pd.DataFrame(players)
        return ncaa_team_season_stats.to_dict()
