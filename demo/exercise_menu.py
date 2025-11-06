import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Window
import sqlite3

class ExerciseMenu(ttk.Frame):
    def __init__(self, master, selected_equipment, on_exercise_selected, on_back):
        super().__init__(master)
        self.selected_equipment = selected_equipment
        self.on_exercise_selected = on_exercise_selected
        self.on_back = on_back
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_exercises()

    def create_widgets(self):
        title = ttk.Label(
            self, 
            text=f"Exercises for {self.selected_equipment}", 
            font=("Arial", 20, "bold"), 
            pady=10
            )
        title.pack()

        self.listbox = ttk.Listbox(self, font=("Arial", 14), height=20)
        self.listbox.pack(fill="both", expand=True, padx=20, pady=10)
        self.listbox.bind("<Double-1>", self.on_exercise_double_click)

        back_button = ttk.Button(
            self, 
            text="Back", 
            style="warning",
            font=("Arial", 16), 
            command=self.on_back
            )
        back_button.pack(pady=10)

    def load_exercises(self):
        conn = sqlite3.connect('exercises.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title FROM exercises WHERE equipment = ?", 
            (self.selected_equipment,)
            )
        exercises = cursor.fetchall()
        conn.close()

        for exercise in exercises:
            self.listbox.insert(ttk.END, exercise[0])

    def on_exercise_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            exercise_name = self.listbox.get(selection[0])
            self.on_exercise_selected(exercise_name)