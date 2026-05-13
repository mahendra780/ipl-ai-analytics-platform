import numpy as np
import pandas as pd


POWERPLAY_MAX_OVER = 6
DEATH_MIN_OVER = 16


def _safe_percentage(numerator, denominator):
    denominator = denominator.replace(0, np.nan)
    return ((numerator / denominator) * 100).fillna(0).round(2)


def _phase_label(overs):
    return np.select(
        [
            overs <= POWERPLAY_MAX_OVER,
            overs >= DEATH_MIN_OVER,
        ],
        [
            "Powerplay",
            "Death Overs",
        ],
        default="Middle Overs",
    )


def _min_max_score(series, higher_is_better=True):
    series = pd.to_numeric(series, errors="coerce").fillna(0)

    if series.max() == series.min():
        return pd.Series(50, index=series.index)

    score = (series - series.min()) / (series.max() - series.min()) * 100

    if not higher_is_better:
        score = 100 - score

    return score


def boundary_percentage(deliveries, min_balls=100):
    """Return percentage of balls faced that result in a four or six."""
    stats = deliveries.groupby("batter", observed=True).agg(
        Balls=("ballnumber", "count"),
        Boundaries=("batsman_run", lambda runs: runs.isin([4, 6]).sum()),
    )
    stats["Boundary %"] = _safe_percentage(stats["Boundaries"], stats["Balls"])
    return stats[stats["Balls"] >= min_balls].sort_values("Boundary %", ascending=False)


def batting_dot_ball_percentage(deliveries, min_balls=100):
    """Return percentage of balls faced where the batter scores no bat runs."""
    stats = deliveries.groupby("batter", observed=True).agg(
        Balls=("ballnumber", "count"),
        DotBalls=("batsman_run", lambda runs: (runs == 0).sum()),
    )
    stats["Dot Ball %"] = _safe_percentage(stats["DotBalls"], stats["Balls"])
    return stats[stats["Balls"] >= min_balls].sort_values("Dot Ball %")


def batting_consistency_score(deliveries, min_innings=10):
    """Score batting consistency using innings-level run variation."""
    innings_runs = (
        deliveries.groupby(["batter", "ID"], observed=True)["batsman_run"]
        .sum()
        .reset_index()
    )

    stats = innings_runs.groupby("batter", observed=True).agg(
        Innings=("ID", "count"),
        AverageRuns=("batsman_run", "mean"),
        RunsStdDev=("batsman_run", "std"),
    )
    stats["RunsStdDev"] = stats["RunsStdDev"].fillna(0)
    coefficient_variation = stats["RunsStdDev"] / stats["AverageRuns"].replace(0, np.nan)
    stats["Consistency Score"] = (100 / (1 + coefficient_variation)).fillna(0).round(2)
    stats["AverageRuns"] = stats["AverageRuns"].round(2)
    stats["RunsStdDev"] = stats["RunsStdDev"].round(2)
    return stats[stats["Innings"] >= min_innings].sort_values(
        "Consistency Score",
        ascending=False,
    )


def phase_wise_strike_rate(deliveries, min_balls=30):
    """Return strike rate by batter and innings phase."""
    phase_data = deliveries.copy()
    phase_data["Phase"] = _phase_label(phase_data["overs"])

    stats = phase_data.groupby(["batter", "Phase"], observed=True).agg(
        Runs=("batsman_run", "sum"),
        Balls=("ballnumber", "count"),
    )
    stats["Strike Rate"] = _safe_percentage(stats["Runs"], stats["Balls"])
    return (
        stats[stats["Balls"] >= min_balls]
        .reset_index()
        .sort_values("Strike Rate", ascending=False)
    )


def boundary_dependency(deliveries, min_runs=300):
    """Return percentage of batter runs that come from fours and sixes."""
    stats = deliveries.groupby("batter", observed=True).agg(
        Runs=("batsman_run", "sum"),
        BoundaryRuns=("batsman_run", lambda runs: runs[runs.isin([4, 6])].sum()),
    )
    stats["Boundary Dependency %"] = _safe_percentage(stats["BoundaryRuns"], stats["Runs"])
    return stats[stats["Runs"] >= min_runs].sort_values(
        "Boundary Dependency %",
        ascending=False,
    )


def average_runs_per_innings(deliveries, min_innings=10):
    """Return average runs per innings for each batter."""
    innings_runs = (
        deliveries.groupby(["batter", "ID"], observed=True)["batsman_run"]
        .sum()
        .reset_index()
    )
    stats = innings_runs.groupby("batter", observed=True).agg(
        Innings=("ID", "count"),
        Runs=("batsman_run", "sum"),
        AverageRunsPerInnings=("batsman_run", "mean"),
    )
    stats.rename(
        columns={
            "AverageRunsPerInnings": "Average Runs/Innings",
        },
        inplace=True,
    )
    stats["Average Runs/Innings"] = stats["Average Runs/Innings"].round(2)
    return stats[stats["Innings"] >= min_innings].sort_values(
        "Average Runs/Innings",
        ascending=False,
    )


def advanced_batting_summary(deliveries):
    """Return a compact batter intelligence table for comparison views."""
    balls = deliveries.groupby("batter", observed=True).agg(
        Runs=("batsman_run", "sum"),
        Balls=("ballnumber", "count"),
        Boundaries=("batsman_run", lambda runs: runs.isin([4, 6]).sum()),
        DotBalls=("batsman_run", lambda runs: (runs == 0).sum()),
        BoundaryRuns=("batsman_run", lambda runs: runs[runs.isin([4, 6])].sum()),
    )
    innings = (
        deliveries.groupby(["batter", "ID"], observed=True)["batsman_run"]
        .sum()
        .groupby("batter", observed=True)
        .agg(Innings="count", AverageRuns="mean")
    )

    summary = balls.join(innings, how="left")
    summary["Strike Rate"] = _safe_percentage(summary["Runs"], summary["Balls"])
    summary["Boundary %"] = _safe_percentage(summary["Boundaries"], summary["Balls"])
    summary["Dot Ball %"] = _safe_percentage(summary["DotBalls"], summary["Balls"])
    summary["Boundary Dependency %"] = _safe_percentage(
        summary["BoundaryRuns"],
        summary["Runs"],
    )
    summary["AverageRuns"] = summary["AverageRuns"].fillna(0).round(2)
    return summary.sort_values("Runs", ascending=False)


def dot_ball_pressure(deliveries, min_balls=100):
    """Return percentage of balls bowled that are dot balls."""
    stats = deliveries.groupby("bowler", observed=True).agg(
        Balls=("ballnumber", "count"),
        DotBalls=("total_run", lambda runs: (runs == 0).sum()),
    )
    stats["Dot Ball Pressure %"] = _safe_percentage(stats["DotBalls"], stats["Balls"])
    return stats[stats["Balls"] >= min_balls].sort_values(
        "Dot Ball Pressure %",
        ascending=False,
    )


def wicket_frequency(deliveries, min_balls=100):
    """Return balls per wicket for each bowler."""
    stats = deliveries.groupby("bowler", observed=True).agg(
        Balls=("ballnumber", "count"),
        Wickets=("isWicketDelivery", "sum"),
    )
    stats["Balls/Wicket"] = (stats["Balls"] / stats["Wickets"].replace(0, np.nan)).round(2)
    return stats[
        (stats["Balls"] >= min_balls)
        & stats["Balls/Wicket"].notna()
    ].sort_values("Balls/Wicket")


def death_over_economy(deliveries, min_balls=60):
    """Return economy rate in death overs."""
    death = deliveries[deliveries["overs"] >= DEATH_MIN_OVER]
    stats = death.groupby("bowler", observed=True).agg(
        Runs=("total_run", "sum"),
        Balls=("ballnumber", "count"),
    )
    stats["Overs"] = stats["Balls"] / 6
    stats["Death Economy"] = (stats["Runs"] / stats["Overs"].replace(0, np.nan)).round(2)
    return stats[stats["Balls"] >= min_balls].sort_values("Death Economy")


def bowling_impact_score(deliveries, min_balls=100):
    """Combine wickets, economy control, and dot-ball pressure into one score."""
    stats = deliveries.groupby("bowler", observed=True).agg(
        Runs=("total_run", "sum"),
        Balls=("ballnumber", "count"),
        Wickets=("isWicketDelivery", "sum"),
        DotBalls=("total_run", lambda runs: (runs == 0).sum()),
    )
    stats["Overs"] = stats["Balls"] / 6
    stats["Economy"] = (stats["Runs"] / stats["Overs"].replace(0, np.nan)).fillna(0)
    stats["Dot Ball Pressure %"] = _safe_percentage(stats["DotBalls"], stats["Balls"])

    eligible = stats[stats["Balls"] >= min_balls].copy()
    eligible["Bowling Impact Score"] = (
        _min_max_score(eligible["Wickets"], higher_is_better=True) * 0.40
        + _min_max_score(eligible["Economy"], higher_is_better=False) * 0.30
        + _min_max_score(eligible["Dot Ball Pressure %"], higher_is_better=True) * 0.30
    ).round(2)

    return eligible.sort_values("Bowling Impact Score", ascending=False)


def advanced_bowling_summary(deliveries):
    """Return a compact bowler intelligence table for comparison views."""
    stats = deliveries.groupby("bowler", observed=True).agg(
        Runs=("total_run", "sum"),
        Balls=("ballnumber", "count"),
        Wickets=("isWicketDelivery", "sum"),
        DotBalls=("total_run", lambda runs: (runs == 0).sum()),
    )
    stats["Overs"] = (stats["Balls"] / 6).round(1)
    stats["Economy"] = (stats["Runs"] / stats["Overs"].replace(0, np.nan)).fillna(0).round(2)
    stats["Dot Ball Pressure %"] = _safe_percentage(stats["DotBalls"], stats["Balls"])
    stats["Balls/Wicket"] = (stats["Balls"] / stats["Wickets"].replace(0, np.nan)).round(2)
    return stats.sort_values("Wickets", ascending=False)


def team_run_rate_progression(deliveries, match_id):
    """Return cumulative run-rate progression by team for one match."""
    match_data = deliveries[deliveries["ID"] == match_id]
    over_scores = (
        match_data.groupby(["innings", "BattingTeam", "overs"], observed=True)["total_run"]
        .sum()
        .reset_index()
        .sort_values(["innings", "overs"])
    )
    over_scores["Cumulative Runs"] = over_scores.groupby(
        ["innings", "BattingTeam"],
        observed=True,
    )["total_run"].cumsum()
    over_scores["Overs Completed"] = over_scores.groupby(
        ["innings", "BattingTeam"],
        observed=True,
    ).cumcount() + 1
    over_scores["Run Rate"] = (
        over_scores["Cumulative Runs"] / over_scores["Overs Completed"]
    ).round(2)
    return over_scores


def over_by_over_momentum(deliveries, match_id):
    """Return over-by-over run and wicket momentum for one match."""
    match_data = deliveries[deliveries["ID"] == match_id]
    momentum = (
        match_data.groupby(["innings", "BattingTeam", "overs"], observed=True)
        .agg(
            Runs=("total_run", "sum"),
            Wickets=("isWicketDelivery", "sum"),
            Boundaries=("batsman_run", lambda runs: runs.isin([4, 6]).sum()),
        )
        .reset_index()
        .sort_values(["innings", "overs"])
    )
    momentum["Momentum Score"] = (
        momentum["Runs"] + momentum["Boundaries"] * 2 - momentum["Wickets"] * 5
    )
    return momentum


def chase_difficulty_index(matches, deliveries):
    """Estimate chase difficulty using target, required scoring rate, and wickets lost."""
    innings_scores = (
        deliveries.groupby(["ID", "innings", "BattingTeam"], observed=True)["total_run"]
        .sum()
        .reset_index()
    )
    first_innings = innings_scores[innings_scores["innings"] == 1].rename(
        columns={
            "BattingTeam": "DefendingTeam",
            "total_run": "TargetScore",
        }
    )
    second_innings = innings_scores[innings_scores["innings"] == 2].rename(
        columns={
            "BattingTeam": "ChasingTeam",
            "total_run": "ChaseScore",
        }
    )

    wickets_lost = (
        deliveries[deliveries["innings"] == 2]
        .groupby("ID", observed=True)["isWicketDelivery"]
        .sum()
        .rename("WicketsLost")
    )

    chase = second_innings.merge(
        first_innings[["ID", "DefendingTeam", "TargetScore"]],
        on="ID",
        how="inner",
    ).merge(
        wickets_lost,
        on="ID",
        how="left",
    )
    chase = chase.merge(
        matches[["ID", "WinningTeam", "Season"]],
        on="ID",
        how="left",
    )

    chase["Target"] = chase["TargetScore"] + 1
    chase["Required Run Rate"] = (chase["Target"] / 20).round(2)
    chase["Result"] = np.where(
        chase["ChasingTeam"].astype(str) == chase["WinningTeam"].astype(str),
        "Won",
        "Lost",
    )
    chase["Chase Difficulty Index"] = (
        chase["Required Run Rate"] * 8
        + chase["WicketsLost"].fillna(0) * 3
        + np.where(chase["Result"] == "Won", 8, 0)
    ).round(2)

    return chase[
        [
            "ID",
            "Season",
            "ChasingTeam",
            "DefendingTeam",
            "Target",
            "ChaseScore",
            "WicketsLost",
            "Required Run Rate",
            "Result",
            "Chase Difficulty Index",
        ]
    ].sort_values("Chase Difficulty Index", ascending=False)
