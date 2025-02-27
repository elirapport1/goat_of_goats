import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_field_hockey_index(row):
    """
    Calculates a single 'Field Hockey Index Score' for each player by combining
    multiple field hockey-specific stats with assigned weights.

    The weights are assigned based on the importance of each statistic in evaluating
    a player's overall contribution to the game. Higher weights are given to more
    impactful and prestigious achievements.

    Adjust multipliers to reflect the importance of each metric in field hockey.
    Negative weights are used for detrimental stats like yellow/red cards.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Basic Career Metrics
    W_YEARS_ACTIVE               = 0.5
    W_TEAMS_PLAYED_FOR           = 1.0
    W_INTERNATIONAL_CAPS         = 0.3
    W_CLUB_CAPS                  = 0.2

    # Offensive Stats
    W_INTERNATIONAL_GOALS        = 2.0
    W_INTERNATIONAL_ASSISTS      = 1.5
    W_CLUB_GOALS                 = 1.0
    W_CLUB_ASSISTS               = 0.8
    W_PENALTY_CORNERS_SCORDED    = 3.0
    W_PENALTY_STROKES_SCORDED    = 2.5
    W_GOALS_FROM_PENALTY_CORNERS = 2.0
    W_GOALS_FROM_PENALTY_STROKES = 1.5
    W_ASSISTS_FROM_PENALTY_CORNERS = 1.2
    W_ASSISTS_FROM_PENALTY_STROKES = 1.0
    W_SHOTS_ON_GOAL              = 0.5
    W_SHOTS_OFF_GOAL             = 0.3
    W_DRIBBLES_COMPLETED         = 0.4
    W_PASS_ACCURACY_PERCENT      = 1.0
    W_BIG_CHANCES_CREATED         = 1.5
    W_BIG_CHANCES_CONVERTED       = 2.0

    # Defensive Stats
    W_DEFENSIVE_BLOCKS           = 1.0
    W_INTERCEPTIONS              = 1.2
    W_TACKLES                     = 1.0
    W_TACKLE_SUCCESS_RATE        = 0.8
    W_CLEARANCES                 = 0.7
    W_BLOCKS                     = 0.9
    W_DEFLECTIONS                = 1.0

    # Discipline
    W_YELLOW_CARDS               = -2.0
    W_RED_CARDS                  = -5.0

    # Awards & Honors
    W_BEST_PLAYER_AWARDS          = 3.0
    W_WORLD_CUP_TITLES            = 5.0
    W_OLYMPIC_MEDALS              = 4.0
    W_HALL_OF_FAME_INDUCTED       = 10.0

    # Advanced Metrics
    W_POSSESSION_TIME_PERCENT     = 1.5
    W_PENALTY_CORNERS_SCORING_EFFICIENCY = 2.0  # penalty_corners_scored / penalty_corners_taken
    W_PENALTY_STROKES_SCORING_EFFICIENCY = 2.5  # penalty_strokes_scored / penalty_strokes_taken
    W_PASS_ACCURACY              = 1.0  # Pass accuracy in percentage
    W_TACKLE_SUCCESS_RATE_METRIC  = 1.0  # Tackle success rate in percentage

    # Financials & Trophies
    W_CAREER_EARNINGS            = 0.05
    W_TOTAL_TROPHIES_WON         = 2.0

    # ------------------- EXTRACT FROM ROW ---------------------
    # Basic Career Metrics
    years_active             = row["years_active"]
    teams_played_for         = row["teams_played_for"]
    international_caps       = row["international_caps"]
    club_caps                = row["club_caps"]

    # Offensive Stats
    international_goals      = row["international_goals"]
    international_assists    = row["international_assists"]
    club_goals               = row["club_goals"]
    club_assists             = row["club_assists"]
    penalty_corners_scored    = row["penalty_corners_scored"]
    penalty_strokes_scored    = row["penalty_strokes_scored"]
    goals_from_penalty_corners = row["goals_from_penalty_corners"]
    goals_from_penalty_strokes = row["goals_from_penalty_strokes"]
    assists_from_penalty_corners = row["assists_from_penalty_corners"]
    assists_from_penalty_strokes = row["assists_from_penalty_strokes"]
    shots_on_goal            = row["shots_on_goal"]
    shots_off_goal           = row["shots_off_goal"]
    dribbles_completed       = row["dribbles_completed"]
    pass_accuracy_percent    = row["pass_accuracy_percent"]
    big_chances_created       = row["big_chances_created"]
    big_chances_converted     = row["big_chances_converted"]

    # Defensive Stats
    defensive_blocks         = row["defensive_blocks"]
    interceptions            = row["interceptions"]
    tackles                   = row["tackles"]
    tackle_success_rate      = row["tackle_success_rate"]
    clearances               = row["clearances"]
    blocks                   = row["blocks"]
    deflections              = row["deflections"]

    # Discipline
    yellow_cards             = row["yellow_cards"]
    red_cards                = row["red_cards"]

    # Awards & Honors
    best_player_awards        = row["best_player_awards"]
    world_cup_titles          = row["world_cup_titles"]
    olympic_medals            = row["olympic_medals"]
    hall_of_fame_inducted     = row["hall_of_fame_inducted"]

    # Advanced Metrics
    possession_time_percent   = row["possession_time_percent"]
    penalty_corners_scoring_efficiency = (row["penalty_corners_scored"] / row["penalty_corners_taken"]) if row["penalty_corners_taken"] > 0 else 0
    penalty_strokes_scoring_efficiency = (row["penalty_strokes_scored"] / row["penalty_strokes_taken"]) if row["penalty_strokes_taken"] > 0 else 0
    pass_accuracy             = row["pass_accuracy_percent"]
    tackle_success_rate_metric = row["tackle_success_rate"]

    # Financials & Trophies
    career_earnings_million_usd = row["career_earnings_million_usd"]
    total_trophies_won         = row["total_trophies_won"]

    # ------------------- CALCULATE SCORE ---------------------
    score = 0.0

    # Basic Career Metrics
    score += years_active              * W_YEARS_ACTIVE
    score += len(teams_played_for.split(',')) * W_TEAMS_PLAYED_FOR  # Assuming teams are comma-separated
    score += international_caps        * W_INTERNATIONAL_CAPS
    score += club_caps                 * W_CLUB_CAPS

    # Offensive Stats
    score += international_goals       * W_INTERNATIONAL_GOALS
    score += international_assists     * W_INTERNATIONAL_ASSISTS
    score += club_goals                * W_CLUB_GOALS
    score += club_assists              * W_CLUB_ASSISTS
    score += penalty_corners_scored     * W_PENALTY_CORNERS_SCORDED
    score += penalty_strokes_scored     * W_PENALTY_STROKES_SCORDED
    score += goals_from_penalty_corners * W_GOALS_FROM_PENALTY_CORNERS
    score += goals_from_penalty_strokes * W_GOALS_FROM_PENALTY_STROKES
    score += assists_from_penalty_corners * W_ASSISTS_FROM_PENALTY_CORNERS
    score += assists_from_penalty_strokes * W_ASSISTS_FROM_PENALTY_STROKES
    score += shots_on_goal             * W_SHOTS_ON_GOAL
    score += shots_off_goal            * W_SHOTS_OFF_GOAL
    score += dribbles_completed        * W_DRIBBLES_COMPLETED
    score += pass_accuracy_percent     * W_PASS_ACCURACY_PERCENT
    score += big_chances_created        * W_BIG_CHANCES_CREATED
    score += big_chances_converted      * W_BIG_CHANCES_CONVERTED

    # Defensive Stats
    score += defensive_blocks          * W_DEFENSIVE_BLOCKS
    score += interceptions             * W_INTERCEPTIONS
    score += tackles                    * W_TACKLES
    score += tackle_success_rate       * W_TACKLE_SUCCESS_RATE
    score += clearances                * W_CLEARANCES
    score += blocks                    * W_BLOCKS
    score += deflections               * W_DEFLECTIONS

    # Discipline
    score += yellow_cards              * W_YELLOW_CARDS
    score += red_cards                 * W_RED_CARDS

    # Awards & Honors
    score += best_player_awards         * W_BEST_PLAYER_AWARDS
    score += world_cup_titles           * W_WORLD_CUP_TITLES
    score += olympic_medals             * W_OLYMPIC_MEDALS
    if hall_of_fame_inducted == 1:
        score += W_HALL_OF_FAME_INDUCTED

    # Advanced Metrics
    score += possession_time_percent    * W_POSSESSION_TIME_PERCENT
    score += penalty_corners_scoring_efficiency * W_PENALTY_CORNERS_SCORING_EFFICIENCY
    score += penalty_strokes_scoring_efficiency * W_PENALTY_STROKES_SCORING_EFFICIENCY
    score += pass_accuracy              * W_PASS_ACCURACY
    score += tackle_success_rate_metric * W_TACKLE_SUCCESS_RATE_METRIC

    # Financials & Trophies
    score += career_earnings_million_usd * W_CAREER_EARNINGS
    score += total_trophies_won          * W_TOTAL_TROPHIES_WON

    return score

def main():
    # 1) Load the dataset
    df = pd.read_csv("field_hockey_dataset.csv")
    
    # 2) Ensure all necessary columns are present
    required_columns = [
        "player_name",
        "position",
        "years_active",
        "teams_played_for",
        "international_caps",
        "international_goals",
        "international_assists",
        "international_yellow_cards",
        "international_red_cards",
        "club_caps",
        "club_goals",
        "club_assists",
        "club_yellow_cards",
        "club_red_cards",
        "penalty_corners_taken",
        "penalty_corners_scored",
        "penalty_strokes_taken",
        "penalty_strokes_scored",
        "goals_from_penalty_corners",
        "goals_from_penalty_strokes",
        "assists_from_penalty_corners",
        "assists_from_penalty_strokes",
        "goals",
        "assists",
        "shots_on_goal",
        "shots_off_goal",
        "dribbles_completed",
        "pass_accuracy_percent",
        "big_chances_created",
        "big_chances_converted",
        "defensive_blocks",
        "interceptions",
        "tackles",
        "tackle_success_rate",
        "clearances",
        "blocks",
        "deflections",
        "faceoffs_won",
        "faceoffs_lost",
        "possession_time_percent",
        "yellow_cards",
        "red_cards",
        "pro_bowls",
        "all_star_selections",
        "best_player_awards",
        "world_cup_titles",
        "olympic_medals",
        "hall_of_fame_inducted",
        "yards_per_attempt",
        "yards_per_carry",
        "yards_per_reception",
        "career_earnings_million_usd",
        "total_trophies_won"
    ]

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        print(f"Missing columns in the dataset: {missing_columns}")
        # Optionally, fill missing columns with 0
        for col in missing_columns:
            df[col] = 0

    # 3) Calculate the Field Hockey Index Score for each player
    df["field_hockey_index"] = df.apply(calc_field_hockey_index, axis=1)

    # 4) Sort players by that score, descending
    df_sorted = df.sort_values(by="field_hockey_index", ascending=False).reset_index(drop=True)

    # 5) Print the ranking
    print("\n====== FIELD HOCKEY INDEX RANKING (TOP 30) ======")
    for i, row in df_sorted.iterrows():
        rank = i + 1
        player_name = row['player_name']
        index_score = row['field_hockey_index']
        print(f"{rank}. {player_name} - Index: {index_score:.1f}")

    # 6) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df_sorted, name_col='player_name', index_col='field_hockey_index')

    # 7) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("field_hockey_index_scored.csv", index=False)

    # 8) Create a line plot of the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title="Top 10 Field Hockey Players by Normalized Index",
        save_path='field_hockey_index_plot.png'
    )

    print("\nResults saved to 'field_hockey_index_scored.csv'.")
    print("Line plot saved as 'field_hockey_index_plot.png'.")

if __name__ == "__main__":
    main()
