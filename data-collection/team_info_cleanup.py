"""
use this file to aggregate and clean up team info data sets
1. team positions from each season --> avg position
2. team atmosphere from each season --> avg stadium capacity ratio
"""
import pandas as pd

def team_position_avg():
    """
    go through each file named data/raw_team_positions/team_data_{season}.csv
    """
    seasons = ['1992-1993', '1993-1994', '1994-1995', '1995-1996', '1996-1997', '1997-1998', '1998-1999', '1999-2000', '2000-2001', '2001-2002', '2002-2003', '2003-2004', '2004-2005', '2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023']


    prem_teams_df = pd.read_csv("data/prem_clubs.csv")
    all_teams = prem_teams_df['club_name'].tolist()

    team_dict = {}
    position_type = {tuple(range(1, 8)): 'top', tuple(range(8, 15)): 'mid', tuple(range(15, 21)): 'relegation'}

    for team in all_teams:
        total_position = 0
        number_of_seasons = 0
        for year in seasons:
            table_position_df = pd.read_csv(f"data/raw_team_positions/team_data_{year}.csv")
            if team in table_position_df['club_name'].values:
                number_of_seasons += 1
                total_position += table_position_df.loc[table_position_df['club_name'] == team, 'table_position'].iloc[0]
        if number_of_seasons > 0:
            avg_position = total_position // number_of_seasons
            if avg_position > 20:
                avg_position = 20
            for key, value in position_type.items():
                if avg_position in key:
                    position_category = value
            team_dict[team] = [avg_position, position_category]
        else:
            team_dict[team] = [20, 'relegation']

    
    data = [(team, info[0], info[1]) for team, info in team_dict.items()]
    team_position_df = pd.DataFrame(data, columns=['club_name', 'avg_position', 'position_type'])
    team_position_df = team_position_df.sort_values(by=['position_type', 'avg_position', 'club_name'], key=lambda x: x.map({'top': 0, 'mid': 1, 'relegation': 2}) if x.name == 'position_type' else x)
    team_position_df.to_csv("data/team_positions.csv", index=False)

    # Merge the team_position_df with prem_teams_df on 'club_name'
    merged_df = pd.merge(team_position_df, prem_teams_df, on='club_name', how='left')
    merged_df.to_csv("data/prem_clubs.csv", index=False)

def team_atmosphere_avg():
    """
    go through each file named data/raw_team_atmosphere/team_data_{season}.csv
    """
    pass

if __name__ == "__main__":
    team_position_avg()
    team_atmosphere_avg()
