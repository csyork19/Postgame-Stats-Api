import requests
from bs4 import BeautifulSoup
from sportsipy.ncaab.schedule import Schedule




import cbbpy.mens_scraper as s



def get_cbb_stats():
    df = s.get_game_info('401638645')
    df_new = s.get_game_ids('04-08-2024')
    play_by_play = s.get_game_boxscore('401638645')

    box_score = s.get_game_boxscore('401638645')

    purdue_schedule = Schedule('purdue')
    for game in purdue_schedule:
        print(game.date)

    return play_by_play.to_json()

def get_duke_stats():
    # Your API key from CollegeFootballData
    # URL of ESPN's NCAA basketball team stats page (example: 2024 season)
    url = 'https://www.espn.com/mens-college-basketball/stats'

    # Mimic a browser request by adding a User-Agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Send an HTTP request to the website with headers
    response = requests.get(url, headers=headers)

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section containing the team stats table
    team_table = soup.find('table', class_='Table Table--align-right')

    # If table found, proceed to extract team stats
    if team_table:
        # Get the headers of the table
        headers = [header.text for header in team_table.find_all('th')]

        print(" | ".join(headers))  # Print table headers (Team, PPG, FG%, etc.)

        # Extract team rows
        rows = team_table.find_all('tr', class_='Table__TR')

        # Iterate over each row in the table
        for row in rows[1:]:  # Skipping the header row
            columns = row.find_all('td')

            if columns:
                team_name = columns[1].text.strip()  # Extract team name
                points_per_game = columns[2].text.strip()  # Extract PPG
                field_goals_percentage = columns[3].text.strip()  # FG%

                # Print the scraped data
                print(f"Team: {team_name}, PPG: {points_per_game}, FG%: {field_goals_percentage}")
    else:
        print("Unable to find the team stats table on the page.")



