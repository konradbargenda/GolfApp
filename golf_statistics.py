import tkinter as tk
from tkinter import ttk
import csv

class StatisticsWindow:
    def __init__(self, root, database, back_callback, pga_data_file='pgaTourData.csv'):
        self.root = root
        self.database = database
        self.back_callback = back_callback  
        
        self.stats_window = tk.Toplevel(self.root)
        self.stats_window.title("Your Rounds Statistics")
        self.stats_window.geometry("400x400")  
        tk.Label(self.stats_window, text="Your Rounds Statistics", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.stats_window, text="Back", command=self.go_back).pack(pady=5)

        self.rounds_data = self.database.get_all_rounds()

        print(f"DEBUG: Rounds data loaded from database: {self.rounds_data}")

        self.pga_players = self.load_pga_players(pga_data_file)

        print(f"DEBUG: Loaded PGA players: {self.pga_players}")  

        tk.Label(self.stats_window, text="Select Rounds to View:").pack(pady=5)
        self.round_options = ["All Rounds", "Last Round", "Last 5 Rounds", "Last 10 Rounds"]
        self.round_var = tk.StringVar()
        self.round_var.set("All Rounds")
        self.round_dropdown = ttk.Combobox(
            self.stats_window, textvariable=self.round_var, values=self.round_options, state="readonly"
        )
        self.round_dropdown.pack(pady=5)
        self.round_dropdown.bind("<<ComboboxSelected>>", self.display_averages)

        tk.Label(self.stats_window, text="Select PGA Player:").pack(pady=5)
        if self.pga_players:
            self.player_var = tk.StringVar()
            self.player_var.set(self.pga_players[0])  
            self.player_dropdown = ttk.Combobox(
                self.stats_window, textvariable=self.player_var, values=self.pga_players, state="readonly"
            )
            self.player_dropdown.pack(pady=5)
            self.player_dropdown.bind("<<ComboboxSelected>>", self.display_player_stats)
        else:
            self.player_var = tk.StringVar()
            self.player_var.set("No Players Available")
            self.player_dropdown = ttk.Combobox(
                self.stats_window, textvariable=self.player_var, values=[self.player_var.get()], state="readonly"
            )
            self.player_dropdown.pack(pady=5)

        self.averages_display = tk.Label(self.stats_window, text="", font=("Helvetica", 12), justify="left")
        self.averages_display.pack(pady=10)

        self.player_stats_display = tk.Label(self.stats_window, text="", font=("Helvetica", 12), justify="left")
        self.player_stats_display.pack(pady=10)

        self.display_averages() 

    def load_pga_players(self, pga_data_file):
        players = []
        try:
            with open(pga_data_file, newline='') as file:
                reader = csv.DictReader(file)
                print(f"DEBUG: CSV Column Names: {reader.fieldnames}")
                for row in reader:
                    players.append(row['Player Name'])
        except FileNotFoundError:
            print(f"DEBUG: File {pga_data_file} not found.")
        return players

    def display_averages(self, event=None):
        option = self.round_var.get()
        all_rounds = self.database.get_all_rounds()

        if not all_rounds:
            self.averages_display.config(text="No rounds available.")
            print("DEBUG: No rounds available.") 
            return

        print(f"DEBUG: Displaying rounds for option '{option}'")

        if option == "All Rounds":
            rounds_to_display = all_rounds
        elif option == "Last Round":
            rounds_to_display = all_rounds[-1:]
        elif option == "Last 5 Rounds":
            rounds_to_display = all_rounds[-5:]
        elif option == "Last 10 Rounds":
            rounds_to_display = all_rounds[-10:]
        else:
            rounds_to_display = all_rounds

        averages = self.calculate_averages(rounds_to_display)

        averages_text = (f"Your Averages for the selected rounds:\n"
                         f"  Average Score: {averages['avg_score']:.2f}\n"
                         f"  Average Fairways Hit: {averages['avg_fairways']:.2f}%\n"
                         f"  Average Putts: {averages['avg_putts']:.2f}\n"
                         f"  Average Up-and-Downs: {averages['avg_up_downs']:.2f}%")
        self.averages_display.config(text=averages_text)
        self.display_player_stats()

    def display_player_stats(self, event=None):
        selected_player = self.player_var.get()
        print(f"DEBUG: Selected player for comparison: {selected_player}")

        player_stats = self.get_player_stats(selected_player)

        if player_stats:
            player_stats_text = (f"Statistics for {selected_player}:\n"
                                 f"  Average Score: {player_stats['avg_score']:.2f}\n"
                                 f"  Fairways Hit: {player_stats['avg_fairways']:.2f}%\n"
                                 f"  Average Putts: {player_stats['avg_putts']:.2f}\n"
                                 f"  Average Up-and-Downs: {player_stats['avg_up_downs']:.2f}%")
            self.player_stats_display.config(text=player_stats_text)
        else:
            self.player_stats_display.config(text="No stats available for this player.")

    def get_player_stats(self, player_name):
        try:
            with open('pgaTourData.csv', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Player Name'] == player_name:
                        return {
                            'avg_score': float(row.get('Average Score', 0)),
                            'avg_fairways': float(row.get('Fairway Percentage', 0)),
                            'avg_putts': float(row.get('Average Putts', 0)),
                            'avg_up_downs': float(row.get('Average Scrambling', 0)),  # Assuming Scrambling is used for up and downs
                        }
        except FileNotFoundError:
            print("DEBUG: pgaTourData.csv not found.")
        return None

    def calculate_averages(self, rounds):
        total_score = 0
        total_fairways_hit = 0
        total_fairways_attempted = 0
        total_putts = 0
        total_up_downs = 0
        total_up_down_attempts = 0
        round_count = len(rounds)

        for round_data in rounds:
            print(f"DEBUG: Round data: {round_data}")

            try:
                total_score += float(round_data.get("Score", 0))
                total_fairways_hit += float(round_data.get("Fairways Hit", 0))
                total_fairways_attempted += float(round_data.get("Fairways Attempted", 0))
                total_putts += float(round_data.get("Putts", 0))
                total_up_downs += float(round_data.get("Up-and-Downs", 0))
                total_up_down_attempts += float(round_data.get("Up-and-Down Attempts", 0))
            except (TypeError, ValueError):
                print("DEBUG: Invalid data detected, skipping.")

        avg_score = total_score / round_count if round_count else 0
        avg_fairways_hit = (total_fairways_hit / total_fairways_attempted * 100) if total_fairways_attempted else 0
        avg_putts = total_putts / round_count if round_count else 0
        avg_up_downs = (total_up_downs / total_up_down_attempts * 100) if total_up_down_attempts else 0

        return {
            "avg_score": avg_score,
            "avg_fairways": avg_fairways_hit,
            "avg_putts": avg_putts,
            "avg_up_downs": avg_up_downs,
        }

    def go_back(self):
        self.stats_window.destroy()
        self.back_callback()  
