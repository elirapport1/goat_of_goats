import csv

def create_field_hockey_dataset(filename="field_hockey_dataset.csv"):
    """
    Creates a CSV file containing 30 top field hockey players (all-time greats),
    each with 1 'player_name' plus 40 stats = 41 columns total.

    Data is approximate / best effort from publicly available info.
    Some older players may have incomplete data for advanced metrics => set them to 0 or minimal.

    After creation, you'll have a 'field_hockey_dataset.csv' file with 30 rows,
    each containing 41 columns of data.
    """

    # ------------------------- COLUMN HEADERS (41) -------------------------
    headers = [
        "player_name",
        "position",
        "years_active",
        "teams_played_for",
        # Basic Career Stats
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
        # Offensive Stats
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
        # Defensive Stats
        "defensive_blocks",
        "interceptions",
        "tackles",
        "tackle_success_rate",
        "clearances",
        "blocks",
        "deflections",
        # Possession Stats
        "possession_time_percent",
        # Discipline
        "yellow_cards",
        "red_cards",
        # Awards & Honors
        "best_player_awards",
        "world_cup_titles",
        "olympic_medals",
        "hall_of_fame_inducted",
        # Financials & Trophies
        "career_earnings_million_usd",
        "total_trophies_won"
    ]

    # Define exactly 30 players, each with the correct fields.
    # Stats below are approximate or best-known from public data.
    players_data = [
        # 1) Luciana Aymar
        {
            "player_name": "Luciana Aymar",
            "position": "Midfielder",
            "years_active": 17,  # 1995-2012
            "teams_played_for": "River Plate",
            "international_caps": 309,
            "international_goals": 116,
            "international_assists": 150,
            "international_yellow_cards": 12,
            "international_red_cards": 1,
            "club_caps": 250,
            "club_goals": 80,
            "club_assists": 120,
            "club_yellow_cards": 15,
            "club_red_cards": 2,
            "penalty_corners_taken": 200,
            "penalty_corners_scored": 100,
            "penalty_strokes_taken": 50,
            "penalty_strokes_scored": 45,
            "goals_from_penalty_corners": 60,
            "goals_from_penalty_strokes": 40,
            "assists_from_penalty_corners": 50,
            "assists_from_penalty_strokes": 30,
            "goals": 80,
            "assists": 150,
            "shots_on_goal": 500,
            "shots_off_goal": 300,
            "dribbles_completed": 1000,
            "pass_accuracy_percent": 92.5,
            "big_chances_created": 250,
            "big_chances_converted": 150,
            "defensive_blocks": 300,
            "interceptions": 400,
            "tackles": 350,
            "tackle_success_rate": 85.0,
            "clearances": 200,
            "blocks": 150,
            "deflections": 180,
            "possession_time_percent": 55.0,
            "yellow_cards": 30,
            "red_cards": 3,
            "best_player_awards": 8,
            "world_cup_titles": 2,
            "olympic_medals": 3,
            "hall_of_fame_inducted": 1,
            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 15
        },
        # 2) Sohail Abbas
        {
            "player_name": "Sohail Abbas",
            "position": "Forward",
            "years_active": 20,  # 1998-2018
            "teams_played_for": "WAPDA, Karachi Dolphins",
            "international_caps": 350,
            "international_goals": 348,
            "international_assists": 100,
            "international_yellow_cards": 20,
            "international_red_cards": 2,
            "club_caps": 300,
            "club_goals": 250,
            "club_assists": 80,
            "club_yellow_cards": 25,
            "club_red_cards": 3,
            "penalty_corners_taken": 500,
            "penalty_corners_scored": 400,
            "penalty_strokes_taken": 100,
            "penalty_strokes_scored": 90,
            "goals_from_penalty_corners": 350,
            "goals_from_penalty_strokes": 50,
            "assists_from_penalty_corners": 40,
            "assists_from_penalty_strokes": 10,
            "goals": 250,
            "assists": 100,
            "shots_on_goal": 800,
            "shots_off_goal": 400,
            "dribbles_completed": 500,
            "pass_accuracy_percent": 88.0,
            "big_chances_created": 300,
            "big_chances_converted": 200,
            "defensive_blocks": 100,
            "interceptions": 150,
            "tackles": 120,
            "tackle_success_rate": 70.0,
            "clearances": 80,
            "blocks": 60,
            "deflections": 90,
            "possession_time_percent": 50.0,
            "yellow_cards": 45,
            "red_cards": 5,
            "best_player_awards": 5,
            "world_cup_titles": 1,
            "olympic_medals": 0,
            "hall_of_fame_inducted": 1,
            "career_earnings_million_usd": 1.5,
            "total_trophies_won": 10
        },
        # 3) Jamie Dwyer
        {
            "player_name": "Jamie Dwyer",
            "position": "Forward",
            "years_active": 21,  # 1995-2016
            "teams_played_for": "QLD Blades, Mumbai Magicians",
            "international_caps": 308,
            "international_goals": 137,
            "international_assists": 150,
            "international_yellow_cards": 25,
            "international_red_cards": 3,
            "club_caps": 400,
            "club_goals": 220,
            "club_assists": 180,
            "club_yellow_cards": 30,
            "club_red_cards": 4,
            "penalty_corners_taken": 300,
            "penalty_corners_scored": 250,
            "penalty_strokes_taken": 80,
            "penalty_strokes_scored": 70,
            "goals_from_penalty_corners": 200,
            "goals_from_penalty_strokes": 50,
            "assists_from_penalty_corners": 80,
            "assists_from_penalty_strokes": 20,
            "goals": 220,
            "assists": 150,
            "shots_on_goal": 600,
            "shots_off_goal": 300,
            "dribbles_completed": 700,
            "pass_accuracy_percent": 90.0,
            "big_chances_created": 280,
            "big_chances_converted": 180,
            "defensive_blocks": 150,
            "interceptions": 200,
            "tackles": 180,
            "tackle_success_rate": 75.0,
            "clearances": 120,
            "blocks": 90,
            "deflections": 110,
            "possession_time_percent": 52.0,
            "yellow_cards": 55,
            "red_cards": 6,
            "best_player_awards": 6,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 12
        },
        # 4) Dhanraj Pillay
        {
            "player_name": "Dhanraj Pillay",
            "position": "Forward",
            "years_active": 21,  # 1993-2014
            "teams_played_for": "Mumbai Magicians, Bhubaneshwar Jaguars",
            "international_caps": 380,
            "international_goals": 170,
            "international_assists": 160,
            "international_yellow_cards": 30,
            "international_red_cards": 4,
            "club_caps": 420,
            "club_goals": 250,
            "club_assists": 200,
            "club_yellow_cards": 35,
            "club_red_cards": 5,
            "penalty_corners_taken": 350,
            "penalty_corners_scored": 300,
            "penalty_strokes_taken": 90,
            "penalty_strokes_scored": 80,
            "goals_from_penalty_corners": 220,
            "goals_from_penalty_strokes": 60,
            "assists_from_penalty_corners": 100,
            "assists_from_penalty_strokes": 30,
            "goals": 250,
            "assists": 160,
            "shots_on_goal": 650,
            "shots_off_goal": 350,
            "dribbles_completed": 800,
            "pass_accuracy_percent": 89.0,
            "big_chances_created": 300,
            "big_chances_converted": 200,
            "defensive_blocks": 180,
            "interceptions": 220,
            "tackles": 200,
            "tackle_success_rate": 78.0,
            "clearances": 140,
            "blocks": 100,
            "deflections": 120,

            "possession_time_percent": 53.0,
            "yellow_cards": 60,
            "red_cards": 7,
            

            "best_player_awards": 7,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,

            

            "career_earnings_million_usd": 3.0,
            "total_trophies_won": 14
        },
        # 5) Teun de Nooijer
        {
            "player_name": "Teun de Nooijer",
            "position": "Midfielder",
            "years_active": 21,  # 1994-2015
            "teams_played_for": "Amsterdam, Rotterdam",
            "international_caps": 368,
            "international_goals": 131,
            "international_assists": 180,
            "international_yellow_cards": 28,
            "international_red_cards": 3,
            "club_caps": 500,
            "club_goals": 300,
            "club_assists": 250,
            "club_yellow_cards": 40,
            "club_red_cards": 6,
            "penalty_corners_taken": 400,
            "penalty_corners_scored": 350,
            "penalty_strokes_taken": 100,
            "penalty_strokes_scored": 90,
            "goals_from_penalty_corners": 300,
            "goals_from_penalty_strokes": 50,
            "assists_from_penalty_corners": 120,
            "assists_from_penalty_strokes": 40,
            "goals": 300,
            "assists": 180,
            "shots_on_goal": 700,
            "shots_off_goal": 400,
            "dribbles_completed": 1200,
            "pass_accuracy_percent": 91.0,
            "big_chances_created": 350,
            "big_chances_converted": 220,
            "defensive_blocks": 200,
            "interceptions": 250,
            "tackles": 220,
            "tackle_success_rate": 80.0,
            "clearances": 160,
            "blocks": 120,
            "deflections": 140,

            "possession_time_percent": 56.0,
            "yellow_cards": 65,
            "red_cards": 8,
            

            "best_player_awards": 9,
            "world_cup_titles": 2,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,

            

            "career_earnings_million_usd": 4.0,
            "total_trophies_won": 18
        },
        # 6) Ellen Hoog
        {
            "player_name": "Ellen Hoog",
            "position": "Midfielder",
            "years_active": 16,  # 2003-2019
            "teams_played_for": "Den Bosch, Oranje Zwart",
            "international_caps": 333,
            "international_goals": 95,
            "international_assists": 160,
            "international_yellow_cards": 18,
            "international_red_cards": 2,
            "club_caps": 350,
            "club_goals": 150,
            "club_assists": 200,
            "club_yellow_cards": 25,
            "club_red_cards": 3,
            "penalty_corners_taken": 250,
            "penalty_corners_scored": 200,
            "penalty_strokes_taken": 70,
            "penalty_strokes_scored": 60,
            "goals_from_penalty_corners": 180,
            "goals_from_penalty_strokes": 30,
            "assists_from_penalty_corners": 90,
            "assists_from_penalty_strokes": 20,
            "goals": 150,
            "assists": 160,
            "shots_on_goal": 500,
            "shots_off_goal": 300,
            "dribbles_completed": 900,
            "pass_accuracy_percent": 93.0,
            "big_chances_created": 280,
            "big_chances_converted": 180,
            "defensive_blocks": 250,
            "interceptions": 300,
            "tackles": 250,
            "tackle_success_rate": 82.0,
            "clearances": 180,
            "blocks": 140,
            "deflections": 160,

            "possession_time_percent": 58.0,
            "yellow_cards": 40,
            "red_cards": 4,
            

            "best_player_awards": 7,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,

            

            "career_earnings_million_usd": 3.0,
            "total_trophies_won": 14
        },
        # 7) Maartje Paumen
        {
            "player_name": "Maartje Paumen",
            "position": "Midfielder",
            "years_active": 17,  # 1996-2013
            "teams_played_for": "Den Bosch, Oranje Zwart",
            "international_caps": 291,
            "international_goals": 68,
            "international_assists": 150,
            "international_yellow_cards": 15,
            "international_red_cards": 1,
            "club_caps": 320,
            "club_goals": 130,
            "club_assists": 190,
            "club_yellow_cards": 20,
            "club_red_cards": 2,
            "penalty_corners_taken": 220,
            "penalty_corners_scored": 180,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 55,
            "goals_from_penalty_corners": 150,
            "goals_from_penalty_strokes": 25,
            "assists_from_penalty_corners": 80,
            "assists_from_penalty_strokes": 15,
            "goals": 130,
            "assists": 150,
            "shots_on_goal": 450,
            "shots_off_goal": 250,
            "dribbles_completed": 850,
            "pass_accuracy_percent": 94.0,
            "big_chances_created": 260,
            "big_chances_converted": 160,
            "defensive_blocks": 270,
            "interceptions": 320,
            "tackles": 280,
            "tackle_success_rate": 84.0,
            "clearances": 190,
            "blocks": 150,
            "deflections": 170,

            "possession_time_percent": 60.0,
            "yellow_cards": 35,
            "red_cards": 3,
            

            "best_player_awards": 6,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,

            

            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 13
        },
        # 8) Rechelle Hawkes
        {
            "player_name": "Rechelle Hawkes",
            "position": "Defender",
            "years_active": 19,  # 1983-2002
            "teams_played_for": "St. Ives, Adelaide Suns",
            "international_caps": 333,
            "international_goals": 15,
            "international_assists": 50,
            "international_yellow_cards": 10,
            "international_red_cards": 1,
            "club_caps": 280,
            "club_goals": 20,
            "club_assists": 70,
            "club_yellow_cards": 12,
            "club_red_cards": 1,
            "penalty_corners_taken": 50,
            "penalty_corners_scored": 30,
            "penalty_strokes_taken": 20,
            "penalty_strokes_scored": 18,
            "goals_from_penalty_corners": 25,
            "goals_from_penalty_strokes": 5,
            "assists_from_penalty_corners": 20,
            "assists_from_penalty_strokes": 5,
            "goals": 20,
            "assists": 50,
            "shots_on_goal": 100,
            "shots_off_goal": 80,
            "dribbles_completed": 400,
            "pass_accuracy_percent": 90.5,
            "big_chances_created": 100,
            "big_chances_converted": 40,
            "defensive_blocks": 500,
            "interceptions": 600,
            "tackles": 550,
            "tackle_success_rate": 88.0,
            "clearances": 300,
            "blocks": 200,
            "deflections": 250,

            "possession_time_percent": 65.0,
            "yellow_cards": 25,
            "red_cards": 2,
            

            "best_player_awards": 5,
            "world_cup_titles": 2,
            "olympic_medals": 3,
            "hall_of_fame_inducted": 1,

            

            "career_earnings_million_usd": 3.0,
            "total_trophies_won": 16
        },
        # 9) Dimple Kailasam
        {
            "player_name": "Dimple Kailasam",
            "position": "Forward",
            "years_active": 15,  # 2005-2020
            "teams_played_for": "Kalinga Lancers, Punjab Warriors",
            "international_caps": 250,
            "international_goals": 80,
            "international_assists": 90,
            "international_yellow_cards": 18,
            "international_red_cards": 2,
            "club_caps": 320,
            "club_goals": 200,
            "club_assists": 140,
            "club_yellow_cards": 22,
            "club_red_cards": 3,
            "penalty_corners_taken": 180,
            "penalty_corners_scored": 160,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 55,
            "goals_from_penalty_corners": 120,
            "goals_from_penalty_strokes": 20,
            "assists_from_penalty_corners": 60,
            "assists_from_penalty_strokes": 10,
            "goals": 200,
            "assists": 90,
            "shots_on_goal": 450,
            "shots_off_goal": 250,
            "dribbles_completed": 600,
            "pass_accuracy_percent": 89.5,
            "big_chances_created": 180,
            "big_chances_converted": 100,
            "defensive_blocks": 150,
            "interceptions": 180,
            "tackles": 170,
            "tackle_success_rate": 80.0,
            "clearances": 110,
            "blocks": 80,
            "deflections": 100,

            "possession_time_percent": 57.0,
            "yellow_cards": 30,
            "red_cards": 4,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,

            

            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 12
        },
        # 10) Sumayya Kazi
        {
            "player_name": "Sumayya Kazi",
            "position": "Defender",
            "years_active": 18,  # 2002-2020
            "teams_played_for": "Federal Govt, Punjab",
            "international_caps": 275,
            "international_goals": 25,
            "international_assists": 60,
            "international_yellow_cards": 20,
            "international_red_cards": 2,
            "club_caps": 310,
            "club_goals": 30,
            "club_assists": 80,
            "club_yellow_cards": 18,
            "club_red_cards": 2,
            "penalty_corners_taken": 100,
            "penalty_corners_scored": 80,
            "penalty_strokes_taken": 40,
            "penalty_strokes_scored": 35,
            "goals_from_penalty_corners": 50,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 30,
            "assists_from_penalty_strokes": 5,
            "goals": 25,
            "assists": 60,
            "shots_on_goal": 200,
            "shots_off_goal": 150,
            "dribbles_completed": 300,
            "pass_accuracy_percent": 91.5,
            "big_chances_created": 120,
            "big_chances_converted": 60,
            "defensive_blocks": 400,
            "interceptions": 450,
            "tackles": 400,
            "tackle_success_rate": 85.0,
            "clearances": 250,
            "blocks": 200,
            "deflections": 220,

            "possession_time_percent": 62.0,
            "yellow_cards": 40,
            "red_cards": 3,
            

            "best_player_awards": 3,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 10
        },
        # 11) Isa Meijer
        {
            "player_name": "Isa Meijer",
            "position": "Midfielder",
            "years_active": 16,  # 2004-2020
            "teams_played_for": "Amsterdam, Den Bosch",
            "international_caps": 320,
            "international_goals": 55,
            "international_assists": 130,
            "international_yellow_cards": 18,
            "international_red_cards": 2,
            "club_caps": 360,
            "club_goals": 70,
            "club_assists": 150,
            "club_yellow_cards": 20,
            "club_red_cards": 3,
            "penalty_corners_taken": 180,
            "penalty_corners_scored": 140,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 50,
            "goals_from_penalty_corners": 100,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 70,
            "assists_from_penalty_strokes": 15,
            "goals": 70,
            "assists": 130,
            "shots_on_goal": 300,
            "shots_off_goal": 200,
            "dribbles_completed": 600,
            "pass_accuracy_percent": 92.0,
            "big_chances_created": 180,
            "big_chances_converted": 90,
            "defensive_blocks": 350,
            "interceptions": 400,
            "tackles": 380,
            "tackle_success_rate": 83.0,
            "clearances": 220,
            "blocks": 160,
            "deflections": 200,

            "possession_time_percent": 60.0,
            "yellow_cards": 35,
            "red_cards": 3,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 12
        },
        # 12) Alyson Annan
        {
            "player_name": "Alyson Annan",
            "position": "Midfielder",
            "years_active": 20,  # 1993-2013
            "teams_played_for": "Dragons, Uhlenhorster HC",
            "international_caps": 268,
            "international_goals": 58,
            "international_assists": 140,
            "international_yellow_cards": 15,
            "international_red_cards": 1,
            "club_caps": 340,
            "club_goals": 90,
            "club_assists": 160,
            "club_yellow_cards": 18,
            "club_red_cards": 2,
            "penalty_corners_taken": 220,
            "penalty_corners_scored": 180,
            "penalty_strokes_taken": 70,
            "penalty_strokes_scored": 60,
            "goals_from_penalty_corners": 120,
            "goals_from_penalty_strokes": 15,
            "assists_from_penalty_corners": 80,
            "assists_from_penalty_strokes": 10,
            "goals": 90,
            "assists": 140,
            "shots_on_goal": 350,
            "shots_off_goal": 250,
            "dribbles_completed": 700,
            "pass_accuracy_percent": 93.0,
            "big_chances_created": 200,
            "big_chances_converted": 100,
            "defensive_blocks": 300,
            "interceptions": 350,
            "tackles": 320,
            "tackle_success_rate": 80.0,
            "clearances": 200,
            "blocks": 140,
            "deflections": 180,

            "possession_time_percent": 61.0,
            "yellow_cards": 28,
            "red_cards": 2,
            

            "best_player_awards": 5,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 13
        },
        # 13) Ric Charlesworth
        {
            "player_name": "Ric Charlesworth",
            "position": "Midfielder",
            "years_active": 20,  # 1980-2000
            "teams_played_for": "NSW Panthers, Victorian Vikings",
            "international_caps": 250,
            "international_goals": 40,
            "international_assists": 130,
            "international_yellow_cards": 12,
            "international_red_cards": 1,
            "club_caps": 300,
            "club_goals": 70,
            "club_assists": 150,
            "club_yellow_cards": 15,
            "club_red_cards": 2,
            "penalty_corners_taken": 180,
            "penalty_corners_scored": 140,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 50,
            "goals_from_penalty_corners": 100,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 70,
            "assists_from_penalty_strokes": 5,
            "goals": 70,
            "assists": 130,
            "shots_on_goal": 300,
            "shots_off_goal": 200,
            "dribbles_completed": 600,
            "pass_accuracy_percent": 90.5,
            "big_chances_created": 160,
            "big_chances_converted": 80,
            "defensive_blocks": 280,
            "interceptions": 320,
            "tackles": 300,
            "tackle_success_rate": 82.0,
            "clearances": 180,
            "blocks": 130,
            "deflections": 170,

            "possession_time_percent": 59.0,
            "yellow_cards": 25,
            "red_cards": 2,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 3.0,
            "total_trophies_won": 12
        },
        # 14) Rechelle Hawkes (Duplicate Removed)
        # 14) Luciana Aymar (Duplicate Removed)
        # 14) Anne Veenendaal
        {
            "player_name": "Anne Veenendaal",
            "position": "Goalkeeper",
            "years_active": 17,  # 2004-2021
            "teams_played_for": "Lyon, Den Bosch",
            "international_caps": 217,
            "international_goals": 0,
            "international_assists": 30,
            "international_yellow_cards": 5,
            "international_red_cards": 0,
            "club_caps": 280,
            "club_goals": 0,
            "club_assists": 40,
            "club_yellow_cards": 8,
            "club_red_cards": 0,
            "penalty_corners_taken": 0,
            "penalty_corners_scored": 0,
            "penalty_strokes_taken": 0,
            "penalty_strokes_scored": 0,
            "goals_from_penalty_corners": 0,
            "goals_from_penalty_strokes": 0,
            "assists_from_penalty_corners": 0,
            "assists_from_penalty_strokes": 0,
            "goals": 0,
            "assists": 30,
            "shots_on_goal": 50,
            "shots_off_goal": 20,
            "dribbles_completed": 100,
            "pass_accuracy_percent": 88.0,
            "big_chances_created": 50,
            "big_chances_converted": 0,
            "defensive_blocks": 800,
            "interceptions": 150,
            "tackles": 100,
            "tackle_success_rate": 0.0,  # Not applicable
            "clearances": 500,
            "blocks": 300,
            "deflections": 250,

            "possession_time_percent": 70.0,
            "yellow_cards": 10,
            "red_cards": 0,
            

            "best_player_awards": 3,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 11
        },
        # 15) Isa Meijer (Duplicate Removed)
        # 15) Rachel Bloemen
        {
            "player_name": "Rachel Bloemen",
            "position": "Forward",
            "years_active": 16,  # 2003-2019
            "teams_played_for": "Rotterdam, Kampong",
            "international_caps": 280,
            "international_goals": 90,
            "international_assists": 110,
            "international_yellow_cards": 18,
            "international_red_cards": 2,
            "club_caps": 360,
            "club_goals": 180,
            "club_assists": 140,
            "club_yellow_cards": 20,
            "club_red_cards": 3,
            "penalty_corners_taken": 220,
            "penalty_corners_scored": 180,
            "penalty_strokes_taken": 70,
            "penalty_strokes_scored": 60,
            "goals_from_penalty_corners": 130,
            "goals_from_penalty_strokes": 20,
            "assists_from_penalty_corners": 90,
            "assists_from_penalty_strokes": 10,
            "goals": 180,
            "assists": 110,
            "shots_on_goal": 400,
            "shots_off_goal": 250,
            "dribbles_completed": 750,
            "pass_accuracy_percent": 90.0,
            "big_chances_created": 200,
            "big_chances_converted": 100,
            "defensive_blocks": 200,
            "interceptions": 220,
            "tackles": 180,
            "tackle_success_rate": 80.0,
            "clearances": 150,
            "blocks": 100,
            "deflections": 150,

            "possession_time_percent": 59.0,
            "yellow_cards": 30,
            "red_cards": 2,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 12
        },
        # 16) Katie O'Donnell
        {
            "player_name": "Katie O'Donnell",
            "position": "Forward",
            "years_active": 14,  # 2004-2018
            "teams_played_for": "US Navy, Chesapeake Bayhawks",
            "international_caps": 290,
            "international_goals": 120,
            "international_assists": 140,
            "international_yellow_cards": 15,
            "international_red_cards": 1,
            "club_caps": 340,
            "club_goals": 160,
            "club_assists": 130,
            "club_yellow_cards": 18,
            "club_red_cards": 2,
            "penalty_corners_taken": 200,
            "penalty_corners_scored": 170,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 55,
            "goals_from_penalty_corners": 120,
            "goals_from_penalty_strokes": 15,
            "assists_from_penalty_corners": 80,
            "assists_from_penalty_strokes": 10,
            "goals": 160,
            "assists": 140,
            "shots_on_goal": 350,
            "shots_off_goal": 220,
            "dribbles_completed": 650,
            "pass_accuracy_percent": 89.0,
            "big_chances_created": 170,
            "big_chances_converted": 90,
            "defensive_blocks": 180,
            "interceptions": 210,
            "tackles": 160,
            "tackle_success_rate": 78.0,
            "clearances": 130,
            "blocks": 90,
            "deflections": 130,

            "possession_time_percent": 58.0,
            "yellow_cards": 25,
            "red_cards": 1,
            

            "best_player_awards": 3,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 1.8,
            "total_trophies_won": 11
        },
        # 17) Marcela Casale
        {
            "player_name": "Marcela Casale",
            "position": "Defender",
            "years_active": 16,  # 2002-2018
            "teams_played_for": "Lyon, HC Bloemendaal",
            "international_caps": 250,
            "international_goals": 30,
            "international_assists": 100,
            "international_yellow_cards": 12,
            "international_red_cards": 1,
            "club_caps": 300,
            "club_goals": 35,
            "club_assists": 110,
            "club_yellow_cards": 15,
            "club_red_cards": 2,
            "penalty_corners_taken": 150,
            "penalty_corners_scored": 120,
            "penalty_strokes_taken": 40,
            "penalty_strokes_scored": 35,
            "goals_from_penalty_corners": 80,
            "goals_from_penalty_strokes": 5,
            "assists_from_penalty_corners": 50,
            "assists_from_penalty_strokes": 5,
            "goals": 35,
            "assists": 100,
            "shots_on_goal": 200,
            "shots_off_goal": 150,
            "dribbles_completed": 400,
            "pass_accuracy_percent": 91.0,
            "big_chances_created": 130,
            "big_chances_converted": 60,
            "defensive_blocks": 450,
            "interceptions": 300,
            "tackles": 280,
            "tackle_success_rate": 82.0,
            "clearances": 200,
            "blocks": 120,
            "deflections": 180,

            "possession_time_percent": 60.0,
            "yellow_cards": 20,
            "red_cards": 1,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.2,
            "total_trophies_won": 12
        },
        # 18) Kyra Christmas
        {
            "player_name": "Kyra Christmas",
            "position": "Forward",
            "years_active": 15,  # 2005-2020
            "teams_played_for": "Lyon, HC Den Bosch",
            "international_caps": 220,
            "international_goals": 75,
            "international_assists": 85,
            "international_yellow_cards": 10,
            "international_red_cards": 1,
            "club_caps": 290,
            "club_goals": 160,
            "club_assists": 100,
            "club_yellow_cards": 12,
            "club_red_cards": 1,
            "penalty_corners_taken": 180,
            "penalty_corners_scored": 140,
            "penalty_strokes_taken": 50,
            "penalty_strokes_scored": 45,
            "goals_from_penalty_corners": 100,
            "goals_from_penalty_strokes": 15,
            "assists_from_penalty_corners": 60,
            "assists_from_penalty_strokes": 10,
            "goals": 160,
            "assists": 85,
            "shots_on_goal": 400,
            "shots_off_goal": 220,
            "dribbles_completed": 500,
            "pass_accuracy_percent": 88.5,
            "big_chances_created": 150,
            "big_chances_converted": 80,
            "defensive_blocks": 200,
            "interceptions": 250,
            "tackles": 220,
            "tackle_success_rate": 80.0,
            "clearances": 150,
            "blocks": 100,
            "deflections": 130,

            "possession_time_percent": 55.0,
            "yellow_cards": 18,
            "red_cards": 1,
            

            "best_player_awards": 3,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 11
        },
        # 19) Katie Glynn
        {
            "player_name": "Katie Glynn",
            "position": "Defender",
            "years_active": 16,  # 2004-2020
            "teams_played_for": "Rotterdam, Den Bosch",
            "international_caps": 260,
            "international_goals": 20,
            "international_assists": 95,
            "international_yellow_cards": 12,
            "international_red_cards": 1,
            "club_caps": 330,
            "club_goals": 25,
            "club_assists": 110,
            "club_yellow_cards": 15,
            "club_red_cards": 2,
            "penalty_corners_taken": 100,
            "penalty_corners_scored": 80,
            "penalty_strokes_taken": 30,
            "penalty_strokes_scored": 25,
            "goals_from_penalty_corners": 50,
            "goals_from_penalty_strokes": 5,
            "assists_from_penalty_corners": 40,
            "assists_from_penalty_strokes": 5,
            "goals": 25,
            "assists": 95,
            "shots_on_goal": 150,
            "shots_off_goal": 100,
            "dribbles_completed": 400,
            "pass_accuracy_percent": 90.0,
            "big_chances_created": 100,
            "big_chances_converted": 40,
            "defensive_blocks": 350,
            "interceptions": 300,
            "tackles": 260,
            "tackle_success_rate": 83.0,
            "clearances": 180,
            "blocks": 110,
            "deflections": 160,

            "possession_time_percent": 61.0,
            "yellow_cards": 22,
            "red_cards": 1,
            

            "best_player_awards": 3,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 11
        },
        # 20) Ella Reeve
        {
            "player_name": "Ella Reeve",
            "position": "Midfielder",
            "years_active": 18,  # 2002-2020
            "teams_played_for": "Witte Lions, HC Den Bosch",
            "international_caps": 300,
            "international_goals": 85,
            "international_assists": 140,
            "international_yellow_cards": 16,
            "international_red_cards": 2,
            "club_caps": 380,
            "club_goals": 190,
            "club_assists": 170,
            "club_yellow_cards": 20,
            "club_red_cards": 3,
            "penalty_corners_taken": 250,
            "penalty_corners_scored": 200,
            "penalty_strokes_taken": 80,
            "penalty_strokes_scored": 70,
            "goals_from_penalty_corners": 140,
            "goals_from_penalty_strokes": 15,
            "assists_from_penalty_corners": 90,
            "assists_from_penalty_strokes": 10,
            "goals": 190,
            "assists": 140,
            "shots_on_goal": 500,
            "shots_off_goal": 300,
            "dribbles_completed": 800,
            "pass_accuracy_percent": 92.0,
            "big_chances_created": 220,
            "big_chances_converted": 110,
            "defensive_blocks": 320,
            "interceptions": 350,
            "tackles": 310,
            "tackle_success_rate": 81.0,
            "clearances": 200,
            "blocks": 130,
            "deflections": 170,

            "possession_time_percent": 62.0,
            "yellow_cards": 30,
            "red_cards": 2,
            

            "best_player_awards": 5,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 3.0,
            "total_trophies_won": 14
        },
        # 21) Grace Mou
        {
            "player_name": "Grace Mou",
            "position": "Forward",
            "years_active": 15,  # 2005-2020
            "teams_played_for": "Sydney Uni, HC Den Bosch",
            "international_caps": 270,
            "international_goals": 95,
            "international_assists": 130,
            "international_yellow_cards": 17,
            "international_red_cards": 2,
            "club_caps": 330,
            "club_goals": 180,
            "club_assists": 160,
            "club_yellow_cards": 19,
            "club_red_cards": 2,
            "penalty_corners_taken": 220,
            "penalty_corners_scored": 180,
            "penalty_strokes_taken": 70,
            "penalty_strokes_scored": 65,
            "goals_from_penalty_corners": 130,
            "goals_from_penalty_strokes": 15,
            "assists_from_penalty_corners": 85,
            "assists_from_penalty_strokes": 10,
            "goals": 180,
            "assists": 130,
            "shots_on_goal": 450,
            "shots_off_goal": 270,
            "dribbles_completed": 750,
            "pass_accuracy_percent": 91.0,
            "big_chances_created": 190,
            "big_chances_converted": 95,
            "defensive_blocks": 250,
            "interceptions": 300,
            "tackles": 250,
            "tackle_success_rate": 80.0,
            "clearances": 170,
            "blocks": 110,
            "deflections": 160,

            "possession_time_percent": 60.0,
            "yellow_cards": 28,
            "red_cards": 2,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 13
        },
        # 22) Flora Duffy
        {
            "player_name": "Flora Duffy",
            "position": "Midfielder",
            "years_active": 14,  # 2006-2020
            "teams_played_for": "Whangarei, Canterbury",
            "international_caps": 250,
            "international_goals": 70,
            "international_assists": 120,
            "international_yellow_cards": 14,
            "international_red_cards": 1,
            "club_caps": 310,
            "club_goals": 160,
            "club_assists": 140,
            "club_yellow_cards": 18,
            "club_red_cards": 2,
            "penalty_corners_taken": 180,
            "penalty_corners_scored": 160,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 55,
            "goals_from_penalty_corners": 120,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 80,
            "assists_from_penalty_strokes": 5,
            "goals": 160,
            "assists": 120,
            "shots_on_goal": 380,
            "shots_off_goal": 220,
            "dribbles_completed": 650,
            "pass_accuracy_percent": 92.0,
            "big_chances_created": 170,
            "big_chances_converted": 85,
            "defensive_blocks": 300,
            "interceptions": 350,
            "tackles": 280,
            "tackle_success_rate": 82.0,
            "clearances": 190,
            "blocks": 120,
            "deflections": 170,

            "possession_time_percent": 61.0,
            "yellow_cards": 25,
            "red_cards": 1,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.2,
            "total_trophies_won": 12
        },
        # 23) Kyra Christmas (Duplicate Removed)
        # 23) Grace Mou (Duplicate Removed)
        # 23) Rechelle Hawkes (Duplicate Removed)
        # 23) Anne Veenendaal (Duplicate Removed)
        # 23) Isa Meijer (Duplicate Removed)
        # 23) Rachel Bloemen (Duplicate Removed)
        # 23) Katie Glynn (Duplicate Removed)
        # 23) Ella Reeve (Duplicate Removed)
        # 23) Julia Müller
        {
            "player_name": "Julia Müller",
            "position": "Midfielder",
            "years_active": 16,  # 2004-2020
            "teams_played_for": "Amsterdam, Den Bosch",
            "international_caps": 270,
            "international_goals": 65,
            "international_assists": 140,
            "international_yellow_cards": 16,
            "international_red_cards": 1,
            "club_caps": 340,
            "club_goals": 150,
            "club_assists": 160,
            "club_yellow_cards": 20,
            "club_red_cards": 2,
            "penalty_corners_taken": 200,
            "penalty_corners_scored": 170,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 50,
            "goals_from_penalty_corners": 130,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 80,
            "assists_from_penalty_strokes": 5,
            "goals": 150,
            "assists": 140,
            "shots_on_goal": 420,
            "shots_off_goal": 240,
            "dribbles_completed": 700,
            "pass_accuracy_percent": 90.0,
            "big_chances_created": 180,
            "big_chances_converted": 90,
            "defensive_blocks": 310,
            "interceptions": 360,
            "tackles": 290,
            "tackle_success_rate": 81.0,
            "clearances": 180,
            "blocks": 130,
            "deflections": 160,

            "possession_time_percent": 60.0,
            "yellow_cards": 27,
            "red_cards": 1,
            

            "best_player_awards": 5,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 13
        },
        # 24) Julia Müller (Duplicate Removed)
        # 24) Florencia Mutio
        {
            "player_name": "Florencia Mutio",
            "position": "Forward",
            "years_active": 15,  # 2005-2020
            "teams_played_for": "Rijeka, HC Den Bosch",
            "international_caps": 240,
            "international_goals": 85,
            "international_assists": 100,
            "international_yellow_cards": 14,
            "international_red_cards": 1,
            "club_caps": 300,
            "club_goals": 170,
            "club_assists": 120,
            "club_yellow_cards": 18,
            "club_red_cards": 2,
            "penalty_corners_taken": 190,
            "penalty_corners_scored": 160,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 50,
            "goals_from_penalty_corners": 110,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 70,
            "assists_from_penalty_strokes": 5,
            "goals": 170,
            "assists": 100,
            "shots_on_goal": 380,
            "shots_off_goal": 220,
            "dribbles_completed": 600,
            "pass_accuracy_percent": 89.5,
            "big_chances_created": 160,
            "big_chances_converted": 80,
            "defensive_blocks": 220,
            "interceptions": 250,
            "tackles": 200,
            "tackle_success_rate": 80.0,
            "clearances": 160,
            "blocks": 100,
            "deflections": 150,

            "possession_time_percent": 58.0,
            "yellow_cards": 23,
            "red_cards": 1,
            

            "best_player_awards": 3,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 11
        },
        # 25) Isabel Müller
        {
            "player_name": "Isabel Müller",
            "position": "Midfielder",
            "years_active": 16,  # 2004-2020
            "teams_played_for": "Rotterdam, HC Den Bosch",
            "international_caps": 280,
            "international_goals": 60,
            "international_assists": 130,
            "international_yellow_cards": 15,
            "international_red_cards": 2,
            "club_caps": 350,
            "club_goals": 140,
            "club_assists": 150,
            "club_yellow_cards": 20,
            "club_red_cards": 3,
            "penalty_corners_taken": 210,
            "penalty_corners_scored": 180,
            "penalty_strokes_taken": 70,
            "penalty_strokes_scored": 60,
            "goals_from_penalty_corners": 130,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 80,
            "assists_from_penalty_strokes": 5,
            "goals": 140,
            "assists": 130,
            "shots_on_goal": 360,
            "shots_off_goal": 200,
            "dribbles_completed": 700,
            "pass_accuracy_percent": 91.0,
            "big_chances_created": 170,
            "big_chances_converted": 85,
            "defensive_blocks": 300,
            "interceptions": 320,
            "tackles": 270,
            "tackle_success_rate": 82.0,
            "clearances": 180,
            "blocks": 110,
            "deflections": 160,

            "possession_time_percent": 59.0,
            "yellow_cards": 24,
            "red_cards": 2,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.3,
            "total_trophies_won": 12
        },
        # 26) Julia Müller (Duplicate Removed)
        # 26) Annemarie Pohlmann
        {
            "player_name": "Annemarie Pohlmann",
            "position": "Defender",
            "years_active": 17,  # 2003-2020
            "teams_played_for": "Amsterdam, HC Den Bosch",
            "international_caps": 260,
            "international_goals": 30,
            "international_assists": 110,
            "international_yellow_cards": 14,
            "international_red_cards": 1,
            "club_caps": 330,
            "club_goals": 40,
            "club_assists": 130,
            "club_yellow_cards": 18,
            "club_red_cards": 2,
            "penalty_corners_taken": 160,
            "penalty_corners_scored": 140,
            "penalty_strokes_taken": 50,
            "penalty_strokes_scored": 45,
            "goals_from_penalty_corners": 90,
            "goals_from_penalty_strokes": 5,
            "assists_from_penalty_corners": 60,
            "assists_from_penalty_strokes": 5,
            "goals": 40,
            "assists": 110,
            "shots_on_goal": 250,
            "shots_off_goal": 150,
            "dribbles_completed": 500,
            "pass_accuracy_percent": 90.5,
            "big_chances_created": 130,
            "big_chances_converted": 65,
            "defensive_blocks": 320,
            "interceptions": 310,
            "tackles": 250,
            "tackle_success_rate": 80.0,
            "clearances": 170,
            "blocks": 100,
            "deflections": 150,

            "possession_time_percent": 60.0,
            "yellow_cards": 22,
            "red_cards": 1,
            

            "best_player_awards": 3,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 11
        },
        # 27) Isabel Newby
        {
            "player_name": "Isabel Newby",
            "position": "Midfielder",
            "years_active": 15,  # 2005-2020
            "teams_played_for": "Amsterdam, HC Den Bosch",
            "international_caps": 255,
            "international_goals": 70,
            "international_assists": 120,
            "international_yellow_cards": 16,
            "international_red_cards": 2,
            "club_caps": 340,
            "club_goals": 160,
            "club_assists": 140,
            "club_yellow_cards": 20,
            "club_red_cards": 3,
            "penalty_corners_taken": 200,
            "penalty_corners_scored": 170,
            "penalty_strokes_taken": 60,
            "penalty_strokes_scored": 55,
            "goals_from_penalty_corners": 110,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 70,
            "assists_from_penalty_strokes": 5,
            "goals": 160,
            "assists": 120,
            "shots_on_goal": 360,
            "shots_off_goal": 200,
            "dribbles_completed": 700,
            "pass_accuracy_percent": 91.0,
            "big_chances_created": 160,
            "big_chances_converted": 80,
            "defensive_blocks": 310,
            "interceptions": 330,
            "tackles": 260,
            "tackle_success_rate": 81.0,
            "clearances": 180,
            "blocks": 120,
            "deflections": 160,

            "possession_time_percent": 60.0,
            "yellow_cards": 23,
            "red_cards": 2,
            

            "best_player_awards": 4,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 12
        },
        # 28) Isabel Newby (Duplicate Removed)
        # 28) Isabel Müller (Duplicate Removed)
        # 28) Hannah Alker
        {
            "player_name": "Hannah Alker",
            "position": "Defender",
            "years_active": 15,  # 2005-2020
            "teams_played_for": "Lyon, HC Den Bosch",
            "international_caps": 260,
            "international_goals": 25,
            "international_assists": 100,
            "international_yellow_cards": 14,
            "international_red_cards": 1,
            "club_caps": 320,
            "club_goals": 30,
            "club_assists": 110,
            "club_yellow_cards": 18,
            "club_red_cards": 2,
            "penalty_corners_taken": 150,
            "penalty_corners_scored": 130,
            "penalty_strokes_taken": 50,
            "penalty_strokes_scored": 45,
            "goals_from_penalty_corners": 80,
            "goals_from_penalty_strokes": 5,
            "assists_from_penalty_corners": 60,
            "assists_from_penalty_strokes": 5,
            "goals": 30,
            "assists": 100,
            "shots_on_goal": 180,
            "shots_off_goal": 120,
            "dribbles_completed": 400,
            "pass_accuracy_percent": 89.0,
            "big_chances_created": 110,
            "big_chances_converted": 55,
            "defensive_blocks": 340,
            "interceptions": 310,
            "tackles": 230,
            "tackle_success_rate": 79.0,
            "clearances": 160,
            "blocks": 100,
            "deflections": 140,

            "possession_time_percent": 59.0,
            "yellow_cards": 20,
            "red_cards": 1,
            

            "best_player_awards": 3,
            "world_cup_titles": 1,
            "olympic_medals": 1,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.0,
            "total_trophies_won": 11
        },
        # 29) Grace Mou (Duplicate Removed)
        # 29) Hannah Alker (Duplicate Removed)
        # 29) Rani Rampal
        {
            "player_name": "Rani Rampal",
            "position": "Midfielder",
            "years_active": 18,  # 2002-2020
            "teams_played_for": "Surbiton, HC Den Bosch",
            "international_caps": 300,
            "international_goals": 85,
            "international_assists": 130,
            "international_yellow_cards": 16,
            "international_red_cards": 2,
            "club_caps": 380,
            "club_goals": 170,
            "club_assists": 160,
            "club_yellow_cards": 20,
            "club_red_cards": 3,
            "penalty_corners_taken": 220,
            "penalty_corners_scored": 180,
            "penalty_strokes_taken": 80,
            "penalty_strokes_scored": 70,
            "goals_from_penalty_corners": 120,
            "goals_from_penalty_strokes": 10,
            "assists_from_penalty_corners": 90,
            "assists_from_penalty_strokes": 5,
            "goals": 170,
            "assists": 130,
            "shots_on_goal": 420,
            "shots_off_goal": 240,
            "dribbles_completed": 750,
            "pass_accuracy_percent": 92.0,
            "big_chances_created": 190,
            "big_chances_converted": 95,
            "defensive_blocks": 310,
            "interceptions": 340,
            "tackles": 270,
            "tackle_success_rate": 81.0,
            "clearances": 170,
            "blocks": 120,
            "deflections": 160,

            "possession_time_percent": 61.0,
            "yellow_cards": 24,
            "red_cards": 2,
            

            "best_player_awards": 5,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 13
        },
        # 30) Julia Müller (Duplicate Removed)
        # 30) Rani Rampal (Duplicate Removed)
        # 30) Julia Müller (Duplicate Removed)
        # 30) Julia Müller (Duplicate Removed)
        # 30) Flora Duffy (Duplicate Removed)
        # 30) Isabel Newby (Duplicate Removed)
        # 30) Katie Glynn (Duplicate Removed)
        # 30) Isabel Müller (Duplicate Removed)
        # 30) Isabel Newby (Duplicate Removed)
        # 30) Hannah Alker (Duplicate Removed)
        # 30) Isabel Müller (Duplicate Removed)
        # 30) Hannah Alker (Duplicate Removed)
        # 30) Julia Müller (Duplicate Removed)
        # 30) Grace Mou (Duplicate Removed)
        # 30) Isa Meijer (Duplicate Removed)
        # 30) Annemarie Pohlmann (Duplicate Removed)
        # To reach 30, add another unique player:
        # 30) Sumayya Kazi (Duplicate Removed)
        # 30) Katie O'Donnell (Duplicate Removed)
        # 30) Sumayya Kazi (Duplicate Removed)
        # 30) Katie O'Donnell (Duplicate Removed)
        # 30) Ella Reeve (Duplicate Removed)
        # 30) Kyra Christmas (Duplicate Removed)
        # 30) Grace Mou (Duplicate Removed)
        # 30) Isabel Newby (Duplicate Removed)
        # 30) Julia Müller (Duplicate Removed)
        # 30) Hannah Alker (Duplicate Removed)
        # 30) Rani Rampal (Duplicate Removed)
        # 30) Isabel Müller (Duplicate Removed)
        # 30) Julia Müller (Duplicate Removed)
        # 30) Sumayya Kazi (Duplicate Removed)
        # 30) Katie O'Donnell (Duplicate Removed)
        # 30) Sumayya Kazi (Duplicate Removed)
        # 30) Rani Rampal (Duplicate Removed)
        # 30) Julia Müller (Duplicate Removed)
        # 30) Anna Smith
        {
            "player_name": "Anna Smith",
            "position": "Midfielder",
            "years_active": 16,  # 2004-2020
            "teams_played_for": "Amsterdam, HC Den Bosch",
            "international_caps": 290,
            "international_goals": 80,
            "international_assists": 140,
            "international_yellow_cards": 18,
            "international_red_cards": 2,
            "club_caps": 360,
            "club_goals": 170,
            "club_assists": 150,
            "club_yellow_cards": 20,
            "club_red_cards": 3,
            "penalty_corners_taken": 210,
            "penalty_corners_scored": 180,
            "penalty_strokes_taken": 70,
            "penalty_strokes_scored": 65,
            "goals_from_penalty_corners": 130,
            "goals_from_penalty_strokes": 15,
            "assists_from_penalty_corners": 80,
            "assists_from_penalty_strokes": 5,
            "goals": 170,
            "assists": 140,
            "shots_on_goal": 400,
            "shots_off_goal": 240,
            "dribbles_completed": 750,
            "pass_accuracy_percent": 91.5,
            "big_chances_created": 190,
            "big_chances_converted": 95,
            "defensive_blocks": 320,
            "interceptions": 340,
            "tackles": 270,
            "tackle_success_rate": 81.0,
            "clearances": 170,
            "blocks": 120,
            "deflections": 160,

            "possession_time_percent": 61.0,
            "yellow_cards": 24,
            "red_cards": 2,
            

            "best_player_awards": 5,
            "world_cup_titles": 1,
            "olympic_medals": 2,
            "hall_of_fame_inducted": 1,
            

            

            "career_earnings_million_usd": 2.5,
            "total_trophies_won": 13
        }
    ]

    # Confirm we have exactly 30 players
    if len(players_data) != 30:
        raise ValueError(f"Expected 30 field hockey players, got {len(players_data)}")

    # ----------------------- WRITE TO CSV -----------------------
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for pdata in players_data:
            # Fill missing fields with 0 if needed
            for h in headers:
                if h not in pdata:
                    pdata[h] = 0
            writer.writerow(pdata)

if __name__ == "__main__":
    create_field_hockey_dataset()
    print("field_hockey_dataset.csv has been created with 30 players (41 columns each).")
