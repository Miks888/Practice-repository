
import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


class FootballLeagueTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("La Liga Tracker")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)

        # Initial team list for demonstration.
        self.teams = [
            "Barcelona",
            "Real Madrid",
            "Atletico Madrid",
            "Athletic Club",
            "Real Sociedad",
            "Villarreal",
            "Real Betis",
            "Sevilla",
            "Valencia",
            "Girona",
            "Getafe",
            "Osasuna",
            "Celta Vigo",
            "Mallorca",
            "Rayo Vallecano",
            "Las Palmas",
            "Espanyol",
            "Leganes",
            "Real Valladolid",
            "Alaves",
        ]

        self.data_file = Path(__file__).with_name("matches.json")
        self.matches = self.load_matches()

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="La Liga Football League Tracker",
            font=("Arial", 20, "bold"),
        )
        title.pack(pady=(15, 5))

        subtitle = ttk.Label(
            self.root,
            text="Record match results and follow the league standings",
        )
        subtitle.pack(pady=(0, 12))

        self.create_match_form()
        self.create_standings_table()

    def create_match_form(self):
        form = ttk.LabelFrame(self.root, text="Enter Match Result")
        form.pack(fill="x", padx=20, pady=8)

        self.home_team = tk.StringVar(value=self.teams[0])
        self.away_team = tk.StringVar(value=self.teams[1])
        self.home_goals = tk.StringVar(value="0")
        self.away_goals = tk.StringVar(value="0")

        ttk.Label(form, text="Home team").grid(
            row=0, column=0, padx=6, pady=10
        )
        ttk.Combobox(
            form,
            textvariable=self.home_team,
            values=self.teams,
            state="readonly",
            width=19,
        ).grid(row=0, column=1, padx=6, pady=10)

        ttk.Label(form, text="Goals").grid(
            row=0, column=2, padx=6, pady=10
        )
        ttk.Entry(
            form,
            textvariable=self.home_goals,
            width=6,
        ).grid(row=0, column=3, padx=6, pady=10)

        ttk.Label(form, text="Away team").grid(
            row=0, column=4, padx=6, pady=10
        )
        ttk.Combobox(
            form,
            textvariable=self.away_team,
            values=self.teams,
            state="readonly",
            width=19,
        ).grid(row=0, column=5, padx=6, pady=10)

        ttk.Label(form, text="Goals").grid(
            row=0, column=6, padx=6, pady=10
        )
        ttk.Entry(
            form,
            textvariable=self.away_goals,
            width=6,
        ).grid(row=0, column=7, padx=6, pady=10)

        ttk.Button(
            form,
            text="Save Result",
            command=self.add_match,
        ).grid(row=1, column=0, columnspan=8, pady=(0, 10))

    def create_standings_table(self):
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "position",
            "team",
            "played",
            "won",
            "drawn",
            "lost",
            "gf",
            "ga",
            "gd",
            "points",
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20,
        )

        headings = {
            "position": "Pos",
            "team": "Team",
            "played": "P",
            "won": "W",
            "drawn": "D",
            "lost": "L",
            "gf": "GF",
            "ga": "GA",
            "gd": "GD",
            "points": "Pts",
        }

        widths = {
            "position": 55,
            "team": 220,
            "played": 65,
            "won": 65,
            "drawn": 65,
            "lost": 65,
            "gf": 65,
            "ga": 65,
            "gd": 65,
            "points": 70,
        }

        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(
                column,
                width=widths[column],
                anchor="center",
            )

        self.table.column("team", anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview,
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_matches(self):
        if not self.data_file.exists():
            return []

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                matches = json.load(file)

            if not isinstance(matches, list):
                raise ValueError("The saved data must be a list of matches.")

            for match in matches:
                if not isinstance(match, dict):
                    raise ValueError("A match entry is not valid.")

                home = match.get("home")
                away = match.get("away")
                home_goals = match.get("home_goals")
                away_goals = match.get("away_goals")

                if home not in self.teams or away not in self.teams:
                    raise ValueError("A saved match contains an unknown team.")

                if home == away:
                    raise ValueError("A team cannot play against itself.")

                if (
                    type(home_goals) is not int
                    or type(away_goals) is not int
                    or home_goals < 0
                    or away_goals < 0
                ):
                    raise ValueError("A saved score is invalid.")

            return matches

        except (OSError, json.JSONDecodeError, ValueError) as error:
            messagebox.showerror(
                "Loading Error",
                f"Could not load saved matches:\n{error}",
            )
            return []

    def save_matches(self):
        try:
            with self.data_file.open("w", encoding="utf-8") as file:
                json.dump(self.matches, file, indent=4)
            return True

        except OSError as error:
            messagebox.showerror(
                "Saving Error",
                f"Could not save match results:\n{error}",
            )
            return False

    def add_match(self):
        home = self.home_team.get()
        away = self.away_team.get()

        if home == away:
            messagebox.showerror(
                "Invalid Match",
                "A team cannot play against itself.",
            )
            return

        try:
            home_goals = int(self.home_goals.get())
            away_goals = int(self.away_goals.get())

            if home_goals < 0 or away_goals < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Score",
                "Enter whole numbers of zero or more for both scores.",
            )
            return

        match = {
            "home": home,
            "away": away,
            "home_goals": home_goals,
            "away_goals": away_goals,
        }

        self.matches.append(match)

        if not self.save_matches():
            self.matches.pop()
            return

        self.refresh_table()

        messagebox.showinfo(
            "Result Saved",
            f"{home} {home_goals} - {away_goals} {away}",
        )

    def calculate_standings(self):
        standings = {
            team: {
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "gf": 0,
                "ga": 0,
                "gd": 0,
                "points": 0,
            }
            for team in self.teams
        }

        for match in self.matches:
            home = match["home"]
            away = match["away"]
            home_goals = match["home_goals"]
            away_goals = match["away_goals"]

            home_stats = standings[home]
            away_stats = standings[away]

            home_stats["played"] += 1
            away_stats["played"] += 1

            home_stats["gf"] += home_goals
            home_stats["ga"] += away_goals
            away_stats["gf"] += away_goals
            away_stats["ga"] += home_goals

            if home_goals > away_goals:
                home_stats["won"] += 1
                away_stats["lost"] += 1
                home_stats["points"] += 3

            elif away_goals > home_goals:
                away_stats["won"] += 1
                home_stats["lost"] += 1
                away_stats["points"] += 3

            else:
                home_stats["drawn"] += 1
                away_stats["drawn"] += 1
                home_stats["points"] += 1
                away_stats["points"] += 1

        for stats in standings.values():
            stats["gd"] = stats["gf"] - stats["ga"]

        return sorted(
            standings.items(),
            key=lambda item: (
                -item[1]["points"],
                -item[1]["gd"],
                -item[1]["gf"],
                item[0],
            ),
        )

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for position, (team, stats) in enumerate(
            self.calculate_standings(),
            start=1,
        ):
            self.table.insert(
                "",
                "end",
                values=(
                    position,
                    team,
                    stats["played"],
                    stats["won"],
                    stats["drawn"],
                    stats["lost"],
                    stats["gf"],
                    stats["ga"],
                    stats["gd"],
                    stats["points"],
                ),
            )


if __name__ == "__main__":
    window = tk.Tk()
    app = FootballLeagueTracker(window)
    window.mainloop()
