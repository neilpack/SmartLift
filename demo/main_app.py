import tkinter as tk
from tkinter import messagebox
import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap import Window
import os
from equipment_menu import EquipmentMenu
from exercise_menu import ExerciseMenu
from exercise_details import ExerciseDetails

class SmartLiftApp:
    def __init__(self):
        self.root = Window(themename="darkly")
        self.root.title("SmartLift")
        self.root.geometry("1080x1920")
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

if __name__ == "__main__":
    app = SmartLiftApp()
    app.run()