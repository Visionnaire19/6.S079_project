"""
inflation adjustment: https://www.in2013dollars.com/europe/inflation/1996?amount=910000 
"""
import pandas as pd

# season_inflation = {'1992/1993': 1.7910, '1993/1994': 1.7910, '1994/1995': 1.7910, '1995/1996':1.7910, '1996/1997':1.7910, '1997/1998':1.7610, '1998/1999':1.7397, '1999/2000':1.7196, '2000/2001':1.6828, '2001/2002':1.6431, '2002/2003':1.6066, '2003/2004':1.5733, '2004/2005': 1.5398, '2005/2006': 1.5067, '2006/2007': 1.4742, '2007/2008': 1.4429, '2008/2009': 1.3963, '2009/2010':1.3919, '2010/2011':1.3697, '2011/2012':1.3334, '2012/2013':1.3009, '2013/2014':1.2836, '2014/2015':1.2781, '2015/2016':1.2777, '2016/2017':1.2746, '2017/2018':1.2531, '2018/2019':1.2298, '2019/2020':1.2120, '2020/2021':1.2031, '2021/2022':1.1692, '2022/2023':1.0708}

prem_transfers_df = pd.read_csv("data/final_data/club_player_transfer_stats.csv")
# prem_transfers_df['adjusted_fee'] = prem_transfers_df.apply(lambda row: row['fee_cleaned'] * season_inflation[row['season']], axis=1)
# prem_transfers_df.drop(columns=['fee_cleaned'], inplace=True)

# prem_transfers_df=prem_transfers_df.rename(columns={'squad': 'club_joining', 'club_involved_name': 'club_leaving'})
# prem_transfers_df=prem_transfers_df.rename(columns={'minutes_played_1': 'minutes_played_joining', 'minutes_played_2': 'minutes_played_leaving', 'goals_1': 'goals_joining', 'goals_2': 'goals_leaving', 'assists_1': 'assists_joining', 'assists_2': 'assists_leaving', 'cards_1': 'cards_joining', 'cards_2': 'cards_leaving'})

prem_transfers_df=prem_transfers_df.rename(columns={'position_type_leaving': 'club_position_type_leaving', 'position_type_joining': 'club_position_type_joining', 'avg_position_leaving': 'club_avg_position_leaving', 'avg_position_joining': 'club_avg_position_joining'})

# prem_transfers_df.drop(columns=['goals_joining', 'assists_joining', 'cards_joining'], inplace=True)


# Reorder columns to make 'adjusted_fee' the 7th column


prem_transfers_df.to_csv('data/final_data/club_player_transfer_stats.csv', index=False)

