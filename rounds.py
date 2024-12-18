import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Round:
    def __init__(self, root, database, back_callback):
        self.root = root
        self.database = database
        self.back_callback = back_callback  

        self.round_window = tk.Toplevel(root)
        self.round_window.title("Add New Round")
        self.round_window.geometry("650x550")  

        tk.Label(self.round_window, text="Par of the Course:").pack(pady=5)
        self.par_entry = tk.Entry(self.round_window)
        self.par_entry.pack(pady=5)

        tk.Label(self.round_window, text="Score:").pack(pady=5)
        self.score_entry = tk.Entry(self.round_window)
        self.score_entry.pack(pady=5)

        fairways_frame = tk.Frame(self.round_window)
        fairways_frame.pack(pady=5)
        tk.Label(fairways_frame, text="Fairways Hit:").pack(side=tk.LEFT, padx=5)
        self.fairways_hit_entry = tk.Entry(fairways_frame, width=10)
        self.fairways_hit_entry.pack(side=tk.LEFT)
        tk.Label(fairways_frame, text="Total Fairways Attempted:").pack(side=tk.LEFT, padx=5)
        self.fairways_attempted_entry = tk.Entry(fairways_frame, width=10)
        self.fairways_attempted_entry.pack(side=tk.LEFT)

        greens_frame = tk.Frame(self.round_window)
        greens_frame.pack(pady=5)
        tk.Label(greens_frame, text="Greens Hit:").pack(side=tk.LEFT, padx=5)
        self.greens_hit_entry = tk.Entry(greens_frame, width=10)
        self.greens_hit_entry.pack(side=tk.LEFT)
        tk.Label(greens_frame, text="Total Greens Attempted:").pack(side=tk.LEFT, padx=5)
        self.greens_attempted_entry = tk.Entry(greens_frame, width=10)
        self.greens_attempted_entry.pack(side=tk.LEFT)

        tk.Label(self.round_window, text="Number of Putts:").pack(pady=5)
        self.putts_entry = tk.Entry(self.round_window)
        self.putts_entry.pack(pady=5)

        up_down_frame = tk.Frame(self.round_window)
        up_down_frame.pack(pady=5)
        tk.Label(up_down_frame, text="Up-and-Downs (Successful):").pack(side=tk.LEFT, padx=5)
        self.up_down_entry = tk.Entry(up_down_frame, width=10)
        self.up_down_entry.pack(side=tk.LEFT)
        tk.Label(up_down_frame, text="Total Up-and-Down Attempts:").pack(side=tk.LEFT, padx=5)
        self.up_down_attempts_entry = tk.Entry(up_down_frame, width=10)
        self.up_down_attempts_entry.pack(side=tk.LEFT)

        tk.Label(self.round_window, text="Notes:").pack(pady=5)
        self.notes_entry = tk.Text(self.round_window, height=5, width=40)
        self.notes_entry.pack(pady=5)

        tk.Button(self.round_window, text="Save Round", command=self.save_round).pack(pady=10)

        back_button = ttk.Button(self.round_window, text="Back", command=self.go_back)
        back_button.pack(pady=10)

    def save_round(self):
        try:
            par = int(self.par_entry.get())
            score = int(self.score_entry.get())
            fairways_hit = int(self.fairways_hit_entry.get())
            fairways_attempted = int(self.fairways_attempted_entry.get())
            greens_hit = int(self.greens_hit_entry.get())
            greens_attempted = int(self.greens_attempted_entry.get())  
            putts = int(self.putts_entry.get())
            up_downs = int(self.up_down_entry.get())
            up_down_attempts = int(self.up_down_attempts_entry.get())
            notes = self.notes_entry.get("1.0", tk.END).strip()

            if not (0 <= fairways_hit <= fairways_attempted <= 18):
                raise ValueError("Fairways hit must be between 0 and total fairways attempted (0 to 18).")
            if not (0 <= greens_hit <= 18):
                raise ValueError("Greens in regulation must be between 0 and 18.")
            if par <= 0:
                raise ValueError("Par must be a positive number.")
            if score <= 0:
                raise ValueError("Score must be a positive number.")
            if not (0 <= up_downs <= up_down_attempts <= 18):
                raise ValueError("Up-and-downs hit must be between 0 and total up-and-down attempts.")

            self.database.save_round(
                par=par,
                score=score,
                fairways_hit=fairways_hit,
                fairways_attempted=fairways_attempted,
                greens_hit=greens_hit,
                greens_attempted=greens_attempted, 
                putts=putts,
                up_downs=up_downs,
                up_down_attempts=up_down_attempts,
                notes=notes
            )

            messagebox.showinfo("Success", "Round saved successfully!")
            
            self.clear_inputs()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def clear_inputs(self):
        self.par_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)
        self.fairways_hit_entry.delete(0, tk.END)
        self.fairways_attempted_entry.delete(0, tk.END)
        self.greens_hit_entry.delete(0, tk.END)
        self.greens_attempted_entry.delete(0, tk.END)
        self.putts_entry.delete(0, tk.END)
        self.up_down_entry.delete(0, tk.END)
        self.up_down_attempts_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

    def go_back(self):
        self.round_window.destroy()  
        self.back_callback()  
