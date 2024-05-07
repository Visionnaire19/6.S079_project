import pandas as pd
import matplotlib.pyplot as plt

def vis1():
    """In general, does the playing time go up or down"""
    player_data = pd.read_csv("data/merged_transfer_stats.csv")
    player_data['minutes_played_1'].fillna(0, inplace=True)
    player_data['minutes_played_2'].fillna(0, inplace=True)
    plt.scatter(player_data['minutes_played_1'], player_data['minutes_played_2'])

    plt.title("Comparison of playing time between two teams")
    plt.xlabel("Minutes played for team 1")
    plt.ylabel("Minutes played for team 2")
    plt.show()

def vis2():
    """Does the transfer fee correlate with the playing time"""
    player_data = pd.read_csv("data/merged_transfer_stats.csv")
    player_data['minutes_played_2'].fillna(0, inplace=True)
    plt.scatter(player_data['fee_cleaned'], player_data['minutes_played_2'])

    plt.title("Transfer fee vs playing time for team 2")
    plt.xlabel("Transfer fee")
    plt.ylabel("Minutes played for team 2")
    plt.show()
if __name__ == "__main__":
    vis2()