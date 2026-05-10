
import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

from sklearn.compose import (
    ColumnTransformer
)

from sklearn.preprocessing import (
    OneHotEncoder
)

from sklearn.pipeline import (
    Pipeline
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.metrics import (
    accuracy_score
)


# =====================================================
# TRAIN WIN PREDICTION MODEL
# =====================================================

def train_model(match_df):

    # ================================================
    # FEATURES & TARGET
    # ================================================

    X = match_df.drop(
        columns=['result']
    )

    y = match_df['result']

    # ================================================
    # TRAIN TEST SPLIT
    # ================================================

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,
            y,

            test_size=0.2,

            random_state=42
        )
    )

    # ================================================
    # CATEGORICAL COLUMNS
    # ================================================

    categorical_cols = [

        'BattingTeam'
    ]

    # ================================================
    # TRANSFORMER
    # ================================================

    transformer = ColumnTransformer(

        transformers=[

            (
                'tnf1',

                OneHotEncoder(
                    drop='first'
                ),

                categorical_cols
            )
        ],

        remainder='passthrough'
    )

    # ================================================
    # PIPELINE
    # ================================================

    pipe = Pipeline([

        ('step1', transformer),

        ('step2', LogisticRegression(
            solver='liblinear'
        ))
    ])

    # ================================================
    # TRAIN MODEL
    # ================================================

    pipe.fit(
        X_train,
        y_train
    )

    # ================================================
    # PREDICTIONS
    # ================================================

    y_pred = pipe.predict(
        X_test
    )

    # ================================================
    # ACCURACY
    # ================================================

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    print(
        "\nModel Accuracy:",
        round(accuracy * 100, 2),
        "%"
    )

    return pipe