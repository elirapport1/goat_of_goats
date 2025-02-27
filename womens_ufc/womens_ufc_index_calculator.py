import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# If needed, add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_womens_ufc_index(row):
    """
    Calculates a single 'Women's UFC Index Score' by combining a variety
    of MMA-related stats:
      - Win/loss record, finishes, doping checks
      - Striking & grappling stats
      - Championship accolades
      - Awards (Fight/Performance of Night)
      - Hall of Fame, major honors
      - Negative weighting for doping test failures, submission/KO losses, etc.
    
    Feel free to adjust these weights based on your research or personal perspective
    on what's important in women's UFC history.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Championship accolades
    W_UFC_CHAMPIONSHIPS_WON   = 5.0
    W_TITLE_DEFENSES          = 2.0
    W_WORLD_TITLES_HELD       = 2.0  # e.g. recognized belts

    # Basic record
    W_TOTAL_FIGHTS            = 0.2
    W_WINS                    = 3.0
    W_LOSSES                  = -2.0
    W_DRAWS                   = 0.5

    # Finishes
    W_KO_TKO_WINS             = 2.0
    W_SUBMISSION_WINS         = 2.0
    W_DECISION_WINS           = 1.0

    # Negative for losses
    W_KO_TKO_LOSSES           = -3.0
    W_SUBMISSION_LOSSES       = -3.0
    W_DECISION_LOSSES         = -1.5

    # Fight stats
    W_SIG_STRIKES_PER_MIN     = 0.5
    W_STRIKE_ACCURACY_PERCENT = 0.2
    W_TAKEDOWNS_PER_15        = 0.5
    W_TAKEDOWN_ACCURACY       = 0.2
    W_SUB_ATTEMPTS_PER_15     = 0.5

    # Additional fight outcomes
    W_AVG_FIGHT_TIME          = 0.1  # fighting longer can be good or neutral
    W_KNOCKDOWNS_SCORED       = 0.5
    W_KNOCKDOWNS_RECEIVED     = -1.0

    # Championship / accolades
    # (We already have W_UFC_CHAMPIONSHIPS_WON and W_TITLE_DEFENSES above)
    
    # Special achievements
    W_PERFORMANCE_OF_THE_NIGHT_AWARDS   = 2.0  # Performance bonuses
    W_FIGHT_OF_THE_NIGHT_AWARDS         = 1.5  # Fight of the Night awards
    W_MAJOR_AWARDS                 = 2.0

    # Hall of Fame
    W_HALL_OF_FAME            = 5.0

    # Rivalries / big upsets
    W_LONGEST_WIN_STREAK      = 0.5
    W_BIGGEST_UPSET_WINS      = 2.0

    # Physical attributes
    W_HEIGHT_CM               = 0.01
    W_REACH_CM                = 0.01

    # Additional
    W_FIGHTS_HOME_COUNTRY     = 0.2

    # Doping
    W_DOPING_PASSED_BONUS     = 0.05  # small bonus per passed test
    W_DOPING_FAILED_PENALTY   = -10.0

    # Career earnings & retirement penalty
    W_CAREER_EARNINGS         = 1.0
    W_RETIREMENT_PENALTY_PER_YEAR = -0.5
    CURRENT_YEAR = 2023

    # ------------------- EXTRACT ROW VALUES ---------------------
    # Basic record
    total_fights  = row["total_mma_fights"]
    wins          = row["wins"]
    losses        = row["losses"]
    draws         = row["draws"]

    # Finishes
    ko_wins           = row["ko_tko_wins"]
    sub_wins          = row["submission_wins"]
    dec_wins          = row["decision_wins"]
    ko_losses         = row["ko_tko_losses"]
    sub_losses        = row["submission_losses"]
    dec_losses        = row["decision_losses"]

    # Titles
    world_titles      = row["world_titles_held"]
    championships_won = row["ufc_championships_won"]
    title_defenses    = row["title_defenses"]

    # Fight stats
    sig_strikes_min = row["avg_significant_strikes_per_min"]
    strike_accuracy = row["avg_strike_accuracy_percent"]
    takedowns_15    = row["avg_takedowns_per_15"]
    takedown_acc    = row["avg_takedown_accuracy_percent"]
    sub_attempts_15 = row["avg_submission_attempts_per_15"]
    avg_fight_time  = row["average_fight_time_minutes"]
    kd_scored       = row["knockdowns_scored"]
    kd_received     = row["knockdowns_received"]

    # Others
    fights_home = row["fights_in_home_country"]
    fight_of_night = row["fight_of_the_night_awards"]
    perf_of_night = row["performance_of_the_night_awards"]
    hall_of_fame  = row["hall_of_fame_inducted"]
    major_awards  = row["major_awards"]
    streak        = row["longest_win_streak"]
    upsets        = row["biggest_upset_wins"]

    height_cm   = row["height_cm"]
    reach_cm    = row["reach_cm"]

    doping_passed  = row["doping_tests_passed"]
    doping_failed  = row["doping_tests_failed"]

    earnings   = row["career_earnings_million_usd"]
    retirement = row["retirement_year"]

    # ------------------- CALCULATE PARTIAL SCORE ----------------
    score = 0.0

    # Record
    score += total_fights * W_TOTAL_FIGHTS
    score += wins         * W_WINS
    score += losses       * W_LOSSES
    score += draws        * W_DRAWS

    # Finish data
    score += ko_wins        * W_KO_TKO_WINS
    score += sub_wins       * W_SUBMISSION_WINS
    score += dec_wins       * W_DECISION_WINS
    score += ko_losses      * W_KO_TKO_LOSSES
    score += sub_losses     * W_SUBMISSION_LOSSES
    score += dec_losses     * W_DECISION_LOSSES

    # Titles
    score += world_titles   * W_WORLD_TITLES_HELD
    score += championships_won * W_UFC_CHAMPIONSHIPS_WON
    score += title_defenses * W_TITLE_DEFENSES

    # Fight stats
    score += sig_strikes_min   * W_SIG_STRIKES_PER_MIN
    score += strike_accuracy   * W_STRIKE_ACCURACY_PERCENT
    score += takedowns_15      * W_TAKEDOWNS_PER_15
    score += takedown_acc      * W_TAKEDOWN_ACCURACY
    score += sub_attempts_15   * W_SUB_ATTEMPTS_PER_15
    score += avg_fight_time    * W_AVG_FIGHT_TIME
    score += kd_scored         * W_KNOCKDOWNS_SCORED
    score += kd_received       * W_KNOCKDOWNS_RECEIVED

    # Additional achievements
    score += perf_of_night     * W_PERFORMANCE_OF_THE_NIGHT_AWARDS
    score += fight_of_night    * W_FIGHT_OF_THE_NIGHT_AWARDS
    score += major_awards      * W_MAJOR_AWARDS
    score += hall_of_fame      * W_HALL_OF_FAME

    # Rivalries / big upsets / streak
    score += streak            * W_LONGEST_WIN_STREAK
    score += upsets            * W_BIGGEST_UPSET_WINS

    # Physical
    score += height_cm * W_HEIGHT_CM
    score += reach_cm  * W_REACH_CM

    # Home fights
    score += fights_home * W_FIGHTS_HOME_COUNTRY

    # Doping
    score += doping_passed  * W_DOPING_PASSED_BONUS
    score += doping_failed  * W_DOPING_FAILED_PENALTY

    # Earnings
    score += earnings * W_CAREER_EARNINGS

    # Retirement penalty
    if retirement != 0 and retirement < CURRENT_YEAR:
        years_since_retirement = CURRENT_YEAR - retirement
        if years_since_retirement > 30:
            years_since_retirement = 30
        score += (years_since_retirement * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("womens_ufc_dataset.csv")
    
    # 2) Calculate the Women's UFC Index Score for each fighter
    df["womens_ufc_index"] = df.apply(calc_womens_ufc_index, axis=1)
    
    # 3) Sort the fighters by that score, descending
    df = df.sort_values(by="womens_ufc_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== WOMEN'S UFC INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        fighter = row['fighter_name']
        idx_score = row['womens_ufc_index']
        print(f"{rank}. {fighter} - Index: {idx_score:.1f}")
    
    # 5) Normalize the scores (0–100)
    normalized_df = normalize_indexes(df, name_col='fighter_name', index_col='womens_ufc_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("womens_ufc_index_scored.csv", index=False)
    
    # 7) Create the plot using the normalized data
    plot_top_10_indexes(
        normalized_df,
        name_col='fighter_name',
        index_col='normalized_index',
        title='Top 10 Women\'s UFC Fighters by Normalized Index',
        save_path='womens_ufc_index_plot.png'
    )
    
    print("\nResults saved to 'womens_ufc_index_scored.csv'.")
    print("Line plot saved as 'womens_ufc_index_plot.png'.")


if __name__ == "__main__":
    main()
