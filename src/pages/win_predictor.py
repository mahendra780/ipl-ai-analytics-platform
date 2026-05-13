import pandas as pd
import streamlit as st


def show_win_predictor(matches, model):
    st.header("IPL Win Predictor")
    st.markdown("---")

    teams = sorted(matches["WinningTeam"].dropna().unique())

    batting_team = st.selectbox("Batting Team", teams)
    bowling_team = st.selectbox("Bowling Team", teams)

    if batting_team == bowling_team:
        st.warning("Please select different teams.")
        return

    target = st.number_input(
        "Target",
        min_value=1,
        value=180,
    )
    current_score = st.number_input(
        "Current Score",
        min_value=0,
        value=100,
    )
    overs_completed = st.number_input(
        "Overs Completed",
        min_value=0.0,
        max_value=20.0,
        value=10.0,
    )
    wickets_left = st.number_input(
        "Wickets Left",
        min_value=0,
        max_value=10,
        value=7,
    )

    if st.button("Predict Win Probability"):
        balls_left = int(120 - (overs_completed * 6))
        runs_left = target - current_score

        if overs_completed > 0:
            current_rr = current_score / overs_completed
        else:
            current_rr = 0

        if balls_left > 0:
            required_rr = runs_left * 6 / balls_left
        else:
            required_rr = 0

        input_df = pd.DataFrame(
            {
                "BattingTeam": [batting_team],
                "target": [target],
                "current_score": [current_score],
                "runs_left": [runs_left],
                "balls_left": [balls_left],
                "wickets_left": [wickets_left],
                "current_rr": [current_rr],
                "required_rr": [required_rr],
            }
        )

        result = model.predict_proba(input_df)

        win_probability = round(result[0][1] * 100, 2)
        lose_probability = round(result[0][0] * 100, 2)

        st.subheader("Prediction")

        col1, col2 = st.columns(2)
        col1.metric(f"{batting_team} Win %", win_probability)
        col2.metric(f"{bowling_team} Win %", lose_probability)

        st.progress(int(win_probability))
        st.success(
            f"{batting_team} has {win_probability}% chance of winning."
        )
