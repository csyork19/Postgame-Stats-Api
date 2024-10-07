# Postgame-Stats-Api
Python FLASK REST API for sports statistics. This application offers stats for NBA.

# Sample Requests
The endpoints can be invoked with an application such as postman, cli tool, front end application etc.
## Player Season Stats
```
curl -X POST http://localhost:5000/api/nba/player/seasonStats \
-H "Content-Type: application/json" \
-d '{
  "playerName": "LeBron James"
}'
```

## Player Career Stats
```
curl -X POST http://localhost:5000/api/nba/player/careerStats \
-H "Content-Type: application/json" \
-d '{
  "playerName": "Stephen Curry"
}'
```

## Player Playoff Stats
```
curl -X POST http://localhost:5000/api/nba/player/playoffStats \
-H "Content-Type: application/json" \
-d '{
  "playerName": "Kawhi Leonard",
  "season": "2023-24"
}'
```
## Player Shot Chart Coordinates
```
curl -X POST http://localhost:5000/api/nba/player/shotChartCoordinates \
-H "Content-Type: application/json" \
-d '{
  "playerName": "Kevin Durant",
  "season": "2023-24"
}'
```

## Team Season Stats
```
curl -X POST http://localhost:5000/api/nba/team/seasonStats \
-H "Content-Type: application/json" \
-d '{
  "teamName": "Golden State Warriors",
  "season": "2023-24"
}'
```
## Team Playoff Stats
```
curl -X POST http://localhost:5000/api/nba/team/playoffStats \
-H "Content-Type: application/json" \
-d '{
  "teamName": "Miami Heat",
  "season": "2022-23"
}'
```


