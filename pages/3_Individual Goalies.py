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

games_z = pd.DataFrame()
games_z['Player'] = games_df['Player']
games_z['Above Avg'] = games_df['Above Avg']
games_z['Date'] = games_df['Date']
games_z['SA'] = stats.zscore(games_df['SA'])
games_z['xGA_per_Shot'] = (games_df['xGA_per_Shot'] - (-0.001745)) / 0.086248
games_z['GSAxAA'] = stats.zscore(games_df['GSAxAA'])
games_z['GSAx'] = stats.zscore(games_df['GSAx'])
games_z['GA'] = stats.zscore(games_df['GA'])

goalie = st.selectbox(label="Select Goalie", options=goalies_df['Player'])
select_chart = alt.Chart(games_z, height=550, width=1800).transform_window(
    index='count()'
).transform_fold(
    ['SA', 'Above Avg', 'xGA_per_Shot', 'GSAxAA', 'GSAx', 'GA']
).transform_filter(
    alt.datum.Player == goalie
).mark_line().encode(
    x=alt.X('key:N', sort=['Above Avg', 'SA', 'xGA_per_Shot', 'GSAxAA', 'GSAx', 'GA'], title=None),
    y=alt.Y('value:Q', title=None),
    color='Above Avg:N',
    detail='index:N',
    opacity=alt.value(0.5),
    tooltip=['Player:N', 'Date:T']
).interactive()

st.altair_chart(select_chart, use_container_width=True)

goalie_filter = games_z[games_z['Player'] == goalie]

cor_goalie = goalie_filter["SA"].corr(goalie_filter["GSAx"])

st.write("Correlation coefficent of SA and GSAx for", goalie, "=", round(cor_goalie, 3))
