import tkinter as tk
from tkinter import messagebox, ttk  
from tkcalendar import Calendar  
class Journal:
    def __init__(self, root, database, back_callback):
        self.root = root
        self.database = database
        self.back_callback = back_callback  

        self.journal_window = tk.Toplevel(root)
        self.journal_window.title("Golf Journal")
        self.journal_window.geometry("450x700") 

        self.canvas = tk.Canvas(self.journal_window)
        self.scrollbar = tk.Scrollbar(self.journal_window, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.create_content(self.scroll_frame)

    def create_content(self, frame):
        tk.Button(frame, text="Back", command=self.go_back).pack(pady=5)

        tk.Label(frame, text="Select Date:").pack(pady=5)
        self.calendar = Calendar(frame)
        self.calendar.pack(pady=5)

        tk.Label(frame, text="Hours of Sleep:").pack(pady=5)
        self.sleep_entry = tk.Entry(frame)
        self.sleep_entry.pack(pady=5)

        tk.Label(frame, text="How Do You Feel:").pack(pady=5)
        self.feeling_entry = tk.Entry(frame, width=50)
        self.feeling_entry.pack(pady=5)

        tk.Label(frame, text="Number of Meals:").pack(pady=5)
        self.meal_count_var = tk.StringVar()
        self.meal_count_dropdown = ttk.Combobox(
            frame, textvariable=self.meal_count_var, state="readonly"
        )
        self.meal_count_dropdown["values"] = [str(i) for i in range(1, 13)]  
        self.meal_count_dropdown.pack(pady=5)
        self.meal_count_dropdown.bind("<<ComboboxSelected>>", self.update_meal_inputs)

        self.meals_frame = tk.Frame(frame)
        self.meals_frame.pack(pady=5)

        tk.Label(frame, text="Notes:").pack(pady=5)
        self.notes_text = tk.Text(frame, width=40, height=10)
        self.notes_text.pack(pady=10)

        tk.Button(frame, text="Save Entry", command=self.save_entry).pack()

    def update_meal_inputs(self, event=None):
        for widget in self.meals_frame.winfo_children():
            widget.destroy()

        try:
            meal_count = int(self.meal_count_var.get())
        except ValueError:
            return

        self.meal_entries = []
        for i in range(meal_count):
            tk.Label(self.meals_frame, text=f"Meal {i + 1}:").pack(pady=2)
            entry = tk.Entry(self.meals_frame, width=50)
            entry.pack(pady=2)
            self.meal_entries.append(entry)

    def save_entry(self):
        date = self.calendar.get_date()
        sleep = self.sleep_entry.get().strip()
        feeling = self.feeling_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        # Gather meals
        meals = [entry.get().strip() for entry in self.meal_entries if entry.get().strip()]

        if date and (sleep or feeling or notes or meals):
            entry = {
                "Date": date,
                "Hours of Sleep": sleep,
                "How You Feel": feeling,
                "Meals": meals,
                "Notes": notes,
            }
            self.database.save_journal_entry(entry)
            messagebox.showinfo("Success", "Journal entry saved.")
            self.journal_window.destroy()
            self.back_callback()  
        else:
            messagebox.showwarning("Empty Entry", "Please fill out at least one field.")

    def go_back(self):
        self.journal_window.destroy()
        self.back_callback()
