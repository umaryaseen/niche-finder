"""
Main script to orchestrate the niche selection pipeline.
"""

from trend_analysis import analyze_keywords
from video_supply_check import add_video_availability
from competition_analysis import add_competition_scores
from score_niches import score_niches
from cpm_estimator import add_cpm_estimates
from evergreen_checker import add_evergreen_scores



def main():
    """
    Run the complete niche analysis pipeline:
    1. Analyze search trends
    2. Estimate video supply
    3. Assess YouTube competition
    4. Score and rank niches
    """
    print("Analyzing Trends...")
    analyze_keywords()

    print("Checking Video Supply...")
    add_video_availability()

    print("Assessing YouTube Competition...")
    add_competition_scores()

    print("Scoring and Ranking Niches...")
    df = score_niches()
    print(df.head())
    add_cpm_estimates()
    add_evergreen_scores()




if __name__ == "__main__":
    main()
