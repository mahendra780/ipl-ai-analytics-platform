import streamlit as st

from src.advanced_analytics import (
    advanced_bowling_summary,
    bowling_impact_score,
    death_over_economy,
    dot_ball_pressure,
    wicket_frequency,
)
from src.ui.charts import create_bar_chart, create_scatter_chart


def show_bowling_analytics(deliveries):
    st.header("Bowling Analytics")
    st.markdown("---")

    tab1, tab2 = st.tabs(
        [
            "Core Analytics",
            "Advanced Intelligence",
        ]
    )

    with tab1:
        _show_core_bowling_analytics(deliveries)

    with tab2:
        _show_advanced_bowling_analytics(deliveries)


def _show_core_bowling_analytics(deliveries):
    bowling_option = st.selectbox(
        "Choose Analysis",
        [
            "Most Wickets",
            "Best Economy",
            "Most Dot Balls",
        ],
    )

    if bowling_option == "Most Wickets":
        data = (
            deliveries[deliveries["isWicketDelivery"] == 1]
            .groupby("bowler")["isWicketDelivery"]
            .count()
            .sort_values(ascending=False)
            .head(10)
        )

    elif bowling_option == "Best Economy":
        bowler_stats = deliveries.groupby("bowler").agg(
            {
                "total_run": "sum",
                "ballnumber": "count",
            }
        )

        bowler_stats["Overs"] = bowler_stats["ballnumber"] / 6
        bowler_stats["Economy"] = bowler_stats["total_run"] / bowler_stats["Overs"]

        data = (
            bowler_stats[bowler_stats["ballnumber"] >= 500]["Economy"]
            .sort_values()
            .head(10)
        )

    else:
        data = (
            deliveries[deliveries["total_run"] == 0]
            .groupby("bowler")["total_run"]
            .count()
            .sort_values(ascending=False)
            .head(10)
        )

    st.write(data)

    if bowling_option == "Most Wickets":
        y_axis_title = "Wickets"
    elif bowling_option == "Best Economy":
        y_axis_title = "Economy"
    else:
        y_axis_title = "Dot Balls"

    fig = create_bar_chart(
        data,
        title=bowling_option,
        x_axis_title="Bowler",
        y_axis_title=y_axis_title,
    )

    st.plotly_chart(fig, use_container_width=True)


def _show_advanced_bowling_analytics(deliveries):
    summary = advanced_bowling_summary(deliveries)
    impact = bowling_impact_score(deliveries)

    col1, col2, col3 = st.columns(3)
    top_pressure = summary[summary["Balls"] >= 100].sort_values(
        "Dot Ball Pressure %",
        ascending=False,
    ).iloc[0]
    best_frequency = summary[summary["Balls/Wicket"].notna()].sort_values(
        "Balls/Wicket",
    ).iloc[0]
    top_impact = impact.iloc[0]

    col1.metric(
        "Best Dot Pressure",
        f"{top_pressure['Dot Ball Pressure %']}%",
        f"{top_pressure.name}",
    )
    col2.metric(
        "Best Wicket Frequency",
        f"{best_frequency['Balls/Wicket']}",
        f"{best_frequency.name}",
    )
    col3.metric(
        "Top Impact Score",
        f"{top_impact['Bowling Impact Score']}",
        f"{top_impact.name}",
    )

    st.markdown("---")

    metric_option = st.selectbox(
        "Choose Advanced Bowling Metric",
        [
            "Dot Ball Pressure",
            "Wicket Frequency",
            "Death Over Economy",
            "Bowling Impact Score",
            "Bowling Comparison Matrix",
        ],
    )

    if metric_option == "Dot Ball Pressure":
        data = dot_ball_pressure(deliveries).head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Dot Ball Pressure %"],
            title="Dot Ball Pressure Leaders",
            x_axis_title="Bowler",
            y_axis_title="Dot Ball Pressure %",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "Wicket Frequency":
        data = wicket_frequency(deliveries).head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Balls/Wicket"],
            title="Best Wicket Frequency",
            x_axis_title="Bowler",
            y_axis_title="Balls per Wicket",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "Death Over Economy":
        data = death_over_economy(deliveries).head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Death Economy"],
            title="Best Death Over Economy",
            x_axis_title="Bowler",
            y_axis_title="Economy",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "Bowling Impact Score":
        data = impact.head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Bowling Impact Score"],
            title="Bowling Impact Score",
            x_axis_title="Bowler",
            y_axis_title="Impact Score",
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        comparison = summary[summary["Balls"] >= 500].head(60).reset_index()
        st.write(
            comparison[
                [
                    "bowler",
                    "Wickets",
                    "Economy",
                    "Dot Ball Pressure %",
                    "Balls/Wicket",
                    "Overs",
                ]
            ].head(20)
        )
        fig = create_scatter_chart(
            comparison,
            x="Economy",
            y="Dot Ball Pressure %",
            color="bowler",
            size="Wickets",
            title="Bowling Comparison Matrix",
            x_axis_title="Economy",
            y_axis_title="Dot Ball Pressure %",
        )
        st.plotly_chart(fig, use_container_width=True)
