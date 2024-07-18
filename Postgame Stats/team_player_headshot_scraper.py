

import requests
from bs4 import BeautifulSoup


def get_team_image_url(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element containing the team image URL
        img_element = soup.find('div', class_='Image__Wrapper aspect-ratio--child')

        if img_element:
            # Extract the image URL
            img_url = img_element.find('img')['alt']
            return img_url
        else:
            print("Team image not found on the page.")
            return None
    else:
        print("Failed to retrieve the webpage.")
        return None


# URL of the Atlanta Hawks team roster page
url = "https://www.espn.com/nba/team/roster/_/name/atl/atlanta-hawks"

# Get the team image URL
team_image_url = get_team_image_url(url)

if team_image_url:
    print("Atlanta Hawks team image URL:", team_image_url)
else:
    print("Failed to retrieve the Atlanta Hawks team image URL.")
