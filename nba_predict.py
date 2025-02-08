import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="catlover123",  # Replace with your actual MySQL password
    database="nba_stats_db"
)

# Fetch game data from MySQL
query = "SELECT game_date, points, rebounds, assists FROM player_game_stats WHERE player_name='Kyrie Irving' ORDER BY game_date"
df = pd.read_sql(query, conn)
conn.close()

# Convert game_date to numerical (number of days since the first game)
df["game_date"] = pd.to_datetime(df["game_date"])
df["days_since_first_game"] = (df["game_date"] - df["game_date"].min()).dt.days

# Features (X) and Target Variables (y)
X = df[['days_since_first_game']]
y_points = df['points']
y_rebounds = df['rebounds']
y_assists = df['assists']

# Train-test split
X_train, X_test, y_train_pts, y_test_pts = train_test_split(X, y_points, test_size=0.2, random_state=42)
X_train, X_test, y_train_reb, y_test_reb = train_test_split(X, y_rebounds, test_size=0.2, random_state=42)
X_train, X_test, y_train_ast, y_test_ast = train_test_split(X, y_assists, test_size=0.2, random_state=42)

# Train models
model_pts = RandomForestRegressor()
model_pts.fit(X_train, y_train_pts)

model_reb = RandomForestRegressor()
model_reb.fit(X_train, y_train_reb)

model_ast = RandomForestRegressor()
model_ast.fit(X_train, y_train_ast)

# Predict next game (day after last game)
future_game = [[df["days_since_first_game"].max() + 1]]
predicted_points = model_pts.predict(future_game)[0]
predicted_rebounds = model_reb.predict(future_game)[0]
predicted_assists = model_ast.predict(future_game)[0]

print(f"🏀 Predicted Stats for Next Game:")
print(f"Points: {predicted_points:.2f}")
print(f"Rebounds: {predicted_rebounds:.2f}")
print(f"Assists: {predicted_assists:.2f}")
