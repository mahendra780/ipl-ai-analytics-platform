import streamlit as st

from src.advanced_analytics import (
    advanced_batting_summary,
    average_runs_per_innings,
    batting_consistency_score,
    batting_dot_ball_percentage,
    boundary_dependency,
    boundary_percentage,
    phase_wise_strike_rate,
)
from src.ui.charts import create_bar_chart, create_scatter_chart


def show_batting_analytics(deliveries):
    st.header("Batting Analytics")
    st.markdown("---")

    tab1, tab2 = st.tabs(
        [
            "Core Analytics",
            "Advanced Intelligence",
        ]
    )

    with tab1:
        _show_core_batting_analytics(deliveries)

    with tab2:
        _show_advanced_batting_analytics(deliveries)


def _show_core_batting_analytics(deliveries):
    batting_option = st.selectbox(
        "Choose Analysis",
        [
            "Top Run Scorers",
            "Most Sixes",
            "Most Fours",
            "Best Strike Rate",
        ],
    )

    if batting_option == "Top Run Scorers":
        data = (
            deliveries.groupby("batter")["batsman_run"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

    elif batting_option == "Most Sixes":
        data = (
            deliveries[deliveries["batsman_run"] == 6]
            .groupby("batter")["batsman_run"]
            .count()
            .sort_values(ascending=False)
            .head(10)
        )

    elif batting_option == "Most Fours":
        data = (
            deliveries[deliveries["batsman_run"] == 4]
            .groupby("batter")["batsman_run"]
            .count()
            .sort_values(ascending=False)
            .head(10)
        )

    else:
        batter_stats = deliveries.groupby("batter").agg(
            {
                "batsman_run": "sum",
                "ballnumber": "count",
            }
        )

        batter_stats["StrikeRate"] = (
            batter_stats["batsman_run"] / batter_stats["ballnumber"]
        ) * 100

        data = (
            batter_stats[batter_stats["ballnumber"] >= 500]["StrikeRate"]
            .sort_values(ascending=False)
            .head(10)
        )

    st.write(data)

    if batting_option == "Top Run Scorers":
        y_axis_title = "Runs"
    elif batting_option == "Most Sixes":
        y_axis_title = "Sixes"
    elif batting_option == "Most Fours":
        y_axis_title = "Fours"
    else:
        y_axis_title = "Strike Rate"

    fig = create_bar_chart(
        data,
        title=batting_option,
        x_axis_title="Batter",
        y_axis_title=y_axis_title,
    )

    st.plotly_chart(fig, use_container_width=True)


def _show_advanced_batting_analytics(deliveries):
    summary = advanced_batting_summary(deliveries)

    col1, col2, col3 = st.columns(3)
    top_boundary = summary.sort_values("Boundary %", ascending=False).iloc[0]
    top_average = summary.sort_values("AverageRuns", ascending=False).iloc[0]
    lowest_dot = summary.sort_values("Dot Ball %").iloc[0]

    col1.metric(
        "Best Boundary %",
        f"{top_boundary['Boundary %']}%",
        f"{top_boundary.name}",
    )
    col2.metric(
        "Best Avg/Innings",
        round(top_average["AverageRuns"], 2),
        f"{top_average.name}",
    )
    col3.metric(
        "Lowest Dot Ball %",
        f"{lowest_dot['Dot Ball %']}%",
        f"{lowest_dot.name}",
    )

    st.markdown("---")

    metric_option = st.selectbox(
        "Choose Advanced Batting Metric",
        [
            "Boundary Percentage",
            "Dot Ball Percentage",
            "Batting Consistency Score",
            "Phase-wise Strike Rate",
            "Boundary Dependency",
            "Average Runs Per Innings",
            "Batting Comparison Matrix",
        ],
    )

    if metric_option == "Boundary Percentage":
        data = boundary_percentage(deliveries).head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Boundary %"],
            title="Boundary Percentage Leaders",
            x_axis_title="Batter",
            y_axis_title="Boundary %",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "Dot Ball Percentage":
        data = batting_dot_ball_percentage(deliveries).head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Dot Ball %"],
            title="Lowest Dot Ball Percentage",
            x_axis_title="Batter",
            y_axis_title="Dot Ball %",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "Batting Consistency Score":
        data = batting_consistency_score(deliveries).head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Consistency Score"],
            title="Batting Consistency Score",
            x_axis_title="Batter",
            y_axis_title="Consistency Score",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "Phase-wise Strike Rate":
        phase_data = phase_wise_strike_rate(deliveries)
        phase = st.selectbox(
            "Select Phase",
            [
                "Powerplay",
                "Middle Overs",
                "Death Overs",
            ],
        )
        data = phase_data[phase_data["Phase"] == phase].head(15)
        st.write(data)
        fig = create_bar_chart(
            data,
            x="batter",
            y="Strike Rate",
            title=f"{phase} Strike Rate Leaders",
            x_axis_title="Batter",
            y_axis_title="Strike Rate",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "Boundary Dependency":
        data = boundary_dependency(deliveries).head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Boundary Dependency %"],
            title="Boundary Dependency",
            x_axis_title="Batter",
            y_axis_title="Runs from Boundaries %",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "Average Runs Per Innings":
        data = average_runs_per_innings(deliveries).head(15)
        st.write(data)
        fig = create_bar_chart(
            data["Average Runs/Innings"],
            title="Average Runs Per Innings",
            x_axis_title="Batter",
            y_axis_title="Average Runs",
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        comparison = summary[summary["Balls"] >= 500].head(60).reset_index()
        st.write(
            comparison[
                [
                    "batter",
                    "Runs",
                    "Strike Rate",
                    "Boundary %",
                    "Dot Ball %",
                    "Boundary Dependency %",
                    "AverageRuns",
                ]
            ].head(20)
        )
        fig = create_scatter_chart(
            comparison,
            x="Strike Rate",
            y="AverageRuns",
            color="batter",
            size="Runs",
            title="Batting Comparison Matrix",
            x_axis_title="Strike Rate",
            y_axis_title="Average Runs/Innings",
        )
        st.plotly_chart(fig, use_container_width=True)
