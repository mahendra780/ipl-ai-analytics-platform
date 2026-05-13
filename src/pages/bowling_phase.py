import streamlit as st

from src.analysis import (
    best_death_bowlers,
    best_powerplay_bowlers,
    most_death_over_wickets,
    most_powerplay_wickets,
)
from src.ui.charts import create_bar_chart


def _render_bar_chart(data, ylabel, title):
    st.write(data)

    fig = create_bar_chart(
        data,
        title=title,
        x_axis_title="Bowler",
        y_axis_title=ylabel,
    )

    st.plotly_chart(fig, use_container_width=True)


def show_bowling_phase_analytics(deliveries):
    st.header("Bowling Phase Analytics")
    st.markdown("---")

    analysis_type = st.selectbox(
        "Choose Analysis",
        [
            "Best Powerplay Bowlers",
            "Most Powerplay Wickets",
            "Best Death Bowlers",
            "Most Death Over Wickets",
        ],
    )

    if analysis_type == "Best Powerplay Bowlers":
        data = best_powerplay_bowlers(deliveries)
        st.subheader("Best Powerplay Economy")
        _render_bar_chart(
            data,
            "Economy",
            "Best Powerplay Bowlers",
        )

    elif analysis_type == "Most Powerplay Wickets":
        data = most_powerplay_wickets(deliveries)
        st.subheader("Most Powerplay Wickets")
        _render_bar_chart(
            data,
            "Wickets",
            "Most Powerplay Wickets",
        )

    elif analysis_type == "Best Death Bowlers":
        data = best_death_bowlers(deliveries)
        st.subheader("Best Death Over Economy")
        _render_bar_chart(
            data,
            "Economy",
            "Best Death Bowlers",
        )

    else:
        data = most_death_over_wickets(deliveries)
        st.subheader("Most Death Over Wickets")
        _render_bar_chart(
            data,
            "Wickets",
            "Most Death Over Wickets",
        )
