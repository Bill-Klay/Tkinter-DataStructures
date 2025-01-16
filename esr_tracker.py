import csv
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

class ESRTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("E-Sports Results Tracker")

        # Set a larger window size
        self.root.geometry("800x600")  # Width x Height
        self.root.resizable(True, True)  # Allow resizing in both directions
        self.root.minsize(600, 400)  # Set minimum size

        # Initialize dictionaries for in-memory storage
        self.teams = {}
        self.games = {}
        self.matches = []

        # Load initial data from CSV files
        self.load_data()

        # Create main menu
        self.main_menu()

    def load_data(self):
        # Load teams from teams.csv
        try:
            with open('database/teams.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.teams[row[0]] = int(row[1])
        except FileNotFoundError:
            pass

        # Load games from games.csv
        try:
            with open('database/games.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.games[row[0]] = []
        except FileNotFoundError:
            pass

        # Load matches from matches.csv
        try:
            with open('database/matches.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.matches.append({
                        'date': row[0],
                        'game': row[1],
                        'team1': row[2],
                        'team2': row[3],
                        'winner': row[4]
                    })
        except FileNotFoundError:
            pass

    def save_data(self):
        # Save teams to teams.csv
        with open('database/teams.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for team, score in self.teams.items():
                writer.writerow([team, score])

        # Save games to games.csv
        with open('database/games.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for game, _ in self.games.items():
                writer.writerow([game])

        # Save matches to matches.csv
        with open('database/matches.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for match in self.matches:
                writer.writerow([
                    match['date'],
                    match['game'],
                    match['team1'],
                    match['team2'],
                    match['winner']
                ])

    def main_menu(self):
        main_frame = self.clear_frame()

        tk.Button(main_frame, text="Admin Mode", command=self.admin_mode).pack(pady=20)
        tk.Button(main_frame, text="Non-Admin Mode", command=self.non_admin_mode).pack(pady=20)

    def user_mode(self):
        # Implement user mode functionality
        pass

    def admin_mode(self):
        self.clear_frame()  # Method to clear the current frame
        
        admin_frame = tk.Frame(self.root)
        admin_frame.pack(fill="both", expand=True)

        tk.Button(admin_frame, text="View All Teams", command=lambda: self.view_teams(admin_frame)).pack(pady=10)
        tk.Button(admin_frame, text="Add New Team", command=self.add_team).pack(pady=10)
        tk.Button(admin_frame, text="Remove Team", command=lambda: self.remove_team(admin_frame)).pack(pady=10)
        
        tk.Button(admin_frame, text="View All Games", command=lambda: self.view_games(admin_frame)).pack(pady=10)
        tk.Button(admin_frame, text="Add New Game", command=self.add_game).pack(pady=10)
        tk.Button(admin_frame, text="Remove Game", command=lambda: self.remove_game(admin_frame)).pack(pady=10)
        
        tk.Button(admin_frame, text="View All Matches", command=self.view_matches).pack(pady=10)
        tk.Button(admin_frame, text="Record Match Result", command=self.record_match).pack(pady=10)
        
        tk.Button(admin_frame, text="Back to Main Menu", command=self.main_menu).pack(pady=10)

    def non_admin_mode(self):
        self.clear_frame()  # Clear the current frame
        
        non_admin_frame = tk.Frame(self.root)
        non_admin_frame.pack(fill="both", expand=True)

        tk.Button(non_admin_frame, text="Display Last 5 Matches", command=self.display_last_5_matches).pack(pady=10)
        tk.Button(non_admin_frame, text="Overall Scoreboard", command=self.overall_scoreboard).pack(pady=10)
        tk.Button(non_admin_frame, text="Game-Specific Scoreboard", command=self.game_specific_scoreboard).pack(pady=10)
        tk.Button(non_admin_frame, text="Back to Main Menu", command=self.main_menu).pack(pady=20)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create a new frame that expands to fill the window
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        return main_frame

    def view_teams(self, parent_frame=None):
        if parent_frame is None:
            self.clear_frame()
            parent_frame = self.root
        
        tk.Label(parent_frame, text="All Teams").pack()
        
        tree = ttk.Treeview(parent_frame, columns=("Name", "Score"), show='headings')
        tree.heading('Name', text='Team Name')
        tree.heading('Score', text='Points')
        
        for team, score in self.teams.items():
            tree.insert('', 'end', values=(team, score))
        
        tree.pack(expand=True, fill=tk.BOTH)
        
        tk.Button(parent_frame, text="Refresh", command=lambda: self.view_teams(parent_frame)).pack(pady=10)
        tk.Button(parent_frame, text="Back to Admin Menu", command=self.admin_mode).pack(pady=10)


    def add_team(self, parent_frame=None):
        if parent_frame is None:
            self.clear_frame()
            parent_frame = self.root
        
        tk.Label(parent_frame, text="Add New Team").pack()
        
        team_name_label = tk.Label(parent_frame, text="Team Name:")
        team_name_label.pack()
        team_name_entry = tk.Entry(parent_frame)
        team_name_entry.pack()
        
        team_score_label = tk.Label(parent_frame, text="Initial Score (default: 0):")
        team_score_label.pack()
        team_score_entry = tk.Entry(parent_frame)
        team_score_entry.pack()
        
        def submit_new_team():
            team_name = team_name_entry.get().strip()
            team_score = team_score_entry.get().strip()
            
            if team_name:
                if team_name not in self.teams:
                    if team_score.isdigit():
                        self.teams[team_name] = int(team_score)
                    else:
                        self.teams[team_name] = 0
                    
                    self.save_data()
                    result_label.config(text=f"Team '{team_name}' added successfully!", fg="green")
                else:
                    result_label.config(text="Team already exists!", fg="red")
            else:
                result_label.config(text="Please enter a team name.", fg="red")
        
        submit_button = tk.Button(parent_frame, text="Submit", command=submit_new_team)
        submit_button.pack()
        
        result_label = tk.Label(parent_frame, text="")
        result_label.pack()
        
        cancel_button = tk.Button(parent_frame, text="Cancel", command=self.admin_mode)
        cancel_button.pack(pady=10)

    def remove_team(self, parent_frame=None):
        if parent_frame is None:
            self.clear_frame()
            parent_frame = self.root
        
        tk.Label(parent_frame, text="Remove Team").pack()
        
        tree = ttk.Treeview(parent_frame, columns=("Name", "Score"), show='headings')
        tree.heading('Name', text='Team Name')
        tree.heading('Score', text='Points')
        
        for team, score in self.teams.items():
            tree.insert('', 'end', values=(team, score))
        
        tree.pack(expand=True, fill=tk.BOTH)
        
        def remove_selected_team():
            selected_item = tree.selection()[0]
            team_to_remove = tree.item(selected_item)['values'][0]
            
            if team_to_remove in self.teams:
                del self.teams[team_to_remove]
                self.save_data()
                tree.delete(*tree.get_children())
                for team, score in self.teams.items():
                    tree.insert('', 'end', values=(team, score))
                result_label.config(text=f"Team '{team_to_remove}' removed successfully!", fg="green")
            else:
                result_label.config(text="Error: Team not found.", fg="red")
        
        remove_button = tk.Button(parent_frame, text="Remove Selected Team", command=remove_selected_team)
        remove_button.pack(pady=10)
        
        result_label = tk.Label(parent_frame, text="")
        result_label.pack()
        
        tk.Button(parent_frame, text="Back to Admin Menu", command=self.admin_mode).pack(pady=10)

    def view_games(self, parent_frame=None):
        if parent_frame is None:
            self.clear_frame()
            parent_frame = self.root
        
        tk.Label(parent_frame, text="All Games").pack()
        
        tree = ttk.Treeview(parent_frame, columns=("Game"), show='headings')
        tree.heading('Game', text='Game Title')
        
        for game in self.games.keys():
            tree.insert('', 'end', values=(game,))
        
        tree.pack(expand=True, fill=tk.BOTH)
        
        tk.Button(parent_frame, text="Refresh", command=lambda: self.view_games(parent_frame)).pack(pady=10)
        tk.Button(parent_frame, text="Back to Admin Menu", command=self.admin_mode).pack(pady=10)

    def add_game(self, parent_frame=None):
        if parent_frame is None:
            self.clear_frame()
            parent_frame = self.root
        
        tk.Label(parent_frame, text="Add New Game").pack()
        
        game_title_label = tk.Label(parent_frame, text="Game Title:")
        game_title_label.pack()
        game_title_entry = tk.Entry(parent_frame)
        game_title_entry.pack()
        
        def submit_new_game():
            game_title = game_title_entry.get().strip()
            
            if game_title:
                if game_title not in self.games:
                    self.games[game_title] = []
                    self.save_data()
                    result_label.config(text=f"Game '{game_title}' added successfully!", fg="green")
                else:
                    result_label.config(text="Game already exists!", fg="red")
            else:
                result_label.config(text="Please enter a game title.", fg="red")
        
        submit_button = tk.Button(parent_frame, text="Submit", command=submit_new_game)
        submit_button.pack()
        
        result_label = tk.Label(parent_frame, text="")
        result_label.pack()
        
        tk.Button(parent_frame, text="Cancel", command=self.admin_mode).pack(pady=10)

    def remove_game(self, parent_frame=None):
        if parent_frame is None:
            self.clear_frame()
            parent_frame = self.root
        
        tk.Label(parent_frame, text="Remove Game").pack()
        
        tree = ttk.Treeview(parent_frame, columns=("Game"), show='headings')
        tree.heading('Game', text='Game Title')
        
        for game in self.games.keys():
            tree.insert('', 'end', values=(game,))
        
        tree.pack(expand=True, fill=tk.BOTH)
        
        def remove_selected_game():
            selected_item = tree.selection()[0]
            game_to_remove = tree.item(selected_item)['values'][0]
            
            if game_to_remove in self.games:
                del self.games[game_to_remove]
                self.save_data()
                tree.delete(*tree.get_children())
                for game in self.games.keys():
                    tree.insert('', 'end', values=(game,))
                result_label.config(text=f"Game '{game_to_remove}' removed successfully!", fg="green")
            else:
                result_label.config(text="Error: Game not found.", fg="red")
        
        remove_button = tk.Button(parent_frame, text="Remove Selected Game", command=remove_selected_game)
        remove_button.pack(pady=10)
        
        result_label = tk.Label(parent_frame, text="")
        result_label.pack()
        
        tk.Button(parent_frame, text="Back to Admin Menu", command=self.admin_mode).pack(pady=10)

    def record_match(self, parent_frame=None):
        if parent_frame is None:
            self.clear_frame()
            parent_frame = self.root
        
        tk.Label(parent_frame, text="Record Match Result").pack()
        
        date_label = tk.Label(parent_frame, text="Match Date (YYYY-MM-DD):")
        date_label.pack()
        date_entry = tk.Entry(parent_frame)
        date_entry.pack()
        
        game_label = tk.Label(parent_frame, text="Select Game:")
        game_label.pack()
        game_var = tk.StringVar(parent_frame)
        game_var.set(list(self.games.keys())[0])  # default value
        game_option = tk.OptionMenu(parent_frame, game_var, *self.games.keys())
        game_option.pack()
        
        team1_label = tk.Label(parent_frame, text="Select Team 1:")
        team1_label.pack()
        team1_var = tk.StringVar(parent_frame)
        team1_var.set(list(self.teams.keys())[0])  # default value
        team1_option = tk.OptionMenu(parent_frame, team1_var, *self.teams.keys())
        team1_option.pack()
        
        team2_label = tk.Label(parent_frame, text="Select Team 2:")
        team2_label.pack()
        team2_var = tk.StringVar(parent_frame)
        team2_var.set(list(self.teams.keys())[1])  # default value
        team2_option = tk.OptionMenu(parent_frame, team2_var, *self.teams.keys())
        team2_option.pack()
        
        winner_label = tk.Label(parent_frame, text="Select Winner:")
        winner_label.pack()
        winner_var = tk.StringVar(parent_frame)
        winner_var.set(list(self.teams.keys())[0])  # default value
        winner_option = tk.OptionMenu(parent_frame, winner_var, *self.teams.keys())
        winner_option.pack()
        
        def submit_match_result():
            match_date = date_entry.get()
            game = game_var.get()
            team1 = team1_var.get()
            team2 = team2_var.get()
            winner = winner_var.get()
            
            if match_date and game and team1 and team2 and winner:
                self.matches.append({
                    'date': match_date,
                    'game': game,
                    'team1': team1,
                    'team2': team2,
                    'winner': winner
                })
                
                # Update team scores
                if winner == team1:
                    self.teams[team1] += 1
                elif winner == team2:
                    self.teams[team2] += 1
                
                self.save_data()
                result_label.config(text=f"Match recorded successfully!", fg="green")
            else:
                result_label.config(text="Please fill out all fields.", fg="red")
        
        submit_button = tk.Button(parent_frame, text="Submit", command=submit_match_result)
        submit_button.pack()
        
        result_label = tk.Label(parent_frame, text="")
        result_label.pack()
        
        tk.Button(parent_frame, text="Cancel", command=self.admin_mode).pack(pady=10)

    def view_matches(self, parent_frame=None):
        if parent_frame is None:
            self.clear_frame()
            parent_frame = self.root
        
        tk.Label(parent_frame, text="All Matches").pack()
        
        tree = ttk.Treeview(parent_frame, columns=("Date", "Game", "Team1", "Team2", "Winner"), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('Game', text='Game/Sport')
        tree.heading('Team1', text='Team 1')
        tree.heading('Team2', text='Team 2')
        tree.heading('Winner', text='Winner')
        
        for match in self.matches:
            tree.insert('', 'end', values=(
                match['date'],
                match['game'],
                match['team1'],
                match['team2'],
                match['winner']
            ))
        
        tree.pack(expand=True, fill=tk.BOTH)
        
        tk.Button(parent_frame, text="Refresh", command=lambda: self.view_matches(parent_frame)).pack(pady=10)
        tk.Button(parent_frame, text="Back to Admin Menu", command=self.admin_mode).pack(pady=10)

    def display_last_5_matches(self):
        self.clear_frame()  # Clear the current frame
        
        last_5_matches_frame = tk.Frame(self.root)
        last_5_matches_frame.pack(fill="both", expand=True)

        # Sort matches by date in descending order
        sorted_matches = sorted(self.matches, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        
        # Display only the last 5 matches
        last_5_matches = sorted_matches[:5]
        
        if last_5_matches:
            tk.Label(last_5_matches_frame, text="Last 5 Matches:", font=('Arial', 14)).pack(pady=10)
            
            for i, match in enumerate(last_5_matches, 1):
                match_info = f"Date: {match['date']}\n"
                match_info += f"Game: {match['game']}\n"
                match_info += f"Teams: {match['team1']} vs {match['team2']}\n"
                match_info += f"Winner: {match['winner']}"
                
                match_frame = tk.Frame(last_5_matches_frame)
                match_frame.pack(pady=10, padx=10)
                
                tk.Label(match_frame, text=f"Match {i}", font=('Arial', 12, 'bold')).pack()
                tk.Label(match_frame, text=match_info, wraplength=400, justify=tk.LEFT).pack()
        else:
            tk.Label(last_5_matches_frame, text="No matches recorded yet.", font=('Arial', 14)).pack(pady=100)
        
        tk.Button(last_5_matches_frame, text="Back to Non-Admin Mode", command=self.non_admin_mode).pack(pady=20)

    def overall_scoreboard(self):
        self.clear_frame()  # Clear the current frame
        
        scoreboard_frame = tk.Frame(self.root)
        scoreboard_frame.pack(fill="both", expand=True)

        # Sort teams by score in descending order
        sorted_teams = sorted(self.teams.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_teams:
            tk.Label(scoreboard_frame, text="Overall Scoreboard:", font=('Arial', 14)).pack(pady=10)
            
            tree = ttk.Treeview(scoreboard_frame, columns=("Team", "Score"), show='headings')
            tree.heading('Team', text='Team Name')
            tree.heading('Score', text='Points')
            
            for team, score in sorted_teams:
                tree.insert('', 'end', values=(team, score))
            
            tree.pack(expand=True, fill=tk.BOTH)
        else:
            tk.Label(scoreboard_frame, text="No teams recorded yet.", font=('Arial', 14)).pack(pady=100)
        
        tk.Button(scoreboard_frame, text="Back to Non-Admin Mode", command=self.non_admin_mode).pack(pady=20)

    def game_specific_scoreboard(self):
        self.clear_frame()  # Clear the current frame
        
        game_scoreboard_frame = tk.Frame(self.root)
        game_scoreboard_frame.pack(fill="both", expand=True)

        # Get unique games from matches
        games = set(match['game'] for match in self.matches)
        
        if games:
            tk.Label(game_scoreboard_frame, text="Select a Game:", font=('Arial', 12)).pack(pady=10)
            
            game_var = tk.StringVar(game_scoreboard_frame)
            game_var.set(next(iter(games)))  # Set default value
            
            game_option = tk.OptionMenu(game_scoreboard_frame, game_var, *sorted(games))
            game_option.pack(pady=10)
            
            def display_game_scoreboard():
                selected_game = game_var.get()
                
                # Filter matches for the selected game
                game_matches = [match for match in self.matches if match['game'] == selected_game]
                
                # Calculate scores for each team in the game
                game_scores = {}
                for match in game_matches:
                    for team in [match['team1'], match['team2']]:
                        if team not in game_scores:
                            game_scores[team] = 0
                        if team == match['winner']:
                            game_scores[team] += 1
                
                # Sort teams by score in descending order
                sorted_teams = sorted(game_scores.items(), key=lambda x: x[1], reverse=True)
                
                if sorted_teams:
                    tk.Label(game_scoreboard_frame, text=f"{selected_game} Scoreboard:", font=('Arial', 14)).pack(pady=10)
                    
                    tree = ttk.Treeview(game_scoreboard_frame, columns=("Team", "Score"), show='headings')
                    tree.heading('Team', text='Team Name')
                    tree.heading('Score', text='Points')
                    
                    for team, score in sorted_teams:
                        tree.insert('', 'end', values=(team, score))
                    
                    tree.pack(expand=True, fill=tk.BOTH)
                else:
                    tk.Label(game_scoreboard_frame, text="No matches recorded for this game yet.", font=('Arial', 14)).pack(pady=100)
            
            tk.Button(game_scoreboard_frame, text="Display Scoreboard", command=display_game_scoreboard).pack(pady=10)
        
        else:
            tk.Label(game_scoreboard_frame, text="No games recorded yet.", font=('Arial', 14)).pack(pady=100)
        
        tk.Button(game_scoreboard_frame, text="Back to Non-Admin Mode", command=self.non_admin_mode).pack(pady=20)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ESRTracker()
    app.run()
