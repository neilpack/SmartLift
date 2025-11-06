import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Window

class EquipmentMenu(ttk.Frame):
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
        title = ttk.Label(self, text="Select Equipment", font=("Arial", 24, "bold"), pady=20)
        title.pack()

        button_frame = ttk.Frame(self)
        button_frame.pack(expand=True)

        for i, option in enumerate(self.equipment_options):
            row = i // 2
            col = i % 2
            button = ttk.Button(
                button_frame,
                text=option,
                width=18,
                height=2,
                style="info", # Previous style line commented out
                # bg="lightblue",
                # font=("Arial", 14, "bold"),
                command=lambda opt=option: self.select_equipment(opt)
            )
            button.grid(row=row, column=col, padx=10, pady=10)
            self.buttons[option] = button

    def select_equipment(self, equipment):
        self.on_equipment_selected(equipment)
