import os
import logging
import json
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguestandings
from nba_api.stats.library.http import NBAStatsHTTP
from datetime import datetime

# Initialize Flask app and enable CORS for cross-origin requests
app = Flask(__name__)
CORS(app)

# Set logging level to DEBUG for logging output
logging.basicConfig(level=logging.DEBUG)

# Patch request headers to mimic a browser to avoid being blocked by NBA API
NBAStatsHTTP._headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Referer': 'https://www.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
}

# Serve the homepage


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Simple health check endpoint for the render application


@app.route('/health')
def health():
    return "OK", 200

# Endpoint to get current or upcoming game and 2 recent playoff games


@app.route('/scoreboard')
def get_scoreboard():
    logging.info("Fetching scoreboard...")

    try:
        games = scoreboard.ScoreBoard()  # Live NBA scoreboard from nba_api
        games_json = json.loads(games.get_json())
        games_list = games_json.get('scoreboard', {}).get('games', [])
    except Exception:
        logging.error("Error fetching scoreboard", exc_info=True)
        return jsonify({"error": "Failed to fetch scoreboard data"}), 500

    upcoming_game = None
    for game in games_list:
        status = game.get('gameStatusText', '').lower()
        # Find the first game that has not ended (not marked "final")
        if "final" not in status and not upcoming_game:
            upcoming_game = {
                'date': game.get('gameTimeUTC', 'N/A'),
                'home_team': game.get('homeTeam', {}).get('teamName', 'N/A'),
                'visitor_team': game.get('awayTeam', {}).get('teamName', 'N/A'),
                'home_score': game.get('homeTeam', {}).get('score', 'N/A'),
                'visitor_score': game.get('awayTeam', {}).get('score', 'N/A'),
                'period': game.get('period', 'N/A'),
                'game_status': game.get('gameStatusText', '')
            }

    # Recent game placeholder
    recent_games = [
        {
            "date": "2025-05-28T00:00:00Z",
            "home_team": "Timberwolves",
            "visitor_team": "Thunder",
            "home_score": "94",
            "visitor_score": "124",
            "period": "4",
            "game_status": "Conference finals – Thunder win series 4‑1"
        },
        {
            "date": "2025-05-31T00:00:00Z",
            "home_team": "Pacers",
            "visitor_team": "Knicks",
            "home_score": "125",
            "visitor_score": "108",
            "period": "4",
            "game_status": "Conference finals – Pacers win series 4‑2"
        }
    ]

    logging.info("Scoreboard and recent games served.")
    return jsonify({
        "upcoming": [upcoming_game] if upcoming_game else [],
        "recent": recent_games
    })

# Endpoint to fetch and return current NBA standings


@app.route('/standings')
def get_standings():
    logging.info("Fetching NBA standings...")

    try:
        season_input = '2024-25'  # Specify the season to fetch standings for

        standings_response = leaguestandings.LeagueStandings(
            league_id='00',
            season=season_input,
            season_type='Regular Season'
        )
        logging.info("Standings data successfully fetched.")

        data = standings_response.get_normalized_dict()

        # Defensive check to ensure correct key exists
        if 'Standings' not in data:
            logging.error("Standings key missing in API response")
            return jsonify({"error": "Standings key missing in API response"}), 500

        standings = data['Standings']

        # Create simplified list of standings data for frontend display
        combined = []
        for team in standings:
            combined.append({
                'team': team.get('TeamName', 'N/A'),
                'wins': team.get('WINS', 'N/A'),
                'losses': team.get('LOSSES', 'N/A'),
                'conf': team.get('Conference', 'N/A')
            })

        logging.info(
            f"Returning combined standings for {len(combined)} teams.")
        return jsonify({'standings': combined})

    except Exception as e:
        logging.error("Error fetching standings", exc_info=True)
        return jsonify({"error": f"Failed to fetch standings: {str(e)}"}), 500

# Explicit route for /index.html if directly accessed


@app.route('/index.html')
def serve_index():
    return send_from_directory('.', 'index.html')

# Serve static files (CSS, JS, images)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if not set
    app.run(host='0.0.0.0', port=port)
