from src.data_loader import load_data

from src.data_cleaning import (
    clean_matches_data,
    clean_deliveries_data,
    save_cleaned_data
)

from src.feature_engineering import (
    create_match_situation
)

from src.model_training import (
    train_model
)

# =====================================================
# LOAD DATA
# =====================================================

matches, deliveries = load_data()

# =====================================================
# CLEAN DATA
# =====================================================

matches = clean_matches_data(matches)

deliveries = clean_deliveries_data(deliveries)

# =====================================================
# SAVE CLEANED DATA
# =====================================================

save_cleaned_data(
    matches,
    deliveries
)

print("✅ Cleaned datasets saved.")

# =====================================================
# CREATE ML DATASET
# =====================================================

match_df = create_match_situation(

    matches,

    deliveries
)

print("✅ Match situation dataset created.")

print(
    "Dataset Shape:",
    match_df.shape
)

# =====================================================
# TRAIN MODEL
# =====================================================

model = train_model(
    match_df
)

print("✅ Win prediction model trained.")