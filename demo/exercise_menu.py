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
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        # Treeview instead of Listbox
        self.tree = ttk.Treeview(self, show="tree")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree.bind("<Double-1>", self.on_exercise_double_click)

        back_button = ttk.Button(
            self, 
            text="Back", 
            style="warning", 
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
            self.tree.insert("", "end", text=exercise[0])

    def on_exercise_double_click(self, event):

        # Get selected item
        item_id = self.tree.focus()
        if item_id:
            # Get exercise name
            exercise_name = self.tree.item(item_id, "text")
            self.on_exercise_selected(exercise_name)