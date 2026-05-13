import pandas as pd
import streamlit as st

from src.api.live_match import (
    LiveMatchAPIError,
    fetch_live_matches,
    get_live_score_snapshot,
)
from src.realtime.live_analytics import (
    over_momentum_projection,
    predict_live_win_probability,
    pressure_index,
    projected_score,
    run_rate_comparison,
)
from src.ui.charts import create_bar_chart, create_gauge_chart, create_line_chart


REFRESH_INTERVAL_OPTIONS = {
    "15 seconds": 15,
    "30 seconds": 30,
    "60 seconds": 60,
}


@st.cache_data(ttl=30, show_spinner=False)
def _fetch_live_matches(match_type):
    return fetch_live_matches(match_type)


@st.cache_data(ttl=20, show_spinner=False)
def _fetch_live_score(match_id):
    snapshot = get_live_score_snapshot(match_id)
    return snapshot.to_dict(), snapshot


def show_live_match_center(matches, model):
    st.header("Live Match Center")
    st.markdown("---")

    _render_live_controls()

    match_type = st.selectbox(
        "Match Type",
        [
            "league",
            "international",
            "domestic",
            "women",
        ],
    )

    try:
        live_matches = _fetch_live_matches(match_type)
    except LiveMatchAPIError as exc:
        st.error(str(exc))
        _show_manual_live_mode(matches, model)
        return

    if not live_matches:
        st.warning("No live matches are currently available from the live data source.")
        _show_manual_live_mode(matches, model)
        return

    selected_match = st.selectbox(
        "Select Live Match",
        live_matches,
        format_func=_format_live_match,
    )
    match_id = selected_match.get("id")

    if not match_id:
        st.error("Selected live match does not contain a valid match id.")
        return

    try:
        _, snapshot = _fetch_live_score(match_id)
    except LiveMatchAPIError as exc:
        st.error(str(exc))
        _show_manual_live_mode(matches, model)
        return

    _render_live_snapshot(snapshot, matches, model)


def _render_live_controls():
    col1, col2 = st.columns([1, 2])
    auto_refresh = col1.toggle("Auto Refresh", value=False)
    interval_label = col2.selectbox(
        "Refresh Interval",
        list(REFRESH_INTERVAL_OPTIONS.keys()),
        index=1,
    )

    if auto_refresh:
        seconds = REFRESH_INTERVAL_OPTIONS[interval_label]
        st.markdown(
            f"<meta http-equiv='refresh' content='{seconds}'>",
            unsafe_allow_html=True,
        )


def _render_live_snapshot(snapshot, matches, model):
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:12px;">
            <span style="background:#ef4444;color:white;padding:4px 10px;border-radius:999px;font-weight:700;">LIVE</span>
            <span>{snapshot.title}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Last refreshed: {snapshot.fetched_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    st.info(snapshot.status)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{snapshot.score}/{snapshot.wickets}")
    col2.metric("Overs", snapshot.overs)
    col3.metric("Current RR", snapshot.current_run_rate)
    col4.metric("Required RR", snapshot.required_run_rate)

    teams = sorted(matches["WinningTeam"].dropna().astype(str).unique())
    batting_team = _team_selectbox(
        "Map Batting Team for ML Model",
        teams,
        snapshot.batting_team,
    )
    target = st.number_input(
        "Target",
        min_value=1,
        value=int(snapshot.target or max(snapshot.score + 1, 1)),
    )

    prediction = _safe_predict(model, snapshot, batting_team, target)

    tab1, tab2, tab3 = st.tabs(
        [
            "Win Probability",
            "Live Analytics",
            "Score Details",
        ]
    )

    with tab1:
        _show_probability_tab(snapshot, prediction)

    with tab2:
        _show_live_analytics_tab(snapshot)

    with tab3:
        _show_score_details(snapshot)


def _show_probability_tab(snapshot, prediction):
    if prediction is None:
        st.warning("Win probability is unavailable for the selected model team mapping.")
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        fig = create_gauge_chart(
            prediction["win_probability"],
            title="Live Win Probability",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric("Projected Score", projected_score(snapshot))
        st.metric("Pressure Index", pressure_index(snapshot))
        st.metric("Chase Probability", f"{prediction['win_probability']}%")

    progression = _update_probability_history(
        snapshot,
        prediction["win_probability"],
    )
    fig = create_line_chart(
        progression,
        x="Overs",
        y="Win Probability",
        title="Probability Progression",
        x_axis_title="Overs",
        y_axis_title="Win Probability %",
    )
    st.plotly_chart(fig, use_container_width=True)


def _show_live_analytics_tab(snapshot):
    rate_data = run_rate_comparison(snapshot)
    fig = create_bar_chart(
        rate_data,
        x="Run Rate Type",
        y="Rate",
        title="Current vs Required Run Rate",
        x_axis_title="Run Rate",
        y_axis_title="Rate",
    )
    st.plotly_chart(fig, use_container_width=True)

    momentum = over_momentum_projection(snapshot)
    fig = create_line_chart(
        momentum,
        x="Over",
        y="Momentum",
        title="Over-by-Over Momentum Projection",
        x_axis_title="Over",
        y_axis_title="Momentum",
    )
    st.plotly_chart(fig, use_container_width=True)


def _show_score_details(snapshot):
    col1, col2, col3 = st.columns(3)
    col1.metric("Batting Team", snapshot.batting_team or "Unavailable")
    col2.metric("Bowling Team", snapshot.bowling_team or "Unavailable")
    col3.metric("Wickets Left", snapshot.wickets_left)

    col4, col5, col6, col7 = st.columns(4)
    col4.metric("Striker", snapshot.striker or "Unavailable")
    col5.metric("Non-striker", snapshot.non_striker or "Unavailable")
    col6.metric("Bowler", snapshot.bowler or "Unavailable")
    col7.metric("Partnership", snapshot.partnership or "Unavailable")

    with st.expander("Raw Live Payload"):
        st.json(snapshot.raw)


def _show_manual_live_mode(matches, model):
    st.subheader("Manual Live Simulator")
    st.caption("Use this when the unofficial live source is unavailable or rate-limited.")

    teams = sorted(matches["WinningTeam"].dropna().astype(str).unique())
    batting_team = st.selectbox("Batting Team", teams)

    score = st.number_input("Current Score", min_value=0, value=100)
    wickets = st.number_input("Wickets Lost", min_value=0, max_value=10, value=3)
    overs = st.number_input("Overs", min_value=0.0, max_value=20.0, value=10.0)
    current_rr = round(score / overs, 2) if overs else 0.0
    target = st.number_input("Target", min_value=1, value=180)
    balls_left = max(120 - int(overs * 6), 0)
    required_rr = round(((target - score) * 6) / balls_left, 2) if balls_left else 0.0

    from src.api.live_match import LiveScoreSnapshot
    from datetime import datetime, timezone

    snapshot = LiveScoreSnapshot(
        match_id="manual",
        title="Manual Live Simulator",
        status="Manual mode",
        batting_team=batting_team,
        bowling_team=None,
        score=score,
        wickets=wickets,
        overs=overs,
        current_run_rate=current_rr,
        required_run_rate=required_rr,
        target=target,
        striker=None,
        non_striker=None,
        bowler=None,
        partnership=None,
        fetched_at=datetime.now(timezone.utc),
        raw={},
    )

    prediction = _safe_predict(model, snapshot, batting_team, target)
    _show_probability_tab(snapshot, prediction)
    _show_live_analytics_tab(snapshot)


def _safe_predict(model, snapshot, batting_team, target):
    try:
        return predict_live_win_probability(
            model,
            snapshot,
            batting_team=batting_team,
            target=target,
        )
    except Exception as exc:
        st.warning(f"Prediction unavailable: {exc}")
        return None


def _update_probability_history(snapshot, win_probability):
    key = f"live_probability_history_{snapshot.match_id}"

    if key not in st.session_state:
        st.session_state[key] = []

    point = {
        "Overs": snapshot.overs,
        "Win Probability": win_probability,
        "Fetched At": snapshot.fetched_at.isoformat(),
    }

    if not st.session_state[key] or st.session_state[key][-1] != point:
        st.session_state[key].append(point)

    st.session_state[key] = st.session_state[key][-30:]

    return pd.DataFrame(st.session_state[key])


def _team_selectbox(label, teams, live_team):
    if live_team in teams:
        index = teams.index(live_team)
    else:
        index = 0

    return st.selectbox(
        label,
        teams,
        index=index,
    )


def _format_live_match(match):
    title = match.get("title", "Untitled Match")
    overview = match.get("overview", "Live")
    return f"{title} - {overview}"
