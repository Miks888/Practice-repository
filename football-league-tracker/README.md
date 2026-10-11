# La Liga Football League Tracker

A Python desktop application for recording football match results and calculating league standings.

## Features

- Display a league table for 20 teams.
- Record home and away match results.
- Validate match scores and prevent teams from playing against themselves.
- Automatically calculate matches played, wins, draws, losses, goals scored, goals conceded, goal difference, and points.
- Sort the table by points, goal difference, and goals scored.
- Save results locally in a JSON file and load them when the application starts.

## Requirements

- Python 3
- Tkinter (usually included with standard Python installations)

## How to Run

Open a terminal in the repository's root folder and run:

```bash
python football-league-tracker/main.py
```

## Data Storage

Match results are stored in `matches.json` in the application folder. The file is created when the first match result is saved.

## Scoring Rules

- Win: 3 points
- Draw: 1 point per team
- Loss: 0 points

## Project Status

This is an educational project. The initial team list is a demonstration list and may not match the current La Liga season.
