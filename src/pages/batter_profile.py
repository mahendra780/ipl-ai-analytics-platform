import streamlit as st

from src.analysis import (
    batter_career_progression,
    batter_profile,
    season_batter_profile,
)

from src.ui.charts import (
    create_line_chart,
)


def _select_batter(
    deliveries,
    key_suffix=""
):

    return st.selectbox(
        "Select Batter",
        sorted(
            deliveries["batter"]
            .dropna()
            .unique()
        ),
        key=f"batter_select_{key_suffix}"
    )


def _render_batter_metrics(profile):

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Matches",
        profile["Matches"]
    )

    col2.metric(
        "Runs",
        profile["Runs"]
    )

    col3.metric(
        "Highest Score",
        profile["Highest Score"]
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "50s",
        profile["50s"]
    )

    col5.metric(
        "100s",
        profile["100s"]
    )

    col6.metric(
        "Strike Rate",
        profile["Strike Rate"]
    )

    col7, col8 = st.columns(2)

    col7.metric(
        "Fours",
        profile["Fours"]
    )

    col8.metric(
        "Sixes",
        profile["Sixes"]
    )


def show_batter_profile(deliveries):

    st.header("Batter Profile")

    st.markdown("---")

    batter_name = _select_batter(
        deliveries,
        "profile"
    )

    profile = batter_profile(
        deliveries,
        batter_name
    )

    _render_batter_metrics(profile)


def show_season_batter_analysis(deliveries):

    st.header("Season-wise Batter Analysis")

    st.markdown("---")

    batter_name = _select_batter(
        deliveries,
        "season"
    )

    season = st.selectbox(
        "Select Season",
        sorted(
            deliveries["Season"]
            .dropna()
            .astype(str)
            .unique()
        ),
        key="season_analysis_select"
    )

    profile = season_batter_profile(
        deliveries,
        batter_name,
        season,
    )

    _render_batter_metrics(profile)


def show_career_progression(deliveries):

    st.header("Batter Career Progression")

    batter_name = _select_batter(
        deliveries,
        "career"
    )

    progression = batter_career_progression(
        deliveries,
        batter_name
    )

    st.markdown("---")

    tab1, tab2 = st.tabs([
        "Season Stats",
        "Career Graph",
    ])

    with tab1:

        st.write(progression)

    with tab2:

        fig = create_line_chart(
            progression,
            title=f"{batter_name} Career Progression",
            x_axis_title="Season",
            y_axis_title="Runs",
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )