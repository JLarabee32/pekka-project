import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import altair as alt

games = pd.read_csv("https://raw.githubusercontent.com/JLarabee32/CMSE830/refs/heads/main/Goalie%20Project%20-%20Games.csv")
games["xGA_per_Shot"] = games["xGA"] / games["SA"]
goalies = pd.read_csv("https://raw.githubusercontent.com/JLarabee32/CMSE830/refs/heads/main/Goalie%20Project%20-%20Goalies.csv")
goalies["GSAx/60"] = (goalies["GSAx"] / goalies["TOI"]) * 60

goalies_df = pd.DataFrame(goalies)
games_df = pd.DataFrame(games)
droplist = ['Season', 'Team', 'GP', 'TOI', 'GA', 'SA', 'FA', 'xGA', 'Sv%', 'FSv%', 'xFSv%', 'dFSv%', 'GSAA', 'GSAx']
goalies_df_dropped = goalies_df.drop(droplist, axis=1)
games_df = games_df.merge(goalies_df_dropped, how='left', on='Player')
games_df["GSAxAA"] = games_df["GSAx"] - games_df["GSAx/60"]
games_df['Above Avg'] = (games_df['GSAx'] > games_df['GSAx/60']).astype(int)

st.title("The Datasets")

st.subheader("Game Logs from evolving-hockey")
st.write(games_df)

st.subheader("Full Season data from NHL")
st.write(goalies_df)

st.subheader("New and Encoded Variables")
st.markdown("""**xGA_per_Shot** = Value created by dividing xGA by the number of shots in that game.  
            **GSAx/60** = Calculated in full season as the number of GSAx per 60 minutes of TOI, merged in to game log dataset as reference of average performance  
            **GSAxAA** = Value of GSAx above their average performance  
            **Above Avg** = Binary variable, encoded as 1 whenever GSAx exceeds GSAx/60, measure of when a goalie exceeds their typical performance""")
