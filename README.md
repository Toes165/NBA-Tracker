# GROUP MEMBERS: Anderson, Gurmehhar, Nhieu, Harri

# NBA Live Scoreboard and Standings Tracker

This project is a web-based application that displays live NBA game scores, recent playoff series, and current NBA standings. It is built using Flask (Python) for the backend and HTML, CSS, and JavaScript for the frontend. Data is fetched using the `nba_api` library, found here: https://github.com/swar/nba_api

---

## Features

- Live game updates (refreshed every 30 seconds)
- Tabs for navigating:
  - Current/Upcoming NBA game
  - Recent playoff series/games
  - League standings with wins/losses and rank
- ESPN team logos displayed for each team
- Message shown when there are no scheduled games today
- Display of NBA season year in standings section

---

## Project Structure

/ProjectRoot  
├── nbaAPI.py                 # Flask backend server  
├── /static  
│   └── style.css          # Optional external stylesheet  
├── index.html             # Optional HTML template (if using render_template) 
├── dependencies.txt       # Python package requirements  
├── server.js              # JS server for local testing  
└── README.md              # Project documentation

---

## How to Run

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Step-by-step Instructions

1. **Clone the repository** (or download the files manually):
   ```bash
   git clone https://github.com/Toes165/NBA-Tracker
   cd NBA-Scoreboard
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r 
   flask
   nba_api
   gunicorn
   flask-cors
   ```

4. **Run the Flask app**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to:
   ```
   http://localhost:5000/
   ```

---

## API Endpoints

- `/scoreboard` — Returns today's current or upcoming game and two recent series.
- `/standings` — Returns the NBA standings with team names, wins, and losses.

Both endpoints use `nba_api`:
- `nba_api.live.nba.endpoints.scoreboard`
- `nba_api.stats.endpoints.leaguestandings`

---

## Design Overview

- Tab-based layout (Games | Standings)
- Simple HTML/CSS with JavaScript dynamic content updates
- 30-second auto-polling for live game scores
- Responsive and modern design

---

## Known Issues / Limitations

- Season year is currently '2024-2025'
- Only games for the current day are shown (no future or full schedule)
- For site to work without being locally ran, it needs to be redeployed after 15 minutes of inactivity
---

## Future Enhancements

- Dynamically fetch and display season year
- Add player statistics and box scores
- Add full game schedule and support for other dates
- Improve mobile responsiveness and accessibility

---



