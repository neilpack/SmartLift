import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Window
import sqlite3

class ExerciseDetails(tk.Frame):
    def __init__(self, master, exercise_name, on_back):
        super().__init__(master)
        self.exercise_name = exercise_name
        self.on_back = on_back
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_details()

    def create_widgets(self):
        title = ttk.Label(
            self, 
            text="Exercise Details", 
            font=("Arial", 20, "bold"), 
            pady=10
            )
        title.pack()

        self.details_frame = ttk.Frame(self)
        self.details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        back_button = ttk.Button(
            self, 
            text="Back", 
            style="warning"
            #font=("Arial", 16), 
            command=self.on_back
            )
        back_button.pack(pady=10)

    def load_details(self):
        conn = sqlite3.connect("exercises.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exercises WHERE title = ?", (self.exercise_name,))
        exercise = cursor.fetchone()
        conn.close()

        if exercise:
            details = {
                "Name": exercise[0],
                "Type": exercise[1],
                "Equipment": exercise[2],
                "Muscle Group": exercise[3],
                "Description": exercise[4],
                "Difficulty": exercise[5]
            }

            for key, value in details.items():
                label = ttk.Label(
                    self.details_frame, 
                    text=f"{key}: {value}",
                    font=("Arial", 14), 
                    anchor="w",
                    justify="left",
                    wraplength=800
                )
                label.pack(fill="x", pady=5)
