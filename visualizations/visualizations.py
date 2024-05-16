import pandas as pd
import matplotlib.pyplot as plt

def vis1():
    """In general, does the playing time go up or down"""
    player_data = pd.read_csv("data/final_data/merged_transfer_stats.csv")
    player_data['minutes_played_leaving'].fillna(0, inplace=True)
    player_data['minutes_played_joining'].fillna(0, inplace=True)
    plt.scatter(player_data['minutes_played_leaving'], player_data['minutes_played_joining'])

    plt.title("Comparison of playing time between two teams")
    plt.xlabel("Minutes played for team 1")
    plt.ylabel("Minutes played for team 2")
    plt.savefig(f"visualizations/Comparison of playing time between two teams.png")

def vis2():
    """Does the transfer fee correlate with the playing time"""
    player_data = pd.read_csv("data/final_data/merged_transfer_stats.csv")
    player_data['minutes_played_leaving'].fillna(0, inplace=True)
    plt.scatter(player_data['adjusted_fee'], player_data['minutes_played_leaving'])

    plt.title("Transfer fee vs playing time for team 2")
    plt.xlabel("Transfer fee (adjusted for inflation)")
    plt.ylabel("Minutes played for team 2")
    plt.savefig(f"visualizations/Transfer fee vs playing time for team 2.png")

if __name__ == "__main__":
    vis1()
    vis2()

