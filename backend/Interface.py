import tkinter as tk
import os as os
import sqlite3
import pandas as pd
import numpy as np

# Function to toggle display of DataFrame
def toggleDisplay():
    global toggled
    toggled = not toggled
    if toggled:
        print(df.head(10))
        button.config(text="YES")
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        button.config(text="NO")

# Create a windows
root = tk.Tk()
root.title("Window")

# Load CSV data into a DataFrame
df = pd.read_csv("datasets\exercises_200.csv")

toggled = False

# Create the button
button = tk.Button(root, text="Yes", command=toggleDisplay, width=15)
button.pack(pady=20)

# Start the GUI event loop
root.mainloop()