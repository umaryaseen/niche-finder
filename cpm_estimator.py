"""
Module to estimate Ads CPM using public RPM data (mocked or scraped).
"""

import pandas as pd
import random


def mock_cpm_estimate(keyword: str) -> float:
    """
    Simulate CPM value assignment based on niche.

    Args:
        keyword (str): Niche keyword.

    Returns:
        float: Simulated CPM value in USD.
    """
    niche_categories = {
        "finance": 7.0,
        "tech": 5.5,
        "fitness": 4.5,
        "pets": 2.5,
        "fails": 2.0,
        "motivation": 3.0,
        "travel": 3.5,
        "gaming": 2.8
    }

    for category, cpm in niche_categories.items():
        if category in keyword.lower():
            return round(random.uniform(cpm - 0.5, cpm + 0.5), 2)

    return round(random.uniform(2.0, 4.0), 2)  # default fallback CPM


def add_cpm_estimates(input_csv: str = "results/competition_scored.csv") -> pd.DataFrame:
    """
    Append CPM estimates to the dataset.

    Args:
        input_csv (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: Updated DataFrame with CPM scores.
    """
    df = pd.read_csv(input_csv)
    df["cpm_usd"] = df["niche"].apply(mock_cpm_estimate)
    df.to_csv("results/cpm_scored.csv", index=False)
    return df
