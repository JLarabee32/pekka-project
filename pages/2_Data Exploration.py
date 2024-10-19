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

st.subheader("Correlation Matrix Heatmap")
gm_droplist = ['Season', 'Game_ID', 'TOI', 'TOI%', 'Sv%', 'FSv%', 'xFSv%', 'dFSv%']
games_df_test = games_df.drop(gm_droplist, axis=1)
numeric_games = games_df_test.select_dtypes(include='number')
corr_matrix_1 = numeric_games.corr()
cormap = plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix_1, annot=True, cmap='coolwarm')
st.pyplot(cormap)
st.markdown("The main things we're looking for here is a positive correlation between Shots Against (SA) and Goals Saved Above Expected Above Average (GSAxAA), SA and Goals Saved Above Expected (GSAx), and Expected Goals Against Per Shot (xGA_per_Shot). Although this heatmap shows a weak correlation between our variables, it is positive and shows there may be a relationship we care about")

st.subheader("GSAx vs xGA per Shot")
fig1, ax1 = plt.subplots()
ax1.scatter(games_df["GSAx"], games_df["xGA_per_Shot"])
ax1.set_xlabel("GSAx")
ax1.set_ylabel("xGA per Shot")
st.pyplot(fig1)

cor_xgaper = games_df["xGA_per_Shot"].corr(games_df["GSAx"])

st.write("Correlation coefficent =", round(cor_xgaper, 3))

st.subheader("GSAx vs Shots Against")
fig2, ax2 = plt.subplots()
ax2.scatter(games_df["GSAx"], games_df["SA"])
ax2.set_xlabel("GSAx")
ax2.set_ylabel("Shots Against")
st.pyplot(fig2)

cor_sa = games_df["SA"].corr(games_df["GSAx"])

st.write("Correlation coefficent =", round(cor_sa, 3))

games_z = pd.DataFrame()
games_z['Player'] = games_df['Player']
games_z['Above Avg'] = games_df['Above Avg']
games_z['Date'] = games_df['Date']
games_z['SA'] = stats.zscore(games_df['SA'])
games_z['xGA_per_Shot'] = (games_df['xGA_per_Shot'] - (-0.001745)) / 0.086248
games_z['GSAxAA'] = stats.zscore(games_df['GSAxAA'])
games_z['GSAx'] = stats.zscore(games_df['GSAx'])
games_z['GA'] = stats.zscore(games_df['GA'])

st.subheader("What Does the Typical Above Average Performance Look Like?")

alt_chart = alt.Chart(games_z, height=550, width=2200).transform_window(
    index='count()'
).transform_fold(
    ['SA', 'Above Avg', 'xGA_per_Shot', 'GSAxAA', 'GSAx', 'GA']
).mark_line().encode(
    x=alt.X('key:N', sort=['Above Avg', 'SA', 'xGA_per_Shot', 'GSAxAA', 'GSAx', 'GA'], title=None),
    y=alt.Y('value:Q', title=None),
    color='Above Avg:N',
    detail='index:N',
    opacity=alt.value(0.5),
    tooltip=['Player:N', 'Date:T']
).interactive()

st.altair_chart(alt_chart, use_container_width=True)
st.write("In this chart SA, xGA_per_shot, GSAxAA, GSAx, and GA are z scaled")

st.subheader("What does this mean?")
st.markdown("What we can see from the typical above average performance shown above is that the typical above average performance, and especially the outlier exceptional performances, come when the team gives up more shots. But there is significant overlap between above and below average performances. What this can imply is that there are different profiles of goalies who perform better with more shots and profiles of goalies who don't necessarily need this. In the next page you can explore individual NHL starting goalies.")



