"""
prem_transfers.csv
club_name,player_name,age,position,club_involved_name,fee,transfer_movement,transfer_period,fee_cleaned,league_name,year,season,country


COLUMNS NEEDED:
club_name --> club player is going to
player_name
age
position --> use to properly weigh goals, assists, tackles, clean sheets (goalie, defender, midfielder, striker, winger)
    maybe just look at <3 years up to them leaving and find a trend within
club_involved_name --> club leaving, use this to only focus on english clubs
transfer_movement --> in or out, only focused on players going into a team (table is inclusive of "in" and "out" direction for prem to prem transfers)
transfer_period --> Winter or Summer (probably not useful)
fee_cleaned --> price as a float in euros, NA is a loan, 0 is a free transfer
season --> ex: 2022/23, can be used if we need to filter by a certain time period


EXAMPLE ROWS:
Newcastle United,Anthony Gordon,21,Left Winger,Everton,€45.60m,in,Winter,45.6,Premier League,2022,2022/2023,England
Everton FC,Anthony Gordon,21,Left Winger,Newcastle,€45.60m,out,Winter,45.6,Premier League,2022,2022/2023,England
Brentford FC,Ellery Balcombe,22,Goalkeeper,Burton Albion,"End of loanJan 4, 2022",in,Winter,NA,Premier League,2021,2021/2022,England
Arsenal FC,Pierre-Emerick Aubameyang,32,Centre-Forward,Barcelona,free transfer,out,Winter,0,Premier League,2021,2021/2022,England

TODO
1. get a list of all teams that have played in the prem from 1992/93 to 2022/23
2. filter by club leaving in ^, fee != 0 or NA, "in" transfer_movement
"""

import pandas as pd
from global_functions import normalize_team_name

prem_transfers_df = pd.read_csv("data/all_prem_transfers.csv")
clubs_stadiums_df = pd.read_csv("data/prem_clubs.csv")

# only want column headers club_name, player_name, age, position, club_involved_name, transfer_movement, transfer_period, fee_cleaned,  season
prem_transfers_df = prem_transfers_df[["club_name", "player_name", "age", "position", "club_involved_name", "transfer_movement", "transfer_period", "fee_cleaned", "season"]]

# Normalize team names
prem_transfers_df['club_name'] = prem_transfers_df['club_name'].apply(normalize_team_name)
prem_transfers_df['club_involved_name'] = prem_transfers_df['club_involved_name'].apply(normalize_team_name)

# Remove rows where fee_cleaned is NaN or 0 (loan or free transfer)
prem_transfers_df = prem_transfers_df[prem_transfers_df['fee_cleaned'].notna() & (prem_transfers_df['fee_cleaned'] != 0)]

# Filter rows to keep only those with transfer_movement equal to "in"
prem_transfers_df = prem_transfers_df[prem_transfers_df['transfer_movement'] == "in"]

# normalize positions
prem_transfers_df['position']=prem_transfers_df['position'].map({'Left Winger': 'Winger', 'Centre-Forward': 'Forward', 'Defensive Midfield': 'Midfielder', 'Central Midfield': 'Midfielder', 'Right-Back': 'Defender', 'Second Striker': 'Striker', 'Centre-Back': 'Centre-Back', 'Left-Back': 'Defender', 'Left Midfield': 'Midfielder', 'Goalkeeper': 'Goalkeeper', 'Right Winger': 'Winger', 'Attacking Midfield': 'Midfielder', 'Right Midfield': 'Midfielder', 'defence': 'Defender'})

# Filter to ensure all 'club_name' and 'club_involved_name' are in 'club_name' from clubs_stadiums_df
valid_clubs = set(clubs_stadiums_df['club_name'])

prem_transfers_df=prem_transfers_df.rename(columns={'club_name': 'club_joining', 'club_involved_name': 'club_leaving'})

def check_valid_club(club, valid_clubs):
    for vc in valid_clubs:
        if club in vc:
            return True
    return False

prem_transfers_df = prem_transfers_df[
    prem_transfers_df['club_joining'].apply(lambda x: check_valid_club(x, valid_clubs)) &
    prem_transfers_df['club_leaving'].apply(lambda x: check_valid_club(x, valid_clubs))
]

prem_transfers_df.to_csv('data/prem_transfers_cleaned.csv', index=False)

