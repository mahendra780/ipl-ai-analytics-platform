import streamlit as st


from src.pages.batting_intelligence import (
show_batting_intelligence
)
from src.pages.bowling_intelligence import (
    show_bowling_intelligence
)
from src.pages.match_intelligence import (
    show_match_intelligence
)

from src.pages.ai_analyst import show_ai_analyst

from src.pages.overview import show_overview
from src.pages.player_comparison import show_player_comparison
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
            "Batting Intelligence",
            "Bowling Intelligence",
            "Match Intelligence",
            "AI Cricket Analyst",
            "Player Comparison",
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
        "Bowling Intelligence": lambda: show_bowling_intelligence(deliveries),
        "Batting Intelligence": lambda: show_batting_intelligence(deliveries),
        "Match Intelligence": lambda: show_match_intelligence(matches,deliveries,model),
        "Player Comparison": lambda: show_player_comparison(deliveries),
        "Win Predictor": lambda: show_win_predictor(matches, model),
    }

    page_renderers[section]()

    st.markdown("---")
    st.caption("Built with Python, Pandas, Machine Learning & Streamlit")


if __name__ == "__main__":
    main()
