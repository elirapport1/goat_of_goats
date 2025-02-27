import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_womens_swimming_index(row):
    """
    Calculates a single 'Women’s Swimming Index Score' by combining:
      - Olympic medals, world champs, world records
      - personal best times (with negative weighting for slower times)
      - doping test outcomes
      - longevity, HOF induction, etc.
    
    Feel free to modify the weights to reflect personal or researched emphasis.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Olympic performance
    W_TOTAL_OLYMPIC_MEDALS  = 2.0
    W_OLYMPIC_GOLD          = 5.0
    W_OLYMPIC_SILVER        = 2.5
    W_OLYMPIC_BRONZE        = 1.5

    # World championships
    W_TOTAL_WCHAMP_MEDALS   = 1.0
    W_WCHAMP_GOLD           = 3.0
    W_WCHAMP_SILVER         = 1.5
    W_WCHAMP_BRONZE         = 1.0

    # World records
    W_WORLD_RECORD_COUNT     = 4.0

    # Times (the smaller, the better). We'll invert them with a negative multiplier
    # e.g. for 50 free, a 24.0 is "better" than 25.0
    # We can add a small negative weight so that lower times yield a higher (less negative) value.
    # scale factor picks how strong these times matter
    W_TIME_PENALTY_50_FREE   = -1.0
    W_TIME_PENALTY_100_FREE  = -0.5
    W_TIME_PENALTY_200_FREE  = -0.2
    W_TIME_PENALTY_400_FREE  = -0.1
    W_TIME_PENALTY_800_FREE  = -0.05
    W_TIME_PENALTY_1500_FREE = -0.02

    # Similarly for strokes
    W_TIME_PENALTY_100_FLY  = -0.4
    W_TIME_PENALTY_200_FLY  = -0.2
    W_TIME_PENALTY_100_BACK = -0.4
    W_TIME_PENALTY_200_BACK = -0.2
    W_TIME_PENALTY_100_BREAST = -0.4
    W_TIME_PENALTY_200_BREAST = -0.2
    W_TIME_PENALTY_200_IM   = -0.2
    W_TIME_PENALTY_400_IM   = -0.1

    # Doping
    W_DOPING_FAILED_PENALTY = -10.0
    W_DOPING_PASSED_BONUS   = 0.1  # small bonus per passed test

    # Other
    W_TOTAL_MEET_POINTS       = 0.5
    W_FINA_SWIMMER_OF_YEAR    = 3.0
    W_CAREER_WIN_PERCENT      = 1.0
    W_MAIN_EVENT_OLYMPIC_TITLES = 2.0
    W_YEARS_ACTIVE            = 0.5
    W_PAN_PAC_MEDALS          = 0.3
    W_COMMONWEALTH_MEDALS     = 0.3
    W_PRIZE_MONEY             = 1.0  # million USD

    # Hall of Fame & retirement penalty (older retirees penalized)
    W_HALL_OF_FAME = 5.0
    W_RETIREMENT_PENALTY_PER_YEAR = -0.5

    # ------------------- EXTRACT ROW VALUES ---------------------
    total_oly_medals   = row["total_olympic_medals"]
    oly_gold           = row["olympic_gold_medals"]
    oly_silver         = row["olympic_silver_medals"]
    oly_bronze         = row["olympic_bronze_medals"]

    total_wch_medals   = row["total_world_champ_medals"]
    wch_gold           = row["world_champ_gold"]
    wch_silver         = row["world_champ_silver"]
    wch_bronze         = row["world_champ_bronze"]

    wr_count           = row["world_record_count"]

    # times
    t_50_free   = row["personal_best_50_free"]
    t_100_free  = row["personal_best_100_free"]
    t_200_free  = row["personal_best_200_free"]
    t_400_free  = row["personal_best_400_free"]
    t_800_free  = row["personal_best_800_free"]
    t_1500_free = row["personal_best_1500_free"]

    t_100_fly   = row["personal_best_100_butterfly"]
    t_200_fly   = row["personal_best_200_butterfly"]
    t_100_back  = row["personal_best_100_back"]
    t_200_back  = row["personal_best_200_back"]
    t_100_breast= row["personal_best_100_breast"]
    t_200_breast= row["personal_best_200_breast"]
    t_200_im    = row["personal_best_200_im"]
    t_400_im    = row["personal_best_400_im"]

    doping_passed = row["doping_tests_passed"]
    doping_failed = row["doping_tests_failed"]

    total_meet_points = row["total_meet_points"]
    fina_swimmer_of_year = row["fina_swimmer_of_year"]
    career_win_pct   = row["career_win_percentage"]
    main_event_titles= row["main_event_olympic_titles"]
    years_active     = row["years_active"]
    pan_pac_medals   = row["pan_pac_medals"]
    commonwealth_medals = row["commonwealth_medals"]
    prize_money      = row["total_prize_money_million_usd"]
    retirement_year  = row["retirement_year"]
    hall_of_fame     = row["hall_of_fame_inducted"]

    # For retirement penalty
    CURRENT_YEAR = 2023

    # ------------------- CALCULATE PARTIAL SCORE ----------------
    score = 0.0

    # Olympic performance
    score += total_oly_medals * W_TOTAL_OLYMPIC_MEDALS
    score += oly_gold         * W_OLYMPIC_GOLD
    score += oly_silver       * W_OLYMPIC_SILVER
    score += oly_bronze       * W_OLYMPIC_BRONZE

    # World championships
    score += total_wch_medals * W_TOTAL_WCHAMP_MEDALS
    score += wch_gold         * W_WCHAMP_GOLD
    score += wch_silver       * W_WCHAMP_SILVER
    score += wch_bronze       * W_WCHAMP_BRONZE

    # World records
    score += wr_count         * W_WORLD_RECORD_COUNT

    # Times (negative penalty, so lower times yield less negative => more positive overall)
    # e.g. a 24.0 in 50 free => 24.0 * -1.0 = -24 => better than -25 for 25.0
    # You can calibrate these as you like.
    score += t_50_free   * W_TIME_PENALTY_50_FREE
    score += t_100_free  * W_TIME_PENALTY_100_FREE
    score += t_200_free  * W_TIME_PENALTY_200_FREE
    score += t_400_free  * W_TIME_PENALTY_400_FREE
    score += t_800_free  * W_TIME_PENALTY_800_FREE
    score += t_1500_free * W_TIME_PENALTY_1500_FREE

    score += t_100_fly   * W_TIME_PENALTY_100_FLY
    score += t_200_fly   * W_TIME_PENALTY_200_FLY
    score += t_100_back  * W_TIME_PENALTY_100_BACK
    score += t_200_back  * W_TIME_PENALTY_200_BACK
    score += t_100_breast* W_TIME_PENALTY_100_BREAST
    score += t_200_breast* W_TIME_PENALTY_200_BREAST
    score += t_200_im    * W_TIME_PENALTY_200_IM
    score += t_400_im    * W_TIME_PENALTY_400_IM

    # Doping
    score += doping_passed * W_DOPING_PASSED_BONUS
    score += doping_failed * W_DOPING_FAILED_PENALTY

    # Other
    score += total_meet_points    * W_TOTAL_MEET_POINTS
    score += fina_swimmer_of_year * W_FINA_SWIMMER_OF_YEAR
    score += career_win_pct       * W_CAREER_WIN_PERCENT
    score += main_event_titles    * W_MAIN_EVENT_OLYMPIC_TITLES
    score += years_active         * W_YEARS_ACTIVE
    score += pan_pac_medals       * W_PAN_PAC_MEDALS
    score += commonwealth_medals  * W_COMMONWEALTH_MEDALS
    score += prize_money          * W_PRIZE_MONEY

    # Hall of Fame
    score += hall_of_fame * W_HALL_OF_FAME

    # Retirement penalty
    if retirement_year != 0 and retirement_year < CURRENT_YEAR:
        years_since_retirement = CURRENT_YEAR - retirement_year
        # Cap penalty so it doesn't overshadow everything
        if years_since_retirement > 30:
            years_since_retirement = 30
        score += (years_since_retirement * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("womens_swimming_dataset.csv")
    
    # 2) Calculate the Women’s Swimming Index Score for each swimmer
    df["womens_swimming_index"] = df.apply(calc_womens_swimming_index, axis=1)
    
    # 3) Sort swimmers by that score, descending
    df = df.sort_values(by="womens_swimming_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking in the console
    print("\n====== WOMEN'S SWIMMING INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        swimmer = row['player_name']
        idx_score = row['womens_swimming_index']
        print(f"{rank}. {swimmer} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='womens_swimming_index')
    
    # 6) Save the sorted results with normalized scores to CSV
    normalized_df.to_csv("womens_swimming_index_scored.csv", index=False)
    
    # 7) Create a line plot (top 10 swimmers) using the normalized data
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Women’s Swimmers by Normalized Index',
        save_path='womens_swimming_index_plot.png'
    )
    
    print("\nResults saved to 'womens_swimming_index_scored.csv'.")
    print("Line plot saved as 'womens_swimming_index_plot.png'.")


if __name__ == "__main__":
    main()
