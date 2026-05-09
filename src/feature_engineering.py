import pandas as pd


# =====================================================
# CREATE MATCH SITUATION DATASET
# =====================================================

def create_match_situation(
    matches,
    deliveries
):

    # ================================================
    # ONLY SECOND INNINGS
    # ================================================

    df = deliveries[
        deliveries['innings'] == 2
    ].copy()

    # ================================================
    # TOTAL TARGET
    # ================================================

    total_score = (

        deliveries[
            deliveries['innings'] == 1
        ]

        .groupby('ID')['total_run']

        .sum()

        .reset_index()
    )

    total_score.rename(

        columns={
            'total_run': 'target'
        },

        inplace=True
    )

    # Add 1 because chasing team must exceed target
    total_score['target'] = (
        total_score['target'] + 1
    )

    # ================================================
    # MERGE TARGET
    # ================================================

    df = df.merge(

        total_score,

        on='ID'
    )

    # ================================================
    # CURRENT SCORE
    # ================================================

    df['current_score'] = (

        df.groupby('ID')['total_run']

        .cumsum()
    )

    # ================================================
    # RUNS LEFT
    # ================================================

    df['runs_left'] = (

        df['target']

        - df['current_score']
    )

    # ================================================
    # BALLS LEFT
    # ================================================

    df['balls_left'] = (

        120

        - (
            df['overs'] * 6

            + df['ballnumber']
        )
    )

    # ================================================
    # WICKETS LEFT
    # ================================================

    df['wickets_left'] = (

        10

        - df.groupby('ID')[
            'isWicketDelivery'
        ].cumsum()
    )

    # ================================================
    # CURRENT RUN RATE
    # ================================================

    balls_played = (

    120 - df['balls_left']
)

    df['current_rr'] = (

        df['current_score'] * 6

        / balls_played.replace(0, 1)
    )

    # ================================================
    # REQUIRED RUN RATE
    # ================================================

    df['required_rr'] = (

        df['runs_left'] * 6

        / df['balls_left']
    )

    # ================================================
    # RESULT COLUMN
    # ================================================

    match_result = matches[

        ['ID', 'WinningTeam']
    ]

    df = df.merge(

        match_result,

        on='ID'
    )

    # ================================================
    # RESULT LABEL
    # ================================================

    df['result'] = (

        df['BattingTeam']

        ==

        df['WinningTeam']
    ).astype(int)

    # ================================================
    # FINAL COLUMNS
    # ================================================

    final_df = df[

        [
            'BattingTeam',

            'target',

            'current_score',

            'runs_left',

            'balls_left',

            'wickets_left',

            'current_rr',

            'required_rr',

            'result'
        ]
    ]

    # ================================================
    # REMOVE INVALID ROWS
    # ================================================

    final_df = final_df[
        final_df['balls_left'] > 0
    ]

    final_df = final_df.dropna()

    return final_df