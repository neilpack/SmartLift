import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap import Window
from datetime import datetime
from workout_history.database_operations import get_workout_history, delete_workout_log, save_workout_log, get_all_exercise_names

class WorkoutHistory(ttk.Frame):
    def __init__(self, master, on_back=None):
        super().__init__(master)
        self.on_back = on_back
        self.showing_form = False
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_history()
    
    def create_widgets(self):
        # Title
        self.title = ttk.Label(self, text="Workout History", font=("Arial", 20, "bold"))
        self.title.pack(pady=10)
        
        # Button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)
        
        self.log_btn = ttk.Button(self.button_frame, text="Log New Workout", style="success",
                          command=self.toggle_log_form)
        self.log_btn.pack(side="left", padx=10)
        
        refresh_btn = ttk.Button(self.button_frame, text="Refresh", style="info",
                              command=self.load_history)
        refresh_btn.pack(side="left", padx=10)
        
        # Main content frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.create_history_view()
        self.create_log_form()
        
        # Bottom buttons
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(pady=10)
        
        self.delete_btn = ttk.Button(bottom_frame, text="Delete Selected", style="danger",
                             command=self.delete_selected)
        self.delete_btn.pack(side="left", padx=10)
        
        if self.on_back:
            back_btn = ttk.Button(bottom_frame, text="Back", style="warning", command=self.on_back)
            back_btn.pack(side="left", padx=10)
    
    def load_history(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load workout history
        try:
            workouts = get_workout_history()
            for workout in workouts:
                workout_id, exercise, sets, reps, weight, date = workout
                # Store workout_id as tag for deletion
                item = self.tree.insert("", "end", values=(date, exercise, sets, reps, weight), tags=(str(workout_id),))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load workout history: {str(e)}")
    
    def create_history_view(self):
        # History table
        self.history_frame = ttk.Frame(self.content_frame)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.history_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview for workout history
        self.tree = ttk.Treeview(self.history_frame, columns=("Date", "Exercise", "Sets", "Reps", "Weight"), 
                                show="headings", yscrollcommand=scrollbar.set)
        
        # Column headings
        self.tree.heading("Date", text="Date")
        self.tree.heading("Exercise", text="Exercise")
        self.tree.heading("Sets", text="Sets")
        self.tree.heading("Reps", text="Reps")
        self.tree.heading("Weight", text="Weight (lbs)")
        
        # Column widths
        self.tree.column("Date", width=100)
        self.tree.column("Exercise", width=200)
        self.tree.column("Sets", width=80)
        self.tree.column("Reps", width=80)
        self.tree.column("Weight", width=100)
        
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Context menu for delete
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right click
        
        self.history_frame.pack(fill="both", expand=True)
    
    def create_log_form(self):
        # Log workout form
        self.form_frame = ttk.Frame(self.content_frame)
        
        form_title = ttk.Label(self.form_frame, text="Log Completed Workout", font=("Arial", 16, "bold"))
        form_title.pack(pady=10)
        
        # Form fields
        fields_frame = ttk.Frame(self.form_frame)
        fields_frame.pack(padx=20, pady=10)
        
        # Exercise selection
        ttk.Label(fields_frame, text="Exercise:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.exercise_var = tk.StringVar()
        self.exercise_combo = ttk.Combobox(fields_frame, textvariable=self.exercise_var, width=25)
        self.exercise_combo['values'] = get_all_exercise_names()
        self.exercise_combo.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Sets
        ttk.Label(fields_frame, text="Sets:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.sets_var = tk.StringVar()
        sets_entry = ttk.Entry(fields_frame, textvariable=self.sets_var, width=27)
        sets_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Reps
        ttk.Label(fields_frame, text="Reps:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.reps_var = tk.StringVar()
        reps_entry = ttk.Entry(fields_frame, textvariable=self.reps_var, width=27)
        reps_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Weight
        ttk.Label(fields_frame, text="Weight (lbs):", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
        self.weight_var = tk.StringVar()
        weight_entry = ttk.Entry(fields_frame, textvariable=self.weight_var, width=27)
        weight_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Date
        ttk.Label(fields_frame, text="Date:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(fields_frame, textvariable=self.date_var, width=27)
        date_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # Form buttons
        form_button_frame = ttk.Frame(self.form_frame)
        form_button_frame.pack(pady=20)
        
        save_btn = ttk.Button(form_button_frame, text="Save Workout", style="success",
                           command=self.save_workout)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ttk.Button(form_button_frame, text="Cancel", style="danger",
                             command=self.toggle_log_form)
        cancel_btn.pack(side="left", padx=10)
    
    def toggle_log_form(self):
        if self.showing_form:
            # Show history
            self.form_frame.pack_forget()
            self.history_frame.pack(fill="both", expand=True)
            self.delete_btn.pack(side="left", padx=10)
            self.log_btn.config(text="Log New Workout")
            self.title.config(text="Workout History")
            self.showing_form = False
        else:
            # Show form
            self.history_frame.pack_forget()
            self.form_frame.pack(fill="both", expand=True)
            self.delete_btn.pack_forget()
            self.log_btn.config(text="View History")
            self.title.config(text="Log Workout")
            self.showing_form = True
            # Clear form
            self.exercise_var.set("")
            self.sets_var.set("")
            self.reps_var.set("")
            self.weight_var.set("")
            self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
    
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
            self.load_history()
            self.toggle_log_form()  # Return to history view
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save workout: {str(e)}")
    
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a workout to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this workout?"):
            try:
                for item in selected:
                    workout_id = self.tree.item(item, "tags")[0]
                    delete_workout_log(workout_id)
                    self.tree.delete(item)
                messagebox.showinfo("Success", "Workout deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete workout: {str(e)}")
    
    def show_context_menu(self, event):
        # Simple right-click delete option
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.delete_selected()

# Test the workout history window
if __name__ == "__main__":
    root = Window(themename="darkly")
    root.title("Workout History Test")
    root.geometry("800x600")
    
    def test_back():
        print("Back button clicked")
    
    app = WorkoutHistory(root, test_back)
    root.mainloop()