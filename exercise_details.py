# Call Libraries
import tkinter as tk
from tkinter import ttk

data = [
    {"id": 1, "name": "Alice", "age": 30, "occupation": "Engineer"},
    {"id": 2, "name": "Bob", "age": 25, "occupation": "Designer"},
    {"id": 3, "name": "Charlie", "age": 35, "occupation": "Product Manager"},
]

# Create Exercise Details Window
def createExerciseDetailsWindow(exercise_id, dataframe):
    filtered = [row for row in dataframe if row["id"] == exercise_id]

    print(filtered)

    # Create Details Window
    win = tk.Toplevel()
    win.title(filtered[0]['name'])
    win.geometry("300x150")

    tree = ttk.Treeview(win, columns =("Age", "Occupation"), show = 'headings' )
    tree.heading('Age', text = "Age")
    tree.heading('Occupation', text = "Occupation")

    tree.insert("", tk.END, values=(filtered[0]["age"], filtered[0]["occupation"]))
    tree.pack(expand=True, fill="both")


root = tk.Tk()
root.withdraw()

createExerciseDetailsWindow(1,data)

root.mainloop()

