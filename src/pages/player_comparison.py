import streamlit as st

from src.recommender.player_similarity import (
    DISPLAY_COLUMNS,
    build_player_feature_matrix,
    get_comparison_chart_data,
    get_player_comparison,
    get_player_similarity_scores,
    get_radar_chart_data,
    get_underrated_alternatives,
)
from src.ui.charts import create_bar_chart, create_radar_chart


@st.cache_data
def _get_player_features(deliveries):
    return build_player_feature_matrix(deliveries)


def show_player_comparison(deliveries):
    st.header("Player Comparison & Similarity Engine")
    st.markdown("---")

    feature_table = _get_player_features(deliveries)
    players = sorted(feature_table.index.tolist())

    tab1, tab2, tab3 = st.tabs(
        [
            "Player Comparison",
            "Similarity Engine",
            "Underrated Alternatives",
        ]
    )

    with tab1:
        _show_player_comparison_tab(feature_table, players)

    with tab2:
        _show_similarity_tab(feature_table, players)

    with tab3:
        _show_underrated_tab(feature_table, players)


def _show_player_comparison_tab(feature_table, players):
    col1, col2 = st.columns(2)

    player_1 = col1.selectbox(
        "Player 1",
        players,
        index=0,
        key="comparison_player_1",
    )
    default_player_2_index = 1 if len(players) > 1 else 0
    player_2 = col2.selectbox(
        "Player 2",
        players,
        index=default_player_2_index,
        key="comparison_player_2",
    )

    if player_1 == player_2:
        st.warning("Please select two different players.")
        return

    comparison = get_player_comparison(
        player_1,
        player_2,
        feature_table,
    )

    _show_comparison_metric_cards(comparison, player_1, player_2)

    st.markdown("---")

    table_tab, chart_tab, radar_tab = st.tabs(
        [
            "Comparison Table",
            "Metric Bars",
            "Player Radar",
        ]
    )

    with table_tab:
        st.write(comparison[DISPLAY_COLUMNS])

    with chart_tab:
        chart_data = get_comparison_chart_data(comparison)
        fig = create_bar_chart(
            chart_data,
            x="Metric",
            y="Value",
            color="Player",
            title=f"{player_1} vs {player_2}",
            x_axis_title="Metric",
            y_axis_title="Value",
        )
        st.plotly_chart(fig, use_container_width=True)

    with radar_tab:
        radar_data = get_radar_chart_data(comparison)
        fig = create_radar_chart(
            radar_data,
            title="Normalized Player Skill Radar",
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Metric Notes"):
        st.write(
            "Radar values are normalized within the selected pair. "
            "Dot Ball Control is inverted from dot ball percentage, so higher is better."
        )


def _show_similarity_tab(feature_table, players):
    selected_player = st.selectbox(
        "Select Player",
        players,
        key="similarity_player",
    )

    similar_players = get_player_similarity_scores(
        selected_player,
        feature_table,
        top_n=5,
    )

    col1, col2, col3 = st.columns(3)
    selected = feature_table.loc[selected_player]
    col1.metric("Runs", int(selected["Runs"]))
    col2.metric("Strike Rate", round(selected["Strike Rate"], 2))
    col3.metric("Average", round(selected["Average"], 2))

    st.markdown("---")
    st.write(similar_players)

    fig = create_bar_chart(
        similar_players["Similarity %"],
        title=f"Players Most Similar to {selected_player}",
        x_axis_title="Player",
        y_axis_title="Similarity %",
    )
    st.plotly_chart(fig, use_container_width=True)

    top_match = similar_players.iloc[0]
    comparison = get_player_comparison(
        selected_player,
        top_match.name,
        feature_table,
    )
    radar_data = get_radar_chart_data(comparison)

    fig = create_radar_chart(
        radar_data,
        title=f"{selected_player} vs Closest Match: {top_match.name}",
    )
    st.plotly_chart(fig, use_container_width=True)


def _show_underrated_tab(feature_table, players):
    selected_player = st.selectbox(
        "Find alternatives for",
        players,
        key="underrated_player",
    )

    alternatives = get_underrated_alternatives(
        selected_player,
        feature_table,
        top_n=5,
    )

    if alternatives.empty:
        st.info("No lower-run alternatives found for this player with the current filters.")
        return

    st.write(alternatives)

    fig = create_bar_chart(
        alternatives["Underrated Score"],
        title=f"Underrated Alternatives to {selected_player}",
        x_axis_title="Player",
        y_axis_title="Underrated Score",
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Why these players?"):
        st.write(
            "Alternatives are players with lower total runs than the selected player, "
            "ranked by similarity plus strong strike-rate and average profiles."
        )


def _show_comparison_metric_cards(comparison, player_1, player_2):
    player_1_stats = comparison.loc[player_1]
    player_2_stats = comparison.loc[player_2]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Runs",
        int(player_1_stats["Runs"]),
        f"{player_2}: {int(player_2_stats['Runs'])}",
    )
    col2.metric(
        "Strike Rate",
        round(player_1_stats["Strike Rate"], 2),
        f"{player_2}: {round(player_2_stats['Strike Rate'], 2)}",
    )
    col3.metric(
        "Average",
        round(player_1_stats["Average"], 2),
        f"{player_2}: {round(player_2_stats['Average'], 2)}",
    )
    col4.metric(
        "Consistency",
        round(player_1_stats["Consistency Score"], 2),
        f"{player_2}: {round(player_2_stats['Consistency Score'], 2)}",
    )
