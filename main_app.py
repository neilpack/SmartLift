import tkinter as tk
from tkinter import messagebox
import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap import Window
import os
from workout_info.equipment_menu import EquipmentMenu
from workout_info.exercise_menu import ExerciseMenu
from workout_info.exercise_details import ExerciseDetails
from generate_workout.generate import GenerateWorkout
from workout_history.workout_history import WorkoutHistory

class MainMenu(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Button Container
        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)

        # Title Frame
        title_frame = ttk.Frame(container)
        title_frame.pack(pady=20)

        ttk.Label(
            title_frame, 
            text="SmartLift", 
            font=("Arial", 42, "bold")
        ).pack()

        ttk.Label(
            title_frame, 
            text="Tailor your workout for what works for you!", 
            font=("Arial", 12),
            foreground="#AAAAAA"
        ).pack(pady=5)

        # Button Frame
        button_card = ttk.Frame(
            container, 
            padding=40,
            bootstyle="secondary"
        )
        button_card.pack(pady=40)

        btn_pad = {"pady": 15, "padx": 10}

        ttk.Button(
            button_card, 
            text="Explore Exercises",
            bootstyle="primary", 
            width=25,
            command=self.app.show_equipment_menu
        ).pack(**btn_pad)

        ttk.Button(
            button_card, 
            text="Generate Workout",
            bootstyle="success", 
            width=25,
            command=self.app.show_workout_generator
        ).pack(**btn_pad)

        ttk.Button(
            button_card, 
            text="Workout History",
            bootstyle="info", 
            width=25,
            command=self.app.show_workout_history
        ).pack(**btn_pad)

        ttk.Button(
            button_card, 
            text="Quit",
            bootstyle="danger", 
            width=25,
            command=self.app.root.quit
        ).pack(**btn_pad)




class SmartLiftApp:
    def __init__(self):
        self.root = Window(themename="darkly")
        self.root.title("SmartLift")
        self.root.geometry("750x1334")
        self.current_frame = None
        self.current_equipment = None
        self.show_main_menu()
        self.root.resizable(True, True)
        # Adjust scaling for high-DPI displays
        new_scale = 3.0
        self.root.tk.call("tk", "scaling", new_scale)


    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_main_menu(self):
        self.clear_frame()
        self.current_frame = MainMenu(self.root, self)

    def show_equipment_menu(self):
        self.clear_frame()
        self.current_frame = EquipmentMenu(self.root, self.show_exercise_menu)

    def show_exercise_menu(self, selected_equipment):
        self.current_equipment = selected_equipment
        self.clear_frame()
        self.current_frame = ExerciseMenu(self.root, selected_equipment, self.show_exercise_details, self.show_main_menu)

    def show_exercise_details(self, exercise_name):
        self.clear_frame()
        self.current_frame = ExerciseDetails(self.root, exercise_name, 
                                           lambda: self.show_exercise_menu(self.current_equipment))
    
    def show_workout_generator(self):
        self.clear_frame()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Generate Workout", font=("Arial", 24, "bold")).pack(pady=30)
        
        equipment_var = tk.StringVar()
        ttk.Label(frame, text="Select Equipment:", font=("Arial", 14)).pack()
        equipment_combo = ttk.Combobox(frame, textvariable=equipment_var, 
                                     values=["Dumbbell", "Barbell", "Bodyweight", "Resistance Band"], width=20)
        equipment_combo.pack(pady=10)
        
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        def generate():
            equipment = equipment_var.get()
            if not equipment:
                messagebox.showwarning("Warning", "Please select equipment")
                return
            
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            generator = GenerateWorkout()
            exercises = generator.generate(equipment)
            
            if exercises:
                ttk.Label(results_frame, text="Your Workout:", font=("Arial", 16, "bold")).pack(pady=10)
                for i, ex in enumerate(exercises, 1):
                    ttk.Label(results_frame, text=f"{i}. {ex['title']} ({ex['muscle_group']})", 
                             font=("Arial", 12)).pack(anchor="w", pady=2)
        
        ttk.Button(frame, text="Generate Workout", style="success", command=generate).pack(pady=20)
        ttk.Button(frame, text="Back to Main Menu", style="warning", command=self.show_main_menu).pack(pady=10)
        
        self.current_frame = frame
    
    def show_workout_history(self):
        self.clear_frame()
        self.current_frame = WorkoutHistory(self.root, self.show_main_menu)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SmartLiftApp()
    app.run()