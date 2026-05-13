import re
from dataclasses import dataclass
from difflib import get_close_matches

import pandas as pd

from src.advanced_analytics import (
    batting_consistency_score,
    boundary_dependency,
    boundary_percentage,
    death_over_economy,
    dot_ball_pressure,
    phase_wise_strike_rate,
    wicket_frequency,
)
from src.recommender.player_similarity import (
    build_player_feature_matrix,
    get_comparison_chart_data,
    get_player_comparison,
    get_player_similarity_scores,
)


@dataclass
class QueryResponse:
    answer: str
    data: pd.DataFrame | pd.Series | None = None
    chart_type: str | None = None
    chart_data: pd.DataFrame | pd.Series | None = None
    x: str | None = None
    y: str | None = None
    color: str | None = None
    title: str | None = None

    def context_for_llm(self):
        if self.data is None:
            return self.answer

        if isinstance(self.data, pd.Series):
            preview = self.data.head(10).to_frame("Value")
        else:
            preview = self.data.head(10)

        return f"{self.answer}\n\nData preview:\n{preview.to_string()}"


def answer_cricket_query(question, matches, deliveries):
    """Interpret natural language cricket questions and return grounded analytics."""
    query = question.lower().strip()
    filtered_deliveries = _filter_deliveries_by_year(deliveries, query)

    if "chase" in query or "chases" in query or "chasing" in query:
        filtered_deliveries = filtered_deliveries[filtered_deliveries["innings"] == 2]

    if "live" in query:
        return QueryResponse(
            answer="For live match intelligence, open the Live Match Center. It supports live score ingestion, win probability, pressure index, projected score, and run-rate comparison.",
        )

    if _is_compare_query(query):
        return _answer_player_comparison(question, filtered_deliveries)

    if "similar" in query or "alternative" in query or "like " in query:
        return _answer_player_similarity(question, filtered_deliveries)

    if "consistent" in query and ("batter" in query or "player" in query):
        data = batting_consistency_score(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_leader_answer("Most consistent IPL batters", data, "Consistency Score"),
            data=data,
            chart_type="bar",
            chart_data=data["Consistency Score"],
            title="Most Consistent IPL Batters",
        )

    if "death" in query and "batter" in query:
        data = _best_death_over_batters(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_series_answer("Top death-over batters", data, "runs"),
            data=data,
            chart_type="bar",
            chart_data=data,
            title="Top Death-Over Batters",
        )

    if "powerplay" in query and "batter" in query:
        data = _best_powerplay_batters(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_series_answer("Best powerplay batters", data, "runs"),
            data=data,
            chart_type="bar",
            chart_data=data,
            title="Best Powerplay Batters",
        )

    if "powerplay" in query and "bowler" in query:
        data = _best_powerplay_bowlers(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_series_answer("Best powerplay bowlers by economy", data, "economy"),
            data=data,
            chart_type="bar",
            chart_data=data,
            title="Best Powerplay Bowlers",
        )

    if "death" in query and "bowler" in query:
        data = _best_death_bowlers(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_series_answer("Best death-over bowlers by economy", data, "economy"),
            data=data,
            chart_type="bar",
            chart_data=data,
            title="Best Death-Over Bowlers",
        )

    if "boundary" in query and "dependency" in query:
        data = boundary_dependency(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_leader_answer("Highest boundary dependency", data, "Boundary Dependency %"),
            data=data,
            chart_type="bar",
            chart_data=data["Boundary Dependency %"],
            title="Boundary Dependency Leaders",
        )

    if "boundary" in query:
        data = boundary_percentage(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_leader_answer("Highest boundary percentage", data, "Boundary %"),
            data=data,
            chart_type="bar",
            chart_data=data["Boundary %"],
            title="Boundary Percentage Leaders",
        )

    if "dot" in query and "bowler" in query:
        data = dot_ball_pressure(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_leader_answer("Best dot-ball pressure bowlers", data, "Dot Ball Pressure %"),
            data=data,
            chart_type="bar",
            chart_data=data["Dot Ball Pressure %"],
            title="Dot Ball Pressure Leaders",
        )

    if "wicket frequency" in query or "balls per wicket" in query:
        data = wicket_frequency(filtered_deliveries).head(10)
        return QueryResponse(
            answer=_leader_answer("Best wicket frequency", data, "Balls/Wicket", lower_is_better=True),
            data=data,
            chart_type="bar",
            chart_data=data["Balls/Wicket"],
            title="Best Wicket Frequency",
        )

    if "strike rate" in query and ("phase" in query or "powerplay" in query or "middle" in query or "death" in query):
        phase = _detect_phase(query)
        data = phase_wise_strike_rate(filtered_deliveries)
        if phase:
            data = data[data["Phase"] == phase]
        data = data.head(10)
        return QueryResponse(
            answer=_leader_answer(f"{phase or 'Phase-wise'} strike-rate leaders", data.set_index("batter"), "Strike Rate"),
            data=data,
            chart_type="bar",
            chart_data=data,
            x="batter",
            y="Strike Rate",
            title=f"{phase or 'Phase-wise'} Strike Rate Leaders",
        )

    data = _top_run_scorers(filtered_deliveries).head(10)
    return QueryResponse(
        answer=_series_answer("Top IPL run scorers", data, "runs"),
        data=data,
        chart_type="bar",
        chart_data=data,
        title="Top IPL Run Scorers",
    )


def _answer_player_comparison(question, deliveries):
    feature_table = build_player_feature_matrix(deliveries)
    players = _extract_players(question, feature_table.index.tolist(), count=2)

    if len(players) < 2:
        return QueryResponse(
            answer="I could not confidently identify two players. Try: Compare V Kohli and RG Sharma.",
        )

    comparison = get_player_comparison(players[0], players[1], feature_table)
    chart_data = get_comparison_chart_data(comparison)
    answer = (
        f"{players[0]} vs {players[1]}: "
        f"{players[0]} has {comparison.loc[players[0], 'Runs']} runs at "
        f"{comparison.loc[players[0], 'Strike Rate']} SR, while {players[1]} has "
        f"{comparison.loc[players[1], 'Runs']} runs at {comparison.loc[players[1], 'Strike Rate']} SR."
    )

    return QueryResponse(
        answer=answer,
        data=comparison,
        chart_type="bar",
        chart_data=chart_data,
        x="Metric",
        y="Value",
        color="Player",
        title=f"{players[0]} vs {players[1]}",
    )


def _answer_player_similarity(question, deliveries):
    feature_table = build_player_feature_matrix(deliveries)
    players = _extract_players(question, feature_table.index.tolist(), count=1)

    if not players:
        return QueryResponse(
            answer="I could not identify the player for similarity analysis. Try: similar players to V Kohli.",
        )

    data = get_player_similarity_scores(players[0], feature_table, top_n=5)
    return QueryResponse(
        answer=_leader_answer(f"Most similar players to {players[0]}", data, "Similarity %"),
        data=data,
        chart_type="bar",
        chart_data=data["Similarity %"],
        title=f"Most Similar Players to {players[0]}",
    )


def _filter_deliveries_by_year(deliveries, query):
    year_match = re.search(r"(?:after|since|from)\s+(20\d{2}|19\d{2})", query)
    before_match = re.search(r"before\s+(20\d{2}|19\d{2})", query)

    if "Season" not in deliveries.columns:
        return deliveries

    seasons = pd.to_numeric(deliveries["Season"].astype(str), errors="coerce")

    if year_match:
        year = int(year_match.group(1))
        return deliveries[seasons >= year]

    if before_match:
        year = int(before_match.group(1))
        return deliveries[seasons < year]

    return deliveries


def _top_run_scorers(deliveries):
    return (
        deliveries.groupby("batter", observed=True)["batsman_run"]
        .sum()
        .sort_values(ascending=False)
    )


def _best_powerplay_batters(deliveries):
    powerplay = deliveries[deliveries["overs"] <= 6]
    return (
        powerplay.groupby("batter", observed=True)["batsman_run"]
        .sum()
        .sort_values(ascending=False)
    )


def _best_death_over_batters(deliveries):
    death = deliveries[deliveries["overs"] >= 16]
    return (
        death.groupby("batter", observed=True)["batsman_run"]
        .sum()
        .sort_values(ascending=False)
    )


def _best_powerplay_bowlers(deliveries):
    powerplay = deliveries[deliveries["overs"] <= 6]
    stats = powerplay.groupby("bowler", observed=True).agg(
        Runs=("total_run", "sum"),
        Balls=("ballnumber", "count"),
    )
    stats["Overs"] = stats["Balls"] / 6
    stats["Economy"] = stats["Runs"] / stats["Overs"].replace(0, float("nan"))
    return stats[stats["Balls"] >= 100]["Economy"].dropna().sort_values()


def _best_death_bowlers(deliveries):
    death = deliveries[deliveries["overs"] >= 16]
    stats = death.groupby("bowler", observed=True).agg(
        Runs=("total_run", "sum"),
        Balls=("ballnumber", "count"),
    )
    stats["Overs"] = stats["Balls"] / 6
    stats["Economy"] = stats["Runs"] / stats["Overs"].replace(0, float("nan"))
    return stats[stats["Balls"] >= 100]["Economy"].dropna().sort_values()


def _extract_players(question, player_names, count):
    lowered_question = question.lower()
    aliases = {
        "kohli": "V Kohli",
        "virat": "V Kohli",
        "rohit": "RG Sharma",
        "sharma": "RG Sharma",
        "dhoni": "MS Dhoni",
        "raina": "SK Raina",
        "de villiers": "AB de Villiers",
        "abd": "AB de Villiers",
        "gayle": "CH Gayle",
        "warner": "DA Warner",
        "rahul": "KL Rahul",
    }
    alias_matches = [
        player
        for alias, player in aliases.items()
        if alias in lowered_question and player in player_names
    ]
    exact_matches = [
        player
        for player in player_names
        if player.lower() in lowered_question
    ]

    initial_matches = []
    for player in alias_matches + exact_matches:
        if player not in initial_matches:
            initial_matches.append(player)

    if len(initial_matches) >= count:
        return initial_matches[:count]

    tokens = re.findall(r"[a-zA-Z][a-zA-Z\s.]{2,}", question)
    candidates = []
    lowered_players = {player.lower(): player for player in player_names}

    for token in tokens:
        matches = get_close_matches(token.lower().strip(), lowered_players.keys(), n=1, cutoff=0.72)
        if matches:
            candidates.append(lowered_players[matches[0]])

    combined = []
    for player in initial_matches + candidates:
        if player not in combined:
            combined.append(player)

    return combined[:count]


def _is_compare_query(query):
    return "compare" in query or " vs " in query or " versus " in query


def _detect_phase(query):
    if "powerplay" in query:
        return "Powerplay"
    if "middle" in query:
        return "Middle Overs"
    if "death" in query:
        return "Death Overs"
    return None


def _series_answer(title, data, unit):
    if data.empty:
        return f"No results found for {title.lower()}."

    top_name = data.index[0]
    top_value = round(float(data.iloc[0]), 2)
    return f"{title}: {top_name} leads with {top_value} {unit}."


def _leader_answer(title, data, column, lower_is_better=False):
    if data.empty:
        return f"No results found for {title.lower()}."

    if isinstance(data, pd.Series):
        top_name = data.index[0]
        top_value = data.iloc[0]
    else:
        top_name = data.index[0]
        top_value = data.iloc[0][column]

    qualifier = "lowest" if lower_is_better else "highest"
    return f"{title}: {top_name} has the {qualifier} mark at {round(float(top_value), 2)}."
