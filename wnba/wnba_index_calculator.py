import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_wnba_index(row):
    """
    Calculates a single 'WNBA Index Score' for each player
    by combining multiple stats with weighted importance.
    
    You can adjust these weight constants based on research
    into what WNBA fans value most (scoring, defense, accolades, etc.).
    """
    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Major accolades
    W_CHAMPIONSHIPS       = 25
    W_FINALS_MVP_AWARDS   = 15
    W_MVP_AWARDS          = 25
    W_DPOY_AWARDS         = 10
    W_ALL_WNBA_TEAMS      = 3
    W_ALL_STAR            = 2
    W_SCORING_TITLES      = 5

    # Traditional stats
    W_POINTS   = 0.003
    W_REBOUNDS = 0.002
    W_ASSISTS  = 0.002
    W_STEALS   = 0.01
    W_BLOCKS   = 0.01

    # Negative or mild penalty stats
    W_TOV_PERCENT_PENALTY = -0.5  # Turnover percentage hurts
    W_USAGE_RATE          = 0.2   # Some bonus for usage (leader role)
    
    # Advanced stats
    W_TS_PERCENT       = 3.0
    W_EFG_PERCENT      = 2.0
    W_PLAYER_PER       = 2.0
    W_WIN_SHARES       = 1.5
    W_PLUS_MINUS       = 1.0
    W_OFF_BPM          = 1.0
    W_DEF_BPM          = 1.0
    W_VORP             = 0.5
    
    # Extra achievements or feats
    W_TRIPLE_DOUBLES   = 1.0
    W_DOUBLE_DOUBLES   = 0.2
    W_GAME_HIGH_POINTS = 0.1
    W_CAREER_HIGH_POINTS = 0.1
    # total_playoff_points might reflect playoff success or longevity
    W_TOTAL_PLAYOFF_PTS = 0.02

    # ------------------- EXTRACT ROW VALUES ---------------------
    # Major accolades
    championships     = row['championships']
    finals_mvp_awards = row['finals_mvp_awards']
    mvp_awards        = row['mvp_awards']
    dpoy_awards       = row['dpoy_awards']
    all_wnba_teams    = row['all_wnba_teams']
    all_star          = row['all_star_appearances']
    scoring_titles    = row['scoring_titles']
    
    # Traditional stats
    points   = row['points']
    rebounds = row['rebounds']
    assists  = row['assists']
    steals   = row['steals']
    blocks   = row['blocks']
    
    # Usage and turnovers
    usage_rate = row['usage_rate']
    tov_percent = row['turnover_percentage']
    
    # Advanced stats
    ts_percent  = row['true_shooting_percentage']
    efg_percent = row['effective_fg_percentage']
    player_per  = row['player_efficiency_rating']
    win_shares  = row['win_shares']
    plus_minus  = row['plus_minus']
    off_bpm     = row['off_bpm']
    def_bpm     = row['def_bpm']
    vorp        = row['vorp']
    
    # Special feats
    triple_doubles   = row['triple_doubles']
    double_doubles   = row['double_doubles']
    game_high_points = row['game_high_points']
    career_high_points = row['career_high_points']
    total_playoff_points = row['total_playoff_points']

    # ------------------- CALCULATE PARTIAL SCORES ----------------
    score = 0.0
    
    # Major accolades
    score += championships     * W_CHAMPIONSHIPS
    score += finals_mvp_awards * W_FINALS_MVP_AWARDS
    score += mvp_awards        * W_MVP_AWARDS
    score += dpoy_awards       * W_DPOY_AWARDS
    score += all_wnba_teams    * W_ALL_WNBA_TEAMS
    score += all_star          * W_ALL_STAR
    score += scoring_titles    * W_SCORING_TITLES
    
    # Traditional stats
    score += points   * W_POINTS
    score += rebounds * W_REBOUNDS
    score += assists  * W_ASSISTS
    score += steals   * W_STEALS
    score += blocks   * W_BLOCKS
    
    # Usage & Turnovers
    # Give some credit for usage rate (leaders often carry heavy load)
    score += usage_rate * W_USAGE_RATE
    # Turnover percentage is penalizing
    score += tov_percent * W_TOV_PERCENT_PENALTY
    
    # Advanced stats
    score += ts_percent   * W_TS_PERCENT
    score += efg_percent  * W_EFG_PERCENT
    score += player_per   * W_PLAYER_PER
    score += win_shares   * W_WIN_SHARES
    score += plus_minus   * W_PLUS_MINUS
    score += off_bpm      * W_OFF_BPM
    score += def_bpm      * W_DEF_BPM
    score += vorp         * W_VORP
    
    # Extra achievements
    score += triple_doubles     * W_TRIPLE_DOUBLES
    score += double_doubles     * W_DOUBLE_DOUBLES
    score += game_high_points   * W_GAME_HIGH_POINTS
    score += career_high_points * W_CAREER_HIGH_POINTS
    score += total_playoff_points * W_TOTAL_PLAYOFF_PTS
    
    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("wnba_dataset.csv")
    
    # 2) Calculate the WNBA Index Score for each player
    df["wnba_index"] = df.apply(calc_wnba_index, axis=1)
    
    # 3) Sort players by that score, descending
    df = df.sort_values(by="wnba_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking in the console
    print("\n====== WNBA INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player = row['player_name']
        idx_score = row['wnba_index']
        print(f"{rank}. {player} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores (0–100 scale)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='wnba_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("wnba_index_scored.csv", index=False)
    
    # 7) Create the line plot using the normalized data (top 10)
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 WNBA Players by Normalized Index',
        save_path='wnba_index_plot.png'
    )
    
    print("\nResults saved to 'wnba_index_scored.csv'.")
    print("Line plot saved as 'wnba_index_plot.png'.")


if __name__ == "__main__":
    main()
