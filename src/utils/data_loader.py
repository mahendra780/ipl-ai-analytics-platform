from pathlib import Path

import pandas as pd


PROCESSED_DATA_DIR = Path("data/processed")
MATCHES_FILE = PROCESSED_DATA_DIR / "matches_cleaned.csv"
DELIVERIES_FILE = PROCESSED_DATA_DIR / "deliveries_cleaned.csv"

MATCH_CATEGORY_COLUMNS = [
    "City",
    "Season",
    "MatchNumber",
    "Team1",
    "Team2",
    "Venue",
    "TossWinner",
    "TossDecision",
    "SuperOver",
    "WinningTeam",
    "WonBy",
    "method",
    "Player_of_Match",
    "Umpire1",
    "Umpire2",
]

DELIVERY_CATEGORY_COLUMNS = [
    "batter",
    "bowler",
    "non-striker",
    "extra_type",
    "player_out",
    "kind",
    "fielders_involved",
    "BattingTeam",
    "Season",
]

MATCH_NUMERIC_COLUMNS = [
    "Margin",
]

DELIVERY_NUMERIC_COLUMNS = [
    "innings",
    "overs",
    "ballnumber",
    "batsman_run",
    "extras_run",
    "total_run",
    "non_boundary",
    "isWicketDelivery",
]


def _convert_to_category(df, columns):
    existing_columns = [column for column in columns if column in df.columns]

    for column in existing_columns:
        df[column] = df[column].astype("category")

    return df


def _optimize_numeric_columns(df, columns):
    existing_columns = [column for column in columns if column in df.columns]

    for column in existing_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
            downcast="integer",
        )

    return df


def optimize_matches_memory(matches):
    if "ID" in matches.columns:
        matches["ID"] = pd.to_numeric(matches["ID"], errors="coerce").astype("int64")

    matches = _convert_to_category(matches, MATCH_CATEGORY_COLUMNS)
    matches = _optimize_numeric_columns(matches, MATCH_NUMERIC_COLUMNS)
    return matches


def optimize_deliveries_memory(deliveries):
    if "ID" in deliveries.columns:
        deliveries["ID"] = pd.to_numeric(deliveries["ID"], errors="coerce").astype("int64")

    deliveries = _convert_to_category(deliveries, DELIVERY_CATEGORY_COLUMNS)
    deliveries = _optimize_numeric_columns(deliveries, DELIVERY_NUMERIC_COLUMNS)
    return deliveries


def load_processed_matches(path=MATCHES_FILE):
    matches = pd.read_csv(path)
    return optimize_matches_memory(matches)


def load_processed_deliveries(path=DELIVERIES_FILE):
    deliveries = pd.read_csv(
        path,
        low_memory=False,
    )
    return optimize_deliveries_memory(deliveries)


def load_processed_data():
    matches = load_processed_matches()
    deliveries = load_processed_deliveries()
    return matches, deliveries
