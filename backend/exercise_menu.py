import tkinter
from tkinter import ttk
import sqlite3

DB_PATH = 'exercises.db'

class ExerciseMenu(ttk.Frame):
    def __init__(self, master, selected_equipment, on_selected_exercise):
        super().__init__(master)
        self.selected_equipment = selected_equipment
        self.on_selected_exercise = on_selected_exercise
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_exercises()

    def create_widgets(self):
        title_label = tkinter.Label(self, text=f"Exercises for {self.selected_equipment}", pady=10)

        # Create a scrollable table for the treeview
        self.tree = ttk.Treeview(self, columns=("Title", "Type", "Muscle Group", "Difficulty"), show="headings")    
        self.tree.heading("Title", text="Exercise Name")    
        self.tree.heading("Type", text="Type")
        self.tree.heading("Muscle Group", text="Muscle Group")
        self.tree.heading("Difficulty", text="Difficulty")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Double click event to select exercise
        self.tree.bind("<Double-1>", self.on_exercise_double_click)

        # Back Button
        back_button = tkinter.Button(self, text="Back", command=self.on_back)  
        back_button.pack(pady=10)   

    def load_exercises(self):
        # Clear existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Connect to the database and fetch exercises
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT title, type, muscle_group, difficulty FROM exercises WHERE equipment = ?", (self.selected_equipment,))
        exercises = cursor.fetchall()
        conn.close()

        # Populate the treeview with exercises
        for exercise in exercises:
            self.tree.insert("", "end", values=exercise)    

    def on_exercise_double_click(self, event):
        selected_item = self.tree.selection()[0]
        exercise_name = self.tree.item(selected_item, "values")[0]
        self.on_selected_exercise(exercise_name)

    def on_back(self):
        self.master.destroy()  # Close the exercise menu window

# INITIAL TEST

def show_exercise_details(exercise_id):
    print(f"Selected exercise ID: {exercise_id} (go to details page)")

root = tkinter.Tk()
root.title("Exercise Menu Example")
root.geometry("1366x768")

app = ExerciseMenu(root, selected_equipment="Dumbbell", on_selected_exercise=show_exercise_details)
root.mainloop()