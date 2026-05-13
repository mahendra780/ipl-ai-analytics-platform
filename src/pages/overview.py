import streamlit as st

from src.ui.charts import create_bar_chart


def show_overview(matches):
    st.header("IPL Overview")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Matches", len(matches))
    col2.metric("Total Seasons", matches["Season"].nunique())
    col3.metric("Total Teams", matches["WinningTeam"].nunique())

    st.subheader("Team Wins")

    team_wins = matches["WinningTeam"].value_counts()

    fig = create_bar_chart(
        team_wins,
        title="Team Wins",
        x_axis_title="Team",
        y_axis_title="Wins",
    )

    st.plotly_chart(fig, use_container_width=True)
