"""
Module to simulate video supply availability for each niche.
"""

import random
import pandas as pd


def mock_video_count(keyword: str) -> int:
    """
    Simulate video availability using a random number.

    Args:
        keyword (str): Niche keyword.

    Returns:
        int: Mock count of video supply.
    """
    return random.randint(100, 1000)


def add_video_availability(trend_csv: str = 'results/trend_scores.csv') -> pd.DataFrame:
    """
    Append mock video supply counts to trend data.

    Args:
        trend_csv (str): Path to trend score CSV.

    Returns:
        pd.DataFrame: Updated DataFrame with video supply.
    """
    df = pd.read_csv(trend_csv)
    df['video_supply'] = df['niche'].apply(mock_video_count)
    df.to_csv('results/scored_niches.csv', index=False)
    return df
