import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_american_football_index(row):
    """
    Calculates a single 'American Football Index Score' for each player by combining
    multiple American football-specific stats with assigned weights.

    The weights are assigned based on the importance of each statistic in evaluating
    a player's overall contribution to the game. Higher weights are given to more
    impactful and prestigious achievements.

    Adjust multipliers to reflect the importance of each metric in American football.
    Negative weights are used for detrimental stats like turnovers or failed field goals.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Career Performance Metrics
    W_GAMES_PLAYED           = 5.0    # Base value for longevity
    W_GAMES_STARTED          = 1.5    # Slightly more for being the starter
    W_WINS                   = 8.0    # Significantly increased - Brady has most wins
    W_LOSSES                 = -4.0   # Adjusted accordingly
    W_TIES                   = 0.0    # Reduced importance

    # Passing Stats (Primarily for Quarterbacks) - Heavily increased
    W_PASSING_COMPLETIONS    = 1.0    # Increased
    W_PASSING_ATTEMPTS       = -0.01   # Reduced penalty
    W_PASSING_YARDS          = 0.15   # Tripled importance
    W_PASSING_TOUCHDOWNS     = 8.0    # Significantly increased
    W_PASSING_INTERCEPTS     = -4.0   # Increased penalty
    W_PASSING_RATING         = 3.0    # Same as above

    # Rushing Stats (Less important for pocket QBs)
    W_RUSHING_ATTEMPTS       = 0.001
    W_RUSHING_YARDS          = 0.001
    W_RUSHING_TOUCHDOWNS     = 0.1
    W_RUSHING_LONGEST_RUN    = 0.02

    # Receiving Stats (Not relevant for QBs)
    W_RECEPTIONS             = 0.0
    W_RECEIVING_YARDS        = 0.0
    W_RECEIVING_TOUCHDOWNS   = 0.0
    W_RECEIVING_LONGEST_REC  = 0.0

    # Defensive Stats (Not relevant for QBs)
    W_TACKLES                = 0.0
    W_SACKS                  = 0.0
    W_FORCED_FUMBLES         = 0.0
    W_FUMBLE_RECOVERIES      = 0.0
    W_INTERCEPTIONS_DEF      = 0.0
    W_PASS_DEFLECTIONS       = 0.0

    # Kicking Stats (Not relevant for QBs)
    W_FIELD_GOALS_MADE       = 0.0
    W_FIELD_GOALS_ATTEMPTED  = 0.0
    W_FIELD_GOAL_PERCENTAGE  = 0.0
    W_LONGEST_FIELD_GOAL     = 0.0
    W_EXTRA_POINTS_MADE      = 0.0
    W_EXTRA_POINTS_ATTEMPTED = 0.0

    # Special Teams Stats (Not relevant for QBs)
    W_PUNT_RETURNS           = 0.0
    W_PUNT_RETURN_YARDS      = 0.0
    W_PUNT_RETURN_TOUCHDOWNS = 0.0
    W_KICK_RETURNS           = 0.0
    W_KICK_RETURN_YARDS      = 0.0
    W_KICK_RETURN_TOUCHDOWNS = 0.0

    # Awards & Honors - Heavily weighted toward championships
    W_PRO_BOWLS              = 2.0    # Reduced further
    W_ALL_PRO_SELECTIONS     = 5.0    # Still meaningful but not dominant
    W_MVP_AWARDS             = 12.0   # Reduced - Brady has 3, Manning has 5
    W_SUPER_BOWL_TITLES      = 75.0   # Massive increase - Brady's 7 rings should dominate
    W_SUPER_BOWL_APPEARANCES = 25.0   # Added to reward 10 SB appearances
    W_HALL_OF_FAME           = 0   # Increased

    # Advanced Metrics - Reduced to minimize era advantages
    W_QUARTERBACK_RATING     = 3.0    # Reduced to not favor modern QBs as much
    W_YARDS_PER_ATTEMPT     = 1.5    # Less emphasis on per-play metrics
    W_YARDS_PER_CARRY        = 0.0    # Not relevant
    W_YARDS_PER_RECEPTION    = 0.0    # Not relevant

    # Financials & Trophies
    W_CAREER_EARNINGS        = 0.2    # Slightly increased
    W_TOTAL_TROPHIES_WON     = 5.0    # Increased

    # Detrimental Stats
    W_TURNOVERS              = -5.0   # Increased penalty
    W_FAILED_FIELD_GOALS     = 0.0    # Not relevant

    # ------------------- EXTRACT FROM ROW ---------------------
    # Career Performance Metrics
    games_played             = row["games_played"]
    games_started            = row["games_started"]
    wins                     = row["wins"]
    losses                   = row["losses"]
    ties                     = row["ties"]

    # Passing Stats
    passing_completions      = row["passing_completions"]
    passing_attempts         = row["passing_attempts"]
    passing_yards            = row["passing_yards"]
    passing_touchdowns       = row["passing_touchdowns"]
    passing_interceptions    = row["passing_interceptions"]
    passing_rating            = row["passing_rating"]

    # Rushing Stats
    rushing_attempts         = row["rushing_attempts"]
    rushing_yards            = row["rushing_yards"]
    rushing_touchdowns       = row["rushing_touchdowns"]
    rushing_longest_run      = row["rushing_longest_run"]

    # Receiving Stats
    receptions               = row["receptions"]
    receiving_yards          = row["receiving_yards"]
    receiving_touchdowns     = row["receiving_touchdowns"]
    receiving_longest_rec    = row["receiving_longest_reception"]

    # Defensive Stats
    tackles                  = row["tackles"]
    sacks                    = row["sacks"]
    forced_fumbles           = row["forced_fumbles"]
    fumble_recoveries        = row["fumble_recoveries"]
    interceptions_def        = row["interceptions_defense"]
    pass_deflections         = row["pass_deflections"]

    # Kicking Stats
    field_goals_made         = row["field_goals_made"]
    field_goals_attempted    = row["field_goals_attempted"]
    field_goal_percentage    = row["field_goal_percentage"]
    longest_field_goal       = row["longest_field_goal"]
    extra_points_made        = row["extra_points_made"]
    extra_points_attempted   = row["extra_points_attempted"]

    # Special Teams Stats
    punt_returns             = row["punt_returns"]
    punt_return_yards        = row["punt_return_yards"]
    punt_return_touchdowns   = row["punt_return_touchdowns"]
    kick_returns             = row["kick_returns"]
    kick_return_yards        = row["kick_return_yards"]
    kick_return_touchdowns   = row["kick_return_touchdowns"]

    # Awards & Honors
    pro_bowls                = row["pro_bowls"]
    all_pro_selections       = row["all_pro_selections"]
    mvp_awards               = row["mvp_awards"]
    super_bowl_titles        = row["super_bowl_titles"]
    super_bowl_appearances   = row["super_bowl_appearances"]
    hall_of_fame             = row["hall_of_fame_inducted"]

    # Advanced Metrics
    quarterback_rating       = row["quarterback_rating"]
    yards_per_attempt        = row["yards_per_attempt"]
    yards_per_carry          = row["yards_per_carry"]
    yards_per_reception      = row["yards_per_reception"]

    # Financials & Trophies
    career_earnings          = row["career_earnings_million_usd"]
    total_trophies_won       = row["total_trophies_won"]

    # Detrimental Stats
    turnovers                = row["turnovers"] if "turnovers" in row else 0
    failed_field_goals       = row["failed_field_goals"] if "failed_field_goals" in row else 0

    # ------------------- CALCULATE SCORE ---------------------
    score = 0.0

    # Career Performance Metrics
    score += games_played         * W_GAMES_PLAYED
    score += games_started        * W_GAMES_STARTED
    score += wins                 * W_WINS
    score += losses               * W_LOSSES
    score += ties                 * W_TIES

    # Passing Stats
    score += passing_completions  * W_PASSING_COMPLETIONS
    score += passing_attempts     * W_PASSING_ATTEMPTS
    score += passing_yards        * W_PASSING_YARDS
    score += passing_touchdowns   * W_PASSING_TOUCHDOWNS
    score += passing_interceptions* W_PASSING_INTERCEPTS
    score += passing_rating       * W_PASSING_RATING

    # Rushing Stats
    score += rushing_attempts     * W_RUSHING_ATTEMPTS
    score += rushing_yards        * W_RUSHING_YARDS
    score += rushing_touchdowns   * W_RUSHING_TOUCHDOWNS
    score += rushing_longest_run  * W_RUSHING_LONGEST_RUN

    # Receiving Stats
    score += receptions           * W_RECEPTIONS
    score += receiving_yards      * W_RECEIVING_YARDS
    score += receiving_touchdowns * W_RECEIVING_TOUCHDOWNS
    score += receiving_longest_rec* W_RECEIVING_LONGEST_REC

    # Defensive Stats
    score += tackles              * W_TACKLES
    score += sacks                * W_SACKS
    score += forced_fumbles       * W_FORCED_FUMBLES
    score += fumble_recoveries    * W_FUMBLE_RECOVERIES
    score += interceptions_def    * W_INTERCEPTIONS_DEF
    score += pass_deflections     * W_PASS_DEFLECTIONS

    # Kicking Stats
    score += field_goals_made     * W_FIELD_GOALS_MADE
    score += field_goals_attempted* W_FIELD_GOALS_ATTEMPTED
    score += field_goal_percentage* W_FIELD_GOAL_PERCENTAGE
    score += longest_field_goal   * W_LONGEST_FIELD_GOAL
    score += extra_points_made    * W_EXTRA_POINTS_MADE
    score += extra_points_attempted* W_EXTRA_POINTS_ATTEMPTED

    # Special Teams Stats
    score += punt_returns         * W_PUNT_RETURNS
    score += punt_return_yards    * W_PUNT_RETURN_YARDS
    score += punt_return_touchdowns* W_PUNT_RETURN_TOUCHDOWNS
    score += kick_returns         * W_KICK_RETURNS
    score += kick_return_yards    * W_KICK_RETURN_YARDS
    score += kick_return_touchdowns* W_KICK_RETURN_TOUCHDOWNS

    # Awards & Honors
    score += pro_bowls            * W_PRO_BOWLS
    score += all_pro_selections   * W_ALL_PRO_SELECTIONS
    score += mvp_awards           * W_MVP_AWARDS
    score += super_bowl_titles    * W_SUPER_BOWL_TITLES
    score += super_bowl_appearances* W_SUPER_BOWL_APPEARANCES
    if hall_of_fame == 1:
        score += W_HALL_OF_FAME

    # Advanced Metrics
    score += quarterback_rating   * W_QUARTERBACK_RATING
    score += yards_per_attempt    * W_YARDS_PER_ATTEMPT
    score += yards_per_carry      * W_YARDS_PER_CARRY
    score += yards_per_reception  * W_YARDS_PER_RECEPTION

    # Financials & Trophies
    score += career_earnings      * W_CAREER_EARNINGS
    score += total_trophies_won   * W_TOTAL_TROPHIES_WON

    # Detrimental Stats
    score += turnovers            * W_TURNOVERS
    score += failed_field_goals   * W_FAILED_FIELD_GOALS

    return score

def main():
    # 1) Load the dataset
    df = pd.read_csv("american_football_dataset.csv")

    # Ensure that all necessary columns are present
    required_columns = [
        "player_name", "position", "years_active", "teams_played_for",
        "games_played", "games_started", "wins", "losses", "ties",
        "passing_completions", "passing_attempts", "passing_yards",
        "passing_touchdowns", "passing_interceptions", "passing_rating",
        "rushing_attempts", "rushing_yards", "rushing_touchdowns",
        "rushing_longest_run", "receptions", "receiving_yards",
        "receiving_touchdowns", "receiving_longest_reception",
        "tackles", "sacks", "forced_fumbles", "fumble_recoveries",
        "interceptions_defense", "pass_deflections",
        "field_goals_made", "field_goals_attempted",
        "field_goal_percentage", "longest_field_goal",
        "extra_points_made", "extra_points_attempted",
        "punt_returns", "punt_return_yards", "punt_return_touchdowns",
        "kick_returns", "kick_return_yards", "kick_return_touchdowns",
        "pro_bowls", "all_pro_selections", "mvp_awards",
        "super_bowl_titles", "hall_of_fame_inducted",
        "quarterback_rating", "yards_per_attempt",
        "yards_per_carry", "yards_per_reception",
        "career_earnings_million_usd", "total_trophies_won",
        "super_bowl_appearances",
        "turnovers", "failed_field_goals"  # Ensure these columns exist
    ]

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        print(f"Missing columns in the dataset: {missing_columns}")
        # Optionally, fill missing columns with 0
        for col in missing_columns:
            df[col] = 0

    # 2) Calculate the American Football Index Score for each player
    df["american_football_index"] = df.apply(calc_american_football_index, axis=1)

    # 3) Sort players by that score, descending
    df_sorted = df.sort_values(by="american_football_index", ascending=False).reset_index(drop=True)

    # 4) Print the ranking
    print("\n====== AMERICAN FOOTBALL INDEX RANKING (TOP 30) ======")
    for i, row in df_sorted.iterrows():
        rank = i + 1
        player_name = row['player_name']
        index_score = row['american_football_index']
        print(f"{rank}. {player_name} - Index: {index_score:.1f}")

    # 5) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df_sorted, name_col='player_name', index_col='american_football_index')

    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("american_football_index_scored.csv", index=False)

    # 7) Create a line plot of the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title="Top 10 American Football Players by Normalized Index",
        save_path='american_football_index_plot.png'
    )

    print("\nResults saved to 'american_football_index_scored.csv'.")
    print("Line plot saved as 'american_football_index_plot.png'.")

if __name__ == "__main__":
    main()
