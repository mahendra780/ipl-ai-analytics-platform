import pandas as pd

# =====================================================
# CLEAN MATCHES DATA
# =====================================================

def clean_matches_data(matches):

    # Remove duplicates
    matches = matches.drop_duplicates()

    # Convert date
    matches['Date'] = pd.to_datetime(matches['Date'])

    # Handle missing values
    matches['WinningTeam'] = (
        matches['WinningTeam']
        .fillna('No Result')
    )

    matches['Player_of_Match'] = (
        matches['Player_of_Match']
        .fillna('Unknown')
    )

    # =================================================
    # TEAM NAME STANDARDIZATION
    # =================================================

    team_mapping = {

        'Delhi Daredevils': 'Delhi Capitals',

        'Kings XI Punjab': 'Punjab Kings',

        'Deccan Chargers': 'Sunrisers Hyderabad',

        'Rising Pune Supergiants':
        'Rising Pune Supergiant'
    }

    # Apply mapping
    matches = matches.replace(team_mapping)

    return matches

# =====================================================
# CLEAN DELIVERIES DATA
# =====================================================

def clean_deliveries_data(deliveries):

    # Remove duplicate rows
    deliveries = deliveries.drop_duplicates()

    # Handle missing values
    deliveries['batter'] = (
        deliveries['batter']
        .fillna('Unknown')
    )

    deliveries['bowler'] = (
        deliveries['bowler']
        .fillna('Unknown')
    )

    return deliveries


# =====================================================
# SAVE CLEANED DATA
# =====================================================

def save_cleaned_data(matches, deliveries):

    matches.to_csv(
        "data/processed/matches_cleaned.csv",
        index=False
    )

    deliveries.to_csv(
        "data/processed/deliveries_cleaned.csv",
        index=False
    )