import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_volleyball_index(row):
    """
    Calculates a single 'Volleyball Index Score' for each player by combining
    multiple volleyball-specific stats with assigned weights.

    The weights are assigned based on the importance of each statistic in evaluating
    a player's overall contribution to the game. Higher weights are given to more
    impactful and prestigious achievements.

    Adjust multipliers to reflect the importance of each metric in volleyball.
    Negative weights are used for detrimental stats like serve errors.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Major Accolades
    W_TOTAL_MEDALS_WON          = 25.0  # Reflects overall success
    W_WORLD_CHAMPIONSHIP_TITLES = 30.0  # Highly prestigious
    W_OLYMPIC_MEDALS            = 35.0  # Most prestigious

    # Awards & Honors
    W_BEST_PLAYER_AWARDS        = 20.0
    W_MVP_AWARDS                = 25.0
    W_BEST_SPIKER_AWARDS        = 15.0
    W_BEST_SERVER_AWARDS        = 15.0
    W_BEST_BLOCKER_AWARDS       = 15.0
    W_BEST_DIGGER_AWARDS         = 10.0
    W_BEST_SETTER_AWARDS         = 10.0

    # Basic Career Metrics
    W_YEARS_ACTIVE              = 1.0
    W_INTERNATIONAL_MATCHES_PLAYED = 0.5
    W_CLUB_MATCHES_PLAYED         = 0.3

    # Offensive Stats
    W_INTERNATIONAL_GOALS_SCORED  = 2.0
    W_INTERNATIONAL_ASSISTS        = 1.5
    W_CLUB_KILLS                   = 1.0
    W_CLUB_ATTACKS                 = 0.8
    W_INTERNATIONAL_SERVES_ACES    = 1.5
    W_CLUB_SERVES_ACES             = 1.0
    W_INTERNATIONAL_SERVES_ERRORS  = -2.0  # Negative weight
    W_CLUB_SERVES_ERRORS           = -1.0  # Negative weight
    W_INTERNATIONAL_ATTACK_PERCENTAGE = 1.5
    W_CLUB_ATTACK_PERCENTAGE         = 1.0

    # Defensive Stats
    W_INTERNATIONAL_BLOCKS         = 2.0
    W_INTERNATIONAL_DIGS           = 1.5
    W_CLUB_BLOCKS                  = 1.0
    W_CLUB_DIGS                    = 0.8

    # Advanced Metrics
    W_KILL_SUCCESS_RATE            = 2.0
    W_SERVE_EFFICIENCY             = 1.5
    W_BLOCK_SUCCESS_RATE           = 1.5
    W_DIG_SUCCESS_RATE             = 1.5
    W_RECEPTION_ACCURACY_PERCENT   = 1.0
    W_ATTACK_EFFICIENCY            = 1.5
    W_SERVE_RECEIVE_EFFICIENCY     = 1.0

    # Financials & Trophies
    W_CAREER_EARNINGS              = 0.05
    W_TOTAL_TROPHIES_WON           = 20.0

    # ------------------- EXTRACT FROM ROW ---------------------
    # Major Accolades
    total_medals_won           = row["total_medals_won"]
    world_championship_titles  = row["world_championship_titles"]
    olympic_medals             = row["olympic_medals"]

    # Awards & Honors
    best_player_awards         = row["best_player_awards"]
    mvp_awards                 = row["mvp_awards"]
    best_spiker_awards         = row["best_spiker_awards"]
    best_server_awards         = row["best_server_awards"]
    best_blocker_awards        = row["best_blocker_awards"]
    best_digger_awards          = row["best_digger_awards"]
    best_setter_awards          = row["best_setter_awards"]

    # Basic Career Metrics
    years_active               = row["years_active"]
    international_matches_played = row["international_matches_played"]
    club_matches_played          = row["club_matches_played"]

    # Offensive Stats
    international_goals_scored   = row["international_goals_scored"]
    international_assists         = row["international_assists"]
    club_kills                    = row["club_kills"]
    club_attacks                  = row["club_attacks"]
    international_serves_aces     = row["international_serves_aces"]
    club_serves_aces              = row["club_serves_aces"]
    international_serves_errors   = row["international_serves_errors"]
    club_serves_errors            = row["club_serves_errors"]
    international_attack_percentage = row["international_attack_percentage"]
    club_attack_percentage         = row["club_attack_percentage"]

    # Defensive Stats
    international_blocks          = row["international_blocks"]
    international_digs            = row["international_digs"]
    club_blocks                   = row["club_blocks"]
    club_digs                     = row["club_digs"]

    # Advanced Metrics
    kill_success_rate             = row["kill_success_rate"]
    serve_efficiency              = row["serve_efficiency"]
    block_success_rate            = row["block_success_rate"]
    dig_success_rate              = row["dig_success_rate"]
    reception_accuracy_percent    = row["reception_accuracy_percent"]
    attack_efficiency             = row["attack_efficiency"]
    serve_receive_efficiency      = row["serve_receive_efficiency"]

    # Financials & Trophies
    career_earnings_million_usd   = row["career_earnings_million_usd"]
    total_trophies_won            = row["total_trophies_won"]

    # ------------------- CALCULATE SCORE ---------------------
    score = 0.0

    # Major Accolades
    score += total_medals_won           * W_TOTAL_MEDALS_WON
    score += world_championship_titles  * W_WORLD_CHAMPIONSHIP_TITLES
    score += olympic_medals             * W_OLYMPIC_MEDALS

    # Awards & Honors
    score += best_player_awards         * W_BEST_PLAYER_AWARDS
    score += mvp_awards                 * W_MVP_AWARDS
    score += best_spiker_awards         * W_BEST_SPIKER_AWARDS
    score += best_server_awards         * W_BEST_SERVER_AWARDS
    score += best_blocker_awards        * W_BEST_BLOCKER_AWARDS
    score += best_digger_awards          * W_BEST_DIGGER_AWARDS
    score += best_setter_awards          * W_BEST_SETTER_AWARDS

    # Basic Career Metrics
    score += years_active               * W_YEARS_ACTIVE
    score += international_matches_played * W_INTERNATIONAL_MATCHES_PLAYED
    score += club_matches_played          * W_CLUB_MATCHES_PLAYED

    # Offensive Stats
    score += international_goals_scored   * W_INTERNATIONAL_GOALS_SCORED
    score += international_assists         * W_INTERNATIONAL_ASSISTS
    score += club_kills                    * W_CLUB_KILLS
    score += club_attacks                  * W_CLUB_ATTACKS
    score += international_serves_aces     * W_INTERNATIONAL_SERVES_ACES
    score += club_serves_aces              * W_CLUB_SERVES_ACES
    score += international_serves_errors   * W_INTERNATIONAL_SERVES_ERRORS
    score += club_serves_errors            * W_CLUB_SERVES_ERRORS
    score += international_attack_percentage * W_INTERNATIONAL_ATTACK_PERCENTAGE
    score += club_attack_percentage         * W_CLUB_ATTACK_PERCENTAGE

    # Defensive Stats
    score += international_blocks          * W_INTERNATIONAL_BLOCKS
    score += international_digs            * W_INTERNATIONAL_DIGS
    score += club_blocks                   * W_CLUB_BLOCKS
    score += club_digs                     * W_CLUB_DIGS

    # Advanced Metrics
    score += kill_success_rate             * W_KILL_SUCCESS_RATE
    score += serve_efficiency              * W_SERVE_EFFICIENCY
    score += block_success_rate            * W_BLOCK_SUCCESS_RATE
    score += dig_success_rate              * W_DIG_SUCCESS_RATE
    score += reception_accuracy_percent    * W_RECEPTION_ACCURACY_PERCENT
    score += attack_efficiency             * W_ATTACK_EFFICIENCY
    score += serve_receive_efficiency      * W_SERVE_RECEIVE_EFFICIENCY

    # Financials & Trophies
    score += career_earnings_million_usd   * W_CAREER_EARNINGS
    score += total_trophies_won            * W_TOTAL_TROPHIES_WON

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("volleyball_dataset.csv")
    
    # 2) Ensure all necessary columns are present
    required_columns = [
        "player_name",
        "gender",
        "position",
        "years_active",
        "national_team",
        "club_team",
        "international_matches_played",
        "international_matches_won",
        "international_matches_lost",
        "international_matches_drawn",
        "international_goals_scored",
        "international_assists",
        "international_blocks",
        "international_digs",
        "international_serves_aces",
        "international_serves_errors",
        "international_attack_percentage",
        "club_matches_played",
        "club_matches_won",
        "club_matches_lost",
        "club_matches_drawn",
        "club_kills",
        "club_attacks",
        "club_blocks",
        "club_digs",
        "club_serves_aces",
        "club_serves_errors",
        "club_attack_percentage",
        "total_medals_won",
        "world_championship_titles",
        "olympic_medals",
        "best_player_awards",
        "mvp_awards",
        "best_spiker_awards",
        "best_server_awards",
        "best_blocker_awards",
        "best_digger_awards",
        "best_setter_awards",
        "hall_of_fame_inducted",
        "career_earnings_million_usd",
        "total_trophies_won",
        "kill_success_rate",
        "serve_efficiency",
        "block_success_rate",
        "dig_success_rate",
        "reception_accuracy_percent",
        "attack_efficiency",
        "serve_receive_efficiency",
        "overall_performance_score",
    ]

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        print(f"Missing columns in the dataset: {missing_columns}")
        # Optionally, fill missing columns with 0
        for col in missing_columns:
            df[col] = 0

    # 3) Calculate the Volleyball Index Score for each player
    df["volleyball_index"] = df.apply(calc_volleyball_index, axis=1)

    # 4) Sort players by that score, descending
    df_sorted = df.sort_values(by="volleyball_index", ascending=False).reset_index(drop=True)

    # 5) Print the ranking
    print("\n====== VOLLEYBALL INDEX RANKING (TOP 30) ======")
    for i, row in df_sorted.iterrows():
        rank = i + 1
        player_name = row['player_name']
        index_score = row['volleyball_index']
        print(f"{rank}. {player_name} - Index: {index_score:.1f}")

    # 6) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df_sorted, name_col='player_name', index_col='volleyball_index')

    # 7) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("volleyball_index_scored.csv", index=False)

    # 8) Create a line plot of the top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title="Top 10 Volleyball Players by Normalized Index",
        save_path='volleyball_index_plot.png'
    )

    print("\nResults saved to 'volleyball_index_scored.csv'.")
    print("Line plot saved as 'volleyball_index_plot.png'.")

if __name__ == "__main__":
    main()
