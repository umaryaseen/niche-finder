"""
Module to normalize and score niches based on trend, video supply, and competition.
"""

import pandas as pd


def normalize(column: pd.Series) -> pd.Series:
    """
    Normalize a numeric pandas Series to 0–1 scale.

    Args:
        column (pd.Series): Column to normalize.

    Returns:
        pd.Series: Normalized values.
    """
    return (column - column.min()) / (column.max() - column.min())


def score_niches(input_csv: str = 'results/competition_scored.csv') -> pd.DataFrame:
    """
    Compute final scores for niches and rank them.

    Args:
        input_csv (str): Path to the CSV with trend, video, and competition data.

    Returns:
        pd.DataFrame: Ranked niche DataFrame.
    """
    df = pd.read_csv(input_csv)

    df['trend_score_norm'] = normalize(pd.Series(df['trend_score']))
    df['video_supply_norm'] = normalize(pd.Series(df['video_supply']))

    # Invert competition: fewer unique channels = better
    df['competition_score'] = df['unique_channels'].max() - df['unique_channels']
    df['competition_norm'] = normalize(pd.Series(df['competition_score']))

    # Weighted score: adjust if needed
    df['final_score'] = (
        df['trend_score_norm'] * 0.5 +
        df['video_supply_norm'] * 0.3 +
        df['competition_norm'] * 0.2
    )

    df = df.sort_values(by='final_score', ascending=False)
    df.to_csv('results/final_ranked_niches.csv', index=False)
    return df
