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
