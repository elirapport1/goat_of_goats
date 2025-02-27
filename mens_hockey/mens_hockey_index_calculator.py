import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# If needed, add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_mens_hockey_index(row):
    """
    Calculates a single 'Men’s Hockey Index Score' by blending a variety
    of NHL/hockey-specific stats:
      - Goals, assists, points, plus-minus
      - Stanley Cups, major trophies (Hart, Art Ross, Maurice Richard, Conn Smythe, Norris, etc.)
      - Defensive stats (hits, blocked shots, Selke, penalty minutes?), doping
      - Hall of Fame, total playoff points, intangible achievements
      - Goalie stats for netminders (career_saves, shutouts)
    
    Negative weighting for doping test failures. Lower weight for older stats if not tracked.
    Adjust these multipliers as you see fit.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # Major Trophies
    W_STANLEY_CUPS          = 10.0
    W_HART_TROPHIES         = 8.0   # MVP
    W_ART_ROSS_TROPHIES     = 5.0   # top scorer
    W_RICHARD_TROPHIES      = 4.0   # top goal scorer
    W_CONN_SM_TROPHIES      = 6.0   # playoff MVP
    W_NORRIS_TROPHIES       = 6.0   # best defenseman
    W_CALDER_TROPHIES       = 3.0   # rookie of year
    W_SELKE_TROPHIES        = 4.0   # best defensive forward

    # Offensive counting stats
    W_TOTAL_GOALS      = 0.7
    W_TOTAL_ASSISTS    = 0.5
    W_TOTAL_POINTS     = 0.1       # slight bonus for total synergy
    W_PLUS_MINUS       = 0.2
    W_GAME_WINNING_GOALS = 0.3
    W_POWERPLAY_GOALS  = 0.15
    W_SHORTHANDED_GOALS= 0.2

    # Defensive or physical stats
    W_PENALTY_MINUTES  = -0.02  # being in the box can be negative, unless an enforcer
    W_HITS             = 0.02   # some value for physical play
    W_BLOCKED_SHOTS    = 0.02   # some value for d-men / 2-way forwards

    # Tournaments
    W_OLYMPIC_MEDALS     = 3.0   # each medal
    W_WORLD_CHAMP_MEDALS = 1.0   # less significant than Olympics in many opinions

    # Additional
    W_ALL_STAR_TEAMS      = 1.5
    W_NOTABLE_AWARDS      = 2.0
    W_DOPING_FAILED_PENALTY = -10.0
    W_DOPING_PASSED_BONUS   = 0.05

    # Time on ice
    W_AVG_TIME_ON_ICE    = 0.2

    # Shots & shooting
    W_TOTAL_SHOTS        = 0.01
    W_SHOOTING_PCT       = 0.5    # bigger chunk for being efficient

    # Faceoff
    W_FACEOFF_WIN_PCT    = 1.0

    # Goalie stats
    W_CAREER_SAVES       = 0.01
    W_CAREER_SHUTOUTS    = 3.0

    # Hall of Fame
    W_HALL_OF_FAME       = 5.0

    # Playoffs
    W_PLAYOFF_POINTS     = 0.3

    # Earnings not strongly correlated with greatness, but let's give a small weight
    W_CAREER_EARNINGS    = 0.05

    # Retirement penalty
    W_RETIREMENT_PENALTY_PER_YEAR = -0.1
    CURRENT_YEAR = 2023

    # ------------------- EXTRACT ROW VALUES ---------------------
    stanley_cups   = row["stanley_cups"]
    hart           = row["hart_trophies"]
    art_ross       = row["art_ross_trophies"]
    richard        = row["maurice_richard_trophies"]
    conn_smythe    = row["conn_smythe_trophies"]
    norris         = row["norris_trophies"]
    calder         = row["calder_trophies"]
    selke          = row["selke_trophies"]

    goals          = row["total_goals"]
    assists        = row["total_assists"]
    points         = row["total_points"]
    plus_minus     = row["plus_minus"]
    gw_goals       = row["game_winning_goals"]
    pp_goals       = row["powerplay_goals"]
    sh_goals       = row["shorthanded_goals"]

    penalty_min    = row["penalty_minutes"]
    hits           = row["hits"]
    blocks         = row["blocked_shots"]

    olympic_medals = row["olympic_medals"]
    wc_medals      = row["world_championship_medals"]

    all_star       = row["all_star_teams"]
    notable_awards = row["notable_awards"]

    doping_failed  = row["doping_tests_failed"]
    doping_passed  = row["doping_tests_passed"]

    toi_avg        = row["average_time_on_ice_min"]
    shots          = row["total_shots_on_goal"]
    shooting_pct   = row["shooting_percentage"]

    faceoff_pct    = row["faceoff_win_percentage"]

    # Goalie stats
    career_saves   = row["career_saves"]
    career_shutouts= row["career_shutouts"]

    hall_of_fame   = row["hall_of_fame_inducted"]
    playoff_points = row["total_playoff_points"]

    earnings       = row["career_earnings_million_usd"]
    retirement     = row["retirement_year"]

    # ------------------- CALCULATE PARTIAL SCORE ----------------
    score = 0.0

    # Trophies
    score += stanley_cups  * W_STANLEY_CUPS
    score += hart          * W_HART_TROPHIES
    score += art_ross      * W_ART_ROSS_TROPHIES
    score += richard       * W_RICHARD_TROPHIES
    score += conn_smythe   * W_CONN_SM_TROPHIES
    score += norris        * W_NORRIS_TROPHIES
    score += calder        * W_CALDER_TROPHIES
    score += selke         * W_SELKE_TROPHIES

    # Offensive counting
    score += goals    * W_TOTAL_GOALS
    score += assists  * W_TOTAL_ASSISTS
    score += points   * W_TOTAL_POINTS
    score += plus_minus * W_PLUS_MINUS
    score += gw_goals   * W_GAME_WINNING_GOALS
    score += pp_goals   * W_POWERPLAY_GOALS
    score += sh_goals   * W_SHORTHANDED_GOALS

    # Physical / defensive
    score += penalty_min * W_PENALTY_MINUTES
    score += hits        * W_HITS
    score += blocks      * W_BLOCKED_SHOTS

    # International
    score += olympic_medals * W_OLYMPIC_MEDALS
    score += wc_medals      * W_WORLD_CHAMP_MEDALS

    # Additional
    score += all_star        *  W_ALL_STAR_TEAMS
    score += notable_awards  *  W_NOTABLE_AWARDS

    # Doping
    score += doping_passed  * W_DOPING_PASSED_BONUS
    score += doping_failed  * W_DOPING_FAILED_PENALTY

    # Time on ice
    score += toi_avg * W_AVG_TIME_ON_ICE

    # Shots & shooting
    score += shots        * W_TOTAL_SHOTS
    score += shooting_pct * W_SHOOTING_PCT

    # Faceoff
    score += faceoff_pct  * W_FACEOFF_WIN_PCT

    # Goalie stats
    score += career_saves    * W_CAREER_SAVES
    score += career_shutouts * W_CAREER_SHUTOUTS

    # Hall of Fame
    score += hall_of_fame * W_HALL_OF_FAME

    # Playoff points
    score += playoff_points  * W_PLAYOFF_POINTS

    # Earnings
    score += earnings        * W_CAREER_EARNINGS

    # Retirement penalty
    if retirement != 0 and retirement < CURRENT_YEAR:
        years_since = CURRENT_YEAR - retirement
        if years_since > 30:
            years_since = 30
        score += (years_since * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("mens_hockey_dataset.csv")
    
    # 2) Calculate the Men’s Hockey Index Score for each player
    df["mens_hockey_index"] = df.apply(calc_mens_hockey_index, axis=1)
    
    # 3) Sort by that index, descending
    df = df.sort_values(by="mens_hockey_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== MEN'S HOCKEY INDEX RANKING (TOP 30) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player_name = row['player_name']
        idx_score = row['mens_hockey_index']
        print(f"{rank}. {player_name} - Index: {idx_score:.1f}")
    
    # 5) Normalize scores (0–100)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='mens_hockey_index')
    
    # 6) Save to CSV
    normalized_df.to_csv("mens_hockey_index_scored.csv", index=False)
    
    # 7) Plot top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Men’s Hockey Players by Normalized Index',
        save_path='mens_hockey_index_plot.png'
    )
    
    print("\nResults saved to 'mens_hockey_index_scored.csv'.")
    print("Line plot saved as 'mens_hockey_index_plot.png'.")


if __name__ == "__main__":
    main()
