import matplotlib.pyplot as plt

# =====================================================
# TEAM PERFORMANCE
# =====================================================

def team_performance(matches):

    return matches['WinningTeam'].value_counts()


# =====================================================
# RESULT ANALYSIS
# =====================================================

def result_analysis(matches):

    return matches['WonBy'].value_counts()


# =====================================================
# TOSS ANALYSIS
# =====================================================

def toss_win_percentage(matches):

    return (
        matches['TossWinner']
        == matches['WinningTeam']
    ).mean()


def toss_decision_distribution(matches):

    return matches['TossDecision'].value_counts()


# =====================================================
# PLAYER ANALYSIS
# =====================================================

def top_players(matches):

    return (
        matches['Player_of_Match']
        .value_counts()
        .head(10)
    )


# =====================================================
# VENUE ANALYSIS
# =====================================================

def venue_analysis(matches):

    return (
        matches['Venue']
        .value_counts()
        .head(10)
    )


# =====================================================
# SEASON ANALYSIS
# =====================================================

def season_trend(matches):

    return (
        matches['Season']
        .value_counts()
        .sort_index()
    )


# =====================================================
# TOP RUN SCORERS
# =====================================================

def top_run_scorers(deliveries):

    return (
        deliveries
        .groupby('batter')['batsman_run']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )


# =====================================================
# MOST SIXES
# =====================================================

def most_sixes(deliveries):

    return (
        deliveries[deliveries['batsman_run'] == 6]
        .groupby('batter')['batsman_run']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )


# =====================================================
# MOST FOURS
# =====================================================

def most_fours(deliveries):

    return (
        deliveries[deliveries['batsman_run'] == 4]
        .groupby('batter')['batsman_run']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )


# =====================================================
# STRIKE RATE
# =====================================================

def top_strike_rate(deliveries):

    batter_stats = (
        deliveries
        .groupby('batter')
        .agg({
            'batsman_run': 'sum',
            'ballnumber': 'count'
        })
    )

    batter_stats['StrikeRate'] = (
        batter_stats['batsman_run']
        / batter_stats['ballnumber']
    ) * 100

    return (
        batter_stats[
            batter_stats['ballnumber'] >= 500
        ]['StrikeRate']
        .sort_values(ascending=False)
        .head(10)
    )


# =====================================================
# PLOT TEAM PERFORMANCE
# =====================================================

def plot_team_performance(matches):

    team_wins = matches['WinningTeam'].value_counts()

    plt.figure(figsize=(12,6))

    team_wins.plot(kind='bar')

    plt.title("Matches Won by Teams")

    plt.xlabel("Teams")

    plt.ylabel("Wins")

    plt.xticks(rotation=90)

    plt.savefig(
        "outputs/charts/team_performance.png"
    )

    plt.close()


# =====================================================
# PLOT RESULT ANALYSIS
# =====================================================

def plot_result_type(matches):

    result = matches['WonBy'].value_counts()

    plt.figure()

    result.plot(kind='bar')

    plt.title("Match Result Type")

    plt.xlabel("Won By")

    plt.ylabel("Count")

    plt.savefig(
        "outputs/charts/result_type.png"
    )

    plt.close()


# =====================================================
# PLOT TOSS DECISION
# =====================================================

def plot_toss_decision(matches):

    toss = matches['TossDecision'].value_counts()

    plt.figure()

    toss.plot(kind='bar')

    plt.title("Toss Decision Distribution")

    plt.xlabel("Decision")

    plt.ylabel("Count")

    plt.savefig(
        "outputs/charts/toss_decision.png"
    )

    plt.close()


# =====================================================
# PLOT TOP PLAYERS
# =====================================================

def plot_top_players(matches):

    players = (
        matches['Player_of_Match']
        .value_counts()
        .head(10)
    )

    plt.figure(figsize=(12,6))

    players.plot(kind='bar')

    plt.title("Top Player of Match Winners")

    plt.xlabel("Players")

    plt.ylabel("Awards")

    plt.xticks(rotation=45)

    plt.savefig(
        "outputs/charts/top_players.png"
    )

    plt.close()


# =====================================================
# PLOT VENUE ANALYSIS
# =====================================================

def plot_venue_analysis(matches):

    venue = (
        matches['Venue']
        .value_counts()
        .head(10)
    )

    plt.figure(figsize=(12,6))

    venue.plot(kind='bar')

    plt.title("Top Venues")

    plt.xlabel("Venue")

    plt.ylabel("Matches")

    plt.xticks(rotation=90)

    plt.savefig(
        "outputs/charts/venue_analysis.png"
    )

    plt.close()


# =====================================================
# PLOT SEASON TREND
# =====================================================

def plot_season_trend(matches):

    season = (
        matches['Season']
        .value_counts()
        .sort_index()
    )

    plt.figure()

    season.plot(
        kind='line',
        marker='o'
    )

    plt.title("Matches Per Season")

    plt.xlabel("Season")

    plt.ylabel("Matches")

    plt.savefig(
        "outputs/charts/season_trend.png"
    )

    plt.close()


# =====================================================
# PLOT TOP RUN SCORERS
# =====================================================

def plot_top_run_scorers(deliveries):

    top_batters = (
        deliveries
        .groupby('batter')['batsman_run']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12,6))

    top_batters.plot(kind='bar')

    plt.title("Top IPL Run Scorers")

    plt.xlabel("Batters")

    plt.ylabel("Runs")

    plt.xticks(rotation=45)

    plt.savefig(
        "outputs/charts/top_run_scorers.png"
    )

    plt.close()


# =====================================================
# PLOT MOST SIXES
# =====================================================

def plot_most_sixes(deliveries):

    sixes = (
        deliveries[deliveries['batsman_run'] == 6]
        .groupby('batter')['batsman_run']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12,6))

    sixes.plot(kind='bar')

    plt.title("Top 10 Six Hitters")

    plt.xlabel("Batters")

    plt.ylabel("Sixes")

    plt.xticks(rotation=45)

    plt.savefig(
        "outputs/charts/most_sixes.png"
    )

    plt.close()


# =====================================================
# PLOT MOST FOURS
# =====================================================

def plot_most_fours(deliveries):

    fours = (
        deliveries[deliveries['batsman_run'] == 4]
        .groupby('batter')['batsman_run']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12,6))

    fours.plot(kind='bar')

    plt.title("Top 10 Four Hitters")

    plt.xlabel("Batters")

    plt.ylabel("Fours")

    plt.xticks(rotation=45)

    plt.savefig(
        "outputs/charts/most_fours.png"
    )

    plt.close()


# =====================================================
# PLOT STRIKE RATE
# =====================================================

def plot_top_strike_rate(deliveries):

    batter_stats = (
        deliveries
        .groupby('batter')
        .agg({
            'batsman_run': 'sum',
            'ballnumber': 'count'
        })
    )

    batter_stats['StrikeRate'] = (
        batter_stats['batsman_run']
        / batter_stats['ballnumber']
    ) * 100

    strike_rate = (
        batter_stats[
            batter_stats['ballnumber'] >= 500
        ]['StrikeRate']
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12,6))

    strike_rate.plot(kind='bar')

    plt.title("Top IPL Strike Rates")

    plt.xlabel("Batters")

    plt.ylabel("Strike Rate")

    plt.xticks(rotation=45)

    plt.savefig(
        "outputs/charts/strike_rate.png"
    )


    plt.close()
# =====================================================
# MOST WICKETS
# =====================================================

def most_wickets(deliveries):

    return (
        deliveries[
            deliveries['isWicketDelivery'] == 1
        ]
        .groupby('bowler')['isWicketDelivery']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )


# =====================================================
# BEST ECONOMY RATE
# =====================================================

def best_economy(deliveries):

    bowler_stats = (
        deliveries
        .groupby('bowler')
        .agg({
            'total_run': 'sum',
            'ballnumber': 'count'
        })
    )

    bowler_stats['Overs'] = (
        bowler_stats['ballnumber'] / 6
    )

    bowler_stats['Economy'] = (
        bowler_stats['total_run']
        / bowler_stats['Overs']
    )

    return (
        bowler_stats[
            bowler_stats['ballnumber'] >= 500
        ]['Economy']
        .sort_values()
        .head(10)
    )


# =====================================================
# MOST DOT BALLS
# =====================================================

def most_dot_balls(deliveries):

    return (
        deliveries[
            deliveries['total_run'] == 0
        ]
        .groupby('bowler')['total_run']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )


# =====================================================
# PLOT MOST WICKETS
# =====================================================

def plot_most_wickets(deliveries):

    wickets = (
        deliveries[
            deliveries['isWicketDelivery'] == 1
        ]
        .groupby('bowler')['isWicketDelivery']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12,6))

    wickets.plot(kind='bar')

    plt.title("Top 10 Wicket Takers")

    plt.xlabel("Bowlers")

    plt.ylabel("Wickets")

    plt.xticks(rotation=45)

    plt.savefig(
        "outputs/charts/most_wickets.png"
    )

    plt.close()


# =====================================================
# PLOT BEST ECONOMY
# =====================================================

def plot_best_economy(deliveries):

    bowler_stats = (
        deliveries
        .groupby('bowler')
        .agg({
            'total_run': 'sum',
            'ballnumber': 'count'
        })
    )

    bowler_stats['Overs'] = (
        bowler_stats['ballnumber'] / 6
    )

    bowler_stats['Economy'] = (
        bowler_stats['total_run']
        / bowler_stats['Overs']
    )

    economy = (
        bowler_stats[
            bowler_stats['ballnumber'] >= 500
        ]['Economy']
        .sort_values()
        .head(10)
    )

    plt.figure(figsize=(12,6))

    economy.plot(kind='bar')

    plt.title("Best IPL Economy Rates")

    plt.xlabel("Bowlers")

    plt.ylabel("Economy")

    plt.xticks(rotation=45)

    plt.savefig(
        "outputs/charts/best_economy.png"
    )

    plt.close()


# =====================================================
# PLOT MOST DOT BALLS
# =====================================================

def plot_most_dot_balls(deliveries):

    dot_balls = (
        deliveries[
            deliveries['total_run'] == 0
        ]
        .groupby('bowler')['total_run']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12,6))

    dot_balls.plot(kind='bar')

    plt.title("Top Dot Ball Bowlers")

    plt.xlabel("Bowlers")

    plt.ylabel("Dot Balls")

    plt.xticks(rotation=45)

    plt.savefig(
        "outputs/charts/dot_balls.png"
    )

    plt.close()
# =====================================================
# BATTER PROFILE
# =====================================================

def batter_profile(deliveries, batter_name):

    # Filter batter data
    batter_data = deliveries[
        deliveries['batter'] == batter_name
    ]

    # ---------------- TOTAL RUNS ---------------- #

    total_runs = (
        batter_data['batsman_run']
        .sum()
    )

    # ---------------- MATCHES PLAYED ---------------- #

    matches_played = (
        batter_data['ID']
        .nunique()
    )

    # ---------------- STRIKE RATE ---------------- #

    balls_played = len(batter_data)

    strike_rate = (
        total_runs / balls_played
    ) * 100

    # ---------------- FOURS ---------------- #

    fours = (
        batter_data[
            batter_data['batsman_run'] == 4
        ].shape[0]
    )

    # ---------------- SIXES ---------------- #

    sixes = (
        batter_data[
            batter_data['batsman_run'] == 6
        ].shape[0]
    )

    # ---------------- RUNS PER MATCH ---------------- #

    runs_per_match = (
        batter_data
        .groupby('ID')['batsman_run']
        .sum()
    )

    # ---------------- HIGHEST SCORE ---------------- #

    highest_score = (
        runs_per_match.max()
    )

    # ---------------- 50s ---------------- #

    fifties = (
        (
            runs_per_match >= 50
        ) &
        (
            runs_per_match < 100
        )
    ).sum()

    # ---------------- 100s ---------------- #

    hundreds = (
        (
            runs_per_match >= 100
        )
    ).sum()

    # ---------------- RETURN PROFILE ---------------- #

    profile = {

        "Batter": batter_name,

        "Matches": int(matches_played),

        "Runs": int(total_runs),

        "Highest Score":int(highest_score),

        "50s": int(fifties),

        "100s":int(hundreds),

        "Fours":int(fours),

        "Sixes":int(sixes),

        "Strike Rate": round(float(
            strike_rate),
            2
        )
    }

    return profile

# =====================================================
# BOWLER PROFILE
# =====================================================

def bowler_profile(deliveries, bowler_name):

    # Filter bowler data
    bowler_data = deliveries[
        deliveries['bowler'] == bowler_name
    ]

    # ---------------- MATCHES PLAYED ---------------- #

    matches_played = (
        bowler_data['ID']
        .nunique()
    )

    # ---------------- TOTAL WICKETS ---------------- #

    wickets = (
        bowler_data[
            bowler_data['isWicketDelivery'] == 1
        ]
        .shape[0]
    )

    # ---------------- TOTAL RUNS CONCEDED ---------------- #

    runs_conceded = (
        bowler_data['total_run']
        .sum()
    )

    # ---------------- BALLS BOWLED ---------------- #

    balls_bowled = len(bowler_data)

    # ---------------- OVERS ---------------- #

    overs = round(
        balls_bowled / 6,
        1
    )

    # ---------------- ECONOMY ---------------- #

    economy = round(
        runs_conceded / (balls_bowled / 6),
        2
    )

    # ---------------- DOT BALLS ---------------- #

    dot_balls = (
        bowler_data[
            bowler_data['total_run'] == 0
        ]
        .shape[0]
    )

    # =================================================
    # BEST BOWLING SPELL
    # =================================================

    match_wickets = (
        bowler_data
        .groupby('ID')['isWicketDelivery']
        .sum()
    )

    best_match_id = (
        match_wickets.idxmax()
    )

    best_wickets = (
        match_wickets.max()
    )

    best_match_data = (
        bowler_data[
            bowler_data['ID']
            == best_match_id
        ]
    )

    best_runs = (
        best_match_data['total_run']
        .sum()
    )

    best_spell = (
        f"{int(best_wickets)}/{int(best_runs)}"
    )

    # ---------------- RETURN PROFILE ---------------- #

    profile = {

        "Bowler": bowler_name,

        "Matches": int(matches_played),

        "Wickets": int(wickets),

        "Overs": float(overs),

        "Economy": float(economy),

        "Dot Balls": int(dot_balls),

        "Best Spell": best_spell
    }

    return profile
# =====================================================
# HEAD TO HEAD ANALYSIS
# =====================================================

def head_to_head(matches, team1, team2):

    # Filter matches between two teams
    h2h_matches = matches[
        (
            (matches['Team1'] == team1)
            &
            (matches['Team2'] == team2)
        )
        |
        (
            (matches['Team1'] == team2)
            &
            (matches['Team2'] == team1)
        )
    ]

    # Total matches
    total_matches = len(h2h_matches)

    # Team wins
    team1_wins = (
        h2h_matches['WinningTeam']
        == team1
    ).sum()

    team2_wins = (
        h2h_matches['WinningTeam']
        == team2
    ).sum()

    # Win percentages
    if total_matches > 0:

        team1_win_pct = round(
            (team1_wins / total_matches) * 100,
            2
        )

        team2_win_pct = round(
            (team2_wins / total_matches) * 100,
            2
        )

    else:

        team1_win_pct = 0

        team2_win_pct = 0

    # Return dictionary
    result = {

        "Team1": team1,

        "Team2": team2,

        "Total Matches": total_matches,

        f"{team1} Wins": int(team1_wins),

        f"{team2} Wins": int(team2_wins),

        f"{team1} Win %": team1_win_pct,

        f"{team2} Win %": team2_win_pct
    }

    return result

# =====================================================
# SEASON BATTER PROFILE
# =====================================================

def season_batter_profile(
    deliveries,
    batter_name,
    season
):

    # Filter data
    batter_data = deliveries[

        (deliveries['batter'] == batter_name)

        &

        (deliveries['Season'] == season)
    ]

    # ---------------- RUNS ---------------- #

    total_runs = (
        batter_data['batsman_run']
        .sum()
    )

    # ---------------- MATCHES ---------------- #

    matches_played = (
        batter_data['ID']
        .nunique()
    )

    # ---------------- BALLS ---------------- #

    balls = len(batter_data)

    # ---------------- STRIKE RATE ---------------- #

    if balls > 0:

        strike_rate = (
            total_runs / balls
        ) * 100

    else:

        strike_rate = 0

    # ---------------- FOURS ---------------- #

    fours = (
        batter_data[
            batter_data['batsman_run'] == 4
        ].shape[0]
    )

    # ---------------- SIXES ---------------- #

    sixes = (
        batter_data[
            batter_data['batsman_run'] == 6
        ].shape[0]
    )

    # ---------------- RUNS PER MATCH ---------------- #

    runs_per_match = (

        batter_data
        .groupby('ID')['batsman_run']
        .sum()
    )

    # ---------------- HIGHEST SCORE ---------------- #

    highest_score = (

        runs_per_match.max()

        if len(runs_per_match) > 0

        else 0
    )

    # ---------------- 50s ---------------- #

    fifties = (

        (
            runs_per_match >= 50
        )

        &

        (
            runs_per_match < 100
        )

    ).sum()

    # ---------------- 100s ---------------- #

    hundreds = (
        (
            runs_per_match >= 100
        )
    ).sum()

    # ---------------- PROFILE ---------------- #

    profile = {

        "Season": season,

        "Batter": batter_name,

        "Matches": int(matches_played),

        "Runs": int(total_runs),

        "Highest Score": int(highest_score),

        "50s": int(fifties),

        "100s": int(hundreds),

        "Fours": int(fours),

        "Sixes": int(sixes),

        "Strike Rate": round(
            float(strike_rate),
            2
        )
    }

    return profile

# =====================================================
# BATTER CAREER PROGRESSION
# =====================================================

def batter_career_progression(
    deliveries,
    batter_name
):

    batter_data = deliveries[
        deliveries['batter'] == batter_name
    ]

    progression = (

        batter_data
        .groupby('Season')['batsman_run']
        .sum()
        .sort_index()
    )

    return progression

# =====================================================
# 1. HIGHEST TEAM SCORES
# =====================================================

def highest_team_scores(deliveries):

    scores = (

        deliveries

        .groupby(
            ['ID', 'innings', 'BattingTeam']
        )['total_run']

        .sum()

        .reset_index()
    )

    scores = scores.sort_values(

        by='total_run',

        ascending=False
    )

    return scores.head(10)


# =====================================================
# 2. HIGHEST SUCCESSFUL CHASES
# =====================================================

def highest_successful_chases(matches, deliveries):

    innings_scores = (

        deliveries

        .groupby(
            ['ID', 'innings', 'BattingTeam']
        )['total_run']

        .sum()

        .reset_index()
    )

    first_innings = (
        innings_scores[
            innings_scores['innings'] == 1
        ]
    )

    second_innings = (
        innings_scores[
            innings_scores['innings'] == 2
        ]
    )

    merged = second_innings.merge(

        first_innings,

        on='ID',

        suffixes=(
            '_chase',
            '_target'
        )
    )

    successful_chases = merged[
        merged['total_run_chase']
        >
        merged['total_run_target']
    ]

    successful_chases = (
        successful_chases
        .sort_values(
            by='total_run_chase',
            ascending=False
        )
    )

    return successful_chases.head(10)


# =====================================================
# 3. LOWEST DEFENDED TOTALS
# =====================================================

def lowest_defended_totals(matches, deliveries):

    innings_scores = (

        deliveries

        .groupby(
            ['ID', 'innings', 'BattingTeam']
        )['total_run']

        .sum()

        .reset_index()
    )

    first_innings = (
        innings_scores[
            innings_scores['innings'] == 1
        ]
    )

    second_innings = (
        innings_scores[
            innings_scores['innings'] == 2
        ]
    )

    merged = first_innings.merge(

        second_innings,

        on='ID',

        suffixes=(
            '_defend',
            '_chase'
        )
    )

    defended = merged[
        merged['total_run_defend']
        >
        merged['total_run_chase']
    ]

    defended = defended.sort_values(

        by='total_run_defend',

        ascending=True
    )

    return defended.head(10)


# =====================================================
# 4. BIGGEST WIN MARGINS
# =====================================================

def biggest_win_margins(matches):

    big_wins = matches[
        matches['WonBy'] == 'Runs'
    ]

    big_wins = big_wins.sort_values(

        by='Margin',

        ascending=False
    )

    return big_wins[
        [
            'WinningTeam',
            'Team1',
            'Team2',
            'Margin',
            'Season'
        ]
    ].head(10)


# =====================================================
# 5. CLOSEST MATCHES
# =====================================================

def closest_matches(matches):

    close_matches = matches[
        matches['WonBy'] == 'Runs'
    ]

    close_matches = close_matches.sort_values(

        by='Margin',

        ascending=True
    )

    return close_matches[
        [
            'WinningTeam',
            'Team1',
            'Team2',
            'Margin',
            'Season'
        ]
    ].head(10)

# =====================================================
# POWERPLAY RUN SCORERS
# =====================================================

def best_powerplay_batters(deliveries):

    powerplay = deliveries[
        deliveries['overs'] <= 6
    ]

    result = (

        powerplay

        .groupby('batter')['batsman_run']

        .sum()

        .sort_values(ascending=False)

        .head(10)
    )

    return result

# =====================================================
# DEATH OVER RUN SCORERS
# =====================================================

def best_death_over_batters(deliveries):

    death = deliveries[
        deliveries['overs'] >= 16
    ]

    result = (

        death

        .groupby('batter')['batsman_run']

        .sum()

        .sort_values(ascending=False)

        .head(10)
    )

    return result

# =====================================================
# BEST DEATH OVER STRIKE RATE
# =====================================================

def death_over_strike_rate(deliveries):

    death = deliveries[
        deliveries['overs'] >= 16
    ]

    stats = (

        death

        .groupby('batter')

        .agg({
            'batsman_run': 'sum',
            'ballnumber': 'count'
        })
    )

    stats['StrikeRate'] = (

        stats['batsman_run']

        / stats['ballnumber']

    ) * 100

    result = (

        stats[
            stats['ballnumber'] >= 100
        ]['StrikeRate']

        .sort_values(ascending=False)

        .head(10)
    )

    return result

# =====================================================
# BEST POWERPLAY ECONOMY
# =====================================================

def best_powerplay_bowlers(deliveries):

    powerplay = deliveries[
        deliveries['overs'] <= 6
    ]

    stats = (

        powerplay

        .groupby('bowler')

        .agg({
            'total_run': 'sum',
            'ballnumber': 'count'
        })
    )

    stats['Overs'] = (
        stats['ballnumber'] / 6
    )

    stats['Economy'] = (

        stats['total_run']

        / stats['Overs']
    )

    result = (

        stats[
            stats['ballnumber'] >= 100
        ]['Economy']

        .sort_values()

        .head(10)
    )

    return result
# =====================================================
# MOST POWERPLAY WICKETS
# =====================================================

def most_powerplay_wickets(deliveries):

    powerplay = deliveries[
        deliveries['overs'] <= 6
    ]

    result = (

        powerplay[
            powerplay['isWicketDelivery'] == 1
        ]

        .groupby('bowler')['isWicketDelivery']

        .count()

        .sort_values(ascending=False)

        .head(10)
    )

    return result
# =====================================================
# BEST DEATH OVER ECONOMY
# =====================================================

def best_death_bowlers(deliveries):

    death = deliveries[
        deliveries['overs'] >= 16
    ]

    stats = (

        death

        .groupby('bowler')

        .agg({
            'total_run': 'sum',
            'ballnumber': 'count'
        })
    )

    stats['Overs'] = (
        stats['ballnumber'] / 6
    )

    stats['Economy'] = (

        stats['total_run']

        / stats['Overs']
    )

    result = (

        stats[
            stats['ballnumber'] >= 100
        ]['Economy']

        .sort_values()

        .head(10)
    )

    return result

# =====================================================
# MOST DEATH OVER WICKETS
# =====================================================

def most_death_over_wickets(deliveries):

    death = deliveries[
        deliveries['overs'] >= 16
    ]

    result = (

        death[
            death['isWicketDelivery'] == 1
        ]

        .groupby('bowler')['isWicketDelivery']

        .count()

        .sort_values(ascending=False)

        .head(10)
    )

    return result