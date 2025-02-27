import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# If needed, add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import normalization helpers
from sports_index_normalizer import normalize_indexes, plot_top_10_indexes

def calc_womens_hockey_index(row):
    """
    Calculates a single 'Women's Hockey Index Score' by blending a variety
    of women's hockey-specific stats:
      - Olympic & World Championship medals
      - International & pro league goals/assists/points
      - Defensive stats (hits, blocked shots), doping checks
      - Hall of Fame, major awards
      - Goalie stats for netminders
      - A mild penalty for retirement age

    Negative weighting for doping test failures, small bonus for doping tests passed.
    Adjust these multipliers as you see fit.
    """

    # ------------------- WEIGHT DEFINITIONS ---------------------
    # International accomplishments
    W_OLYMPIC_GOLD               = 10.0
    W_TOTAL_OLYMPIC_MEDALS       = 3.0    # each additional medal beyond gold
    W_WORLD_CHAMP_MEDALS         = 2.0

    # Offensive stats (International + Pro)
    W_INT_GOALS       = 0.3
    W_INT_ASSISTS     = 0.2
    W_INT_POINTS      = 0.1   # mild synergy bonus
    W_PRO_GOALS       = 0.25
    W_PRO_ASSISTS     = 0.15
    W_PRO_POINTS      = 0.05  # mild synergy
    W_PLUS_MINUS      = 0.1
    W_POWERPLAY_GOALS = 0.15
    W_SHORTHANDED_GOALS = 0.2
    W_GAME_WINNING_GOALS = 0.25

    # Defensive/physical stats
    W_HITS            = 0.02
    W_BLOCKED_SHOTS   = 0.02
    W_PENALTY_MINUTES = -0.02

    # Key achievements
    W_CHAMPIONSHIPS_WON  = 5.0  # e.g. Clarkson Cup, Isobel Cup, NCAA titles
    W_MVP_AWARDS         = 3.0
    W_BEST_FORWARD       = 2.5
    W_BEST_DEF          = 2.5
    W_BEST_GOALIE        = 3.0
    W_ALL_STAR_TEAMS     = 1.0
    W_MAJOR_TOURNEY_MVP  = 3.0
    W_NOTABLE_AWARDS     = 1.5

    # Goalie-specific
    W_CAREER_SAVES       = 0.01
    W_CAREER_SHUTOUTS    = 3.0
    W_GOALS_AGAINST_AVG  = -2.0   # lower is better => negative weight
    W_SAVE_PERCENTAGE    = 3.0    # higher is better

    # Other
    W_AVG_TIME_ON_ICE    = 0.2
    W_SHOOTING_PERCENTAGE= 0.5
    W_FACEOFF_WIN_PCT    = 1.0
    W_DOPING_FAILED_PENALTY = -10.0
    W_DOPING_PASSED_BONUS   = 0.05
    W_HALL_OF_FAME       = 5.0
    W_CAREER_EARNINGS    = 0.1

    # Retirement penalty
    W_RETIREMENT_PENALTY_PER_YEAR = -0.1
    CURRENT_YEAR = 2023

    # ------------------- EXTRACT ROW VALUES ---------------------
    # Basic info
    olympic_gold       = row["olympic_gold_medals"]
    total_olympic      = row["total_olympic_medals"]
    wc_medals          = row["world_championship_medals"]

    # Offense: international
    int_goals    = row["total_international_goals"]
    int_assists  = row["total_international_assists"]
    int_points   = row["total_international_points"]

    # Offense: pro leagues
    pro_goals    = row["total_pro_league_goals"]
    pro_assists  = row["total_pro_league_assists"]
    pro_points   = row["total_pro_league_points"]

    plus_minus_val     = row["plus_minus"]
    pims              = row["penalty_minutes"]
    pp_goals          = row["powerplay_goals"]
    sh_goals          = row["shorthanded_goals"]
    gw_goals          = row["game_winning_goals"]

    # Defensive/physical
    hits             = row["hits"]
    blocked          = row["blocked_shots"]

    # Achievements
    champs_won       = row["championships_won"]
    mvp_awards       = row["mvp_awards"]
    best_fwd         = row["best_forward_awards"]
    best_def         = row["best_defenseman_awards"]
    best_goalie      = row["best_goalie_awards"]
    all_star         = row["all_star_teams"]
    major_tourney_mvp= row["major_tournament_mvp"]
    notable_awards   = row["notable_awards"]

    # Goalie stats
    saves        = row["career_saves"]
    shutouts     = row["career_shutouts"]
    gaa          = row["goals_against_average"]
    sv_percent   = row["save_percentage"]

    # Additional
    avg_toi        = row["average_time_on_ice_min"]
    shooting_pct   = row["shooting_percentage"]
    faceoff_pct    = row["faceoff_win_percentage"]

    doping_failed  = row["doping_tests_failed"]
    doping_passed  = row["doping_tests_passed"]
    hall_of_fame   = row["hall_of_fame_inducted"]
    earnings       = row["career_earnings_million_usd"]
    retirement     = row["retirement_year"]

    # ------------------- CALCULATE PARTIAL SCORE ----------------
    score = 0.0

    # International medals
    score += olympic_gold  * W_OLYMPIC_GOLD
    # Each additional Olympic medal (silver/bronze) beyond gold gets smaller weight
    if total_olympic > olympic_gold:
        extra_oly = total_olympic - olympic_gold
        score += extra_oly * W_TOTAL_OLYMPIC_MEDALS

    score += wc_medals * W_WORLD_CHAMP_MEDALS

    # International offense
    score += int_goals   * W_INT_GOALS
    score += int_assists * W_INT_ASSISTS
    score += int_points  * W_INT_POINTS

    # Pro league offense
    score += pro_goals   * W_PRO_GOALS
    score += pro_assists * W_PRO_ASSISTS
    score += pro_points  * W_PRO_POINTS

    # plus-minus and penalty
    score += plus_minus_val * W_PLUS_MINUS
    score += pims           * W_PENALTY_MINUTES

    # PP, SH, GW goals
    score += pp_goals * W_POWERPLAY_GOALS
    score += sh_goals * W_SHORTHANDED_GOALS
    score += gw_goals * W_GAME_WINNING_GOALS

    # Defensive/physical
    score += hits    * W_HITS
    score += blocked * W_BLOCKED_SHOTS

    # Achievements
    score += champs_won  * W_CHAMPIONSHIPS_WON
    score += mvp_awards  * W_MVP_AWARDS
    score += best_fwd    * W_BEST_FORWARD
    score += best_def    * W_BEST_DEF
    score += best_goalie * W_BEST_GOALIE
    score += all_star    * W_ALL_STAR_TEAMS
    score += major_tourney_mvp * W_MAJOR_TOURNEY_MVP
    score += notable_awards    * W_NOTABLE_AWARDS

    # Goalie stats
    score += saves     * W_CAREER_SAVES
    score += shutouts  * W_CAREER_SHUTOUTS
    score += gaa       * W_GOALS_AGAINST_AVG        # negative weight => see below
    # Because GAA is negative weighting, we do: score += gaa * negative_value
    # but we already set W_GOALS_AGAINST_AVG = -2.0 above, so no separate logic needed
    score += sv_percent * W_SAVE_PERCENTAGE

    # Additional
    score += avg_toi      * W_AVG_TIME_ON_ICE
    score += shooting_pct * W_SHOOTING_PERCENTAGE
    score += faceoff_pct  * W_FACEOFF_WIN_PCT

    # Doping
    score += doping_passed * W_DOPING_PASSED_BONUS
    score += doping_failed * W_DOPING_FAILED_PENALTY

    # Hall of Fame
    score += hall_of_fame * W_HALL_OF_FAME

    # Earnings
    score += earnings * W_CAREER_EARNINGS

    # Retirement penalty
    if retirement != 0 and retirement < CURRENT_YEAR:
        years_since = CURRENT_YEAR - retirement
        if years_since > 30:
            years_since = 30
        score += (years_since * W_RETIREMENT_PENALTY_PER_YEAR)

    return score


def main():
    # 1) Load the dataset
    df = pd.read_csv("womens_hockey_dataset.csv")
    
    # 2) Calculate the Women's Hockey Index Score for each player
    df["womens_hockey_index"] = df.apply(calc_womens_hockey_index, axis=1)
    
    # 3) Sort players by that index, descending
    df = df.sort_values(by="womens_hockey_index", ascending=False).reset_index(drop=True)
    
    # 4) Print the ranking
    print("\n====== WOMEN'S HOCKEY INDEX RANKING (TOP 25) ======")
    for i, row in df.iterrows():
        rank = i + 1
        player_name = row['player_name']
        idx_score = row['womens_hockey_index']
        print(f"{rank}. {player_name} - Index: {idx_score:.1f}")
    
    # 5) Normalize the index scores (0–100)
    normalized_df = normalize_indexes(df, name_col='player_name', index_col='womens_hockey_index')
    
    # 6) Save the sorted results with normalized scores to a new CSV
    normalized_df.to_csv("womens_hockey_index_scored.csv", index=False)
    
    # 7) Create a line plot for top 10
    plot_top_10_indexes(
        normalized_df,
        name_col='player_name',
        index_col='normalized_index',
        title='Top 10 Womens Hockey Players by Normalized Index',
        save_path='womens_hockey_index_plot.png'
    )
    
    print("\nResults saved to 'womens_hockey_index_scored.csv'.")
    print("Line plot saved as 'womens_hockey_index_plot.png'.")


if __name__ == "__main__":
    main()
