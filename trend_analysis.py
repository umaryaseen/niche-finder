"""
Module to analyze Google Trends data using pytrends.
"""

from pytrends.request import TrendReq
import pandas as pd
import time
import random

pytrends = TrendReq(hl='en-US', tz=360)


def get_trend_score(keyword: str, max_retries: int = 3) -> float:
    """
    Get the average search interest score for a keyword.

    Args:
        keyword (str): The keyword to analyze.
        max_retries (int): Maximum number of retry attempts.

    Returns:
        float: Average trend score over the past 12 months.
    """
    for attempt in range(max_retries):
        try:
            pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')
            df = pytrends.interest_over_time()
            if df.empty:
                return 0.0
            return float(df[keyword].mean())
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 5 + random.uniform(1, 3)  # Exponential backoff
                print(f"Rate limited for '{keyword}', waiting {wait_time:.1f}s (attempt {attempt + 1})")
                time.sleep(wait_time)
                continue
            else:
                print(f"Error fetching trend score for '{keyword}': {e}")
                return 0.0
    return 0.0


def analyze_keywords(niche_file: str = 'niches.txt') -> pd.DataFrame:
    """
    Analyze search trends for a list of niche keywords.

    Args:
        niche_file (str): Path to the text file with keywords.

    Returns:
        pd.DataFrame: DataFrame containing trend scores.
    """
    with open(niche_file, 'r') as f:
        keywords = [line.strip() for line in f.readlines()]

    results = []
    for i, keyword in enumerate(keywords):
        score = get_trend_score(keyword)
        print(f"{keyword}: {score}")
        results.append({'niche': keyword, 'trend_score': score})
        
        # Longer delay between requests to avoid rate limiting
        if i < len(keywords) - 1:  # Don't sleep after the last request
            delay = 5 + random.uniform(2, 5)  # 5-10 seconds
            print(f"Waiting {delay:.1f}s before next request...")
            time.sleep(delay)

    df = pd.DataFrame(results)
    df.to_csv('results/trend_scores.csv', index=False)
    return df
