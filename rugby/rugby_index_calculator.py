import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_rugby_index(row):
    """
    Calculates a single 'Rugby Index Score' for each player
    by combining multiple stats with weighted importance.
    
    You can adjust these weight constants based on your research
    into what rugby fans value most (e.g. tries, defense, leadership, championships).
    """
    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Major accolades
    W_WORLD_CUP_TITLES             = 40
    W_INTERNATIONAL_CHAMPIONSHIPS  = 15
    W_CLUB_CHAMPIONSHIPS           = 5
    W_INTERNATIONAL_PLAYER_OF_YEAR = 20
    W_MAN_OF_THE_MATCH             = 1.0

    # Scoring / Attack
    W_TRIES_SCORED         = 3.0
    W_TOTAL_POINTS_SCORED  = 0.5
    W_CONVERSIONS          = 1.0
    W_PENALTY_GOALS        = 2.0
    W_DROP_GOALS           = 3.0
    W_TRIES_ASSISTED       = 1.0
    W_TOTAL_METERS_CARRIED = 0.02
    W_DEFENDERS_BEATEN     = 0.5
    W_CLEAN_BREAKS         = 1.0
    W_OFFLOADS            = 0.3
    W_PASSES              = 0.05
    W_PICK_AND_GO_METERS  = 0.01
    W_MATCH_WINNING_KICKS = 3.0
    W_AVERAGE_KICK_DISTANCE = 0.2

    # Defense / Forwards
    W_TACKLES_MADE         = 0.2
    W_TACKLE_SUCCESS_PCT   = 1.5
    W_TURNOVERS_WON        = 1.0
    W_TURNOVERS_CONCEDED   = -1.0  # Negative
    W_HANDLING_ERRORS      = -0.5  # Mistakes
    W_LINEOUTS_WON         = 0.5
    W_LINEOUTS_STOLEN      = 1.0
    W_SCRUMS_WON           = 0.3
    W_SCRUMS_LOST          = -0.5
    W_RUCKS_COMPLETED      = 0.1
    W_RUCK_SUCCESS_PCT     = 1.0
    W_TRIES_SAVED          = 2.0

    # Discipline
    W_RED_CARDS            = -5.0
    W_YELLOW_CARDS         = -2.0

    # Longevity / leadership
    W_TEST_CAPS            = 0.2
    W_CAREER_LENGTH_YEARS  = 1.0
    W_CAPTAINED_MATCHES    = 0.3

    # ------------------- EXTRACT ROW VALUES ---------------------
    test_caps                = row['test_caps']
    total_points_scored      = row['total_points_scored']
    tries_scored             = row['tries_scored']
    conversions              = row['conversions']
    penalty_goals            = row['penalty_goals']
    drop_goals               = row['drop_goals']
    total_meters_carried     = row['total_meters_carried']
    defenders_beaten         = row['defenders_beaten']
    clean_breaks             = row['clean_breaks']
    offloads                 = row['offloads']
    passes                   = row['passes']
    handling_errors          = row['handling_errors']
    tackles_made             = row['tackles_made']
    tackle_success           = row['tackle_success_percent']
    turnovers_won            = row['turnovers_won']
    turnovers_conceded       = row['turnovers_conceded']
    lineouts_won             = row['lineouts_won']
    lineouts_stolen          = row['lineouts_stolen']
    scrums_won               = row['scrums_won']
    scrums_lost              = row['scrums_lost']
    rucks_completed          = row['rucks_completed']
    ruck_success             = row['ruck_success_percent']
    pick_and_go_meters       = row['pick_and_go_meters']
    tries_saved              = row['tries_saved']
    tries_assisted           = row['tries_assisted']
    total_appearances_club   = row['total_appearances_club']  # (Not weighted below by default; add if you want)
    total_points_club        = row['total_points_club']       # (Likewise)
    club_championships_won   = row['club_championships_won']
    international_champs     = row['international_rugby_championships']
    world_cup_titles         = row['world_cup_titles']
    player_of_year_awards    = row['international_player_of_year_awards']
    man_of_match_awards      = row['man_of_the_match_awards']
    red_cards                = row['red_cards']
    yellow_cards             = row['yellow_cards']
    captained_matches        = row['captained_matches']
    match_winning_kicks      = row['match_winning_kicks']
    average_kick_distance    = row['average_kick_distance']
    career_length_years      = row['career_length_years']

    # ------------------- CALCULATE PARTIAL SCORES ----------------
    score = 0.0

    # Major accolades
    score += world_cup_titles       * W_WORLD_CUP_TITLES
    score += international_champs   * W_INTERNATIONAL_CHAMPIONSHIPS
    score += club_championships_won * W_CLUB_CHAMPIONSHIPS
    score += player_of_year_awards  * W_INTERNATIONAL_PLAYER_OF_YEAR
    score += man_of_match_awards    * W_MAN_OF_THE_MATCH

    # Scoring / Attack
    score += tries_scored           * W_TRIES_SCORED
    score += total_points_scored    * W_TOTAL_POINTS_SCORED
    score += conversions            * W_CONVERSIONS
    score += penalty_goals          * W_PENALTY_GOALS
    score += drop_goals             * W_DROP_GOALS
    score += tries_assisted         * W_TRIES_ASSISTED
    score += total_meters_carried   * W_TOTAL_METERS_CARRIED
    score += defenders_beaten       * W_DEFENDERS_BEATEN
    score += clean_breaks           * W_CLEAN_BREAKS
    score += offloads               * W_OFFLOADS
    score += passes                 * W_PASSES
    score += pick_and_go_meters     * W_PICK_AND_GO_METERS
    score += match_winning_kicks    * W_MATCH_WINNING_KICKS
    score += average_kick_distance  * W_AVERAGE_KICK_DISTANCE

    # Defense / Forwards
    score += tackles_made        * W_TACKLES_MADE
    score += tackle_success      * W_TACKLE_SUCCESS_PCT
    score += turnovers_won       * W_TURNOVERS_WON
    score += (turnovers_conceded * W_TURNOVERS_CONCEDED)  # negative weight
    score += (handling_errors    * W_HANDLING_ERRORS)     # negative weight
    score += lineouts_won        * W_LINEOUTS_WON
    score += lineouts_stolen     * W_LINEOUTS_STOLEN
    score += scrums_won          * W_SCRUMS_WON
    score += scrums_lost         * W_SCRUMS_LOST          # negative if scrums_lost is positive
    score += rucks_completed     * W_RUCKS_COMPLETED
    score += ruck_success        * W_RUCK_SUCCESS_PCT
    score += tries_saved         * W_TRIES_SAVED

    # Discipline
    score += (red_cards    * W_RED_CARDS)
    score += (yellow_cards * W_YELLOW_CARDS)

    # Longevity / leadership
    score += test_caps           * W_TEST_CAPS
    score += career_length_years * W_CAREER_LENGTH_YEARS
    score += captained_matches   * W_CAPTAINED_MATCHES

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("rugby_dataset.csv")
    
    # 2) Calculate the Rugby Index Score for each player
    df["rugby_index"] = df.apply(calc_rugby_index, axis=1)
    
    # 3) Sort players by that score, descending
    df = df.sort_values(by="rugby_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== RUGBY INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player = row['player_name']
        idx_score = row['rugby_index']
        print(f"{rank}. {player} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='rugby_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("rugby_index_scored.csv", index=False)
    
    # 7) Create the plot using the normalized data
    plot_top_10_indexes(normalized_df, 
                       name_col='player_name',
                       index_col='normalized_index',
                       title='Top 10 Rugby Players by Normalized Index',
                       save_path='rugby_index_plot.png')
    
    print("\nResults saved to 'rugby_index_scored.csv'.")
    print("Line plot saved as 'rugby_index_plot.png'.")


if __name__ == "__main__":
    main()
