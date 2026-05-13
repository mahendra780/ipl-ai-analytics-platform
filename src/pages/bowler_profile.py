import streamlit as st

from src.analysis import bowler_profile


def show_bowler_profile(deliveries):
    st.header("Bowler Profile")
    st.markdown("---")

    bowler_name = st.selectbox(
        "Select Bowler",
        sorted(deliveries["bowler"].dropna().unique()),
    )

    profile = bowler_profile(deliveries, bowler_name)

    col1, col2, col3 = st.columns(3)
    col1.metric("Matches", profile["Matches"])
    col2.metric("Wickets", profile["Wickets"])
    col3.metric("Overs", profile["Overs"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Economy", profile["Economy"])
    col5.metric("Dot Balls", profile["Dot Balls"])
    col6.metric("Best Spell", profile["Best Spell"])
