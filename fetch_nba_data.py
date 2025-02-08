import mysql.connector
import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="catlover123",  # Replace with your actual MySQL password
    database="nba_stats_db"
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_game_stats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(50),
        game_date DATE,
        opponent VARCHAR(10),
        points INT,
        rebounds INT,
        assists INT
    )
""")

# Players to fetch
player_names = ["Dereck Lively", "Kyrie Irving", "Anthony Davis"]

# Function to get player ID
def get_player_id(name):
    player_dict = players.get_players()
    for player in player_dict:
        if player["full_name"] == name:
            return player["id"]
    return None

# Fetch game logs and insert into SQL
for name in player_names:
    player_id = get_player_id(name)
    if player_id:
        game_logs = playergamelog.PlayerGameLog(player_id=player_id, season="2023").get_data_frames()[0]  # Use latest season
        for _, game in game_logs.iterrows():
            cursor.execute("""
    INSERT INTO player_game_stats (player_name, game_date, opponent, points, rebounds, assists)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (name, pd.to_datetime(game["GAME_DATE"]).strftime('%Y-%m-%d'),
      game["MATCHUP"][-3:], int(game["PTS"]), int(game["REB"]), int(game["AST"])))


conn.commit()
cursor.close()
conn.close()

print("Player game stats successfully inserted into MySQL!")
