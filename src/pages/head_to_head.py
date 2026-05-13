import streamlit as st

from src.analysis import head_to_head


def show_head_to_head(matches):
    st.header("Head-to-Head Team Comparison")
    st.markdown("---")

    teams = sorted(matches["WinningTeam"].dropna().unique())

    team1 = st.selectbox("Select Team 1", teams)
    team2 = st.selectbox("Select Team 2", teams)

    if team1 == team2:
        st.warning("Please select two different teams.")
        return

    result = head_to_head(matches, team1, team2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Matches", result["Total Matches"])
    col2.metric(f"{team1} Wins", result[f"{team1} Wins"])
    col3.metric(f"{team2} Wins", result[f"{team2} Wins"])

    st.subheader("Win Percentage")

    col4, col5 = st.columns(2)
    col4.metric(f"{team1} Win %", result[f"{team1} Win %"])
    col5.metric(f"{team2} Win %", result[f"{team2} Win %"])
