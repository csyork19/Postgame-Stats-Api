class Constants:
    nba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT", "FTA", "FTM", "FT_PCT", "GAME_DATE",
        "MATCHUP", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV", "WL"]
    advanced_stats_columns = [
        "PLAYER_NAME", "TEAM_ABBREVIATION", "MIN", "PTS", "REB", "AST", "STL", "BLK", "TOV", "FGM", "FGA", "FG_PCT",
        "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "PLUS_MINUS"
    ]
    get_advanced_player_stats = ["GAME_ID", "TEAM_ID", "TEAM_ABBREVIATION", "TEAM_CITY", "PLAYER_ID", "PLAYER_NAME",
                       "START_POSITION", "COMMENT", "MIN", "E_OFF_RATING", "OFF_RATING", "E_DEF_RATING", "DEF_RATING",
                       "E_NET_RATING", "NET_RATING", "AST_PCT", "AST_TOV", "AST_RATIO", "OREB_PCT", "DREB_PCT","REB_PCT",
                       "TM_TOV_PCT", "EFG_PCT", "TS_PCT", "USG_PCT", "E_USG_PCT", "E_PACE", "PACE", "PACE_PER40", "POSS",
                                 "PIE"]
    player_stats = [
        "PLAYER_NAME", "TEAM_ABBREVIATION", "MIN", "PTS", "REB", "AST", "STL", "BLK", "TOV", "FGM", "FGA", "FG_PCT",
        "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "PLUS_MINUS"
    ]
    wnba_player_stat_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "GAME_DATE", "MATCHUP", "MIN", "OREB", "PF",
        "PLUS_MINUS", "PTS", "REB", "STL", "TOV", "WL"
    ]
    fields_to_average = ["MIN", "E_OFF_RATING", "OFF_RATING", "E_DEF_RATING", "DEF_RATING", "E_NET_RATING",
                         "NET_RATING",
                         "AST_PCT", "AST_TOV", "AST_RATIO", "OREB_PCT", "DREB_PCT", "REB_PCT", "TM_TOV_PCT", "EFG_PCT",
                         "TS_PCT",
                         "USG_PCT", "E_USG_PCT", "E_PACE", "PACE", "PACE_PER40", "POSS"]
    nba_player_stat_avg_columns = [
        "AST", "BLK", "DREB", "FG3A", "FG3M", "FG3_PCT", "FGA", "FGM", "FG_PCT",
        "FTA", "FTM", "FT_PCT", "MIN", "OREB", "PF", "PLUS_MINUS", "PTS", "REB", "STL", "TOV"]

    team_logo_images = {
        "Philadelphia 76ers": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/76ers.png",
        "Atlanta Hawks": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/atlanta.png",
        "Boston Celtics": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/boston.png",
        "Brooklyn Nets": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/brooklyn.png",
        "Milwaukee Bucks": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/bucks.png",
        "Chicago Bulls": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/bulls.png",
        "Cleveland Cavaliers": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/cavs.png",
        "Los Angeles Clippers": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/clippers.png",
        "Memphis Grizzlies": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/grizzlies.png",
        "Miami Heat": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/heat.png",
        "Charlotte Hornets": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/hornets.png",
        "Utah Jazz": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/jazz.png",
        "Sacramento Kings": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/kings.png",
        "New York Knicks": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/knicks.png",
        "Los Angeles Lakers": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/lakers.png",
        "Orlando Magic": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/magic.png",
        "Dallas Mavericks": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/mavericks.png",
        "Denver Nuggets": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/nuggets.png",
        "Indiana Pacers": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/pacers.png",
        "New Orleans Pelicans": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/pelicans.png",
        "Detroit Pistons": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/pistons.png",
        "Toronto Raptors": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/raptors.png",
        "Houston Rockets": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/rockets.png",
        "San Antonio Spurs": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/spurs.png",
        "Phoenix Suns": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/suns.png",
        "Oklahoma City Thunder": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/thunder.png",
        "Trae Young": "/Users/stormyork/Documents/Personal Projects/Postgame-Stats-Api/Postgame Stats/team_logo/t_young.png"
    }
