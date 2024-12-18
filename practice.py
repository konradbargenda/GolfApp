import tkinter as tk
from tkinter import ttk

class Practice:
    def __init__(self, root, database, back_callback):
        self.root = root
        self.database = database
        self.back_callback = back_callback  
        
        self.practice_window = tk.Toplevel(root)
        self.practice_window.title("Golf Practice")

        self.time_label = tk.Label(self.practice_window, text="Enter time you want to spend on practice (minutes):")
        self.time_label.pack()

        self.time_entry = tk.Entry(self.practice_window)
        self.time_entry.pack()

        self.driving_label = tk.Label(self.practice_window, text="Select Driving Exercise:")
        self.driving_label.pack()

        self.driving_var = tk.StringVar(value="Tee Shot Points")
        self.driving_options = [
            "Tee Shot Points",
            "14 Fairways"
        ]
        self.driving_dropdown = ttk.Combobox(self.practice_window, textvariable=self.driving_var, values=self.driving_options)
        self.driving_dropdown.pack()
        self.driving_dropdown.bind("<<ComboboxSelected>>", self.show_driving_exercise)

        self.driving_description = tk.Label(self.practice_window, text="", justify="left", anchor="w")
        self.driving_description.pack()

        self.greens_label = tk.Label(self.practice_window, text="Select Greens Exercise:")
        self.greens_label.pack()

        self.greens_var = tk.StringVar(value="7 Circle Trajectory")
        self.greens_options = [
            "7 Circle Trajectory",
            "Side Danger 50-100",
            "Side Danger 100-150",
            "Side Danger 150-200",
            "7 Circle Trajectory (Hard)"
        ]
        self.greens_dropdown = ttk.Combobox(self.practice_window, textvariable=self.greens_var, values=self.greens_options)
        self.greens_dropdown.pack()
        self.greens_dropdown.bind("<<ComboboxSelected>>", self.show_greens_exercise)

        self.greens_description = tk.Label(self.practice_window, text="", justify="left", anchor="w")
        self.greens_description.pack()

        self.putting_label = tk.Label(self.practice_window, text="Select Putting Exercise:")
        self.putting_label.pack()

        self.putting_var = tk.StringVar(value="Speed Drill")
        self.putting_options = [
            "Speed Drill",
            "Make 100 Putts"
        ]
        self.putting_dropdown = ttk.Combobox(self.practice_window, textvariable=self.putting_var, values=self.putting_options)
        self.putting_dropdown.pack()
        self.putting_dropdown.bind("<<ComboboxSelected>>", self.show_putting_exercise)

        self.putting_description = tk.Label(self.practice_window, text="", justify="left", anchor="w")
        self.putting_description.pack()

        self.chipping_label = tk.Label(self.practice_window, text="Select Chipping Exercise:")
        self.chipping_label.pack()

        self.chipping_var = tk.StringVar(value="Up and Down Challenge")
        self.chipping_options = [
            "Up and Down Challenge",
            "20-Yard Chip Circle Drill"
        ]
        self.chipping_dropdown = ttk.Combobox(self.practice_window, textvariable=self.chipping_var, values=self.chipping_options)
        self.chipping_dropdown.pack()
        self.chipping_dropdown.bind("<<ComboboxSelected>>", self.show_chipping_exercise)

        self.chipping_description = tk.Label(self.practice_window, text="", justify="left", anchor="w")
        self.chipping_description.pack()

        self.submit_button = tk.Button(self.practice_window, text="Submit", command=self.calculate_practice_time)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.practice_window, text="", justify="left", anchor="w")
        self.result_label.pack()

        back_button = tk.Button(self.practice_window, text="Back", command=self.go_back)
        back_button.pack(pady=10)

    def calculate_practice_time(self):
        try:
            total_time = int(self.time_entry.get())
            if total_time <= 0:
                self.result_label.config(text="Please enter a valid number of minutes.")
                return

            driving_time = self.calculate_driving_time()

            greens_time = self.calculate_greens_time()

            putting_time = self.calculate_putting_time()

            chipping_time = self.calculate_chipping_time()

            self.result_label.config(
                text=(
                    f"Based on your time input ({total_time} minutes):\n\n"
                    f"Driving: {driving_time}%\n"
                    f"Greens: {greens_time}%\n"
                    f"Putting: {putting_time}%\n"
                    f"Chipping: {chipping_time}%"
                )
            )

        except ValueError:
            self.result_label.config(text="Please enter a valid number of minutes.")

    def calculate_driving_time(self):
        return 40  

    def calculate_greens_time(self):
        return 30  

    def calculate_putting_time(self):
        return 20  

    def calculate_chipping_time(self):
        return 10  

    def show_driving_exercise(self, event=None):
        exercises = {
            "Tee Shot Points": (
                "You will hit 14 balls with your driver.\n"
                "Pick a different target for each shot.\n"
                "Create 2 zones with the middle being your target:\n"
                "  - 25y wide = 2 points\n"
                "  - 45y wide = 1 point\n\n"
                "Shot rules:\n"
                "  - Shot 1: No penalties.\n"
                "  - Shot 2: Missing 45y zone to the right = -1 point.\n"
                "  - Shot 3: Missing 45y zone to the left = -1 point.\n"
                "  - Shot 4: Missing 45y zone on either side = -1 point, etc.\n\n"
                "Shot 13: No penalties.\n"
                "Shot 14: Penalties on both sides.\n"
                "Write down your score."
            ),
            "14 Fairways": (
                "You take 14 balls and pick a fairway 25 meters wide.\n"
                "You change clubs every shot between your 3 longest clubs in the bag.\n"
                "If you miss the fairway, you add 2 more balls to the pile."
            )
        }
        self.driving_description.config(text=exercises.get(self.driving_var.get(), ""))

    def show_greens_exercise(self, event=None):
        exercises = {
            "7 Circle Trajectory": (
                "Take your 8 iron.\n"
                "How many shots does it take you to hit a ball through each circle?\n"
                "Then take your 5 iron and do the same thing."
            ),
            "Side Danger 50-100": (
                "Targets at 50, 60, 70, 80, 90, 100 yds.\n"
                "Alternate 'dangerous' side for 24 shots.\n"
                "  - Miss dangerous side = -5 points.\n"
                "  - Miss safe side < 5% = 3 points.\n"
                "  - Miss safe side < 10% = 1 point.\n"
                "  - Miss safe side > 10% = 0 points."
            )
        }
        self.greens_description.config(text=exercises.get(self.greens_var.get(), ""))

    def show_putting_exercise(self, event=None):
        exercises = {
            "Speed Drill": (
                "Place 5 balls at 3, 6, 9, 12, and 15 feet.\n"
                "Putt each ball aiming for consistent speed.\n"
                "Repeat 3 rounds for each distance."
            ),
            "Make 100 Putts": (
                "Pick a flat 5-foot putt.\n"
                "Make 100 putts in a row.\n"
                "If you miss, start over!"
            )
        }
        self.putting_description.config(text=exercises.get(self.putting_var.get(), ""))

    def show_chipping_exercise(self, event=None):
        exercises = {
            "Up and Down Challenge": (
                "Pick 10 chipping locations.\n"
                "Chip to the green and try to one-putt.\n"
                "Score 1 point for each successful up and down."
            ),
            "20-Yard Chip Circle Drill": (
                "Pick a 20-yard chip shot.\n"
                "Place targets in a 3-foot circle around the hole.\n"
                "Try to land 10 balls within the circle."
            )
        }
        self.chipping_description.config(text=exercises.get(self.chipping_var.get(), ""))

    def go_back(self):
        self.practice_window.destroy()  
        self.back_callback()  
