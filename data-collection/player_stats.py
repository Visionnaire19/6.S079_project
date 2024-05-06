"""
This file is used to collect data from the premier league website

https://www.premierleague.com/players?se=1&cl=-1 has data from 1992/93 on players.
data is lackluster from seasons before 2005/06 season

can use this to collect player goal, assits, tackles, & clean sheets based on player names
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from functools import reduce
import pandas as pd
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Choose Chrome Browser
webdriver_service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


year_ranges = [
    "1992-1993", "1993-1994", "1994-1995", "1995-1996", "1996-1997", "1997-1998", 
    "1998-1999", "1999-2000", "2000-2001", "2001-2002", "2002-2003", "2003-2004", 
    "2004-2005", "2005-2006", "2006-2007", "2007-2008", "2008-2009", "2009-2010", 
    "2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", 
    "2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", 
    "2022-2023"
]
def get_url(range):
    return f"https://fbref.com/en/comps/9/{range}/stats/{range}-Premier-League-Stats"

def get_raw_data():
    for range in year_ranges:
        url = get_url(range)
        driver.get(url)
        time.sleep(3)  # give the page time to load JavaScript content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        players = pd.read_html(str(soup), match="Player Standard Stats")[0]
        # print(len(players))
        # print(data.text)
        # players = pd.read_html(data.text, match= "Player Standard Stats")
        players.to_csv(f"../data/player_data_{range}.csv", index=False)

def clean_data():
    #Limit to players transferred within the premier league
    transfers = pd.read_csv("data/prem_transfers_cleaned.csv")
    players_names = set(transfers['player_name'].tolist())
    print(players_names)
    for range in year_ranges:
        path = f"data/player_data_{range}.csv"
        player_data = pd.read_csv(path)
        filtered = player_data[player_data['Player'].isin(players_names)]
        # filtered['cards'] = filtered['CrdY'] + filtered['CrdR']
        # filtered = filtered.drop(columns=['CrdY','CrdR'])
        rename_dict = {"Player":"player_name", "Nation":"nation", "Squad":"squad","Min":"minutes_played", "Gls":"goals", "Ast": "assists"}
        columns_to_keep = ["Player", "Nation","Squad","Min", "Gls", "Ast","cards"]
        filtered = filtered[columns_to_keep].rename(columns=rename_dict)
        filtered.to_csv(path, index=False)

def merge_data():
    dataframes = []
    for range in year_ranges:
        path = f"data/raw_player_stats/player_data_{range}.csv"
        dataframes.append( pd.read_csv(path))
    df_merged = pd.concat(dataframes, ignore_index=True)
    # Drop duplicate columns created in the merging process
    df_merged = df_merged[[col for col in df_merged.columns if not col.endswith('_drop')]]  
    df_aggregated = df_merged.groupby(['player_name', 'squad']).agg({
        'nation': 'first',  # Presuming 'nation' does not change
        'minutes_played': 'sum',
        'goals': 'sum',
        'assists': 'sum',
        'cards': 'sum'}).reset_index()
    df_aggregated.to_csv("data/aggregate_stats.csv")

if __name__ == "__main__":
    merge_data()
    
