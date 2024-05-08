"""
use this file to collect data about the team's average position finsih within the prem

categorical: top of table (1-7), upper half (8-14), middle table (15-20)

look at all seasons team was in the prem, then get their overall average position within the prem

url = https://fbref.com/en/comps/9/1995-1996/1995-1996-Premier-League-Stats
url = https://fbref.com/en/comps/9/{year}/{year}-Premier-League-Stats
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Ensure this import is correct
from bs4 import BeautifulSoup
import time
import pandas as pd
from global_functions import normalize_team_name

seasons = ['1992-1993', '1993-1994', '1994-1995', '1995-1996', '1996-1997', '1997-1998', '1998-1999', '1999-2000', '2000-2001', '2001-2002', '2002-2003', '2003-2004', '2004-2005', '2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023']

# avg_position_df = pd.DataFrame(columns=[''])
def getUrl(year):
    return f"https://fbref.com/en/comps/9/{year}/{year}-Premier-League-Stats"

# data/raw_team_positions/team_data_1992-1993.csv
def scrape_team_positions():
    service = Service('/Users/qudus/chromedriver/mac_arm-124.0.6367.91/chromedriver-mac-arm64/chromedriver') 
    driver = webdriver.Chrome(service=service) 

    for year in seasons:
        url = getUrl(year)
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', class_='stats_table sortable min_width force_mobilize now_sortable')
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        team_data = []
        for index, row in enumerate(rows):
            club_name = row.find('td', {'data-stat': 'team'}).find('a').text
            table_position = index + 1
            team_data.append({'club_name': club_name, 'table_position': table_position})

        df = pd.DataFrame(team_data)
        df['club_name'] = df['club_name'].apply(normalize_team_name)
        df.to_csv(f'data/raw_team_positions/team_data_{year}.csv', index=False)
        print(f'Saved team data for {year}')
    
    driver.quit()
        

if __name__ == "__main__":
    scrape_team_positions()

