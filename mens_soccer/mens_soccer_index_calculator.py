import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_soccer_index(row):
    """
    Calculates a single 'Soccer Index Score' for each player by combining
    multiple soccer-specific stats:
      - Club and international performance (appearances, goals, assists, etc.)
      - Trophies & accolades
      - Discipline (red/yellow cards)
      - Doping tests and injuries
      - Advanced metrics (pass accuracy, key passes, etc.)
      - Earnings and Hall of Fame induction
    
    Adjust multipliers to reflect the importance of each metric in soccer.
    Higher weights are assigned to more prestigious achievements.
    Negative weights are used for detrimental stats like red cards or doping failures.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Club Performance
    W_CLUB_APPEARANCES     = 0.02
    W_CLUB_GOALS           = 0.05
    W_CLUB_ASSISTS         = 0.04
    W_CLUB_MINUTES_PLAYED  = 0.0001  # Minimal weight

    # International Performance
    W_INT_CAPS             = 0.03
    W_INT_GOALS            = 0.07
    W_INT_ASSISTS          = 0.05
    W_INT_MINUTES_PLAYED   = 0.0001  # Minimal weight

    # Ratios / Per-Game Metrics
    W_CLUB_GOAL_RATIO      = 10.0
    W_INT_GOAL_RATIO       = 12.0

    # Trophies & Accolades
    W_FIFA_WORLD_CUP_TITLES      = 30.0
    W_CONTINENTAL_TITLES         = 15.0
    W_LEAGUE_TITLES              = 20.0
    W_CHAMPIONS_LEAGUE_TITLES    = 25.0
    W_DOMESTIC_CUP_TITLES        = 10.0
    W_MAJOR_INDIVIDUAL_AWARDS    = 20.0
    W_BALLON_DOR_WINDS            = 25.0

    # Additional Performance
    W_HAT_TRICKS                  = 5.0
    W_PENALTY_GOALS               = 3.0
    W_FREE_KICK_GOALS             = 4.0
    W_RED_CARDS                   = -5.0
    W_YELLOW_CARDS                = -1.0
    W_MAN_OF_THE_MATCH_AWARDS     = 2.0
    W_CAPTAINCY_APPEARANCES       = 3.0

    # Creative / Advanced Metrics
    W_KEY_PASSES_PER_GAME         = 2.0
    W_DRIBBLES_COMPLETED_PER_GAME = 2.0
    W_BIG_CHANCES_CREATED         = 3.0
    W_PASS_ACCURACY_PERCENT       = 1.5

    # Defensive / Goalkeeper Stats
    W_CLEAN_SHEETS                = 5.0
    W_TACKLES_WON_PER_GAME        = 1.5
    W_INTERCEPTIONS_PER_GAME      = 1.5
    W_SAVES_PER_GAME              = 3.0  # Relevant for Goalkeepers

    # Doping & Injuries
    W_DOPING_TESTS_PASSED         = 0.02
    W_DOPING_TESTS_FAILED         = -20.0
    W_MAJOR_INJURIES_COUNT        = -2.0

    # Hall of Fame & Earnings
    W_HALL_OF_FAME_INDUCTED       = 15.0
    W_CAREER_EARNINGS_MILLION_USD = 0.05
    W_TOTAL_TROPHIES_WON          = 1.0

    # ------------------- EXTRACT FROM ROW --------------
    # Club Performance
    club_appearances    = row["club_appearances"]
    club_goals          = row["club_goals"]
    club_assists        = row["club_assists"]
    club_minutes_played = row["club_minutes_played"]

    # International Performance
    international_caps         = row["international_caps"]
    international_goals        = row["international_goals"]
    international_assists      = row["international_assists"]
    international_minutes_played = row["international_minutes_played"]

    # Ratios / Per-Game Metrics
    club_goal_ratio      = row["club_goal_ratio"]
    international_goal_ratio = row["international_goal_ratio"]

    # Trophies & Accolades
    fifa_world_cup_titles      = row["fifa_world_cup_titles"]
    continental_titles         = row["continental_titles"]
    league_titles              = row["league_titles"]
    champions_league_titles    = row["champions_league_titles"]
    domestic_cup_titles        = row["domestic_cup_titles"]
    major_individual_awards    = row["major_individual_awards"]
    ballon_dor_wins            = row["ballon_dor_wins"]

    # Additional Performance
    hat_tricks                  = row["hat_tricks"]
    penalty_goals               = row["penalty_goals"]
    free_kick_goals             = row["free_kick_goals"]
    red_cards                   = row["red_cards"]
    yellow_cards                = row["yellow_cards"]
    man_of_the_match_awards     = row["man_of_the_match_awards"]
    captaincy_appearances       = row["captaincy_appearances"]

    # Creative / Advanced Metrics
    key_passes_per_game         = row["key_passes_per_game"]
    dribbles_completed_per_game = row["dribbles_completed_per_game"]
    big_chances_created         = row["big_chances_created"]
    pass_accuracy_percent       = row["pass_accuracy_percent"]

    # Defensive / Goalkeeper Stats
    clean_sheets                = row["clean_sheets"]
    tackles_won_per_game        = row["tackles_won_per_game"]
    interceptions_per_game      = row["interceptions_per_game"]
    saves_per_game              = row["saves_per_game"]

    # Doping & Injuries
    doping_tests_passed         = row["doping_tests_passed"]
    doping_tests_failed         = row["doping_tests_failed"]
    major_injuries_count        = row["major_injuries_count"]

    # Hall of Fame & Earnings
    hall_of_fame_inducted       = row["hall_of_fame_inducted"]
    career_earnings_million_usd = row["career_earnings_million_usd"]
    total_trophies_won          = row["total_trophies_won"]

    # ------------------- CALCULATE SCORE --------------
    score = 0.0

    # Club Performance
    score += club_appearances    * W_CLUB_APPEARANCES
    score += club_goals          * W_CLUB_GOALS
    score += club_assists        * W_CLUB_ASSISTS
    score += club_minutes_played * W_CLUB_MINUTES_PLAYED

    # International Performance
    score += international_caps         * W_INT_CAPS
    score += international_goals        * W_INT_GOALS
    score += international_assists      * W_INT_ASSISTS
    score += international_minutes_played * W_INT_MINUTES_PLAYED

    # Ratios / Per-Game Metrics
    score += club_goal_ratio      * W_CLUB_GOAL_RATIO
    score += international_goal_ratio * W_INT_GOAL_RATIO

    # Trophies & Accolades
    score += fifa_world_cup_titles      * W_FIFA_WORLD_CUP_TITLES
    score += continental_titles         * W_CONTINENTAL_TITLES
    score += league_titles              * W_LEAGUE_TITLES
    score += champions_league_titles    * W_CHAMPIONS_LEAGUE_TITLES
    score += domestic_cup_titles        * W_DOMESTIC_CUP_TITLES
    score += major_individual_awards    * W_MAJOR_INDIVIDUAL_AWARDS
    score += ballon_dor_wins            * W_BALLON_DOR_WINDS

    # Additional Performance
    score += hat_tricks                  * W_HAT_TRICKS
    score += penalty_goals               * W_PENALTY_GOALS
    score += free_kick_goals             * W_FREE_KICK_GOALS
    score += red_cards                   * W_RED_CARDS
    score += yellow_cards                * W_YELLOW_CARDS
    score += man_of_the_match_awards     * W_MAN_OF_THE_MATCH_AWARDS
    score += captaincy_appearances       * W_CAPTAINCY_APPEARANCES

    # Creative / Advanced Metrics
    score += key_passes_per_game         * W_KEY_PASSES_PER_GAME
    score += dribbles_completed_per_game * W_DRIBBLES_COMPLETED_PER_GAME
    score += big_chances_created         * W_BIG_CHANCES_CREATED
    score += pass_accuracy_percent       * W_PASS_ACCURACY_PERCENT

    # Defensive / Goalkeeper Stats
    score += clean_sheets                * W_CLEAN_SHEETS
    score += tackles_won_per_game        * W_TACKLES_WON_PER_GAME
    score += interceptions_per_game      * W_INTERCEPTIONS_PER_GAME
    score += saves_per_game              * W_SAVES_PER_GAME

    # Doping & Injuries
    score += doping_tests_passed         * W_DOPING_TESTS_PASSED
    score += doping_tests_failed         * W_DOPING_TESTS_FAILED
    score += major_injuries_count        * W_MAJOR_INJURIES_COUNT

    # Hall of Fame & Earnings
    if hall_of_fame_inducted == 1:
        score += W_HALL_OF_FAME_INDUCTED
    score += career_earnings_million_usd * W_CAREER_EARNINGS_MILLION_USD
    score += total_trophies_won          * W_TOTAL_TROPHIES_WON

    return score

def main():
    # 1) Load the dataset
    df = pd.read_csv("mens_soccer_dataset.csv")

    # 2) Calculate the Soccer Index Score for each player
    df["soccer_index"] = df.apply(calc_soccer_index, axis=1)

    # 3) Sort players by that score, descending
    df = df.sort_values(by="soccer_index", ascending=False).reset_index(drop=True)

    # 4) Print the ranking
    print("\n====== MEN'S SOCCER INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player_name = row['player_name']
        idx_score = row['soccer_index']
        print(f"{rank}. {player_name} - Index: {idx_score:.1f}")

    # 5) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='soccer_index')

    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("mens_soccer_index_scored.csv", index=False)

    # 7) Create a line plot of the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title="Top 10 Men's Soccer Players by Normalized Index",
        save_path='mens_soccer_index_plot.png'
    )

    print("\nResults saved to 'mens_soccer_index_scored.csv'.")
    print("Line plot saved as 'mens_soccer_index_plot.png'.")

if __name__ == "__main__":
    main()
