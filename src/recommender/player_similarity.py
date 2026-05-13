import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

from src.advanced_analytics import (
    advanced_batting_summary,
    batting_consistency_score,
    phase_wise_strike_rate,
)


SIMILARITY_FEATURES = [
    "Strike Rate",
    "Average",
    "Boundary %",
    "Dot Ball Control",
    "Consistency Score",
    "Average Runs/Innings",
    "Powerplay SR",
    "Middle Overs SR",
    "Death Overs SR",
]


DISPLAY_COLUMNS = [
    "Runs",
    "Balls",
    "Innings",
    "Strike Rate",
    "Average",
    "Boundary %",
    "Dot Ball %",
    "Consistency Score",
    "Average Runs/Innings",
    "Powerplay SR",
    "Middle Overs SR",
    "Death Overs SR",
]


def build_player_feature_matrix(deliveries, min_balls=300, min_innings=10):
    """Build reusable batter feature vectors for comparison and recommendations."""
    summary = advanced_batting_summary(deliveries)
    consistency = batting_consistency_score(
        deliveries,
        min_innings=min_innings,
    )[["Consistency Score"]]
    phase = phase_wise_strike_rate(deliveries, min_balls=30)

    phase_features = (
        phase.pivot_table(
            index="batter",
            columns="Phase",
            values="Strike Rate",
            aggfunc="mean",
            observed=True,
        )
        .rename(
            columns={
                "Powerplay": "Powerplay SR",
                "Middle Overs": "Middle Overs SR",
                "Death Overs": "Death Overs SR",
            }
        )
    )

    features = summary.join(consistency, how="left").join(phase_features, how="left")
    features = features[features["Balls"] >= min_balls].copy()
    features.index = features.index.astype(str)
    features.index.name = "Player"

    features["Average"] = (
        features["Runs"] / features["Innings"].replace(0, np.nan)
    ).fillna(0)
    features["Average Runs/Innings"] = features["AverageRuns"].fillna(0)
    features["Dot Ball Control"] = 100 - features["Dot Ball %"].fillna(0)
    features["Consistency Score"] = features["Consistency Score"].fillna(0)

    for column in ["Powerplay SR", "Middle Overs SR", "Death Overs SR"]:
        features[column] = features[column].fillna(features["Strike Rate"])

    numeric_columns = list(dict.fromkeys(DISPLAY_COLUMNS + SIMILARITY_FEATURES))
    features[numeric_columns] = features[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce",
    ).fillna(0)

    return features.sort_values("Runs", ascending=False)


def normalize_player_features(feature_table, feature_columns=SIMILARITY_FEATURES):
    """Scale features before similarity scoring."""
    scaler = StandardScaler()
    matrix = scaler.fit_transform(feature_table[feature_columns])
    return matrix, scaler


def get_player_similarity_scores(player_name, feature_table, top_n=5):
    """Return the most statistically similar batters using cosine similarity."""
    if player_name not in feature_table.index:
        raise ValueError(f"Player not found in feature table: {player_name}")

    matrix, _ = normalize_player_features(feature_table)
    player_position = feature_table.index.get_loc(player_name)
    scores = cosine_similarity(
        matrix[player_position].reshape(1, -1),
        matrix,
    ).flatten()

    result = feature_table[DISPLAY_COLUMNS].copy()
    result["Similarity %"] = (scores * 100).round(2)
    result = result.drop(index=player_name)

    return result.sort_values("Similarity %", ascending=False).head(top_n)


def get_player_comparison(player_1, player_2, feature_table):
    """Return side-by-side comparison data for two batters."""
    missing_players = [
        player
        for player in [player_1, player_2]
        if player not in feature_table.index
    ]

    if missing_players:
        raise ValueError(f"Missing players: {', '.join(missing_players)}")

    selected = feature_table.loc[[player_1, player_2], DISPLAY_COLUMNS].copy()
    selected = selected.round(2)

    return selected


def get_comparison_chart_data(comparison):
    """Convert comparison table into long format for grouped Plotly charts."""
    chart_metrics = [
        "Strike Rate",
        "Average",
        "Boundary %",
        "Dot Ball %",
        "Consistency Score",
        "Average Runs/Innings",
        "Powerplay SR",
        "Middle Overs SR",
        "Death Overs SR",
    ]

    return (
        comparison[chart_metrics]
        .reset_index()
        .melt(
            id_vars="Player",
            var_name="Metric",
            value_name="Value",
        )
    )


def get_radar_chart_data(comparison):
    """Normalize comparison rows into 0-100 values for radar charts."""
    radar_metrics = [
        "Strike Rate",
        "Average",
        "Boundary %",
        "Dot Ball %",
        "Consistency Score",
        "Powerplay SR",
        "Middle Overs SR",
        "Death Overs SR",
    ]
    radar = comparison[radar_metrics].copy()
    radar["Dot Ball %"] = 100 - radar["Dot Ball %"]
    radar.rename(columns={"Dot Ball %": "Dot Ball Control"}, inplace=True)

    for column in radar.columns:
        max_value = radar[column].max()
        if max_value > 0:
            radar[column] = (radar[column] / max_value) * 100
        else:
            radar[column] = 0

    return radar.round(2)


def get_underrated_alternatives(player_name, feature_table, top_n=5):
    """Find similar players with lower total runs but strong rate metrics."""
    similar = get_player_similarity_scores(
        player_name,
        feature_table,
        top_n=len(feature_table) - 1,
    )
    target = feature_table.loc[player_name]
    alternatives = similar[similar["Runs"] < target["Runs"]].copy()
    alternatives["Underrated Score"] = (
        alternatives["Similarity %"] * 0.60
        + (alternatives["Strike Rate"] / target["Strike Rate"]) * 20
        + (alternatives["Average"] / target["Average"]) * 20
    ).replace([np.inf, -np.inf], 0)
    alternatives["Underrated Score"] = alternatives["Underrated Score"].round(2)

    return alternatives.sort_values(
        ["Underrated Score", "Similarity %"],
        ascending=False,
    ).head(top_n)
