import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_basketball_index(row):
    """
    Calculates a single 'Basketball Index Score' for each player
    by combining multiple stats with weighted importance.
    
    You can tune or extend these weights based on further research
    or personal judgment of each metric's cultural / historical impact.
    """
    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Major accolades
    W_CHAMPIONSHIPS        = 30   # Reduced slightly (from 35) to reflect a bit more balance 
    W_MVP_AWARDS           = 30   # Equal to championships—society heavily values both
    W_FINALS_MVP_AWARDS    = 15   # Still important, but less than a regular-season MVP or ring
    W_ALL_NBA_TEAMS        = 5    # Remains the same
    W_ALL_STAR_APPEARANCES = 2    # Remains the same; All-Star is big but less than All-NBA

    
    # Traditional counting stats (mild weights)
    W_POINTS       = 0.005  # fans value raw scoring heavily
    W_REBOUNDS     = 0.003  # 
    W_ASSISTS      = 0.003  # playmaking is key in perception
    W_STEALS       = 0.01    
    W_BLOCKS       = 0.01 
    W_TOV_PENALTY  = -0.02  # turnovers matter but are part of being a creator

    
    # Advanced stats
    W_CAREER_PER   = 2.0   # Keep as is
    W_CAREER_WS    = 2.0   # Slightly increased (from 1.5)
    W_CAREER_BPM   = 2.0   # Keep as is
    W_OFF_BPM      = 1.0   # Keep as is
    W_DEF_BPM      = 1.0   # Keep as is
    W_VORP         = 1.0   # Increase from 0.5 for a more balanced advanced profile

    
    # Shooting efficiency
    W_TS_PERCENT   = 8.0   # Slightly down from 10
    W_EFG_PERCENT  = 4.0   # Slightly down from 5

    
    # Extra achievements
    W_TRIPLE_DOUBLES    = 0.3 
    W_FORTY_POINT_GAMES = 0.2 

    
    # ------------------- EXTRACT ROW VALUES ---------------------
    championships        = row['championships']
    mvp_awards           = row['mvp_awards']
    finals_mvp_awards    = row['finals_mvp_awards']
    all_nba_teams        = row['all_nba_teams']
    all_star_appearances = row['all_star_appearances']
    
    points   = row['points']
    rebounds = row['total_rebounds']
    assists  = row['assists']
    steals   = row['steals']
    blocks   = row['blocks']
    tov      = row['turnovers']  # turnovers
    
    career_per = row['career_per']
    career_ws  = row['career_ws']
    career_bpm = row['career_bpm']
    off_bpm    = row['offensive_bpm']
    def_bpm    = row['defensive_bpm']
    vorp       = row['vorp']
    
    ts_percent  = row['true_shooting_percentage']     # e.g. 56.9 means 56.9
    efg_percent = row['effective_fg_percentage']      # e.g. 51.0 means 51.0
    
    triple_doubles      = row['triple_doubles']
    forty_plus_point_games = row['forty_plus_point_games']
    
    # ------------------- CALCULATE PARTIAL SCORES ----------------
    score = 0.0
    
    # Major accolades
    score += championships        * W_CHAMPIONSHIPS
    score += mvp_awards           * W_MVP_AWARDS
    score += finals_mvp_awards    * W_FINALS_MVP_AWARDS
    score += all_nba_teams        * W_ALL_NBA_TEAMS
    score += all_star_appearances * W_ALL_STAR_APPEARANCES
    
    # Traditional stats
    score += points   * W_POINTS
    score += rebounds * W_REBOUNDS
    score += assists  * W_ASSISTS
    score += steals   * W_STEALS
    score += blocks   * W_BLOCKS
    
    # Turnovers penalize
    score += tov * W_TOV_PENALTY
    
    # Advanced stats
    score += career_per   * W_CAREER_PER
    score += career_ws    * W_CAREER_WS
    score += career_bpm   * W_CAREER_BPM
    score += off_bpm      * W_OFF_BPM
    score += def_bpm      * W_DEF_BPM
    score += vorp         * W_VORP
    
    # Shooting efficiency
    score += ts_percent   * W_TS_PERCENT
    score += efg_percent  * W_EFG_PERCENT
    
    # Extra achievements
    score += triple_doubles       * W_TRIPLE_DOUBLES
    score += forty_plus_point_games * W_FORTY_POINT_GAMES
    
    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("basketball_dataset.csv")
    
    # 2) Calculate the Basketball Index Score for each player
    df["basketball_index"] = df.apply(calc_basketball_index, axis=1)
    
    # 3) Sort players by that score, descending
    df = df.sort_values(by="basketball_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== BASKETBALL INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player = row['player_name']
        idx_score = row['basketball_index']
        print(f"{rank}. {player} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='basketball_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("basketball_index_scored.csv", index=False)
    
    # 7) Create the plot using the normalized data
    plot_top_10_indexes(normalized_df, 
                       name_col='player_name',
                       index_col='normalized_index',
                       title='Top 10 Basketball Players by Normalized Index',
                       save_path='basketball_index_plot.png')
    
    print("\nResults saved to 'basketball_index_scored.csv'.")
    print("Line plot saved as 'basketball_index_plot.png'.")


if __name__ == "__main__":
    main()
