import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the normalization and plotting helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_womens_boxing_index(row):
    """
    Calculates a single 'Women's Boxing Index Score' by combining the 40+ stats from the dataset.
    Each stat has a weight that reflects its perceived importance in women's boxing:
      - Major accolades (undisputed, ring magazine, lineal, # world titles)
      - Win/loss record, KO rate
      - Punch stats per round
      - Doping checks
      - Hall of fame induction, etc.
    
    Negative weighting for losses, doping test failures, knockdowns received, etc.
    Adjust these multipliers to your preference.
    """

    # --------------------- WEIGHT DEFINITIONS ---------------------
    # High-level achievements
    W_WORLD_TITLES_HELD      = 3.0
    W_UNDISPUTED_TITLES      = 5.0
    W_LINEAL_TITLES          = 2.0
    W_RING_MAG_TITLES        = 2.0

    # Win/loss record
    W_TOTAL_FIGHTS           = 0.2
    W_WINS                   = 3.0
    W_LOSSES                 = -2.0
    W_DRAWS                  = 0.5
    W_KOS                    = 1.5
    W_KO_PERCENT             = 2.0
    W_SIGNATURE_WIN          = 2.0
    W_MAJOR_UPSET_WINS       = 2.5

    # Title defenses
    W_TITLE_DEFENSES         = 1.0
    W_UNIFIED_DEFENSES       = 2.0
    W_YEARS_AS_CHAMPION      = 1.5

    # Punch stats (averages per round)
    W_LANDED_PER_ROUND       = 0.5
    W_THROWN_PER_ROUND       = 0.1

    # Knockdowns
    W_KD_SCORED              = 0.5
    W_KD_RECEIVED            = -1.5

    # Physical attributes (mild or no direct effect)
    W_HEIGHT_CM              = 0.01
    W_REACH_CM               = 0.01

    # Additional personal stats
    W_AGE_AT_DEBUT           = 0.0  # neutral or negative if older
    W_FIGHTS_IN_HOMETOWN     = 0.1

    # Doping
    W_DOPING_PASSED_BONUS    = 0.05
    W_DOPING_FAILED_PENALTY  = -10.0

    # Hall of Fame
    W_HALL_OF_FAME           = 5.0

    # Major awards (like BWAA, ESPN, etc.)
    W_MAJOR_AWARDS           = 2.0

    # Rivalries
    W_NOTABLE_RIVALRIES      = 1.0

    # Attendance & PPV
    W_AVG_ATTENDANCE         = 0.0002  # scale so e.g. 5k => +1
    W_PPV_BUYS_MILLIONS      = 2.0

    # Longevity & Streak
    W_LONGEST_WIN_STREAK     = 0.5
    W_YEARS_ACTIVE           = 0.3

    # Earnings & Retirement penalty
    W_CAREER_EARNINGS        = 1.0
    W_RETIREMENT_PENALTY_PER_YEAR = -0.5
    CURRENT_YEAR = 2023

    # Trainer name doesn’t usually factor into index scoring, so we skip it.

    # --------------------- EXTRACT ROW VALUES ---------------------
    world_titles = row["world_titles_held"]
    undisputed   = row["undisputed_titles"]
    lineal       = row["lineal_titles"]
    ring_mag     = row["ring_magazine_titles"]

    total_fights = row["total_fights"]
    wins         = row["wins"]
    losses       = row["losses"]
    draws        = row["draws"]
    kos          = row["kos"]
    ko_pct       = row["ko_percentage"]
    signature_win= row["signature_win"]
    major_upsets = row["major_upset_wins"]

    title_defenses    = row["title_defenses"]
    unified_defenses  = row["unified_title_defenses"]
    years_as_champion = row["years_as_champion"]

    landed_per_round  = row["avg_punches_landed_per_round"]
    thrown_per_round  = row["avg_punches_thrown_per_round"]
    kd_scored         = row["knockdowns_scored"]
    kd_received       = row["knockdowns_received"]

    height_cm  = row["height_cm"]
    reach_cm   = row["reach_cm"]
    age_debut  = row["age_at_debut"]
    hometown_fights = row["fights_in_hometown"]

    doping_passed = row["doping_tests_passed"]
    doping_failed = row["doping_tests_failed"]

    hof_inducted   = row["hall_of_fame_inducted"]
    major_awards   = row["major_awards"]
    notable_rivalries = row["notable_rivalries"]
    avg_attendance = row["avg_attendance_events"]
    ppv_buys       = row["ppv_buys_millions"]

    longest_streak = row["longest_win_streak"]
    years_active   = row["years_active"]
    career_earnings= row["career_earnings_million_usd"]
    retirement     = row["retirement_year"]

    # --------------------- CALCULATE PARTIAL SCORE ----------------
    score = 0.0

    # Major accolades
    score += world_titles   * W_WORLD_TITLES_HELD
    score += undisputed     * W_UNDISPUTED_TITLES
    score += lineal         * W_LINEAL_TITLES
    score += ring_mag       * W_RING_MAG_TITLES

    # Record
    score += total_fights   * W_TOTAL_FIGHTS
    score += wins           * W_WINS
    score += losses         * W_LOSSES
    score += draws          * W_DRAWS
    score += kos            * W_KOS
    score += ko_pct         * W_KO_PERCENT
    score += signature_win  * W_SIGNATURE_WIN
    score += major_upsets   * W_MAJOR_UPSET_WINS

    # Titles & defenses
    score += title_defenses    * W_TITLE_DEFENSES
    score += unified_defenses  * W_UNIFIED_DEFENSES
    score += years_as_champion * W_YEARS_AS_CHAMPION

    # Punch stats
    score += landed_per_round  * W_LANDED_PER_ROUND
    score += thrown_per_round  * W_THROWN_PER_ROUND

    # Knockdowns
    score += kd_scored   * W_KD_SCORED
    score += kd_received * W_KD_RECEIVED

    # Physical attributes
    score += height_cm * W_HEIGHT_CM
    score += reach_cm  * W_REACH_CM

    # Additional
    score += hometown_fights * W_FIGHTS_IN_HOMETOWN
    score += doping_passed   * W_DOPING_PASSED_BONUS
    score += doping_failed   * W_DOPING_FAILED_PENALTY
    score += hof_inducted    * W_HALL_OF_FAME
    score += major_awards    * W_MAJOR_AWARDS
    score += notable_rivalries * W_NOTABLE_RIVALRIES
    score += avg_attendance    * W_AVG_ATTENDANCE
    score += ppv_buys          * W_PPV_BUYS_MILLIONS
    score += longest_streak    * W_LONGEST_WIN_STREAK
    score += years_active      * W_YEARS_ACTIVE
    score += career_earnings   * W_CAREER_EARNINGS

    # Retirement penalty
    if retirement != 0 and retirement < CURRENT_YEAR:
        years_since = CURRENT_YEAR - retirement
        if years_since > 30:
            years_since = 30
        score += (years_since * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("womens_boxing_dataset.csv")
    
    # 2) Calculate the Women’s Boxing Index Score for each boxer
    df["womens_boxing_index"] = df.apply(calc_womens_boxing_index, axis=1)
    
    # 3) Sort the boxers by that score, descending
    df = df.sort_values(by="womens_boxing_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== WOMEN'S BOXING INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        fighter = row["player_name"]
        idx_score = row["womens_boxing_index"]
        print(f"{rank}. {fighter} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='womens_boxing_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("womens_boxing_index_scored.csv", index=False)
    
    # 7) Create the line plot for the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Women’s Boxers by Normalized Index',
        save_path='womens_boxing_index_plot.png'
    )
    
    print("\nResults saved to 'womens_boxing_index_scored.csv'.")
    print("Line plot saved as 'womens_boxing_index_plot.png'.")


if __name__ == "__main__":
    main()
