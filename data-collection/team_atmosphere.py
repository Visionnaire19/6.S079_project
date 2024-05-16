"""
use this file to collect data about all prem teams average stadium attendance : stadium capacity from 1992 to 2022
https://www.transfermarkt.us/premier-league/besucherzahlen/wettbewerb/GB1/plus/0?saison_id=2023
https://www.transfermarkt.us/premier-league/besucherzahlen/wettbewerb/GB1/plus/0?saison_id={year}
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Ensure this import is correct
from bs4 import BeautifulSoup
import time
import pandas as pd
from global_functions import normalize_team_name
import re

years = ['1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

stadium_to_club = {}


def getUrl(year):
    return f"https://www.transfermarkt.us/premier-league/besucherzahlen/wettbewerb/GB1/plus/0?saison_id={year}"

# data/raw_stadium_attendance/stadium_attendance_{year}.csv
def scrape_team_attendance():
    service = Service('/Users/qudus/chromedriver/mac_arm-124.0.6367.91/chromedriver-mac-arm64/chromedriver') 
    driver = webdriver.Chrome(service=service) 

    for year in years:
        url = getUrl(year)
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table_html = soup.find('table', class_='items')

        df = pd.read_html(str(table_html))[0]
        df = df.dropna(subset=['#']).reset_index(drop=True)
        df = df.drop(columns=['#'])
        df = df.drop(columns=['Spectators'])

        # Regex to split stadium and club names
        df['club_name'] = df['Stadium'].apply(lambda x: re.split(r'(?<=[a-z])(?=[A-Z])', x, 1)[1].strip() if len(re.split(r'(?<=[a-z])(?=[A-Z])', x, 1)) > 1 else '')
        
        df['Stadium'] = df['Stadium'].apply(lambda x: re.split(r'(?<=[a-z])(?=[A-Z])', x, 1)[0].strip())

        df['club_name'] = df['club_name'].apply(normalize_team_name)

        df.rename(columns={'Stadium': 'stadium', 'Capacity': 'capacity', 'Average': 'avg_attendance'}, inplace=True)

        df.to_csv(f'data/raw_stadium_attendance/stadium_attendance_{year}.csv', index=False)
        print(f'Saved team data for {year}')
    
    driver.quit()
        

if __name__ == "__main__":
    scrape_team_attendance()