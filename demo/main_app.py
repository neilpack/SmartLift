import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

class SmartLiftApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SmartLift")
        self.root.geometry("800x600")
        self.current_frame = None
        self.current_equipment = None
        self.show_equipment_menu()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_equipment_menu(self):
        self.clear_frame()
        self.current_frame = EquipmentMenu(self.root, self.show_exercise_menu)

    def show_exercise_menu(self, selected_equipment):
        self.current_equipment = selected_equipment
        self.clear_frame()
        self.current_frame = ExerciseMenu(self.root, selected_equipment, self.show_exercise_details, self.show_equipment_menu)

    def show_exercise_details(self, exercise_name):
        self.clear_frame()
        self.current_frame = ExerciseDetails(self.root, exercise_name, 
                                           lambda: self.show_exercise_menu(self.current_equipment))

    def run(self):
        self.root.mainloop()

class EquipmentMenu(tk.Frame):
    def __init__(self, master, on_equipment_selected):
        super().__init__(master)
        self.on_equipment_selected = on_equipment_selected
        self.pack(fill="both", expand=True)
        
        self.equipment_options = [
            "Barbell", "Dumbbell", "Kettlebell", "Bodyweight", 
            "Machine", "Cable", "Resistance Band", "Medicine Ball"
        ]
        
        self.buttons = {}
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Select Equipment", font=("Arial", 24, "bold"), pady=20)
        title.pack()

        # Create a frame for buttons in 2 columns
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True)

        for i, option in enumerate(self.equipment_options):
            row = i // 2
            col = i % 2
            button = tk.Button(
                button_frame,
                text=option,
                width=18,
                height=2,
                bg="lightblue",
                font=("Arial", 14, "bold"),
                command=lambda opt=option: self.select_equipment(opt)
            )
            button.grid(row=row, column=col, padx=10, pady=10)
            self.buttons[option] = button

    def select_equipment(self, equipment):
        self.on_equipment_selected(equipment)

class ExerciseMenu(tk.Frame):
    def __init__(self, master, selected_equipment, on_exercise_selected, on_back):
        super().__init__(master)
        self.selected_equipment = selected_equipment
        self.on_exercise_selected = on_exercise_selected
        self.on_back = on_back
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_exercises()

    def create_widgets(self):
        title = tk.Label(self, text=f"Exercises for {self.selected_equipment}", font=("Arial", 20, "bold"), pady=10)
        title.pack()

        self.listbox = tk.Listbox(self, font=("Arial", 14), height=20)
        self.listbox.pack(fill="both", expand=True, padx=20, pady=10)
        self.listbox.bind("<Double-1>", self.on_exercise_double_click)

        back_button = tk.Button(self, text="Back", font=("Arial", 16), command=self.on_back)
        back_button.pack(pady=10)

    def load_exercises(self):
        conn = sqlite3.connect('exercises.db')
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM exercises WHERE equipment = ?", (self.selected_equipment,))
        exercises = cursor.fetchall()
        conn.close()

        for exercise in exercises:
            self.listbox.insert(tk.END, exercise[0])

    def on_exercise_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            exercise_name = self.listbox.get(selection[0])
            self.on_exercise_selected(exercise_name)

class ExerciseDetails(tk.Frame):
    def __init__(self, master, exercise_name, on_back):
        super().__init__(master)
        self.exercise_name = exercise_name
        self.on_back = on_back
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_details()

    def create_widgets(self):
        title = tk.Label(self, text="Exercise Details", font=("Arial", 20, "bold"), pady=10)
        title.pack()

        self.details_frame = tk.Frame(self)
        self.details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        back_button = tk.Button(self, text="Back", font=("Arial", 16), command=self.on_back)
        back_button.pack(pady=10)

    def load_details(self):
        conn = sqlite3.connect('exercises.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exercises WHERE title = ?", (self.exercise_name,))
        exercise = cursor.fetchone()
        conn.close()

        if exercise:
            details = {
                'Name': exercise[0],
                'Type': exercise[1],
                'Equipment': exercise[2],
                'Muscle Group': exercise[3],
                'Description': exercise[4],
                'Difficulty': exercise[5]
            }

            for key, value in details.items():
                label = tk.Label(self.details_frame, text=f"{key}: {value}", 
                               font=("Arial", 14), anchor='w', justify='left', wraplength=800)
                label.pack(fill='x', pady=5)

if __name__ == "__main__":
    app = SmartLiftApp()
    app.run()