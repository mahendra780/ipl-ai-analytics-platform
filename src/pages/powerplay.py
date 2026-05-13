import streamlit as st

from src.analysis import (
    best_death_over_batters,
    best_powerplay_batters,
    death_over_strike_rate,
)
from src.ui.charts import create_bar_chart


def _render_bar_chart(data, ylabel, title, use_tabs=False):
    if use_tabs:
        tab1, tab2 = st.tabs(
            [
                "Stats Table",
                "Visualization",
            ]
        )

        with tab1:
            st.write(data)

        with tab2:
            _plot_series(data, ylabel, title)

        return

    st.write(data)
    _plot_series(data, ylabel, title)


def _plot_series(data, ylabel, title):
    fig = create_bar_chart(
        data,
        title=title,
        x_axis_title="Batter",
        y_axis_title=ylabel,
    )
    st.plotly_chart(fig, use_container_width=True)


def show_powerplay_analysis(deliveries):
    st.header("Powerplay & Death Overs Analysis")
    st.markdown("---")

    analysis_type = st.selectbox(
        "Choose Analysis",
        [
            "Best Powerplay Batters",
            "Best Death Over Batters",
            "Best Death Over Strike Rate",
        ],
    )

    if analysis_type == "Best Powerplay Batters":
        data = best_powerplay_batters(deliveries)
        st.subheader("Top Powerplay Run Scorers")
        st.markdown("---")
        _render_bar_chart(
            data,
            "Runs",
            "Best Powerplay Batters",
            use_tabs=True,
        )

    elif analysis_type == "Best Death Over Batters":
        data = best_death_over_batters(deliveries)
        st.subheader("Top Death Over Run Scorers")
        _render_bar_chart(
            data,
            "Runs",
            "Best Death Over Batters",
        )

    else:
        data = death_over_strike_rate(deliveries)
        st.subheader("Best Death Over Strike Rates")
        _render_bar_chart(
            data,
            "Strike Rate",
            "Death Over Strike Rates",
        )
