import pandas as pd

def load_data():

    matches = pd.read_csv(
        "data/raw/matches.csv"
    )

    deliveries = pd.read_csv(
        "data/raw/deliveries.csv"
    )

    # Merge season into deliveries
    deliveries = deliveries.merge(

        matches[['ID', 'Season']],

        on='ID',

        how='left'
    )

    return matches, deliveries