import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_womens_tennis_index(row):
    """
    Calculates a single 'Women's Tennis Index Score' by blending:
    - Major accolades (Grand Slams, WTA Finals, WTA 1000, Olympics)
    - Weeks/Year-End #1
    - Career totals (titles, match wins, etc.)
    - Serve/return stats
    - Negative weight for double faults or advanced age retirement
    - Additional stats like Fed Cup, big title counts, H2H vs top 10, etc.
    """

    # -------------- WEIGHT DEFINITIONS --------------
    # Major accolades
    W_GRAND_SLAM_SINGLES    = 15
    W_GRAND_SLAM_DOUBLES    = 3
    W_WEEKS_AT_NO1          = 0.1
    W_YEAR_END_NO1          = 2
    W_OLYMPIC_GOLD          = 2
    W_FED_CUP_TITLES        = 1.5
    W_WTA_1000_TITLES       = 0.5
    W_WTA_FINALS_TITLES     = 2
    W_HALL_OF_FAME          = 5

    # Career totals
    W_CAREER_SINGLES_TITLES = 0.5
    W_CAREER_DOUBLES_TITLES = 0.3
    W_CAREER_MATCH_WINS      = 0.01
    W_MATCH_WIN_PCT          = 3.0  # overall success
    W_YEARS_ACTIVE           = 0.2  # longevity bonus

    # Serve/return (positive)
    W_ACES                        = 0.0005
    W_FIRST_SERVE_PCT            = 1.0
    W_FIRST_SERVE_PTS_WON_PCT    = 1.5
    W_SECOND_SERVE_PTS_WON_PCT   = 1.0
    W_BREAK_POINTS_SAVED_PCT     = 1.0
    W_SERVICE_GAMES_WON_PCT      = 2.0
    W_RETURN_GAMES_WON_PCT       = 2.0
    W_TIE_BREAKS_WON_PCT         = 1.0

    # Negative
    W_DOUBLE_FAULTS              = -0.0005

    # Surface/event distribution
    W_HARD_TITLES   = 0.2
    W_CLAY_TITLES   = 0.2
    W_GRASS_TITLES  = 0.2
    W_INDOOR_TITLES = 0.1

    # Misc achievements
    W_PRIZE_MONEY_MILLION_USD = 0.5
    W_HEAD_TO_HEAD_TOP10_WINS = 0.3
    W_BEST_CALENDAR_YEAR_WINS = 0.2
    W_CONSECUTIVE_MATCHES_WON = 0.2
    W_BIG_TITLES_COUNT        = 1.0  # total of Slams + WTA Finals + WTA 1000

    # 3-set / longevity
    W_3_SET_MATCH_WINS     = 0.1
    W_3_SETTERS_PLAYED     = 0.05
    W_LONGEST_MATCH_HOURS  = 0.1   # minor factor
    W_RETIREMENT_YEAR_PENALTY = -1.0  # small penalty if retired many years ago

    # -------------- EXTRACT ROW VALUES --------------
    # Major accolades
    slam_singles     = row["grand_slam_singles_titles"]
    slam_doubles     = row["grand_slam_doubles_titles"]
    weeks_no1        = row["weeks_at_no1"]
    year_end_no1     = row["year_end_no1_finishes"]
    olympic_gold     = row["olympic_gold_medals"]
    fed_cup          = row["fed_cup_titles"]
    wta_1000         = row["wta_1000_titles"]
    wta_finals       = row["wta_finals_titles"]
    hall_of_fame     = row["hall_of_fame_inducted"]

    # Career totals
    singles_titles   = row["career_singles_titles"]
    doubles_titles   = row["career_doubles_titles"]
    career_wins      = row["career_match_wins"]
    win_pct          = row["career_win_percentage"]
    years_active     = row["years_active"]

    # Serve/return
    aces             = row["aces"]
    double_faults    = row["double_faults"]
    first_serve_pct  = row["first_serve_percentage"]
    first_srv_pts_won= row["first_serve_points_won_percentage"]
    second_srv_pts_won = row["second_serve_points_won_percentage"]
    bp_saved_pct     = row["break_points_saved_percentage"]
    svc_games_won_pct= row["service_games_won_percentage"]
    return_games_won_pct = row["return_games_won_percentage"]
    tiebreaks_won_pct = row["tie_breaks_won_percentage"]

    # Surface/event distribution
    hard_titles      = row["hard_court_titles"]
    clay_titles      = row["clay_court_titles"]
    grass_titles     = row["grass_court_titles"]
    indoor_titles    = row["indoor_court_titles"]

    # Misc
    prize_money_m    = row["career_prize_money_million_usd"]
    h2h_top10_wins   = row["head_to_head_vs_top10_wins"]
    best_year_wins   = row["best_calendar_year_match_record"]
    consec_matches   = row["most_consecutive_matches_won"]
    big_titles       = row["big_titles_count"]

    # 3-set / longevity
    three_set_wins    = row["three_set_match_wins"]
    three_set_played  = row["three_setters_played"]
    longest_match_hrs = row["longest_match_hours"]
    retirement_year   = row["career_retirement_year"]

    # -------------- CALCULATE PARTIAL SCORES --------------
    score = 0.0

    # Major accolades
    score += slam_singles       * W_GRAND_SLAM_SINGLES
    score += slam_doubles       * W_GRAND_SLAM_DOUBLES
    score += weeks_no1          * W_WEEKS_AT_NO1
    score += year_end_no1       * W_YEAR_END_NO1
    score += olympic_gold       * W_OLYMPIC_GOLD
    score += fed_cup            * W_FED_CUP_TITLES
    score += wta_1000           * W_WTA_1000_TITLES
    score += wta_finals         * W_WTA_FINALS_TITLES
    score += hall_of_fame       * W_HALL_OF_FAME

    # Career totals
    score += singles_titles     * W_CAREER_SINGLES_TITLES
    score += doubles_titles     * W_CAREER_DOUBLES_TITLES
    score += career_wins        * W_CAREER_MATCH_WINS
    score += win_pct            * W_MATCH_WIN_PCT
    score += years_active       * W_YEARS_ACTIVE

    # Serve / return
    score += aces               * W_ACES
    score += (double_faults     * W_DOUBLE_FAULTS)
    score += first_serve_pct    * W_FIRST_SERVE_PCT
    score += first_srv_pts_won  * W_FIRST_SERVE_PTS_WON_PCT
    score += second_srv_pts_won * W_FIRST_SERVE_PTS_WON_PCT
    score += bp_saved_pct       * W_BREAK_POINTS_SAVED_PCT
    score += svc_games_won_pct  * W_SERVICE_GAMES_WON_PCT
    score += return_games_won_pct * W_RETURN_GAMES_WON_PCT
    score += tiebreaks_won_pct  * W_TIE_BREAKS_WON_PCT

    # Surface/event distribution
    score += hard_titles   * W_HARD_TITLES
    score += clay_titles   * W_CLAY_TITLES
    score += grass_titles  * W_GRASS_TITLES
    score += indoor_titles * W_INDOOR_TITLES

    # Misc achievements
    score += prize_money_m      * W_PRIZE_MONEY_MILLION_USD
    score += h2h_top10_wins     * W_HEAD_TO_HEAD_TOP10_WINS
    score += best_year_wins     * W_BEST_CALENDAR_YEAR_WINS
    score += consec_matches     * W_CONSECUTIVE_MATCHES_WON
    score += big_titles         * W_BIG_TITLES_COUNT

    # 3-set / longevity
    score += three_set_wins     * W_3_SET_MATCH_WINS
    score += three_set_played   * W_3_SETTERS_PLAYED
    score += longest_match_hrs  * W_LONGEST_MATCH_HOURS

    # Retirement penalty
    current_year = 2023
    if retirement_year != 0:
        years_since_retirement = current_year - retirement_year
        # Cap penalty so it doesn't overshadow everything
        if years_since_retirement > 30:
            years_since_retirement = 30
        score += years_since_retirement * W_RETIREMENT_YEAR_PENALTY

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("womens_tennis_dataset.csv")
    
    # 2) Calculate the Women's Tennis Index Score for each player
    df["womens_tennis_index"] = df.apply(calc_womens_tennis_index, axis=1)
    
    # 3) Sort players by that score, descending
    df = df.sort_values(by="womens_tennis_index", ascending=False).reset_index(drop=True)
    
    # 4) Print out the ranking
    print("\n====== WOMEN'S TENNIS INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player = row['player_name']
        idx_score = row['womens_tennis_index']
        print(f"{rank}. {player} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores (0–100 scale)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='womens_tennis_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("womens_tennis_index_scored.csv", index=False)
    
    # 7) Create a line plot for the top 10 using the normalized data
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Women’s Tennis Players by Normalized Index',
        save_path='womens_tennis_index_plot.png'
    )
    
    print("\nResults saved to 'womens_tennis_index_scored.csv'.")
    print("Line plot saved as 'womens_tennis_index_plot.png'.")


if __name__ == "__main__":
    main()
