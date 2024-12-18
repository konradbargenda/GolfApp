import tkinter as tk
from tkinter import ttk
from golf_database import Database  
from journal import Journal  
from rounds import Round  
from golf_statistics import StatisticsWindow  
from journal_viewer import JournalViewer  
from practice import Practice 

class GolfApp:
    def __init__(self, root, database):
        self.root = root
        self.database = database
        self.root.title("Golf Journal & Statistics")
        self.root.geometry("550x450")

        tk.Label(self.root, text="Golf Journal & Stats", font=("Helvetica", 18, "bold")).pack(pady=10)

        ttk.Button(self.root, text="Golf Journal", width=25, command=self.open_journal).pack(pady=10)
        ttk.Button(self.root, text="Golf Statistics", width=25, command=self.view_statistics).pack(pady=10)
        ttk.Button(self.root, text="Add New Round", width=25, command=self.add_round).pack(pady=10)
        ttk.Button(self.root, text="View Journal Entries", width=25, command=self.open_journal_viewer).pack(pady=10)
        ttk.Button(self.root, text="Practice", width=25, command=self.open_practice).pack(pady=10)

        tk.Label(self.root, text="Enhance your golf game with stats and practice!", font=("Arial", 10, "italic")).pack(pady=20)

    def open_journal(self):
        """Open the Journal window."""
        self.root.withdraw()  
        Journal(self.root, self.database, self.show_main_window)

    def add_round(self):
        """Open the Round entry window."""
        self.root.withdraw()
        Round(self.root, self.database, self.show_main_window)

    def view_statistics(self):
        """Open the Golf Statistics window."""
        self.root.withdraw()
        StatisticsWindow(self.root, self.database, self.show_main_window)

    def open_journal_viewer(self):
        """Open the Journal Viewer window."""
        self.root.withdraw()
        JournalViewer(self.root, self.database, self.show_main_window)

    def open_practice(self):
        """Open the Practice window."""
        self.root.withdraw()
        Practice(self.root, self.database, self.show_main_window)

    def show_main_window(self):
        """Show the main window again."""
        self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    database = Database()  
    app = GolfApp(root, database)
    root.mainloop()
