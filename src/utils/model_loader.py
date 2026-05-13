from pathlib import Path

import joblib

from src.feature_engineering import create_match_situation
from src.model_training import train_model
from src.utils.data_loader import load_processed_data


MODEL_DIR = Path("models")
WIN_PREDICTOR_MODEL_PATH = MODEL_DIR / "win_predictor.pkl"


def save_model(model, model_path=WIN_PREDICTOR_MODEL_PATH):
    model_path = Path(model_path)
    model_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    joblib.dump(model, model_path)


def load_model(model_path=WIN_PREDICTOR_MODEL_PATH):
    return joblib.load(model_path)


def train_and_save_win_predictor(model_path=WIN_PREDICTOR_MODEL_PATH):
    matches, deliveries = load_processed_data()
    matches = matches.copy()
    deliveries = deliveries.copy()
    matches["WinningTeam"] = matches["WinningTeam"].astype("string")
    deliveries["BattingTeam"] = deliveries["BattingTeam"].astype("string")

    match_df = create_match_situation(matches, deliveries)
    model = train_model(match_df)
    save_model(model, model_path)
    return model


def load_or_train_win_predictor(model_path=WIN_PREDICTOR_MODEL_PATH):
    model_path = Path(model_path)

    if model_path.exists():
        return load_model(model_path)

    return train_and_save_win_predictor(model_path)
