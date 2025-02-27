import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_mens_swimming_index(row):
    """
    Calculates a single 'Men’s Swimming Index Score' by blending:
      - Olympic performance (total, gold, silver, bronze)
      - World Championships performance (total, gold, silver, bronze)
      - World record counts
      - Times (with negative weighting so that lower times => higher final score)
      - Doping test outcomes
      - Longevity (years active), total meet points
      - Hall of Fame induction, retirement penalty, etc.
    
    Feel free to tweak or expand these weight definitions.
    """

    # -------------- WEIGHT DEFINITIONS --------------
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

    # Times (the smaller, the better).  
    # We'll give a negative multiplier. E.g. t_50_free * W_TIME_50_FREE => negative total
    # so a lower time yields a more favorable (less negative => higher net) result.
    # You can calibrate these penalty magnitudes to your preference:
    W_TIME_50_FREE    = -1.0
    W_TIME_100_FREE   = -0.5
    W_TIME_200_FREE   = -0.3
    W_TIME_400_FREE   = -0.2
    W_TIME_800_FREE   = -0.1
    W_TIME_1500_FREE  = -0.05

    W_TIME_100_FLY    = -0.4
    W_TIME_200_FLY    = -0.2
    W_TIME_100_BACK   = -0.4
    W_TIME_200_BACK   = -0.2
    W_TIME_100_BREAST = -0.4
    W_TIME_200_BREAST = -0.2
    W_TIME_200_IM     = -0.2
    W_TIME_400_IM     = -0.1

    # Doping
    W_DOPING_FAILED_PENALTY = -10.0
    W_DOPING_PASSED_BONUS   = 0.1

    # Additional
    W_TOTAL_MEET_POINTS       = 0.5
    W_FINA_SWIMMER_OF_YEAR    = 3.0
    W_CAREER_WIN_PERCENT      = 1.0
    W_MAIN_EVENT_OLYMPIC_TITLES = 2.0
    W_YEARS_ACTIVE            = 0.5
    W_PAN_PAC_MEDALS          = 0.3
    W_COMMONWEALTH_MEDALS     = 0.3
    W_PRIZE_MONEY             = 1.0  # million USD

    # Hall of Fame & retirement penalty
    W_HALL_OF_FAME = 5.0
    W_RETIREMENT_PENALTY_PER_YEAR = -0.5
    CURRENT_YEAR = 2023

    # -------------- EXTRACT ROW VALUES --------------
    # Olympic
    total_oly = row["total_olympic_medals"]
    gold_oly  = row["olympic_gold_medals"]
    silver_oly= row["olympic_silver_medals"]
    bronze_oly= row["olympic_bronze_medals"]

    # World Champs
    total_wch = row["total_world_champ_medals"]
    gold_wch  = row["world_champ_gold"]
    silver_wch= row["world_champ_silver"]
    bronze_wch= row["world_champ_bronze"]

    # Records
    wr_count   = row["world_record_count"]

    # Times
    t_50_free    = row["personal_best_50_free"]
    t_100_free   = row["personal_best_100_free"]
    t_200_free   = row["personal_best_200_free"]
    t_400_free   = row["personal_best_400_free"]
    t_800_free   = row["personal_best_800_free"]
    t_1500_free  = row["personal_best_1500_free"]
    t_100_fly    = row["personal_best_100_butterfly"]
    t_200_fly    = row["personal_best_200_butterfly"]
    t_100_back   = row["personal_best_100_back"]
    t_200_back   = row["personal_best_200_back"]
    t_100_breast = row["personal_best_100_breast"]
    t_200_breast = row["personal_best_200_breast"]
    t_200_im     = row["personal_best_200_im"]
    t_400_im     = row["personal_best_400_im"]

    doping_passed = row["doping_tests_passed"]
    doping_failed = row["doping_tests_failed"]

    total_points = row["total_meet_points"]
    fina_swimmer_of_year = row["fina_swimmer_of_year"]
    career_win_pct = row["career_win_percentage"]
    main_event_oly_titles = row["main_event_olympic_titles"]
    years_active = row["years_active"]
    pan_pac_medals = row["pan_pac_medals"]
    cwealth_medals = row["commonwealth_medals"]
    prize_money = row["total_prize_money_million_usd"]
    retirement = row["retirement_year"]
    hof_inducted= row["hall_of_fame_inducted"]

    # -------------- CALCULATE SCORE --------------
    score = 0.0

    # Olympic
    score += total_oly  * W_TOTAL_OLYMPIC_MEDALS
    score += gold_oly   * W_OLYMPIC_GOLD
    score += silver_oly * W_OLYMPIC_SILVER
    score += bronze_oly * W_OLYMPIC_BRONZE

    # World champs
    score += total_wch   * W_TOTAL_WCHAMP_MEDALS
    score += gold_wch    * W_WCHAMP_GOLD
    score += silver_wch  * W_WCHAMP_SILVER
    score += bronze_wch  * W_WCHAMP_BRONZE

    # Records
    score += wr_count * W_WORLD_RECORD_COUNT

    # Times
    score += t_50_free    * W_TIME_50_FREE
    score += t_100_free   * W_TIME_100_FREE
    score += t_200_free   * W_TIME_200_FREE
    score += t_400_free   * W_TIME_400_FREE
    score += t_800_free   * W_TIME_800_FREE
    score += t_1500_free  * W_TIME_1500_FREE
    score += t_100_fly    * W_TIME_100_FLY
    score += t_200_fly    * W_TIME_200_FLY
    score += t_100_back   * W_TIME_100_BACK
    score += t_200_back   * W_TIME_200_BACK
    score += t_100_breast * W_TIME_100_BREAST
    score += t_200_breast * W_TIME_200_BREAST
    score += t_200_im     * W_TIME_200_IM
    score += t_400_im     * W_TIME_400_IM

    # Doping
    score += doping_passed * W_DOPING_PASSED_BONUS
    score += doping_failed * W_DOPING_FAILED_PENALTY

    # Additional
    score += total_points          * W_TOTAL_MEET_POINTS
    score += fina_swimmer_of_year  * W_FINA_SWIMMER_OF_YEAR
    score += career_win_pct        * W_CAREER_WIN_PERCENT
    score += main_event_oly_titles * W_MAIN_EVENT_OLYMPIC_TITLES
    score += years_active          * W_YEARS_ACTIVE
    score += pan_pac_medals        * W_PAN_PAC_MEDALS
    score += cwealth_medals        * W_COMMONWEALTH_MEDALS
    score += prize_money           * W_PRIZE_MONEY

    # Hall of Fame
    score += hof_inducted * W_HALL_OF_FAME

    # Retirement penalty
    if retirement != 0 and retirement < CURRENT_YEAR:
        years_since = CURRENT_YEAR - retirement
        if years_since > 30:
            years_since = 30
        score += (years_since * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("mens_swimming_dataset.csv")
    
    # 2) Calculate the Men’s Swimming Index Score for each swimmer
    df["mens_swimming_index"] = df.apply(calc_mens_swimming_index, axis=1)
    
    # 3) Sort swimmers by that score (descending)
    df = df.sort_values(by="mens_swimming_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== MEN'S SWIMMING INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        name = row['player_name']
        idx_score = row['mens_swimming_index']
        print(f"{rank}. {name} - Index: {idx_score:.1f}")
    
    # 5) Normalize the scores (0–100 scale)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='mens_swimming_index')
    
    # 6) Save results to a new CSV
    normalized_df.to_csv("mens_swimming_index_scored.csv", index=False)
    
    # 7) Create the line plot of top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Men’s Swimmers by Normalized Index',
        save_path='mens_swimming_index_plot.png'
    )
    
    print("\nResults saved to 'mens_swimming_index_scored.csv'.")
    print("Line plot saved as 'mens_swimming_index_plot.png'.")


if __name__ == "__main__":
    main()
