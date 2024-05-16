"""
data/final_data/merged_transfer_stats.csv --> player_name,age,club_leaving,club_joining,position,transfer_period,adjusted_fee,season,minutes_played_leaving,goals_leaving,assists_leaving,cards_leaving,minutes_played_joining,goals_joining,assists_joining,cards_joining

data/final_data/prem_clubs.csv --> club_name,avg_attendance,avg_position,position_type,stadium

need merge avg_attendance,avg_position,position_type for club_joining and club_leaving for each player
per player:
club_leaving --> avg_attendance_leaving,avg_position_leaving,position_type_leaving
club_joining --> avg_attendance_joining,avg_position_joining,position_type_joining

so each row should have in this order:
player_name,age,club_leaving,club_joining,position,transfer_period,adjusted_fee,season,minutes_played_leaving,goals_leaving,assists_leaving,cards_leaving,minutes_played_joining,goals_joining,assists_joining,cards_joining,avg_attendance_leaving,avg_position_leaving,position_type_leaving,avg_attendance_joining,avg_position_joining,position_type_joining
"""

import pandas as pd

# Load datasets
transfers_df = pd.read_csv("data/final_data/merged_transfer_stats.csv")
clubs_df = pd.read_csv("data/final_data/prem_clubs.csv")

# Merge club leaving data
transfers_df = transfers_df.merge(clubs_df[['club_name', 'avg_attendance', 'avg_position', 'position_type']], left_on='club_leaving', right_on='club_name', how='left')
transfers_df.rename(columns={
    'avg_attendance': 'avg_attendance_leaving',
    'avg_position': 'avg_position_leaving',
    'position_type': 'position_type_leaving'
}, inplace=True)
transfers_df.drop(columns=['club_name'], inplace=True)

# Merge club joining data
transfers_df = transfers_df.merge(clubs_df[['club_name', 'avg_attendance', 'avg_position', 'position_type']], left_on='club_joining', right_on='club_name', how='left')
transfers_df.rename(columns={
    'avg_attendance': 'avg_attendance_joining',
    'avg_position': 'avg_position_joining',
    'position_type': 'position_type_joining'
}, inplace=True)
transfers_df.drop(columns=['club_name'], inplace=True)

# Handle NaN or null values in 'minutes_played_joining' by setting them to 0
transfers_df['minutes_played_joining'] = transfers_df['minutes_played_joining'].fillna(0)

# Save the merged data
transfers_df.to_csv('data/final_data/club_player_transfer_stats.csv', index=False)


