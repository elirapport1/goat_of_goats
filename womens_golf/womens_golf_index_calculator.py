import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# If needed, add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_womens_golf_index(row):
    """
    Calculates a single 'Women’s Golf Index Score' by combining a variety
    of women's golf-specific stats:
      - LPGA Tour wins, LET wins, Major wins
      - Times & weeks at #1 ranking
      - Scoring average, driving distance, doping checks
      - Hall of Fame, notable awards, etc.
    
    Negative weighting for doping test failures, higher negative for worse stats
    (like higher scoring average). Adjust these multipliers as you see fit.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Career accomplishments
    W_LPGA_WINS          = 3.0
    W_LET_WINS           = 1.5
    W_MAJOR_WINS         = 6.0
    W_TIMES_WORLD_NO1    = 2.0   # # times reached #1
    W_WEEKS_WORLD_NO1    = 0.1   # each week at #1
    W_CME_CHAMP          = 3.0   # CME Globe championships

    # Majors performance
    W_RUNNER_UP_MAJORS   = 1.0
    W_TOP_10_MAJORS      = 0.3
    W_TOP_5_MAJORS       = 0.5
    W_TOP_3_MAJORS       = 0.7

    # Team events
    W_SOLHEIM_CUPS       = 1.0

    # Stroke-play stats
    W_SCORING_AVG        = -2.0  # lower is better => negative weight
    W_DRIVING_DIST       = 0.02
    W_AVG_PUTTS          = -1.0  # lower is better
    W_WEDGE_PROX         = -0.3  # smaller distance => better => negative

    # Strokes gained
    W_SG_OFF_TEE         = 1.5
    W_SG_APPROACH        = 2.0
    W_SG_PUTTING         = 1.0
    W_SG_TEE_TO_GREEN    = 2.5

    # Additional tournaments & wins
    W_SIGNATURE_WINS     = 1.0
    W_ALL_TOUR_WINS      = 0.5
    W_WINS_OUTSIDE       = 0.3
    W_RUNNER_UPS_TOTAL   = 0.2

    # Ranking & accolades
    W_SEASONS_TOP50_WR   = 0.2
    W_LEADING_MONEY_LIST = 2.0
    W_LPGA_PLAYER_OF_YEAR= 3.0
    W_VARDON_EQUIV       = 1.5  # e.g., LPGA Vare Trophy
    W_ROLEX_PLAYER_OF_YEAR = 3.0
    W_NOTABLE_AWARDS     = 2.0

    # Doping & Hall of Fame
    W_DOPING_PASSED_BONUS   = 0.02
    W_DOPING_FAILED_PENALTY = -10.0
    W_HALL_OF_FAME          = 5.0

    # Misc
    W_HOLES_IN_ONE       = 0.05
    W_CAREER_EARNINGS    = 0.3

    # Retirement penalty
    W_RETIREMENT_PENALTY_PER_YEAR = -0.2
    CURRENT_YEAR = 2023

    # ------------------- EXTRACT ROW VALUES ---------------------
    lpga_wins     = row["total_lpga_tour_wins"]
    let_wins      = row["total_let_tour_wins"]
    major_wins    = row["total_major_wins"]
    times_no1     = row["times_world_no1"]
    weeks_no1     = row["total_weeks_at_no1"]
    cme_champ     = row["cme_globe_championships"]
    
    runner_up_maj = row["runner_ups_in_majors"]
    top_10_maj    = row["top_10_in_majors"]
    top_5_maj     = row["top_5_in_majors"]
    top_3_maj     = row["top_3_in_majors"]
    
    solheim_cups  = row["solheim_cups_played"]
    
    scoring_avg   = row["scoring_average"]
    drive_dist    = row["average_driving_distance_yards"]
    avg_putts     = row["avg_putting_strokes_per_round"]
    wedge_prox    = row["wedge_distance_proximity_feet"]
    
    sg_off_tee    = row["strokes_gained_off_tee"]
    sg_approach   = row["strokes_gained_approach"]
    sg_putting    = row["strokes_gained_putting"]
    sg_tee2green  = row["strokes_gained_tee_to_green"]
    
    signature_wins= row["signature_tournaments_won"]
    all_tour_wins = row["wins_across_all_tours"]
    wins_outside  = row["wins_outside_lpga_let"]
    runner_ups    = row["runner_ups_total"]
    
    seasons_top50 = row["seasons_in_top50_world_ranking"]
    leading_money = row["leading_money_list_times"]
    lpga_poy      = row["lpga_player_of_year_times"]
    vardon_equiv  = row["vardon_trophy_equiv_times"]
    rolex_poy     = row["rolex_player_of_year_times"]
    notable_awards= row["notable_awards"]
    
    doping_passed = row["doping_tests_passed"]
    doping_failed = row["doping_tests_failed"]
    hall_of_fame  = row["hall_of_fame_inducted"]
    
    holes_in_one  = row["hole_in_ones"]
    earnings_m    = row["career_earnings_million_usd"]
    retirement    = row["retirement_year"]

    # ------------------- CALCULATE PARTIAL SCORE ----------------
    score = 0.0

    # Career achievements
    score += lpga_wins   * W_LPGA_WINS
    score += let_wins    * W_LET_WINS
    score += major_wins  * W_MAJOR_WINS
    score += times_no1   * W_TIMES_WORLD_NO1
    score += weeks_no1   * W_WEEKS_WORLD_NO1
    score += cme_champ   * W_CME_CHAMP

    # Majors performance
    score += runner_up_maj * W_RUNNER_UP_MAJORS
    score += top_10_maj    * W_TOP_10_MAJORS
    score += top_5_maj     * W_TOP_5_MAJORS
    score += top_3_maj     * W_TOP_3_MAJORS

    # Team events
    score += solheim_cups  * W_SOLHEIM_CUPS

    # Stroke-play stats
    score += scoring_avg   * W_SCORING_AVG  # negative multiplier
    score += drive_dist    * W_DRIVING_DIST
    score += avg_putts     * W_AVG_PUTTS    # negative multiplier
    score += wedge_prox    * W_WEDGE_PROX   # negative multiplier

    score += sg_off_tee    * W_SG_OFF_TEE
    score += sg_approach   * W_SG_APPROACH
    score += sg_putting    * W_SG_PUTTING
    score += sg_tee2green  * W_SG_TEE_TO_GREEN

    # Additional tournaments/wins
    score += signature_wins* W_SIGNATURE_WINS
    score += all_tour_wins * W_ALL_TOUR_WINS
    score += wins_outside  * W_WINS_OUTSIDE
    score += runner_ups    * W_RUNNER_UPS_TOTAL

    # Ranking & accolades
    score += seasons_top50     * W_SEASONS_TOP50_WR
    score += leading_money     * W_LEADING_MONEY_LIST
    score += lpga_poy          * W_LPGA_PLAYER_OF_YEAR
    score += vardon_equiv      * W_VARDON_EQUIV
    score += rolex_poy         * W_ROLEX_PLAYER_OF_YEAR
    score += notable_awards    * W_NOTABLE_AWARDS

    # Doping & Hall of Fame
    score += doping_passed  * W_DOPING_PASSED_BONUS
    score += doping_failed  * W_DOPING_FAILED_PENALTY
    score += hall_of_fame   * W_HALL_OF_FAME

    # Misc
    score += holes_in_one   * W_HOLES_IN_ONE
    score += earnings_m     * W_CAREER_EARNINGS

    # Retirement penalty
    if retirement != 0 and retirement < CURRENT_YEAR:
        years_since_retirement = CURRENT_YEAR - retirement
        # cap so it doesn't overshadow everything
        if years_since_retirement > 30:
            years_since_retirement = 30
        score += (years_since_retirement * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("womens_golf_dataset.csv")
    
    # 2) Calculate the Women’s Golf Index Score for each player
    df["womens_golf_index"] = df.apply(calc_womens_golf_index, axis=1)
    
    # 3) Sort players by that score, descending
    df = df.sort_values(by="womens_golf_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== WOMEN'S GOLF INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        golfer = row['player_name']
        idx_score = row['womens_golf_index']
        print(f"{rank}. {golfer} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='womens_golf_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("womens_golf_index_scored.csv", index=False)
    
    # 7) Create a line plot of the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Women’s Golfers by Normalized Index',
        save_path='womens_golf_index_plot.png'
    )
    
    print("\nResults saved to 'womens_golf_index_scored.csv'.")
    print("Line plot saved as 'womens_golf_index_plot.png'.")


if __name__ == "__main__":
    main()
