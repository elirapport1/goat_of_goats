import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to Python path for imports (if needed)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_mlb_index(row):
    """
    Calculates a single 'MLB Index Score' for each player by combining 
    a variety of batting, pitching, defensive, and accolade metrics.
    
    Each stat has a weight that reflects its perceived importance 
    in MLB history and fan culture. You can refine these weights
    as desired.
    """
    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Major accolades
    W_HALL_OF_FAME       = 20
    W_WORLD_SERIES       = 10
    W_MVP                = 15
    W_CY_YOUNG           = 12
    W_GOLD_GLOVES        = 3
    W_SILVER_SLUGGERS    = 2
    W_ALL_STAR           = 2
    W_TRIPLE_CROWNS      = 5
    
    # Key batting stats
    W_HITS                    = 0.001
    W_HOME_RUNS               = 0.05
    W_RBI                     = 0.01
    W_RUNS                    = 0.01
    W_STOLEN_BASES            = 0.01
    W_BATTING_AVG             = 25
    W_OBP                     = 25
    W_SLG                     = 20
    W_OPS                     = 15
    W_WOBA                    = 20
    W_WRC_PLUS                = 0.2
    W_OPS_PLUS                = 0.2
    W_TOTAL_BASES             = 0.001
    
    # Negative batting events
    W_STRIKEOUTS_BATTING_PENALTY = -0.0005
    W_DOUBLE_PLAYS_GROUNDED_PENALTY = -0.001
    
    # Pitching stats (0 for most hitters)
    # Lower ERA & WHIP = better, so negative multipliers
    W_ERA                    = -10
    W_PITCHER_WINS           = 0.05
    W_PITCHER_STRIKEOUTS     = 0.01
    W_PITCHER_SAVES          = 0.1
    W_PITCHER_WHIP           = -5
    
    # Special pitching feats
    W_PERFECT_GAMES          = 3
    W_NO_HITTERS             = 1
    
    # Advanced / composite metrics
    W_WAR                    = 4
    W_JAWS                   = 2
    W_DEF_RUNS_SAVED         = 0.05
    W_CAREER_POSTSEASON_WAR  = 2

    # ------------------- EXTRACT ROW VALUES ---------------------
    hall_of_fame     = row['hall_of_fame']  # 1 or 0
    world_series      = row['world_series_titles']
    mvp_awards        = row['mvp_awards']
    cy_young_awards   = row['cy_young_awards']
    gold_gloves       = row['gold_gloves']
    silver_sluggers   = row['silver_sluggers']
    all_star          = row['all_star_appearances']
    triple_crowns     = row['triple_crowns']
    
    hits              = row['hits']
    home_runs         = row['home_runs']
    rbi               = row['rbi']
    runs_scored       = row['runs']
    stolen_bases      = row['stolen_bases']
    batting_avg       = row['batting_avg']
    on_base_percentage= row['on_base_percentage']
    slugging_pct      = row['slugging_percentage']
    ops_val           = row['ops']
    woba              = row['woba']
    wrc_plus          = row['wrc_plus']
    ops_plus          = row['ops_plus']
    total_bases       = row['total_bases']
    strikeouts_bat    = row['strikeouts_batting']
    gdp               = row['double_plays_grounded_into']  # GIDP
    
    era               = row['era']
    pitcher_wins      = row['pitcher_wins']
    pitcher_strikeouts= row['pitcher_strikeouts']
    pitcher_saves     = row['pitcher_saves']
    pitcher_whip      = row['pitcher_whip']
    perfect_games     = row['perfect_games']
    no_hitters        = row['no_hitters']
    
    war_val           = row['war']
    jaws_val          = row['jaws']
    def_runs_saved    = row['def_runs_saved']
    postseason_war    = row['career_postseason_war']

    # ------------------- CALCULATE PARTIAL SCORES ----------------
    score = 0.0
    
    # Accolades
    score += hall_of_fame    * W_HALL_OF_FAME
    score += world_series    * W_WORLD_SERIES
    score += mvp_awards      * W_MVP
    score += cy_young_awards * W_CY_YOUNG
    score += gold_gloves     * W_GOLD_GLOVES
    score += silver_sluggers * W_SILVER_SLUGGERS
    score += all_star        * W_ALL_STAR
    score += triple_crowns   * W_TRIPLE_CROWNS
    
    # Batting stats
    score += hits            * W_HITS
    score += home_runs       * W_HOME_RUNS
    score += rbi             * W_RBI
    score += runs_scored     * W_RUNS
    score += stolen_bases    * W_STOLEN_BASES
    score += batting_avg     * W_BATTING_AVG
    score += on_base_percentage * W_OBP
    score += slugging_pct    * W_SLG
    score += ops_val         * W_OPS
    score += woba            * W_WOBA
    score += wrc_plus        * W_WRC_PLUS
    score += ops_plus        * W_OPS_PLUS
    score += total_bases     * W_TOTAL_BASES
    
    # Negative batting
    score += strikeouts_bat  * W_STRIKEOUTS_BATTING_PENALTY
    score += gdp             * W_DOUBLE_PLAYS_GROUNDED_PENALTY

    # Pitching stats
    score += era             * W_ERA
    score += pitcher_wins    * W_PITCHER_WINS
    score += pitcher_strikeouts * W_PITCHER_STRIKEOUTS
    score += pitcher_saves   * W_PITCHER_SAVES
    score += pitcher_whip    * W_PITCHER_WHIP
    score += perfect_games   * W_PERFECT_GAMES
    score += no_hitters      * W_NO_HITTERS

    # Advanced
    score += war_val         * W_WAR
    score += jaws_val        * W_JAWS
    score += def_runs_saved  * W_DEF_RUNS_SAVED
    score += postseason_war  * W_CAREER_POSTSEASON_WAR

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("mlb_dataset.csv")
    
    # 2) Calculate the MLB Index Score for each player
    df["mlb_index"] = df.apply(calc_mlb_index, axis=1)
    
    # 3) Sort players by that score, descending
    df = df.sort_values(by="mlb_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking in the console
    print("\n====== MLB INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player = row['player_name']
        idx_score = row['mlb_index']
        print(f"{rank}. {player} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores (0–100 scale)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='mlb_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("mlb_index_scored.csv", index=False)
    
    # 7) Create the line plot using the normalized data (top 10)
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 MLB Players by Normalized Index',
        save_path='mlb_index_plot.png'
    )
    
    print("\nResults saved to 'mlb_index_scored.csv'.")
    print("Line plot saved as 'mlb_index_plot.png'.")


if __name__ == "__main__":
    main()
