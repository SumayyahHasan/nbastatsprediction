import streamlit as st
import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="catlover123",
    database="nba_stats_db"
)

# Fetch player names
player_query = "SELECT DISTINCT player_name FROM player_game_stats"
players = pd.read_sql(player_query, conn)["player_name"].tolist()

# Streamlit UI
st.title("🏀 NBA Player Stat Predictor")
selected_player = st.selectbox("Select a Player", players)

# Fetch data for selected player
query = f"SELECT game_date, points, rebounds, assists FROM player_game_stats WHERE player_name='{selected_player}' ORDER BY game_date"
df = pd.read_sql(query, conn)
conn.close()

if not df.empty:
    # Convert dates
    df["game_date"] = pd.to_datetime(df["game_date"])
    df["days_since_first_game"] = (df["game_date"] - df["game_date"].min()).dt.days

    # Train Model
    X = df[['days_since_first_game']]
    y_points = df['points']
    model_pts = RandomForestRegressor().fit(X, y_points)
    
    future_game = [[df["days_since_first_game"].max() + 1]]
    predicted_points = model_pts.predict(future_game)[0]

    st.write(f"**Predicted Points for {selected_player}'s Next Game: {predicted_points:.2f}**")
    st.line_chart(df.set_index("game_date")["points"], use_container_width=True)
else:
    st.write("No game data available for this player.")
