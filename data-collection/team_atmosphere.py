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

years = ['1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

club_to_stadium = {'AnfieldLiverpool FC': 'Anfield', 'Old TraffordManchester United': 'Old Trafford', 'Villa ParkAston Villa': 'Villa Park', 'Elland RoadLeeds United': 'Elland Road', 'Tottenham Hotspur StadiumTottenham Hotspur': 'Tottenham Hotspur', 'HillsboroughSheffield Wednesday': 'Hillsborough', 'Etihad StadiumManchester City': 'Etihad', 'Emirates StadiumArsenal FC': 'Emirates', 'The City GroundNottingham Forest': 'The City Ground', 'Goodison ParkEverton FC': 'Goodison Park', 'Bramall LaneSheffield United': 'Bramall Lane', 'Stamford BridgeChelsea FC': 'Stamford Bridge', 'Portman RoadIpswich Town': 'Portman Road', 'Riverside StadiumMiddlesbrough FC': 'Riverside', 'Carrow RoadNorwich City': 'Carrow Road', 'Ewood ParkBlackburn Rovers': 'Ewood Park', 'Selhurst ParkCrystal Palace': 'Selhurst Park', 'St Mary\'s StadiumSouthampton FC': 'St Mary\'s', 'Loftus Road StadiumQueens Park Rangers': 'Loftus Road', 'Coventry Building Society ArenaCoventry City': 'Coventry', 'Boundary ParkOldham Athletic': 'Boundary Park', 'Selhurst ParkWimbledon FC (- 2004)': 'Selhurst Park'}

stadium_to_club = {'Anfield' : 'Liverpool FC', 'Old Trafford' : 'Manchester United', 'Villa Park' : 'Aston Villa', 'Elland Road' : 'Leeds United', 'Tottenham Hotspur' : 'Tottenham Hotspur', 'Hillsborough' : 'Sheffield Wednesday', 'Etihad' : 'Manchester City', 'Emirates' : 'Arsenal FC', 'The City Ground' : 'Nottingham Forest', 'Goodison Park' : 'Everton FC', 'Bramall Lane' : 'Sheffield United', 'Stamford Bridge' : 'Chelsea FC', 'Portman Road' : 'Ipswich Town', 'Riverside' : 'Middlesbrough FC', 'Carrow Road' : 'Norwich City', 'Ewood Park' : 'Blackburn Rovers', 'Selhurst Park' : 'Crystal Palace', 'St Mary\'s' : 'Southampton FC', 'Loftus Road' : 'Queens Park Rangers', 'Coventry' : 'Coventry City', 'Boundary Park' : 'Oldham Athletic', 'Selhurst Park' : 'Wimbledon FC'}


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

        df['Stadium'] = df['Stadium'].map(club_to_stadium)
        df = df.drop(columns=['Spectators'])
        df['club_name'] = df['Stadium'].map(stadium_to_club)

        df['club_name'] = df['club_name'].apply(normalize_team_name)
        df.rename(columns={'Stadium': 'stadium', 'Capacity': 'capacity', 'Average': 'avg_attendance'}, inplace=True)

        df.to_csv(f'data/raw_stadium_attendance/stadium_attendance_{year}.csv', index=False)
        print(f'Saved team data for {year}')
    
    driver.quit()
        

if __name__ == "__main__":
    scrape_team_attendance()