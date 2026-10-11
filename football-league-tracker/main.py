
import tkinter as tk
from tkinter import ttk, messagebox


class FootballLeagueTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("La Liga Tracker")
        self.root.geometry("900x550")
        self.root.minsize(750, 450)

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

        self.matches = []

         
        self.create_match_form()

        title = ttk.Label(
            root,
            text="La Liga Football League Tracker",
            font=("Arial", 20, "bold"),
        )
        title.pack(pady=15)

        subtitle = ttk.Label(
            root,
            text="Manage match results and track league standings",
        )
        subtitle.pack(pady=5)

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
            root,
            columns=columns,
            show="headings",
            height=18,
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

        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=70, anchor="center")

        self.table.column("team", width=190, anchor="w")
        self.table.pack(fill="both", expand=True, padx=20, pady=15)

        self.refresh_table()

    def create_match_form(self):
        form = ttk.LabelFrame(self.root, text="Enter Match Result")
        form.pack(fill="x", padx=20, pady=5)

        self.home_team = tk.StringVar(value=self.teams[0])
        self.away_team = tk.StringVar(value=self.teams[1])
        self.home_goals = tk.StringVar(value="0")
        self.away_goals = tk.StringVar(value="0")

        ttk.Label(form, text="Home team:").grid(
            row=0, column=0, padx=5, pady=8
        )
        ttk.Combobox(
            form,
            textvariable=self.home_team,
            values=self.teams,
            state="readonly",
            width=18,
        ).grid(row=0, column=1, padx=5, pady=8)

        ttk.Label(form, text="Goals:").grid(
            row=0, column=2, padx=5, pady=8
        )
        ttk.Entry(
            form, textvariable=self.home_goals, width=5
        ).grid(row=0, column=3, padx=5, pady=8)

        ttk.Label(form, text="Away team:").grid(
            row=0, column=4, padx=5, pady=8
        )
        ttk.Combobox(
            form,
            textvariable=self.away_team,
            values=self.teams,
            state="readonly",
            width=18,
        ).grid(row=0, column=5, padx=5, pady=8)

        ttk.Label(form, text="Goals:").grid(
            row=0, column=6, padx=5, pady=8
        )
        ttk.Entry(
            form, textvariable=self.away_goals, width=5
        ).grid(row=0, column=7, padx=5, pady=8)

        ttk.Button(
            form,
            text="Save Result",
            command=self.add_match,
        ).grid(row=1, column=0, columnspan=8, pady=8)

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

        self.matches.append({
            "home": home,
            "away": away,
            "home_goals": home_goals,
            "away_goals": away_goals,
        })

        self.refresh_table()

        messagebox.showinfo(
            "Result Saved",
            f"{home} {home_goals} - {away_goals} {away}",
        )

    def calculate_standings(self):
        standings = {}

        for team in self.teams:
            standings[team] = {
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "gf": 0,
                "ga": 0,
                "points": 0,
            }

        for match in self.matches:
            home = match["home"]
            away = match["away"]
            home_goals = match["home_goals"]
            away_goals = match["away_goals"]

            standings[home]["played"] += 1
            standings[away]["played"] += 1

            standings[home]["gf"] += home_goals
            standings[home]["ga"] += away_goals
            standings[away]["gf"] += away_goals
            standings[away]["ga"] += home_goals

            if home_goals > away_goals:
                standings[home]["won"] += 1
                standings[away]["lost"] += 1
                standings[home]["points"] += 3
            elif home_goals < away_goals:
                standings[away]["won"] += 1
                standings[home]["lost"] += 1
                standings[away]["points"] += 3
            else:
                standings[home]["drawn"] += 1
                standings[away]["drawn"] += 1
                standings[home]["points"] += 1
                standings[away]["points"] += 1

        for team, stats in standings.items():
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
            self.calculate_standings(), start=1
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
