import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("dark_background")
from src.analysis import batter_profile
from src.analysis import bowler_profile
from src.analysis import head_to_head
from src.analysis import season_batter_profile
from src.analysis import batter_career_progression
from src.analysis import (

    highest_team_scores,

    highest_successful_chases,

    lowest_defended_totals,

    biggest_win_margins,

    closest_matches
)
from src.analysis import (

    best_powerplay_batters,

    best_death_over_batters,

    death_over_strike_rate
)
from src.analysis import (

    best_powerplay_bowlers,

    most_powerplay_wickets,

    best_death_bowlers,

    most_death_over_wickets
)
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

matches = pd.read_csv(
    "data/processed/matches_cleaned.csv"
)

deliveries = pd.read_csv(
    "data/processed/deliveries_cleaned.csv",
    low_memory=False

)
from src.feature_engineering import (
    create_match_situation
)

from src.model_training import (
    train_model
)

# =====================================================
# TRAIN MODEL
# =====================================================

match_df = create_match_situation(
    matches,
    deliveries
)

model = train_model(
    match_df
)

# =====================================================
# TITLE
# =====================================================

# st.title("🏏 IPL Analytics Dashboard")

st.markdown("""

# 🏏 IPL AI Analytics Platform

### Advanced Cricket Intelligence & Win Prediction System

""")

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.markdown("""

# 🏏 IPL Analytics

### AI Powered Dashboard

""")
section = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Batting Analytics",
        "Bowling Analytics",
        "Batter Profile",
        "Bowler Profile",
        "Head-to-Head",
        "Season-wise Batter Analysis",
        "Career Progression",
        "Advanced Match Insights",
        "Powerplay & Death Overs",
        "Bowling Phase Analytics",
        "Win Predictor",

    ]
)

# =====================================================
# OVERVIEW
# =====================================================

if section == "Overview":

    st.header("IPL Overview")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Matches",
        len(matches)
    )

    col2.metric(
        "Total Seasons",
        matches['Season'].nunique()
    )

    col3.metric(
        "Total Teams",
        matches['WinningTeam'].nunique()
    )

    st.subheader("Team Wins")

    team_wins = (
        matches['WinningTeam']
        .value_counts()
    )

    fig, ax = plt.subplots(figsize=(12,6))

    team_wins.plot(kind='bar', ax=ax)

    plt.xticks(rotation=90)

    st.pyplot(fig)

# =====================================================
# BATTING ANALYTICS
# =====================================================

elif section == "Batting Analytics":

    st.header("Batting Analytics")

    st.markdown("---")

    batting_option = st.selectbox(
        "Choose Analysis",
        [
            "Top Run Scorers",
            "Most Sixes",
            "Most Fours",
            "Best Strike Rate",

        ]
    )

    # TOP RUNS
    if batting_option == "Top Run Scorers":

        data = (
            deliveries
            .groupby('batter')['batsman_run']
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.write(data)

        fig, ax = plt.subplots(figsize=(12,6))

        data.plot(kind='bar', ax=ax)

        st.pyplot(fig)

    # MOST SIXES
    elif batting_option == "Most Sixes":

        data = (
            deliveries[
                deliveries['batsman_run'] == 6
            ]
            .groupby('batter')['batsman_run']
            .count()
            .sort_values(ascending=False)
            .head(10)
        )

        st.write(data)

        fig, ax = plt.subplots(figsize=(12,6))

        data.plot(kind='bar', ax=ax)

        st.pyplot(fig)

    # MOST FOURS
    elif batting_option == "Most Fours":

        data = (
            deliveries[
                deliveries['batsman_run'] == 4
            ]
            .groupby('batter')['batsman_run']
            .count()
            .sort_values(ascending=False)
            .head(10)
        )

        st.write(data)

        fig, ax = plt.subplots(figsize=(12,6))

        data.plot(kind='bar', ax=ax)

        st.pyplot(fig)

    # STRIKE RATE
    elif batting_option == "Best Strike Rate":

        batter_stats = (
            deliveries
            .groupby('batter')
            .agg({
                'batsman_run': 'sum',
                'ballnumber': 'count'
            })
        )

        batter_stats['StrikeRate'] = (
            batter_stats['batsman_run']
            / batter_stats['ballnumber']
        ) * 100

        data = (
            batter_stats[
                batter_stats['ballnumber'] >= 500
            ]['StrikeRate']
            .sort_values(ascending=False)
            .head(10)
        )

        st.write(data)

        fig, ax = plt.subplots(figsize=(12,6))

        data.plot(kind='bar', ax=ax)

        st.pyplot(fig)

# =====================================================
# BOWLING ANALYTICS
# =====================================================

elif section == "Bowling Analytics":

    st.header("Bowling Analytics")

    st.markdown("---")

    bowling_option = st.selectbox(
        "Choose Analysis",
        [
            "Most Wickets",
            "Best Economy",
            "Most Dot Balls"
        ]
    )

    # MOST WICKETS
    if bowling_option == "Most Wickets":

        data = (
            deliveries[
                deliveries['isWicketDelivery'] == 1
            ]
            .groupby('bowler')['isWicketDelivery']
            .count()
            .sort_values(ascending=False)
            .head(10)
        )

        st.write(data)

        fig, ax = plt.subplots(figsize=(12,6))

        data.plot(kind='bar', ax=ax)

        st.pyplot(fig)

    # BEST ECONOMY
    elif bowling_option == "Best Economy":

        bowler_stats = (
            deliveries
            .groupby('bowler')
            .agg({
                'total_run': 'sum',
                'ballnumber': 'count'
            })
        )

        bowler_stats['Overs'] = (
            bowler_stats['ballnumber'] / 6
        )

        bowler_stats['Economy'] = (
            bowler_stats['total_run']
            / bowler_stats['Overs']
        )

        data = (
            bowler_stats[
                bowler_stats['ballnumber'] >= 500
            ]['Economy']
            .sort_values()
            .head(10)
        )

        st.write(data)

        fig, ax = plt.subplots(figsize=(12,6))

        data.plot(kind='bar', ax=ax)

        st.pyplot(fig)

    # DOT BALLS
    elif bowling_option == "Most Dot Balls":

        data = (
            deliveries[
                deliveries['total_run'] == 0
            ]
            .groupby('bowler')['total_run']
            .count()
            .sort_values(ascending=False)
            .head(10)
        )

        st.write(data)

        fig, ax = plt.subplots(figsize=(12,6))

        data.plot(kind='bar', ax=ax)

        st.pyplot(fig)
# =====================================================
# BATTER PROFILE
# =====================================================

elif section == "Batter Profile":

    st.header("🏏 Batter Profile")

    st.markdown("---")

    # Batter selection
    batter_name = st.selectbox(
        "Select Batter",
        sorted(
            deliveries['batter']
            .dropna()
            .unique()
        )
    )

    # Get profile
    profile = batter_profile(
        deliveries,
        batter_name
    )

    # ================= KPI CARDS ================= #

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Matches",
        profile['Matches']
    )

    col2.metric(
        "Runs",
        profile['Runs']
    )

    col3.metric(
        "Highest Score",
        profile['Highest Score']
    )

    # ================= SECOND ROW ================= #

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "50s",
        profile['50s']
    )

    col5.metric(
        "100s",
        profile['100s']
    )

    col6.metric(
        "Strike Rate",
        profile['Strike Rate']
    )

    # ================= THIRD ROW ================= #

    col7, col8 = st.columns(2)

    col7.metric(
        "Fours",
        profile['Fours']
    )

    col8.metric(
        "Sixes",
        profile['Sixes']
    )
# =====================================================
# SEASON-WISE BATTER ANALYSIS
# =====================================================

elif section == "Season-wise Batter Analysis":

    st.header("📈 Season-wise Batter Analysis")

    st.markdown("---")

    # Batter selection
    batter_name = st.selectbox(

        "Select Batter",

        sorted(
            deliveries['batter']
            .dropna()
            .unique()
        )
    )

    # Season selection
    season = st.selectbox(

        "Select Season",

        sorted(
            deliveries['Season']
            .dropna()
            .astype(str)
            .unique()
        )
    )

    # Get profile
    profile = season_batter_profile(

        deliveries,

        batter_name,

        season
    )

    # ================= ROW 1 ================= #

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Matches",
        profile['Matches']
    )

    col2.metric(
        "Runs",
        profile['Runs']
    )

    col3.metric(
        "Highest Score",
        profile['Highest Score']
    )

    # ================= ROW 2 ================= #

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "50s",
        profile['50s']
    )

    col5.metric(
        "100s",
        profile['100s']
    )

    col6.metric(
        "Strike Rate",
        profile['Strike Rate']
    )

    # ================= ROW 3 ================= #

    col7, col8 = st.columns(2)

    col7.metric(
        "Fours",
        profile['Fours']
    )

    col8.metric(
        "Sixes",
        profile['Sixes']
    )

# =====================================================
# CAREER PROGRESSION
# =====================================================

elif section == "Career Progression":

    st.header("📈 Batter Career Progression")

    batter_name = st.selectbox(

        "Select Batter",

        sorted(
            deliveries['batter']
            .dropna()
            .unique()
        )
    )

    progression = batter_career_progression(

        deliveries,

        batter_name
    )

    st.markdown("---")

    tab1, tab2 = st.tabs([
        "📊 Season Stats",
        "📈 Career Graph"
    ])

    # =============================================
    # TAB 1
    # =============================================

    with tab1:

        st.write(progression)

    # =============================================
    # TAB 2
    # =============================================

    with tab2:

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        progression.plot(

            kind='line',

            marker='o',

            ax=ax
        )

        plt.title(
            f"{batter_name} Career Progression"
        )

        plt.xlabel("Season")

        plt.ylabel("Runs")

        plt.xticks(rotation=45)

        st.pyplot(fig)

# =====================================================
# ADVANCED MATCH INSIGHTS
# =====================================================

elif section == "Advanced Match Insights":

    st.header("🔥 Advanced Match Insights")

    st.markdown("---")

    insight_option = st.selectbox(

        "Choose Insight",

        [
            "Highest Team Scores",
            "Highest Successful Chases",
            "Lowest Defended Totals",
            "Biggest Win Margins",
            "Closest Matches"
        ]
    )
    # =================================================
    # HIGHEST TEAM SCORES
    # =================================================

    if insight_option == "Highest Team Scores":

        data = highest_team_scores(
            deliveries
        )

        st.subheader(
            "Highest Team Totals in IPL"
        )

        st.markdown("---")

        # =============================================
        # CREATE TABS
        # =============================================

        tab1, tab2 = st.tabs([
            "📊 Stats Table",
            "📈 Visualization"
        ])

        # =============================================
        # TAB 1 → TABLE
        # =============================================

        with tab1:

            st.write(data)

        # =============================================
        # TAB 2 → CHART
        # =============================================

        with tab2:

            fig, ax = plt.subplots(
                figsize=(12,6)
            )

            labels = (
                data['BattingTeam']
                + " ("
                + data['total_run']
                .astype(str)
                + ")"
            )

            ax.bar(
                labels,
                data['total_run']
            )

            plt.xticks(rotation=90)

            plt.ylabel("Runs")

            plt.title(
                "Highest Team Scores"
            )

            st.pyplot(fig)
    # =================================================
    # HIGHEST SUCCESSFUL CHASES
    # =================================================

    elif insight_option == "Highest Successful Chases":

        data = highest_successful_chases(
            matches,
            deliveries
        )

        st.subheader(
            "Highest Successful Chases"
        )

        st.markdown("---")

        tab1, tab2 = st.tabs([
            "📊 Stats Table",
            "📈 Visualization"
        ])

        # ============================================
        # TAB 1
        # ============================================

        with tab1:

            st.write(data)

        # ============================================
        # TAB 2
        # ============================================

        with tab2:

            fig, ax = plt.subplots(
                figsize=(12,6)
            )

            labels = (
                data['BattingTeam_chase']
                + " ("
                + data['total_run_chase']
                .astype(str)
                + ")"
            )

            ax.bar(
                labels,
                data['total_run_chase']
            )

            plt.xticks(rotation=90)

            plt.ylabel("Runs")

            plt.title(
                "Highest Successful Chases"
            )

            st.pyplot(fig)
    # =================================================
    # BIGGEST WIN MARGINS
    # =================================================

    elif insight_option == "Biggest Win Margins":

        data = biggest_win_margins(
            matches
        )

        st.subheader(
            "Biggest Wins by Runs"
        )

        st.markdown("---")

        tab1, tab2 = st.tabs([
            "📊 Stats Table",
            "📈 Visualization"
        ])

        with tab1:

            st.write(data)

        with tab2:

            fig, ax = plt.subplots(
                figsize=(12,6)
            )

            labels = (
                data['WinningTeam']
                + " ("
                + data['Margin']
                .astype(str)
                + ")"
            )

            ax.bar(
                labels,
                data['Margin']
            )

            plt.xticks(rotation=90)

            plt.ylabel("Runs")

            plt.title(
                "Biggest Win Margins"
            )

            st.pyplot(fig)

    # =================================================
    # LOWEST DEFENDED TOTALS
    # =================================================

    elif insight_option == "Lowest Defended Totals":

        data = lowest_defended_totals(
            matches,
            deliveries
        )

        st.subheader(
            "Lowest Successfully Defended Totals"
        )

        st.markdown("---")

        tab1, tab2 = st.tabs([
            "📊 Stats Table",
            "📈 Visualization"
        ])

        with tab1:

            st.write(data)

        with tab2:

            fig, ax = plt.subplots(
                figsize=(12,6)
            )

            labels = (
                data['BattingTeam_defend']
                + " ("
                + data['total_run_defend']
                .astype(str)
                + ")"
            )

            ax.bar(
                labels,
                data['total_run_defend']
            )

            plt.xticks(rotation=90)

            plt.ylabel("Runs")

            plt.title(
                "Lowest Defended Totals"
            )

            st.pyplot(fig)

    # =================================================
    # CLOSEST MATCHES
    # =================================================

    elif insight_option == "Closest Matches":

        data = closest_matches(
            matches
        )

        st.subheader(
            "Closest IPL Matches"
        )

        st.markdown("---")

        tab1, tab2 = st.tabs([
            "📊 Stats Table",
            "📈 Visualization"
        ])

        with tab1:

            st.write(data)

        with tab2:

            fig, ax = plt.subplots(
                figsize=(12,6)
            )

            labels = (
                data['WinningTeam']
                + " ("
                + data['Margin']
                .astype(str)
                + ")"
            )

            ax.bar(
                labels,
                data['Margin']
            )

            plt.xticks(rotation=90)

            plt.ylabel("Winning Margin")

            plt.title(
                "Closest Matches"
            )

            st.pyplot(fig)




# =====================================================
# BOWLER PROFILE
# =====================================================

elif section == "Bowler Profile":

    st.header("🎯 Bowler Profile")

    st.markdown("---")

    # Bowler selection
    bowler_name = st.selectbox(
        "Select Bowler",
        sorted(
            deliveries['bowler']
            .dropna()
            .unique()
        )
    )

    # Get profile
    profile = bowler_profile(
        deliveries,
        bowler_name
    )

    # ================= FIRST ROW ================= #

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Matches",
        profile['Matches']
    )

    col2.metric(
        "Wickets",
        profile['Wickets']
    )

    col3.metric(
        "Overs",
        profile['Overs']
    )

    # ================= SECOND ROW ================= #

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Economy",
        profile['Economy']
    )

    col5.metric(
        "Dot Balls",
        profile['Dot Balls']
    )

    col6.metric(
        "Best Spell",
        profile['Best Spell']
    )


# =====================================================
# HEAD TO HEAD
# =====================================================

elif section == "Head-to-Head":

    st.header("⚔️ Head-to-Head Team Comparison")

    st.markdown("---")

    # Team selection
    teams = sorted(
        matches['WinningTeam']
        .dropna()
        .unique()
    )

    team1 = st.selectbox(
        "Select Team 1",
        teams
    )

    team2 = st.selectbox(
        "Select Team 2",
        teams
    )

    # Prevent same team comparison
    if team1 == team2:

        st.warning(
            "Please select two different teams."
        )

    else:

        # Get results
        result = head_to_head(
            matches,
            team1,
            team2
        )

        # ================= KPIs ================= #

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Matches",
            result['Total Matches']
        )

        col2.metric(
            f"{team1} Wins",
            result[f"{team1} Wins"]
        )

        col3.metric(
            f"{team2} Wins",
            result[f"{team2} Wins"]
        )

        # ================= WIN PERCENTAGES ================= #

        st.subheader("Win Percentage")

        col4, col5 = st.columns(2)

        col4.metric(
            f"{team1} Win %",
            result[f"{team1} Win %"]
        )

        col5.metric(
            f"{team2} Win %",
            result[f"{team2} Win %"]
        )

# =====================================================
# POWERPLAY & DEATH OVERS ANALYSIS
# =====================================================

elif section == "Powerplay & Death Overs":

    st.header("🔥 Powerplay & Death Overs Analysis")

    st.markdown("---")

    analysis_type = st.selectbox(

        "Choose Analysis",

        [
            "Best Powerplay Batters",

            "Best Death Over Batters",

            "Best Death Over Strike Rate"
        ]
    )

    # =============================================
    # POWERPLAY BATTERS
    # =============================================

    if analysis_type == "Best Powerplay Batters":

        data = best_powerplay_batters(
            deliveries
        )

        st.subheader(
            "Top Powerplay Run Scorers"
        )

        st.markdown("---")

        tab1, tab2 = st.tabs([
            "📊 Stats Table",
            "📈 Visualization"
        ])

        # ============================================
        # TAB 1
        # ============================================

        with tab1:

            st.write(data)

        # ============================================
        # TAB 2
        # ============================================

        with tab2:

            fig, ax = plt.subplots(
                figsize=(12,6)
            )

            data.plot(
                kind='bar',
                ax=ax
            )

            plt.xticks(rotation=45)

            plt.ylabel("Runs")

            plt.title(
                "Best Powerplay Batters"
            )

            st.pyplot(fig)

    # =============================================
    # DEATH OVER BATTERS
    # =============================================

    elif analysis_type == "Best Death Over Batters":

        data = best_death_over_batters(
            deliveries
        )

        st.subheader(
            "Top Death Over Run Scorers"
        )

        st.write(data)

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        data.plot(
            kind='bar',
            ax=ax
        )

        plt.xticks(rotation=45)

        plt.ylabel("Runs")

        plt.title(
            "Best Death Over Batters"
        )

        st.pyplot(fig)

    # =============================================
    # DEATH OVER STRIKE RATE
    # =============================================

    elif analysis_type == "Best Death Over Strike Rate":

        data = death_over_strike_rate(
            deliveries
        )

        st.subheader(
            "Best Death Over Strike Rates"
        )

        st.write(data)

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        data.plot(
            kind='bar',
            ax=ax
        )

        plt.xticks(rotation=45)

        plt.ylabel("Strike Rate")

        plt.title(
            "Death Over Strike Rates"
        )

        st.pyplot(fig)

# =====================================================
# BOWLING PHASE ANALYTICS
# =====================================================

elif section == "Bowling Phase Analytics":

    st.header("🎯 Bowling Phase Analytics")

    st.markdown("---")

    analysis_type = st.selectbox(

        "Choose Analysis",

        [
            "Best Powerplay Bowlers",

            "Most Powerplay Wickets",

            "Best Death Bowlers",

            "Most Death Over Wickets"
        ]
    )

    # =============================================
    # POWERPLAY ECONOMY
    # =============================================

    if analysis_type == "Best Powerplay Bowlers":

        data = best_powerplay_bowlers(
            deliveries
        )

        st.subheader(
            "Best Powerplay Economy"
        )

        st.write(data)

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        data.plot(
            kind='bar',
            ax=ax
        )

        plt.xticks(rotation=45)

        plt.ylabel("Economy")

        plt.title(
            "Best Powerplay Bowlers"
        )

        st.pyplot(fig)

    # =============================================
    # POWERPLAY WICKETS
    # =============================================

    elif analysis_type == "Most Powerplay Wickets":

        data = most_powerplay_wickets(
            deliveries
        )

        st.subheader(
            "Most Powerplay Wickets"
        )

        st.write(data)

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        data.plot(
            kind='bar',
            ax=ax
        )

        plt.xticks(rotation=45)

        plt.ylabel("Wickets")

        plt.title(
            "Most Powerplay Wickets"
        )

        st.pyplot(fig)

    # =============================================
    # DEATH OVER ECONOMY
    # =============================================

    elif analysis_type == "Best Death Bowlers":

        data = best_death_bowlers(
            deliveries
        )

        st.subheader(
            "Best Death Over Economy"
        )

        st.write(data)

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        data.plot(
            kind='bar',
            ax=ax
        )

        plt.xticks(rotation=45)

        plt.ylabel("Economy")

        plt.title(
            "Best Death Bowlers"
        )

        st.pyplot(fig)

    # =============================================
    # DEATH OVER WICKETS
    # =============================================

    elif analysis_type == "Most Death Over Wickets":

        data = most_death_over_wickets(
            deliveries
        )

        st.subheader(
            "Most Death Over Wickets"
        )

        st.write(data)

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        data.plot(
            kind='bar',
            ax=ax
        )

        plt.xticks(rotation=45)

        plt.ylabel("Wickets")

        plt.title(
            "Most Death Over Wickets"
        )

        st.pyplot(fig)
# =====================================================
# WIN PREDICTOR
# =====================================================

elif section == "Win Predictor":

    st.header("🤖 IPL Win Predictor")
    st.markdown("---")

    # =============================================
    # TEAM SELECTION
    # =============================================

    teams = sorted(
        matches['WinningTeam']
        .dropna()
        .unique()
    )

    batting_team = st.selectbox(
        "Batting Team",
        teams
    )

    bowling_team = st.selectbox(
        "Bowling Team",
        teams
    )

    # Prevent same team selection
    if batting_team == bowling_team:

        st.warning(
            "Please select different teams."
        )

    else:

        # =========================================
        # MATCH INPUTS
        # =========================================

        target = st.number_input(
            "Target",
            min_value=1,
            value=180
        )

        current_score = st.number_input(
            "Current Score",
            min_value=0,
            value=100
        )

        overs_completed = st.number_input(
            "Overs Completed",
            min_value=0.0,
            max_value=20.0,
            value=10.0
        )

        wickets_left = st.number_input(
            "Wickets Left",
            min_value=0,
            max_value=10,
            value=7
        )

        # =========================================
        # PREDICTION BUTTON
        # =========================================

        if st.button("Predict Win Probability"):

            # -------------------------------------
            # BALLS LEFT
            # -------------------------------------

            balls_left = int(
                120 - (overs_completed * 6)
            )

            # -------------------------------------
            # RUNS LEFT
            # -------------------------------------

            runs_left = (
                target - current_score
            )

            # -------------------------------------
            # CURRENT RR
            # -------------------------------------

            if overs_completed > 0:

                current_rr = (

                    current_score

                    / overs_completed
                )

            else:

                current_rr = 0

            # -------------------------------------
            # REQUIRED RR
            # -------------------------------------

            if balls_left > 0:

                required_rr = (

                    runs_left * 6

                    / balls_left
                )

            else:

                required_rr = 0

            # =====================================
            # CREATE INPUT DATAFRAME
            # =====================================

            input_df = pd.DataFrame({

                'BattingTeam': [
                    batting_team
                ],

                'target': [
                    target
                ],

                'current_score': [
                    current_score
                ],

                'runs_left': [
                    runs_left
                ],

                'balls_left': [
                    balls_left
                ],

                'wickets_left': [
                    wickets_left
                ],

                'current_rr': [
                    current_rr
                ],

                'required_rr': [
                    required_rr
                ]
            })

            # =====================================
            # PREDICTION
            # =====================================

            result = model.predict_proba(
                input_df
            )

            win_probability = round(
                result[0][1] * 100,
                2
            )

            lose_probability = round(
                result[0][0] * 100,
                2
            )

            # =====================================
            # DISPLAY RESULTS
            # =====================================

            st.subheader("Prediction")

            col1, col2 = st.columns(2)

            col1.metric(
                f"{batting_team} Win %",
                win_probability
            )

            col2.metric(
                f"{bowling_team} Win %",
                lose_probability
            )

            # =====================================
            # PROGRESS BARS
            # =====================================

            st.progress(
                int(win_probability)
            )

            st.success(
                f"{batting_team} has "
                f"{win_probability}% "
                f"chance of winning."
            )

st.markdown("---")

st.caption(
    "Built with Python, Pandas, "
    "Machine Learning & Streamlit"
)