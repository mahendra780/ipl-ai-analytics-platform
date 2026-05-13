import streamlit as st

from src.pages.batting import (
    show_batting_analytics,
)

from src.pages.batter_profile import (
    show_batter_profile,
    show_season_batter_analysis,
    show_career_progression,
)


def show_batting_intelligence(deliveries):

    st.title("🏏 Batting Intelligence")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analytics",
        "👤 Batter Profile",
        "📅 Season Analysis",
        "📈 Career Progression",
    ])

    # TAB 1
    with tab1:

        show_batting_analytics(
            deliveries
        )

    # TAB 2
    with tab2:

        show_batter_profile(
            deliveries
        )

    # TAB 3
    with tab3:

        show_season_batter_analysis(
            deliveries
        )

    # TAB 4
    with tab4:

        show_career_progression(
            deliveries
        )