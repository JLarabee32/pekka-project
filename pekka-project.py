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


st.title("The Pekka Project")
st.subheader("Or: The Analytical Argument for More Shots")

st.image("https://thunder1320.com/wp-content/uploads/2022/06/Pekka-Rinne-2.jpg")

st.markdown("The image shown above is the inspiration for this project, Pekka Rinne. Rinne is probably the best goaltender in Nashville Predators history, and in the 2011 and 2012 seasons he led the league in shots against while putting up career numbers and winning a Vezina Trophy for the league's best goaltender. However the head coach he played for, Barry Trotz, was known for a defensive style that emphasized allowing the opponent to take shots from the outside and controlling the middle. Inflating shots against without sacrificing quality shots. When Trotz was replaced as head coach in 2014 by Peter Laviolette, Pekka Rinne's performance began to fall off. Coincidentally Laviolette was known for a suffocating defensive style that emphasized minimizing any shots against. This begs the question: were more shots allowing Rinne to be more engaged in the game and thus make more and better saves? This project will examine that argument")
