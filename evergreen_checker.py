"""
Module to assess evergreen potential for each niche by checking video age and view patterns.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"


def is_evergreen(published_at: str) -> bool:
    """
    Determine if a video is older than 6 months.

    Args:
        published_at (str): ISO 8601 publish date.

    Returns:
        bool: True if older than 6 months, False otherwise.
    """
    try:
        publish_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
        return (datetime.utcnow() - publish_date) > timedelta(days=180)
    except Exception as e:
        print(f"Date parse error: {e}")
        return False


def evergreen_score_for_keyword(keyword: str, max_results: int = 20) -> float:
    """
    Calculate percentage of videos older than 6 months in top search results.

    Args:
        keyword (str): Niche keyword.
        max_results (int): Number of videos to evaluate.

    Returns:
        float: Ratio (0.0 to 1.0) of evergreen videos.
    """
    try:
        search_params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "order": "viewCount",
            "maxResults": max_results,
            "key": YOUTUBE_API_KEY
        }
        search_resp = requests.get(SEARCH_URL, params=search_params).json()
        video_ids = [item["id"]["videoId"] for item in search_resp.get("items", [])]

        if not video_ids:
            return 0.0

        video_params = {
            "part": "snippet",
            "id": ",".join(video_ids),
            "key": YOUTUBE_API_KEY
        }
        video_resp = requests.get(VIDEO_URL, params=video_params).json()
        evergreen_flags = [is_evergreen(item["snippet"]["publishedAt"]) for item in video_resp.get("items", [])]

        return sum(evergreen_flags) / len(evergreen_flags) if evergreen_flags else 0.0
    except Exception as e:
        print(f"Error calculating evergreen score for '{keyword}': {e}")
        return 0.0


def add_evergreen_scores(input_csv: str = "results/cpm_scored.csv") -> pd.DataFrame:
    """
    Append evergreen potential scores to the dataset.

    Args:
        input_csv (str): Path to CSV file with niche data.

    Returns:
        pd.DataFrame: Updated DataFrame with evergreen scores.
    """
    df = pd.read_csv(input_csv)
    df["evergreen_ratio"] = df["niche"].apply(evergreen_score_for_keyword)
    df.to_csv("results/evergreen_scored.csv", index=False)
    return df
