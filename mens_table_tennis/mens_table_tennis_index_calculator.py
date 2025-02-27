import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_table_tennis_index(row):
    """
    Calculates a single 'Table Tennis Index Score' for each player by combining
    multiple table tennis-specific stats with assigned weights.

    The weights are assigned based on the importance of each statistic in evaluating
    a player's overall contribution to the sport. Higher weights are given to more
    impactful and prestigious achievements.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Major Accolades
    W_OLYMPIC_MEDALS               = 35.0  # Most prestigious
    W_WORLD_CHAMPIONSHIPS          = 30.0  # Highly prestigious
    W_WORLD_CUP_TITLES             = 25.0
    W_ASIAN_GAMES_MEDALS           = 20.0  # Significant regional achievement
    W_BWF_WORLD_SERIES_TITLES      = 15.0  # Major tournament wins
    W_BWF_GRAND_SLAM_TITLES        = 20.0
    W_BWF_OLYMPIC_TITLES           = 25.0
    W_BWF_SUPER_SERIES_TITLES      = 15.0
    W_BWF_WORLD_SUPERSERIES_CHAMPIONSHIPS = 20.0
    W_BWF_WORLD_SERIES_TITLES      = 10.0

    # Awards & Honors
    W_BEST_PLAYER_AWARDS            = 20.0
    W_MVP_AWARDS                    = 25.0
    W_MOST_IMPROVED_PLAYER_AWARDS   = 10.0
    W_SPORTSMANSHIP_AWARDS          = 10.0
    W_HALL_OF_FAME_INDUCTED         = 30.0

    # Career Metrics
    W_YEARS_ACTIVE                  = 1.0
    W_HIGHEST_WORLD_RANKING         = 15.0
    W_WORLD_RANKING_HISTORY         = 10.0
    W_INTERNATIONAL_MATCHES_PLAYED  = 0.5
    W_INTERNATIONAL_MATCHES_WON     = 0.5
    W_INTERNATIONAL_TITLES_WON      = 2.0
    W_INTERNATIONAL_TITLE_PERCENTAGE = 2.0

    # Performance Stats
    W_TOTAL_POINTS_SCORED           = 0.002  # Fans value scoring ability
    W_TOTAL_SERVES                  = 0.003
    W_TOTAL_VOLLEYS                 = 0.002
    W_TOTAL_SMASHES                 = 0.003
    W_TOTAL_DROPSHOTS               = 0.002
    W_TOTAL_DEFENSIVE_BLOCKS        = 0.005
    W_TOTAL_OFFENSIVE_BLOCKS        = 0.004
    W_SERVE_ACCURACY_PERCENT        = 0.5
    W_RETURN_ACCURACY_PERCENT       = 0.5
    W_SMASH_SUCCESS_RATE            = 1.0
    W_DROPSHOT_SUCCESS_RATE         = 0.8
    W_VOLLEYS_SUCCESS_RATE          = 0.7
    W_OVERALL_EFFICIENCY            = 1.0
    W_OFFENSIVE_EFFICIENCY          = 1.0
    W_DEFENSIVE_EFFICIENCY          = 0.8
    W_REACTION_TIME_MS              = -0.05  # Faster reaction time is better
    W_SERVE_RECEIVE_EFFICIENCY      = 0.5

    # Financials & Trophies
    W_CAREER_EARNINGS               = 0.05
    W_TOTAL_TROPHIES_WON            = 20.0

    # ------------------- EXTRACT FROM ROW ---------------------
    # Major Accolades
    olympic_medals                  = row["olympic_medals"]
    world_championship_titles       = row["world_championship_titles"]
    world_cup_titles                = row["world_cup_titles"]
    asian_games_medals              = row["asian_games_medals"]
    bwf_world_series_titles         = row["bwf_world_series_titles"]
    bwf_grand_slam_titles           = row["bwf_grand_slam_titles"]
    bwf_olympic_titles              = row["bwf_olympic_titles"]
    bwf_super_series_titles         = row["bwf_super_series_titles"]
    bwf_world_superseries_championships = row["bwf_world_superseries_championships"]
    bwf_world_series_titles         = row["bwf_world_series_titles"]

    # Awards & Honors
    best_player_awards              = row["best_player_awards"]
    mvp_awards                      = row["mvp_awards"]
    most_improved_player_awards     = row["most_improved_player_awards"]
    sportsmanship_awards            = row["sportsmanship_awards"]
    hall_of_fame_inducted           = row["hall_of_fame_inducted"]

    # Career Metrics
    years_active                    = row["years_active"]
    highest_world_ranking           = row["highest_world_ranking"]
    world_ranking_history           = row["world_ranking_history"]
    international_matches_played    = row["international_matches_played"]
    international_matches_won       = row["international_matches_won"]
    international_titles_won        = row["international_titles_won"]
    international_title_percentage  = row["international_title_percentage"]

    # Performance Stats
    total_points_scored             = row["total_points_scored"]
    total_serves                    = row["total_serves"]
    total_volleys                   = row["total_volleys"]
    total_smashes                   = row["total_smashes"]
    total_dropshots                 = row["total_dropshots"]
    total_defensive_blocks          = row["total_defensive_blocks"]
    total_offensive_blocks          = row["total_offensive_blocks"]
    serve_accuracy_percent          = row["serve_accuracy_percent"]
    return_accuracy_percent         = row["return_accuracy_percent"]
    smash_success_rate              = row["smash_success_rate"]
    dropshot_success_rate           = row["dropshot_success_rate"]
    volleys_success_rate            = row["volleys_success_rate"]
    overall_efficiency              = row["overall_efficiency"]
    offensive_efficiency            = row["offensive_efficiency"]
    defensive_efficiency            = row["defensive_efficiency"]
    reaction_time_ms                = row["reaction_time_ms"]
    serve_receive_efficiency        = row["serve_receive_efficiency"]

    # Financials & Trophies
    career_earnings_million_usd       = row["career_earnings_million_usd"]
    total_trophies_won                = row["total_trophies_won"]

    # ------------------- CALCULATE SCORE ---------------------
    score = 0.0

    # Major Accolades
    score += olympic_medals                     * W_OLYMPIC_MEDALS
    score += world_championship_titles          * W_WORLD_CHAMPIONSHIPS
    score += world_cup_titles                   * W_WORLD_CUP_TITLES
    score += asian_games_medals                 * W_ASIAN_GAMES_MEDALS
    score += bwf_world_series_titles            * W_BWF_WORLD_SERIES_TITLES
    score += bwf_grand_slam_titles              * W_BWF_GRAND_SLAM_TITLES
    score += bwf_olympic_titles                 * W_BWF_OLYMPIC_TITLES
    score += bwf_super_series_titles            * W_BWF_SUPER_SERIES_TITLES
    score += bwf_world_superseries_championships * W_BWF_WORLD_SUPERSERIES_CHAMPIONSHIPS
    score += bwf_world_series_titles            * W_BWF_WORLD_SERIES_TITLES

    # Awards & Honors
    score += best_player_awards                 * W_BEST_PLAYER_AWARDS
    score += mvp_awards                         * W_MVP_AWARDS
    score += most_improved_player_awards        * W_MOST_IMPROVED_PLAYER_AWARDS
    score += sportsmanship_awards               * W_SPORTSMANSHIP_AWARDS
    score += hall_of_fame_inducted              * W_HALL_OF_FAME_INDUCTED

    # Career Metrics
    score += years_active                       * W_YEARS_ACTIVE
    score += highest_world_ranking              * W_HIGHEST_WORLD_RANKING
    score += world_ranking_history              * W_WORLD_RANKING_HISTORY
    score += international_matches_played       * W_INTERNATIONAL_MATCHES_PLAYED
    score += international_matches_won           * W_INTERNATIONAL_MATCHES_WON
    score += international_titles_won            * W_INTERNATIONAL_TITLES_WON
    score += international_title_percentage      * W_INTERNATIONAL_TITLE_PERCENTAGE

    # Performance Stats
    score += total_points_scored                 * W_TOTAL_POINTS_SCORED
    score += total_serves                        * W_TOTAL_SERVES
    score += total_volleys                       * W_TOTAL_VOLLEYS
    score += total_smashes                       * W_TOTAL_SMASHES
    score += total_dropshots                     * W_TOTAL_DROPSHOTS
    score += total_defensive_blocks              * W_TOTAL_DEFENSIVE_BLOCKS
    score += total_offensive_blocks              * W_TOTAL_OFFENSIVE_BLOCKS
    score += serve_accuracy_percent              * W_SERVE_ACCURACY_PERCENT
    score += return_accuracy_percent             * W_RETURN_ACCURACY_PERCENT
    score += smash_success_rate                  * W_SMASH_SUCCESS_RATE
    score += dropshot_success_rate               * W_DROPSHOT_SUCCESS_RATE
    score += volleys_success_rate                * W_VOLLEYS_SUCCESS_RATE
    score += overall_efficiency                  * W_OVERALL_EFFICIENCY
    score += offensive_efficiency                * W_OFFENSIVE_EFFICIENCY
    score += defensive_efficiency                * W_DEFENSIVE_EFFICIENCY
    score += reaction_time_ms                    * W_REACTION_TIME_MS
    score += serve_receive_efficiency            * W_SERVE_RECEIVE_EFFICIENCY

    # Financials & Trophies
    score += career_earnings_million_usd         * W_CAREER_EARNINGS
    score += total_trophies_won                  * W_TOTAL_TROPHIES_WON

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("mens_table_tennis_dataset.csv")

    # 2) Ensure all necessary columns are present
    required_columns = [
        "player_name",
        "country",
        "handedness",
        "playing_style",
        "years_active",
        "highest_world_ranking",
        "world_ranking_history",
        "international_matches_played",
        "international_matches_won",
        "international_matches_lost",
        "international_titles_won",
        "international_title_percentage",
        "olympic_medals",
        "world_championship_titles",
        "world_cup_titles",
        "asian_games_medals",
        "bwf_world_series_titles",
        "bwf_grand_slam_titles",
        "bwf_olympic_titles",
        "bwf_super_series_titles",
        "bwf_world_superseries_championships",
        "bwf_world_series_titles",
        "total_points_scored",
        "total_serves",
        "total_volleys",
        "total_smashes",
        "total_dropshots",
        "total_defensive_blocks",
        "total_offensive_blocks",
        "serve_accuracy_percent",
        "return_accuracy_percent",
        "smash_success_rate",
        "dropshot_success_rate",
        "volleys_success_rate",
        "overall_efficiency",
        "offensive_efficiency",
        "defensive_efficiency",
        "reaction_time_ms",
        "serve_receive_efficiency",
        "career_earnings_million_usd",
        "total_trophies_won",
        "best_player_awards",
        "mvp_awards",
        "most_improved_player_awards",
        "sportsmanship_awards",
        "hall_of_fame_inducted",
        "coach_achievements",
        "overall_performance_score",
    ]

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        print(f"Missing columns in the dataset: {missing_columns}")
        # Optionally, fill missing columns with 0
        for col in missing_columns:
            df[col] = 0

    # 3) Calculate the Table Tennis Index Score for each player
    df["table_tennis_index"] = df.apply(calc_table_tennis_index, axis=1)

    # 4) Sort players by that score, descending
    df_sorted = df.sort_values(by="table_tennis_index", ascending=False).reset_index(drop=True)

    # 5) Print the ranking
    print("\n====== MEN'S TABLE TENNIS INDEX RANKING (TOP 30) ======")
    for i, row in df_sorted.iterrows():
        rank = i + 1
        player_name = row['player_name']
        index_score = row['table_tennis_index']
        print(f"{rank}. {player_name} - Index: {index_score:.1f}")

    # 6) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df_sorted, name_col='player_name', index_col='table_tennis_index')

    # 7) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("mens_table_tennis_index_scored.csv", index=False)

    # 8) Create a line plot of the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title="Top 10 Men's Table Tennis Players by Normalized Index",
        save_path='mens_table_tennis_index_plot.png'
    )

    print("\nResults saved to 'mens_table_tennis_index_scored.csv'.")
    print("Line plot saved as 'mens_table_tennis_index_plot.png'.")


if __name__ == "__main__":
    main()
