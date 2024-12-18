import tkinter as tk
from tkinter import messagebox

class JournalViewer:
    def __init__(self, root, database, back_callback):
        self.root = root
        self.database = database
        self.back_callback = back_callback  
        self.viewer_window = tk.Toplevel(self.root)  
        self.viewer_window.title("View Journal Entries")
        self.viewer_window.geometry("500x500")

        tk.Button(self.viewer_window, text="Back", command=self.go_back).pack(pady=5)

        tk.Label(self.viewer_window, text="Journal Entries", font=("Helvetica", 16)).pack(pady=10)

        self.canvas = tk.Canvas(self.viewer_window)
        self.scrollbar = tk.Scrollbar(self.viewer_window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.load_journal_entries()

    def load_journal_entries(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        entries = self.database.get_all_journal_entries()

        for entry in entries:
            date = entry["Date"]
            sleep = entry.get("Hours of Sleep", "N/A")
            button_text = f"Date: {date} | Sleep: {sleep} hrs"
            button = tk.Button(self.scrollable_frame, text=button_text, width=50,
                               command=lambda e=entry: self.view_entry(e))
            button.pack(pady=5)

    def view_entry(self, entry):
        details_window = tk.Toplevel(self.viewer_window)
        details_window.title("Journal Entry Details")
        details_window.geometry("400x400")

        tk.Label(details_window, text=f"Date: {entry['Date']}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(details_window, text=f"Hours of Sleep: {entry.get('Hours of Sleep', 'N/A')}").pack(pady=5)
        tk.Label(details_window, text=f"How You Feel: {entry.get('How You Feel', 'N/A')}").pack(pady=5)

        meals = entry.get("Meals", [])
        tk.Label(details_window, text="Meals:").pack(pady=5)

        if isinstance(meals, list) and meals:
            for i, meal in enumerate(meals, start=1):
                meal_text = str(meal)  
                tk.Label(details_window, text=f"  Meal {i}: {meal_text}").pack(pady=2)
        elif isinstance(meals, str):  
            meals_list = meals.split()  
            for i, meal in enumerate(meals_list, start=1):
                tk.Label(details_window, text=f"  Meal {i}: {meal}").pack(pady=2)
        else:
            tk.Label(details_window, text="  No meals recorded.").pack(pady=2)

        tk.Label(details_window, text="Notes:").pack(pady=5)
        notes = entry.get("Notes", "No notes available.")
        tk.Label(details_window, text=notes, wraplength=350, justify="left").pack(pady=5)

        tk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)

    def go_back(self):
        self.viewer_window.destroy()
        self.back_callback()

    def refresh_view(self):
        self.load_journal_entries()
