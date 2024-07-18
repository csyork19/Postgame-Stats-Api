import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download image
def download_image(image_url, directory):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_name = os.path.basename(image_url)
        with open(os.path.join(directory, image_name), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {image_name}")
    else:
        print(f"Failed to download {image_url}")

# Main function to retrieve NBA team logos
def retrieve_nba_team_logos(page_num, directory):
    url = f"https://www.stickpng.com/cat/sports/basketball/nba-teams?page={page_num}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img', src=True)
        for image in images:
            image_url = urljoin(url, image['src'])
            download_image(image_url, directory)
    else:
        print("Failed to fetch website")

if __name__ == "__main__":
    page_num = 3  # Change this to the desired page number
    directory = "nba_logos"  # Change this to the desired directory
    create_directory(directory)
    retrieve_nba_team_logos(page_num, directory)