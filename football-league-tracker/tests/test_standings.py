
import sys
import unittest
from pathlib import Path

# Make main.py importable from the tests folder.
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from main import FootballLeagueTracker


class TestLeagueStandings(unittest.TestCase):
    def setUp(self):
        # Test the calculation logic without opening a GUI window.
        self.app = FootballLeagueTracker.__new__(FootballLeagueTracker)
        self.app.teams = ["Barcelona", "Real Madrid", "Atletico Madrid"]
        self.app.matches = []

    def test_home_win(self):
        self.app.matches = [
            {
                "home": "Barcelona",
                "away": "Real Madrid",
                "home_goals": 2,
                "away_goals": 1,
            }
        ]

        standings = dict(self.app.calculate_standings())

        self.assertEqual(standings["Barcelona"]["points"], 3)
        self.assertEqual(standings["Barcelona"]["won"], 1)
        self.assertEqual(standings["Real Madrid"]["lost"], 1)

    def test_draw(self):
        self.app.matches = [
            {
                "home": "Barcelona",
                "away": "Real Madrid",
                "home_goals": 1,
                "away_goals": 1,
            }
        ]

        standings = dict(self.app.calculate_standings())

        self.assertEqual(standings["Barcelona"]["points"], 1)
        self.assertEqual(standings["Real Madrid"]["points"], 1)
        self.assertEqual(standings["Barcelona"]["drawn"], 1)

    def test_goal_difference(self):
        self.app.matches = [
            {
                "home": "Barcelona",
                "away": "Real Madrid",
                "home_goals": 3,
                "away_goals": 1,
            }
        ]

        standings = dict(self.app.calculate_standings())

        self.assertEqual(standings["Barcelona"]["gd"], 2)
        self.assertEqual(standings["Real Madrid"]["gd"], -2)

    def test_table_is_sorted_by_points(self):
        self.app.matches = [
            {
                "home": "Barcelona",
                "away": "Real Madrid",
                "home_goals": 2,
                "away_goals": 0,
            },
            {
                "home": "Atletico Madrid",
                "away": "Barcelona",
                "home_goals": 1,
                "away_goals": 0,
            },
        ]

        standings = self.app.calculate_standings()

        self.assertEqual(standings[0][0], "Barcelona")
        self.assertEqual(standings[0][1]["points"], 3)


if __name__ == "__main__":
    unittest.main()
