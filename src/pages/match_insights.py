import streamlit as st

from src.advanced_analytics import (
    chase_difficulty_index,
    over_by_over_momentum,
    team_run_rate_progression,
)
from src.analysis import (
    biggest_win_margins,
    closest_matches,
    highest_successful_chases,
    highest_team_scores,
    lowest_defended_totals,
)
from src.ui.charts import create_bar_chart, create_multi_line_chart


def _show_table_and_bar_chart(data, labels, values, ylabel, title):
    tab1, tab2 = st.tabs(
        [
            "Stats Table",
            "Visualization",
        ]
    )

    with tab1:
        st.write(data)

    with tab2:
        chart_data = data.copy()
        chart_data["ChartLabel"] = labels

        fig = create_bar_chart(
            chart_data,
            x="ChartLabel",
            y=values.name,
            title=title,
            x_axis_title="Match",
            y_axis_title=ylabel,
        )

        st.plotly_chart(fig, use_container_width=True)


def show_match_insights(matches, deliveries):
    st.header("Advanced Match Insights")
    st.markdown("---")

    tab1, tab2 = st.tabs(
        [
            "Record Insights",
            "Match Intelligence",
        ]
    )

    with tab1:
        _show_record_insights(matches, deliveries)

    with tab2:
        _show_match_intelligence(matches, deliveries)


def _show_record_insights(matches, deliveries):
    insight_option = st.selectbox(
        "Choose Insight",
        [
            "Highest Team Scores",
            "Highest Successful Chases",
            "Lowest Defended Totals",
            "Biggest Win Margins",
            "Closest Matches",
        ],
    )

    if insight_option == "Highest Team Scores":
        data = highest_team_scores(deliveries)
        st.subheader("Highest Team Totals in IPL")
        st.markdown("---")

        labels = data["BattingTeam"].astype(str) + " (" + data["total_run"].astype(str) + ")"
        _show_table_and_bar_chart(
            data,
            labels,
            data["total_run"],
            "Runs",
            "Highest Team Scores",
        )

    elif insight_option == "Highest Successful Chases":
        data = highest_successful_chases(matches, deliveries)
        st.subheader("Highest Successful Chases")
        st.markdown("---")

        labels = (
            data["BattingTeam_chase"].astype(str)
            + " ("
            + data["total_run_chase"].astype(str)
            + ")"
        )
        _show_table_and_bar_chart(
            data,
            labels,
            data["total_run_chase"],
            "Runs",
            "Highest Successful Chases",
        )

    elif insight_option == "Biggest Win Margins":
        data = biggest_win_margins(matches)
        st.subheader("Biggest Wins by Runs")
        st.markdown("---")

        labels = data["WinningTeam"].astype(str) + " (" + data["Margin"].astype(str) + ")"
        _show_table_and_bar_chart(
            data,
            labels,
            data["Margin"],
            "Runs",
            "Biggest Win Margins",
        )

    elif insight_option == "Lowest Defended Totals":
        data = lowest_defended_totals(matches, deliveries)
        st.subheader("Lowest Successfully Defended Totals")
        st.markdown("---")

        labels = (
            data["BattingTeam_defend"].astype(str)
            + " ("
            + data["total_run_defend"].astype(str)
            + ")"
        )
        _show_table_and_bar_chart(
            data,
            labels,
            data["total_run_defend"],
            "Runs",
            "Lowest Defended Totals",
        )

    else:
        data = closest_matches(matches)
        st.subheader("Closest IPL Matches")
        st.markdown("---")

        labels = data["WinningTeam"].astype(str) + " (" + data["Margin"].astype(str) + ")"
        _show_table_and_bar_chart(
            data,
            labels,
            data["Margin"],
            "Winning Margin",
            "Closest Matches",
        )


def _show_match_intelligence(matches, deliveries):
    match_ids = sorted(deliveries["ID"].dropna().unique(), reverse=True)

    metric_option = st.selectbox(
        "Choose Match Intelligence Metric",
        [
            "Team Run Rate Progression",
            "Over-by-Over Momentum",
            "Chase Difficulty Index",
        ],
    )

    if metric_option == "Chase Difficulty Index":
        data = chase_difficulty_index(matches, deliveries)

        col1, col2, col3 = st.columns(3)
        hardest = data.iloc[0]
        successful = data[data["Result"] == "Won"]
        hardest_success = successful.iloc[0] if not successful.empty else hardest
        average_index = round(data["Chase Difficulty Index"].mean(), 2)

        col1.metric("Hardest Chase Index", hardest["Chase Difficulty Index"], hardest["ChasingTeam"])
        col2.metric(
            "Hardest Successful Chase",
            hardest_success["Chase Difficulty Index"],
            hardest_success["ChasingTeam"],
        )
        col3.metric("Average Difficulty", average_index)

        st.write(data.head(20))

        fig = create_bar_chart(
            data.head(15),
            x="ChasingTeam",
            y="Chase Difficulty Index",
            title="Most Difficult Chases",
            x_axis_title="Chasing Team",
            y_axis_title="Difficulty Index",
            color="Result",
        )
        st.plotly_chart(fig, use_container_width=True)
        return

    match_id = st.selectbox(
        "Select Match ID",
        match_ids,
    )

    if metric_option == "Team Run Rate Progression":
        data = team_run_rate_progression(deliveries, match_id)
        data["Team Innings"] = (
            data["BattingTeam"].astype(str)
            + " - Innings "
            + data["innings"].astype(str)
        )

        st.write(data)

        fig = create_multi_line_chart(
            data,
            x="Overs Completed",
            y="Run Rate",
            color="Team Innings",
            title=f"Team Run Rate Progression - Match {match_id}",
            x_axis_title="Overs Completed",
            y_axis_title="Run Rate",
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        data = over_by_over_momentum(deliveries, match_id)
        data["Team Innings"] = (
            data["BattingTeam"].astype(str)
            + " - Innings "
            + data["innings"].astype(str)
        )

        col1, col2, col3 = st.columns(3)
        best_over = data.sort_values("Momentum Score", ascending=False).iloc[0]
        highest_runs = data.sort_values("Runs", ascending=False).iloc[0]
        wicket_over = data.sort_values("Wickets", ascending=False).iloc[0]

        col1.metric("Peak Momentum", best_over["Momentum Score"], best_over["BattingTeam"])
        col2.metric("Best Scoring Over", highest_runs["Runs"], highest_runs["BattingTeam"])
        col3.metric("Most Wickets in Over", wicket_over["Wickets"], wicket_over["BattingTeam"])

        st.write(data)

        fig = create_multi_line_chart(
            data,
            x="overs",
            y="Momentum Score",
            color="Team Innings",
            title=f"Over-by-Over Momentum - Match {match_id}",
            x_axis_title="Over",
            y_axis_title="Momentum Score",
        )
        st.plotly_chart(fig, use_container_width=True)
