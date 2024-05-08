"""
use this to collect data on all teams to ever play in the prem

https://www.premierleague.com/clubs 
"""

import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Ensure this import is correct
from bs4 import BeautifulSoup
import time
import pandas as pd
from global_functions import normalize_team_name

def fetch_clubs_and_stadiums():
    url = "https://www.premierleague.com/clubs"
    service = Service('/Users/qudus/chromedriver/mac_arm-124.0.6367.91/chromedriver-mac-arm64/chromedriver') # download using npx @puppeteer/browsers install chromedriver@124.0.6367 (or whatever version you have)
    driver = webdriver.Chrome(service=service) 
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    clubs_data = soup.find_all('td', class_='team')

    clubs_stadiums = []
    for club in clubs_data:
        name = club.find('div', class_='team-index__club-name').text.strip()
        stadium = club.find('div', class_='team-index__stadium-name').text.strip()
        if not stadium:
            stadium = club.find('div', class_='team-index__stadium-name u-show-mob').text.strip()
        
        clubs_stadiums.append({'club_name': name, 'stadium': stadium})

    return clubs_stadiums

def save_to_csv(clubs_stadiums):
    directory = '/Users/qudus/Desktop/6.S079/6.S079_project/data/'

    filepath = os.path.join(directory, 'prem_clubs.csv')
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['club_name', 'stadium'])
        writer.writeheader()
        for club_stadium in clubs_stadiums:
            writer.writerow(club_stadium)

if __name__ == "__main__":

    clubs_stadiums = fetch_clubs_and_stadiums()
    save_to_csv(clubs_stadiums)
    df = pd.read_csv('data/prem_clubs.csv')
    df['club_name'] = df['club_name'].apply(normalize_team_name)

    df.to_csv('data/prem_clubs.csv', index=False)

