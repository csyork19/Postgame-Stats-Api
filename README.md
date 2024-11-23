
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

## Contributions  
Contributions are welcome! Feel free to submit issues or create pull requests to improve the API.  

## License  
This project is licensed under the MIT License.  
