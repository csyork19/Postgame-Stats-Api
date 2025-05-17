
# PostGame Stats API  

PostGame Stats is a **Flask-based REST API** that provides free access to comprehensive **NBA statistics**. The API offers detailed player and team data, as well as visualized shot charts, making it an ideal resource for analysts, developers, and basketball enthusiasts looking to integrate NBA stats into their projects.  

## Features  
- **Player Statistics**: Access player performance metrics, including points, rebounds, assists, and more.  
- **Team Statistics**: Retrieve team-level data such as standings, win-loss records, and advanced stats.  
- **Shot Charts**: Get shot location data visualized on a court for individual players or teams.  
- **Free and Accessible**: Open to all users without any subscription or access fees.  

## Technology Stack  
- **Backend**: Python Flask  
- **API**: RESTful architecture for seamless integration  
- **Data Processing**: Powered by Pandas for efficient manipulation and analysis  

## Usage  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/postgame-stats.git  
   cd postgame-stats  
   ```  
4. Access the API at `http://127.0.0.1:5000`.  

## Example Endpoints  
- **Player Stats**: `/api/nba/player/seasonAverages`  
- **Team Stats**: `/api/team/seasonStats`  
- **Team Playoff Ststs**: `/api/team/playoffStats`

## Sample Request
- **Player Stats**: `/api/nba/player/perSeasonAverages`  
```
{
    "playerName": "Mark Williams",
    "season": "2024-25"
}
```
- **Player Stats**: `/api/team/playoffStats`
```
{
    "teamName": "Golden State Warriors",
    "season": "2024-25"
}
```

## Sample Response
- **Player Stats**: `/api/nba/player/perSeasonAverages`  
```
[
    {
        "AST": 1,
        "BLK": 2,
        "DREB": 1,
        "FG3A": 0,
        "FG3M": 0,
        "FG3_PCT": 0.0,
        "FGA": 4,
        "FGM": 2,
        "FG_PCT": 0.5,
        "FTA": 0,
        "FTM": 0,
        "FT_PCT": 0.0,
        "GAME_DATE": "Dec 08, 2023",
        "MATCHUP": "CHA vs. TOR",
        "MIN": 20,
        "OREB": 2,
        "PF": 2,
        "PLUS_MINUS": 5,
        "PTS": 4,
        "REB": 3,
        "STL": 1,
        "TOV": 1,
        "WL": "W"
    },
    {
        "AST": 0,
        "BLK": 0,
        "DREB": 4,
        "FG3A": 0,
        "FG3M": 0,
        "FG3_PCT": 0.0,
        "FGA": 6,
        "FGM": 4,
        "FG_PCT": 0.667,
        "FTA": 4,
        "FTM": 3,
        "FT_PCT": 0.75,
        "GAME_DATE": "Dec 02, 2023",
        "MATCHUP": "CHA vs. MIN",
        "MIN": 29,
        "OREB": 2,
        "PF": 6,
        "PLUS_MINUS": -8,
        "PTS": 11,
        "REB": 6,
        "STL": 0,
        "TOV": 1,
        "WL": "L"
    },
    {
        "AST": 1,
        "BLK": 3,
        "DREB": 7,
        "FG3A": 0,
        "FG3M": 0,
        "FG3_PCT": 0.0,
        "FGA": 12,
        "FGM": 5,
        "FG_PCT": 0.417,
        "FTA": 2,
        "FTM": 2,
        "FT_PCT": 1.0,
        "GAME_DATE": "Nov 30, 2023",
        "MATCHUP": "CHA @ BKN",
        "MIN": 32,
        "OREB": 5,
        "PF": 2,
        "PLUS_MINUS": -2,
        "PTS": 12,
        "REB": 12,
        "STL": 1,
        "TOV": 0,
        "WL": "W"
    },
    {
        "AST": 0,
        "BLK": 0,
        "DREB": 6,
        "FG3A": 0,
        "FG3M": 0,
        "FG3_PCT": 0.0,
        "FGA": 9,
        "FGM": 5,
        "FG_PCT": 0.556,
        "FTA": 2,
        "FTM": 2,
        "FT_PCT": 1.0,
        "GAME_DATE": "Nov 28, 2023",
        "MATCHUP": "CHA @ NYK",
        "MIN": 25,
        "OREB": 6,
        "PF": 2,
        "PLUS_MINUS": -7,
        "PTS": 12,
        "REB": 12,
        "STL": 1,
        "TOV": 0,
        "WL": "L"
    }
]
.
.
.
.
```

## Contributions  
Contributions are welcome! Feel free to submit issues or create pull requests to improve the API.  

## License  
This project is licensed under the MIT License.  
