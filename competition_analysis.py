"""
Module to analyze YouTube competition using the YouTube Data API.
"""

import pandas as pd
import requests
from typing import List, Optional
from collections import Counter
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Set your API key as an environment variable
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def get_unique_channels_for_niche(keyword: str, max_results: int = 20) -> Optional[int]:
    """
    Count the number of unique YouTube channels with top-viewed videos for a given keyword.

    Args:
        keyword (str): Niche keyword to search for.
        max_results (int): Number of top videos to analyze.

    Returns:
        Optional[int]: Count of unique channels or None on failure.
    """
    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "order": "viewCount",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    try:
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        channels = [item["snippet"]["channelTitle"] for item in data.get("items", [])]
        unique_channel_count = len(set(channels))
        return unique_channel_count
    except Exception as e:
        print(f"Error fetching YouTube data for '{keyword}': {e}")
        return None


def add_competition_scores(input_csv: str = "results/scored_niches.csv") -> pd.DataFrame:
    """
    Append competition scores (fewer unique channels = better score).

    Args:
        input_csv (str): Path to CSV with trend and supply data.

    Returns:
        pd.DataFrame: Updated DataFrame with competition score.
    """
    df = pd.read_csv(input_csv)
    df["unique_channels"] = df["niche"].apply(get_unique_channels_for_niche)
    df.to_csv("results/competition_scored.csv", index=False)
    return df
