import pandas as pd


def build_live_prediction_input(snapshot, batting_team, target=None):
    """Create the existing win-predictor feature frame from a live score snapshot."""
    target = target or snapshot.target or max(snapshot.score + 1, 1)
    runs_left = target - snapshot.score
    balls_left = snapshot.balls_left

    if snapshot.overs > 0:
        current_rr = snapshot.score / snapshot.overs
    else:
        current_rr = 0

    if balls_left > 0:
        required_rr = runs_left * 6 / balls_left
    else:
        required_rr = 0

    return pd.DataFrame(
        {
            "BattingTeam": [batting_team],
            "target": [target],
            "current_score": [snapshot.score],
            "runs_left": [runs_left],
            "balls_left": [balls_left],
            "wickets_left": [snapshot.wickets_left],
            "current_rr": [current_rr],
            "required_rr": [required_rr],
        }
    )


def predict_live_win_probability(model, snapshot, batting_team, target=None):
    """Predict live win probability using the persisted IPL model pipeline."""
    input_df = build_live_prediction_input(
        snapshot,
        batting_team=batting_team,
        target=target,
    )
    result = model.predict_proba(input_df)

    return {
        "win_probability": round(result[0][1] * 100, 2),
        "lose_probability": round(result[0][0] * 100, 2),
        "input": input_df,
    }


def projected_score(snapshot):
    """Project final score using current run rate."""
    if snapshot.overs <= 0:
        return snapshot.score

    return round(snapshot.current_run_rate * 20)


def pressure_index(snapshot):
    """Estimate live pressure from required rate, current rate, wickets, and balls left."""
    rate_gap = max(snapshot.required_run_rate - snapshot.current_run_rate, 0)
    wicket_pressure = max(10 - snapshot.wickets_left, 0) * 3
    ball_pressure = max(120 - snapshot.balls_left, 0) / 120 * 20
    pressure = rate_gap * 7 + wicket_pressure + ball_pressure

    return round(min(pressure, 100), 2)


def run_rate_comparison(snapshot):
    return pd.DataFrame(
        {
            "Run Rate Type": [
                "Current RR",
                "Required RR",
            ],
            "Rate": [
                snapshot.current_run_rate,
                snapshot.required_run_rate,
            ],
        }
    )


def probability_progression(snapshot, current_probability):
    """Build a compact projected probability path for visualization."""
    overs = [max(snapshot.overs - 2, 0), snapshot.overs, min(snapshot.overs + 2, 20)]
    probabilities = [
        max(current_probability - pressure_index(snapshot) * 0.15, 0),
        current_probability,
        min(current_probability + max(snapshot.current_run_rate - snapshot.required_run_rate, 0) * 2, 100),
    ]

    return pd.DataFrame(
        {
            "Overs": overs,
            "Win Probability": [round(value, 2) for value in probabilities],
        }
    )


def over_momentum_projection(snapshot):
    """Create a lightweight live momentum projection from current scoring state."""
    current_over = int(snapshot.overs)
    start_over = max(current_over - 4, 0)
    overs = list(range(start_over, min(current_over + 2, 20) + 1))
    base_rate = snapshot.current_run_rate or 0

    return pd.DataFrame(
        {
            "Over": overs,
            "Momentum": [
                round(base_rate + (over - current_over) * 0.35 - snapshot.wickets * 0.15, 2)
                for over in overs
            ],
        }
    )
