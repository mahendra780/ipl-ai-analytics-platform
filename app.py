import streamlit as st

from src.pages.batter_profile import (
    show_batter_profile,
    show_career_progression,
    show_season_batter_analysis,
)
from src.pages.ai_analyst import show_ai_analyst
from src.pages.batting import show_batting_analytics
from src.pages.bowler_profile import show_bowler_profile
from src.pages.bowling import show_bowling_analytics
from src.pages.bowling_phase import show_bowling_phase_analytics
from src.pages.head_to_head import show_head_to_head
from src.pages.live_match_center import show_live_match_center
from src.pages.match_insights import show_match_insights
from src.pages.overview import show_overview
from src.pages.player_comparison import show_player_comparison
from src.pages.powerplay import show_powerplay_analysis
from src.pages.win_predictor import show_win_predictor
from src.utils.data_loader import load_processed_data
from src.utils.model_loader import load_or_train_win_predictor

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    layout="wide",
)


@st.cache_data
def get_processed_data():
    return load_processed_data()


@st.cache_resource
def get_win_predictor_model():
    return load_or_train_win_predictor()


def render_header():
    st.markdown(
        """
        # IPL AI Analytics Platform

        ### Advanced Cricket Intelligence & Win Prediction System
        """
    )


def render_sidebar():
    st.sidebar.markdown(
        """
        # IPL Analytics

        ### AI Powered Dashboard
        """
    )

    return st.sidebar.radio(
        "Navigation",
        [
            "Overview",
            "AI Cricket Analyst",
            "Batting Analytics",
            "Bowling Analytics",
            "Batter Profile",
            "Bowler Profile",
            "Head-to-Head",
            "Season-wise Batter Analysis",
            "Career Progression",
            "Player Comparison",
            "Advanced Match Insights",
            "Powerplay & Death Overs",
            "Bowling Phase Analytics",
            "Live Match Center",
            "Win Predictor",
        ],
    )


def main():
    matches, deliveries = get_processed_data()
    model = get_win_predictor_model()

    render_header()
    section = render_sidebar()

    page_renderers = {
        "Overview": lambda: show_overview(matches),
        "AI Cricket Analyst": lambda: show_ai_analyst(matches, deliveries),
        "Batting Analytics": lambda: show_batting_analytics(deliveries),
        "Bowling Analytics": lambda: show_bowling_analytics(deliveries),
        "Batter Profile": lambda: show_batter_profile(deliveries),
        "Bowler Profile": lambda: show_bowler_profile(deliveries),
        "Head-to-Head": lambda: show_head_to_head(matches),
        "Season-wise Batter Analysis": lambda: show_season_batter_analysis(deliveries),
        "Career Progression": lambda: show_career_progression(deliveries),
        "Player Comparison": lambda: show_player_comparison(deliveries),
        "Advanced Match Insights": lambda: show_match_insights(matches, deliveries),
        "Powerplay & Death Overs": lambda: show_powerplay_analysis(deliveries),
        "Bowling Phase Analytics": lambda: show_bowling_phase_analytics(deliveries),
        "Live Match Center": lambda: show_live_match_center(matches, model),
        "Win Predictor": lambda: show_win_predictor(matches, model),
    }

    page_renderers[section]()

    st.markdown("---")
    st.caption("Built with Python, Pandas, Machine Learning & Streamlit")


if __name__ == "__main__":
    main()
