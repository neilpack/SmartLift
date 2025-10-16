import os
import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def fetch_exercise_details(exercise_id):
    # Connect to the database
    conn = sqlite3.connect('backend/exercises.db')
    cursor = conn.cursor()

    # Load the 'exercises' table into a DataFrame
    df = pd.read_sql_query("SELECT * FROM exercises", conn)

    # Close the database connection
    conn.close()

    # Search for the exercise by ID [After we get the db set up a bit more solid]
    exercise = df[df['title'] == "Barbell Bench Press"]

    if exercise.empty:
        return None

    # Extract details into variables
    exercise_details_name = exercise.iloc[0]['title']
    exercise_details_type = exercise.iloc[0]['type']
    exercise_details_equipment = exercise.iloc[0]['equipment']
    exercise_details_muscle = exercise.iloc[0]['muscle_group']
    exercise_details_difficulty = exercise.iloc[0]['difficulty']
    exercise_details_description = exercise.iloc[0]['description']

    return {
        'name': exercise_details_name,
        'type': exercise_details_type,
        'equipment': exercise_details_equipment,
        'muscle_group': exercise_details_muscle,
        'difficulty': exercise_details_difficulty,
        'description': exercise_details_description
    }

def display_exercise_details(details):
    # Create a simple Tkinter window
    window = tk.Tk()
    window.title("Exercise Details")

    # Display each detail
    for key, value in details.items():
        label = tk.Label(window, text=f"{key.capitalize()}: {value}", anchor='w', justify='left')
        label.pack(fill='x', padx=10, pady=5)

    window.mainloop()

def main():
    # This will matter once we modify the database 'exercises' to ACTUALLY have an id
    exercise_id = 1

    details = fetch_exercise_details(exercise_id)
    if details:
        display_exercise_details(details)
    else:
        messagebox.showerror("Error", f"No exercise found with ID {exercise_id}")



def display_entire_database():
    db_path = 'backend/exercises.db'

    # Check if the path is valid
    if not os.path.exists(db_path):
        print(f"!! Database file not found at: {db_path} !!")
        return

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("!! No tables found in the database. !!")
    else:
        print("\n=== Entire Database Contents ===")
        for table_name in tables:
            table = table_name[0]
            print(f"\n--- Table: {table} ---")
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            print(df.to_string(index=False))

    # Close the connection
    conn.close()

main()