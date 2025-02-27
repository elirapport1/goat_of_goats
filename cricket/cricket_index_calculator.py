import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_cricket_index(row):
    """
    Calculates a single 'Cricket Index Score' for each player by combining
    multiple cricket-specific stats:
      - Test batting & bowling performance (runs, average, 100s, wickets, etc.)
      - ODI & T20I stats
      - Fielding stats (catches, stumpings)
      - ICC ranks, doping checks, Hall of Fame, World Cup wins
      - Possibly all-rounder performance

    Adjust multipliers to reflect your personal or researched weighting for
    how the cricket world values each metric.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Test batting
    W_TEST_RUNS          = 0.05
    W_TEST_AVG           = 2.0
    W_TEST_100S          = 2.5
    W_TEST_50S           = 0.8
    W_TEST_TRIPLE_CENT   = 10.0   # triple hundreds are extremely rare
    W_TEST_DOUBLE_CENT   = 4.0

    # Test bowling
    W_TEST_WICKETS       = 0.05
    W_TEST_BOWL_AVG      = -2.0   # lower average => better => negative weight
    W_TEST_5W_INN        = 2.0
    W_TEST_10W_MATCH     = 3.0

    # ODI batting
    W_ODI_RUNS           = 0.03
    W_ODI_AVG            = 1.5
    W_ODI_100S           = 2.0
    W_ODI_50S            = 0.6

    # ODI bowling
    W_ODI_WICKETS        = 0.03
    W_ODI_BOWL_AVG       = -1.5   # lower is better => negative

    # T20I batting
    W_T20_RUNS           = 0.02
    W_T20_AVG            = 1.2
    W_T20_100S           = 3.0
    W_T20_50S            = 0.5

    # T20I bowling
    W_T20_WICKETS        = 0.02
    W_T20_BOWL_AVG       = -1.2

    # Fielding
    W_CATCHES            = 0.01
    W_STUMPINGS          = 0.05

    # Additional achievements
    W_PLAYER_OF_MATCH    = 0.1
    W_ICC_BEST_BAT_RANK  = -0.05  # rank 1 => score = -0.05 * 1 => negative means lower rank => better
    W_ICC_BEST_BOWL_RANK = -0.05
    W_ICC_BEST_ALLR_RANK = -0.05
    W_HALL_OF_FAME       = 5.0
    W_WORLD_CUP_WINS     = 3.0
    W_NOTABLE_AWARDS     = 1.0

    # Captaincy
    W_TEST_CAPTAINCY_WINS = 0.1

    # Doping
    W_DOPING_FAILED_PENALTY = -10.0
    W_DOPING_PASSED_BONUS   = 0.02

    # Earnings
    W_EARNINGS             = 0.05

    # -------------- EXTRACT FROM ROW --------------
    # Test batting
    test_runs    = row["test_runs"]
    test_avg     = row["test_batting_average"]
    test_100s    = row["test_100s"]
    test_50s     = row["test_50s"]
    test_triples = row["test_triple_centuries"]
    test_doubles = row["test_double_centuries"]

    # Test bowling
    test_wickets   = row["test_wickets"]
    test_bowl_avg  = row["test_bowling_average"]
    test_5w        = row["test_5w_innings"]
    test_10w       = row["test_10w_match"]

    # ODI batting
    odi_runs   = row["odi_runs"]
    odi_avg    = row["odi_batting_average"]
    odi_100s   = row["odi_100s"]
    odi_50s    = row["odi_50s"]

    # ODI bowling
    odi_wickets    = row["odi_wickets"]
    odi_bowl_avg   = row["odi_bowling_average"]

    # T20I batting
    t20_runs   = row["t20i_runs"]
    t20_avg    = row["t20i_batting_average"]
    t20_100s   = row["t20i_100s"]
    t20_50s    = row["t20i_50s"]

    # T20I bowling
    t20_wickets   = row["t20i_wickets"]
    t20_bowl_avg  = row["t20i_bowling_average"]

    # Fielding
    catches       = row["catches"]
    stumpings     = row["stumpings"]

    # Additional
    player_of_match      = row["player_of_the_match_awards"]
    icc_bat_rank         = row["icc_best_batting_rank"]
    icc_bowl_rank        = row["icc_best_bowling_rank"]
    icc_allr_rank        = row["icc_best_allrounder_rank"]
    hall_of_fame         = row["icc_hall_of_fame_inducted"]
    wc_wins              = row["world_cup_wins"]
    doping_failed        = row["doping_tests_failed"]
    doping_passed        = row["doping_tests_passed"]
    test_capt_wins       = row["test_captaincy_wins"]
    notable_awards       = row["notable_awards"]
    earnings_m           = row["career_earnings_million_usd"]

    # -------------- CALCULATE SCORE --------------
    score = 0.0

    # Test batting
    score += test_runs    * W_TEST_RUNS
    score += test_avg     * W_TEST_AVG
    score += test_100s    * W_TEST_100S
    score += test_50s     * W_TEST_50S
    score += test_triples * W_TEST_TRIPLE_CENT
    score += test_doubles * W_TEST_DOUBLE_CENT

    # Test bowling
    score += test_wickets   * W_TEST_WICKETS
    score += test_bowl_avg  * W_TEST_BOWL_AVG
    score += test_5w        * W_TEST_5W_INN
    score += test_10w       * W_TEST_10W_MATCH

    # ODI batting
    score += odi_runs   * W_ODI_RUNS
    score += odi_avg    * W_ODI_AVG
    score += odi_100s   * W_ODI_100S
    score += odi_50s    * W_ODI_50S

    # ODI bowling
    score += odi_wickets    * W_ODI_WICKETS
    score += odi_bowl_avg   * W_ODI_BOWL_AVG

    # T20I batting
    score += t20_runs   * W_T20_RUNS
    score += t20_avg    * W_T20_AVG
    score += t20_100s   * W_T20_100S
    score += t20_50s    * W_T20_50S

    # T20I bowling
    score += t20_wickets   * W_T20_WICKETS
    score += t20_bowl_avg  * W_T20_BOWL_AVG

    # Fielding
    score += catches   * W_CATCHES
    score += stumpings * W_STUMPINGS

    # Additional achievements
    score += player_of_match * W_PLAYER_OF_MATCH

    # Negative rank => the better the rank => the more negative the product
    # Actually, we want rank=1 => big bonus, so let's do invert. 
    # But we have a negative multiplier, so if rank=1 => rank * -0.05 => -0.05 => that's a small negative
    # Let's do a small offset so rank=1 => e.g. 0. 
    # For simplicity, let's just proceed with negative weighting
    score += icc_bat_rank  * W_ICC_BEST_BAT_RANK
    score += icc_bowl_rank * W_ICC_BEST_BOWL_RANK
    score += icc_allr_rank * W_ICC_BEST_ALLR_RANK

    if hall_of_fame == 1:
        score += W_HALL_OF_FAME
    score += wc_wins * W_WORLD_CUP_WINS
    score += notable_awards * W_NOTABLE_AWARDS

    # Captaincy
    score += test_capt_wins * W_TEST_CAPTAINCY_WINS

    # Doping
    score += doping_passed * W_DOPING_PASSED_BONUS
    score += doping_failed * W_DOPING_FAILED_PENALTY

    # Earnings
    score += earnings_m * W_EARNINGS

    return score

def main():
    # 1) Load the dataset
    df = pd.read_csv("cricket_dataset.csv")

    # 2) Calculate the Cricket Index Score for each player
    df["cricket_index"] = df.apply(calc_cricket_index, axis=1)

    # 3) Sort players by that score, descending
    df = df.sort_values(by="cricket_index", ascending=False).reset_index(drop=True)

    # 4) Print the ranking
    print("\n====== CRICKET INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player_name = row['player_name']
        idx_score = row['cricket_index']
        print(f"{rank}. {player_name} - Index: {idx_score:.1f}")

    # 5) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='cricket_index')

    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("cricket_index_scored.csv", index=False)

    # 7) Create a line plot of the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Cricketers by Normalized Index',
        save_path='cricket_index_plot.png'
    )

    print("\nResults saved to 'cricket_index_scored.csv'.")
    print("Line plot saved as 'cricket_index_plot.png'.")

if __name__ == "__main__":
    main()
