import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_mens_golf_index(row):
    """
    Calculates a single 'Men’s Golf Index Score' by blending:
      - Major wins, total PGA wins, weeks at #1, FedEx Cup, etc.
      - Statistical performance (scoring average, driving distance, strokes gained)
      - Doping checks, Hall of Fame, major awards, etc.

    Adjust the multipliers to suit your perspective on what's most important 
    in assessing a golfer’s legacy and skill.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Career accomplishments
    W_TOTAL_PGA_WINS           = 3.0
    W_TOTAL_EURO_WINS          = 1.5
    W_MAJOR_WINS               = 6.0
    W_TIMES_WORLD_NO1          = 2.0   # # times they rose to #1
    W_WEEKS_AT_NO1             = 0.1   # each week
    W_FEDEX_CUP_CHAMP          = 3.0

    # Performance in majors
    W_RUNNER_UP_MAJORS         = 1.0
    W_TOP_10_MAJORS            = 0.3
    W_TOP_5_MAJORS             = 0.5
    W_TOP_3_MAJORS             = 0.7

    # Ryder Cup or international team appearances (for some context)
    W_RYDER_CUPS               = 1.0

    # Stroke-play stats
    W_SCORING_AVG              = -2.0  # lower is better => negative weight
    W_DRIVING_DISTANCE         = 0.02
    W_AVG_PUTTING_STROKES      = -1.0  # smaller is better
    W_WEDGE_PROXIMITY          = -0.3  # feet => lower is better
    W_STROKES_GAINED_OFF_TEE   = 1.5
    W_STROKES_GAINED_APPROACH  = 2.0
    W_STROKES_GAINED_PUTTING   = 1.0
    W_STROKES_GAINED_TTG       = 2.5

    # Additional tours & events
    W_SIGNATURE_TOURNEYS_WON   = 1.0
    W_WINS_ACROSS_ALL_TOURS    = 0.5
    W_WINS_OUTSIDE_PGA_EURO    = 0.3

    # Runner-ups total
    W_RUNNER_UPS_TOTAL         = 0.2

    # Additional accolades
    W_SEASONS_IN_TOP50_WR      = 0.2
    W_LEADING_MONEY_LIST       = 2.0
    W_PGA_PLAYER_OF_YEAR       = 3.0
    W_PGA_TOUR_PLAYER_OF_YEAR  = 3.0
    W_VARDON_TROPHY            = 1.5
    W_BYRON_NELSON_AWARD       = 1.5
    W_MAJOR_AWARDS_BONUS       = 2.0  # For e.g. "lifetime achievement"

    # Doping & HoF
    W_DOPING_PASSED_BONUS      = 0.02
    W_DOPING_FAILED_PENALTY    = -10.0
    W_HALL_OF_FAME             = 5.0

    # Misc stats
    W_HOLES_IN_ONE             = 0.05

    # Earnings
    W_CAREER_EARNINGS          = 0.0

    # Retirement penalty
    W_RETIREMENT_PENALTY_PER_YEAR = -0.2
    CURRENT_YEAR = 2023

    # ------------------- EXTRACT ROW VALUES ---------------------
    pga_wins       = row["total_pga_tour_wins"]
    euro_wins      = row["total_euro_tour_wins"]
    majors         = row["total_major_wins"]
    times_no1      = row["times_world_no1"]
    weeks_no1      = row["total_weeks_at_no1"]
    fedex_champ    = row["fedex_cup_championships"]

    runner_up_majors = row["runner_ups_in_majors"]
    top_10_majors    = row["top_10_in_majors"]
    top_5_majors     = row["top_5_in_majors"]
    top_3_majors     = row["top_3_in_majors"]

    ryder_cups       = row["ryder_cups_played"]

    scoring_avg      = row["scoring_average"]
    driving_distance = row["average_driving_distance_yards"]
    avg_putts        = row["avg_putting_strokes_per_round"]
    wedge_prox       = row["wedge_distance_proximity_feet"]

    sg_off_tee       = row["strokes_gained_off_tee"]
    sg_approach      = row["strokes_gained_approach"]
    sg_putting       = row["strokes_gained_putting"]
    sg_tee_to_green  = row["strokes_gained_tee_to_green"]

    signature_wins   = row["signature_tournaments_won"]
    all_tour_wins    = row["wins_across_all_tours"]
    wins_outside     = row["wins_outside_pga_euro"]
    runner_ups_total = row["runner_ups_total"]

    seasons_top50_wr = row["seasons_in_top50_world_ranking"]
    lead_money_list  = row["leading_money_list_times"]
    pga_poy          = row["pga_player_of_year_times"]
    pga_tour_poy     = row["pga_tour_player_of_year_times"]
    vardon_trophy    = row["vardon_trophy_times"]
    byron_award      = row["byron_nelson_award_times"]

    doping_passed = row["doping_tests_passed"]
    doping_failed = row["doping_tests_failed"]
    hall_of_fame  = row["hall_of_fame_inducted"]

    holes_in_one  = row["hole_in_ones"]
    earnings_m    = row["career_earnings_million_usd"]
    retirement    = row["retirement_year"]

    # ------------------- CALCULATE PARTIAL SCORE ----------------
    score = 0.0

    # Major achievements
    score += pga_wins      * W_TOTAL_PGA_WINS
    score += euro_wins     * W_TOTAL_EURO_WINS
    score += majors        * W_MAJOR_WINS
    score += times_no1     * W_TIMES_WORLD_NO1
    score += weeks_no1     * W_WEEKS_AT_NO1
    score += fedex_champ   * W_FEDEX_CUP_CHAMP

    score += runner_up_majors * W_RUNNER_UP_MAJORS
    score += top_10_majors    * W_TOP_10_MAJORS
    score += top_5_majors     * W_TOP_5_MAJORS
    score += top_3_majors     * W_TOP_3_MAJORS

    score += ryder_cups       * W_RYDER_CUPS

    # Performance stats
    score += scoring_avg       * W_SCORING_AVG     # negative weight => lower average is better
    score += driving_distance  * W_DRIVING_DISTANCE
    score += avg_putts         * W_AVG_PUTTING_STROKES
    score += wedge_prox        * W_WEDGE_PROXIMITY

    score += sg_off_tee       * W_STROKES_GAINED_OFF_TEE
    score += sg_approach      * W_STROKES_GAINED_APPROACH
    score += sg_putting       * W_STROKES_GAINED_PUTTING
    score += sg_tee_to_green  * W_STROKES_GAINED_TTG

    # Additional tournaments
    score += signature_wins    * W_SIGNATURE_TOURNEYS_WON
    score += all_tour_wins     * W_WINS_ACROSS_ALL_TOURS
    score += wins_outside      * W_WINS_OUTSIDE_PGA_EURO
    score += runner_ups_total  * W_RUNNER_UPS_TOTAL

    # Seasons in top 50
    score += seasons_top50_wr  * W_SEASONS_IN_TOP50_WR

    # Extra accolades
    score += lead_money_list   * W_LEADING_MONEY_LIST
    score += pga_poy           * W_PGA_PLAYER_OF_YEAR
    score += pga_tour_poy      * W_PGA_TOUR_PLAYER_OF_YEAR
    score += vardon_trophy     * W_VARDON_TROPHY
    score += byron_award       * W_BYRON_NELSON_AWARD
    # Could also add a "lifetime achievement" bonus or "major awards" category

    # Doping & Hall of Fame
    score += doping_passed   * W_DOPING_PASSED_BONUS
    score += doping_failed   * W_DOPING_FAILED_PENALTY
    score += hall_of_fame    * W_HALL_OF_FAME

    # Misc
    score += holes_in_one    * W_HOLES_IN_ONE
    score += earnings_m      * W_CAREER_EARNINGS

    # Retirement penalty
    if retirement != 0 and retirement < CURRENT_YEAR:
        years_since_retirement = CURRENT_YEAR - retirement
        if years_since_retirement > 30:
            years_since_retirement = 30
        score += (years_since_retirement * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("mens_golf_dataset.csv")
    
    # 2) Calculate the Men’s Golf Index Score for each player
    df["mens_golf_index"] = df.apply(calc_mens_golf_index, axis=1)
    
    # 3) Sort players by that score, descending
    df = df.sort_values(by="mens_golf_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== MEN'S GOLF INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        golfer = row['player_name']
        idx_score = row['mens_golf_index']
        print(f"{rank}. {golfer} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores to 0–100
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='mens_golf_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("mens_golf_index_scored.csv", index=False)
    
    # 7) Create a line plot of the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Men’s Golfers by Normalized Index',
        save_path='mens_golf_index_plot.png'
    )
    
    print("\nResults saved to 'mens_golf_index_scored.csv'.")
    print("Line plot saved as 'mens_golf_index_plot.png'.")


if __name__ == "__main__":
    main()
