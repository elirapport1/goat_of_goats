import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# If needed, add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_mens_ufc_index(row):
    """
    Calculates a single 'Men's UFC Index Score' by combining various MMA stats:
      - Record (wins, losses, draws), finishes (KO/Sub),
      - Championship accolades (# UFC belts, title defenses, etc.),
      - Striking and grappling metrics (significant strikes, takedowns, etc.),
      - Doping record, Hall of Fame, major awards, etc.
    
    Negative weighting for doping failures, knockdowns received, losses, etc.
    Adjust these multipliers to reflect your personal or researched viewpoint.
    """

    # -------------------- WEIGHT DEFINITIONS --------------------
    # Championship achievements
    W_UFC_CHAMPIONSHIPS_WON   = 5.0
    W_TITLE_DEFENSES          = 2.0
    W_WORLD_TITLES_HELD       = 2.0   # # recognized belts

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
    W_STRIKE_ACCURACY         = 0.2
    W_TAKEDOWNS_PER_15        = 0.5
    W_TAKEDOWN_ACCURACY       = 0.2
    W_SUB_ATTEMPTS_PER_15     = 0.5

    # Additional
    W_AVG_FIGHT_TIME          = 0.1
    W_KNOCKDOWNS_SCORED       = 0.5
    W_KNOCKDOWNS_RECEIVED     = -1.0

    # Awards
    W_FIGHT_OF_THE_NIGHT_AWARDS        = 1.5
    W_PERFORMANCE_OF_THE_NIGHT_AWARDS  = 1.5
    W_MAJOR_AWARDS                 = 2.0

    # Hall of Fame
    W_HALL_OF_FAME            = 5.0

    # Rivalries / big upsets
    W_LONGEST_WIN_STREAK      = 0.5
    W_BIGGEST_UPSET_WINS      = 2.0

    # Physical attributes
    W_HEIGHT_CM               = 0.01
    W_REACH_CM                = 0.01

    # Home fights
    W_FIGHTS_HOME_COUNTRY     = 0.2

    # Doping
    W_DOPING_PASSED_BONUS     = 0.05
    W_DOPING_FAILED_PENALTY   = -10.0

    # Career earnings & retirement penalty
    W_CAREER_EARNINGS         = 1.0
    W_RETIREMENT_PENALTY_PER_YEAR = -0.5
    CURRENT_YEAR = 2023

    # -------------------- EXTRACT ROW VALUES --------------------
    total_fights = row["total_mma_fights"]
    wins         = row["wins"]
    losses       = row["losses"]
    draws        = row["draws"]

    ko_wins          = row["ko_tko_wins"]
    sub_wins         = row["submission_wins"]
    dec_wins         = row["decision_wins"]
    ko_losses        = row["ko_tko_losses"]
    sub_losses       = row["submission_losses"]
    dec_losses       = row["decision_losses"]

    world_titles     = row["world_titles_held"]
    champ_won        = row["ufc_championships_won"]
    title_defenses   = row["title_defenses"]

    height_cm   = row["height_cm"]
    reach_cm    = row["reach_cm"]

    sig_strikes = row["avg_significant_strikes_per_min"]
    strike_acc  = row["avg_strike_accuracy_percent"]
    td_15       = row["avg_takedowns_per_15"]
    td_acc      = row["avg_takedown_accuracy_percent"]
    sub_15      = row["avg_submission_attempts_per_15"]
    fight_time  = row["average_fight_time_minutes"]

    kd_scored   = row["knockdowns_scored"]
    kd_received = row["knockdowns_received"]

    fights_home = row["fights_in_home_country"]
    fight_of_night = row["fight_of_the_night_awards"]
    perf_of_night  = row["performance_of_the_night_awards"]
    hof_inducted   = row["hall_of_fame_inducted"]
    major_awards   = row["major_awards"]
    streak         = row["longest_win_streak"]
    upset_wins     = row["biggest_upset_wins"]

    doping_passed = row["doping_tests_passed"]
    doping_failed = row["doping_tests_failed"]

    earnings      = row["career_earnings_million_usd"]
    retirement    = row["retirement_year"]

    # -------------------- CALCULATE SCORE ------------------------
    score = 0.0

    # Basic record
    score += total_fights * W_TOTAL_FIGHTS
    score += wins         * W_WINS
    score += losses       * W_LOSSES
    score += draws        * W_DRAWS

    # Finishes
    score += ko_wins      * W_KO_TKO_WINS
    score += sub_wins     * W_SUBMISSION_WINS
    score += dec_wins     * W_DECISION_WINS
    score += ko_losses    * W_KO_TKO_LOSSES
    score += sub_losses   * W_SUBMISSION_LOSSES
    score += dec_losses   * W_DECISION_LOSSES

    # Title & defenses
    score += world_titles   * W_WORLD_TITLES_HELD
    score += champ_won      * W_UFC_CHAMPIONSHIPS_WON
    score += title_defenses * W_TITLE_DEFENSES

    # Fight stats
    score += sig_strikes  * W_SIG_STRIKES_PER_MIN
    score += strike_acc   * W_STRIKE_ACCURACY
    score += td_15        * W_TAKEDOWNS_PER_15
    score += td_acc       * W_TAKEDOWN_ACCURACY
    score += sub_15       * W_SUB_ATTEMPTS_PER_15
    score += fight_time   * W_AVG_FIGHT_TIME
    score += kd_scored    * W_KNOCKDOWNS_SCORED
    score += kd_received  * W_KNOCKDOWNS_RECEIVED

    # Awards
    score += fight_of_night   * W_FIGHT_OF_THE_NIGHT_AWARDS
    score += perf_of_night    * W_PERFORMANCE_OF_THE_NIGHT_AWARDS
    score += major_awards     * W_MAJOR_AWARDS
    score += hof_inducted     * W_HALL_OF_FAME

    # Rivalries / upsets / streak
    score += streak           * W_LONGEST_WIN_STREAK
    score += upset_wins       * W_BIGGEST_UPSET_WINS

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
        years_since = CURRENT_YEAR - retirement
        if years_since > 30:
            years_since = 30
        score += (years_since * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("mens_ufc_dataset.csv")
    
    # 2) Calculate the Men's UFC Index Score for each fighter
    df["mens_ufc_index"] = df.apply(calc_mens_ufc_index, axis=1)
    
    # 3) Sort fighters by that score, descending
    df = df.sort_values(by="mens_ufc_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== MEN'S UFC INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        fighter = row['fighter_name']
        idx_score = row['mens_ufc_index']
        print(f"{rank}. {fighter} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df, name_col='fighter_name', index_col='mens_ufc_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("mens_ufc_index_scored.csv", index=False)
    
    # 7) Create a line plot for the top 10 fighters
    plot_top_10_indexes(
        normalized_df,
        name_col='fighter_name',
        index_col='normalized_index',
        title='Top 10 Mens UFC Fighters by Normalized Index',
        save_path='mens_ufc_index_plot.png'
    )
    
    print("\nResults saved to 'mens_ufc_index_scored.csv'.")
    print("Line plot saved as 'mens_ufc_index_plot.png'.")


if __name__ == "__main__":
    main()
