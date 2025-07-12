import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


class NCAAPlayerStats:
    def get_player_season_stats(self: str, game_id: str) -> dict:
        return "testing"


class NCAATeamStats:
    def get_team_season_stats(self: str, game_id: str) -> dict:
        team_name = self
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        # Step 1: Request the teams list page with headers
        teams_url = "https://www.espn.com/mens-college-basketball/teams"
        response = requests.get(teams_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        team_id = None
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            if team_name.lower() in a_tag.text.lower():
                match = re.search(r'/id/(\d+)/', href)
                if match:
                    team_id = match.group(1)
                    break

        players = []
        if team_id:
            ncaa_mens_team_stats_url = f"https://www.espn.com/mens-college-basketball/team/stats/_/id/{team_id}"
            ncaa_mens_team_stats_response = requests.get(ncaa_mens_team_stats_url, headers=headers)
            ncaa_player_soup = BeautifulSoup(ncaa_mens_team_stats_response.text, "html.parser")
            rows = ncaa_player_soup.select(".Table__Scroller table tbody tr")
            names = ncaa_player_soup.select(".Table--fixed-left .Table__TBODY a.AnchorLink")

            # Loop through rows and collect stats
            for name_tag, row in zip(names, rows):
                cells = row.find_all("span", {"data-testid": "statCell"})
                if len(cells) >= 10:  # Ensure it's a stat row
                    stats = {
                        "Name": name_tag.text.strip(),
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
                    players.append(stats)
        ncaa_team_season_stats = pd.DataFrame(players)
        return ncaa_team_season_stats.to_dict()
