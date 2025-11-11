import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap import Window
from datetime import datetime
from database_operations import save_workout_log, get_all_exercise_names

class LogWorkout(ttk.Toplevel):
    def __init__(self, parent, on_save_callback=None):
        super().__init__(parent)
        self.on_save_callback = on_save_callback
        self.title("Log Workout")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Center the window
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = ttk.Label(self, text="Log Completed Workout", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Form frame
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Exercise selection
        ttk.Label(form_frame, text="Exercise:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.exercise_var = tk.StringVar()
        self.exercise_combo = ttk.Combobox(form_frame, textvariable=self.exercise_var, width=25)
        self.exercise_combo['values'] = get_all_exercise_names()
        self.exercise_combo.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Sets
        ttk.Label(form_frame, text="Sets:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.sets_var = tk.StringVar()
        sets_entry = ttk.Entry(form_frame, textvariable=self.sets_var, width=27)
        sets_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Reps
        ttk.Label(form_frame, text="Reps:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.reps_var = tk.StringVar()
        reps_entry = ttk.Entry(form_frame, textvariable=self.reps_var, width=27)
        reps_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Weight
        ttk.Label(form_frame, text="Weight (lbs):", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
        self.weight_var = tk.StringVar()
        weight_entry = ttk.Entry(form_frame, textvariable=self.weight_var, width=27)
        weight_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Date
        ttk.Label(form_frame, text="Date:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(form_frame, textvariable=self.date_var, width=27)
        date_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        save_btn = ttk.Button(button_frame, text="Save Workout", style="success",
                           command=self.save_workout)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", style="danger",
                             command=self.destroy)
        cancel_btn.pack(side="left", padx=10)
    
    def save_workout(self):
        # Validate inputs
        if not self.exercise_var.get():
            messagebox.showerror("Error", "Please select an exercise")
            return
        
        try:
            sets = int(self.sets_var.get())
            reps = int(self.reps_var.get())
            weight = float(self.weight_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for sets, reps, and weight")
            return
        
        if sets <= 0 or reps <= 0 or weight < 0:
            messagebox.showerror("Error", "Sets and reps must be positive, weight cannot be negative")
            return
        
        try:
            # Save to database
            save_workout_log(
                exercise_name=self.exercise_var.get(),
                sets=sets,
                reps=reps,
                weight=weight,
                date=self.date_var.get()
            )
            
            messagebox.showinfo("Success", "Workout logged successfully!")
            
            # Call callback if provided
            if self.on_save_callback:
                self.on_save_callback()
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save workout: {str(e)}")

# Test the log workout window
if __name__ == "__main__":
    app = Window(themename="darkly")
    app.withdraw()  # Hide main window
    
    def test_callback():
        print("Workout saved!")
    
    log_window = LogWorkout(app, test_callback)
    app.mainloop()