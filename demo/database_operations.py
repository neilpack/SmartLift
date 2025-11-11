import sqlite3
from datetime import datetime

def save_workout_log(exercise_name, sets, reps, weight, date=None, user="default_user"):
    """Save a completed workout to the database"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect('exercises.db')
    cursor = conn.cursor()
    
    # Get exercise_id from exercise name (assuming we need it for foreign key)
    cursor.execute("SELECT rowid FROM exercises WHERE title = ?", (exercise_name,))
    exercise_result = cursor.fetchone()
    exercise_id = exercise_result[0] if exercise_result else None
    
    # Insert workout log
    cursor.execute("""
        INSERT INTO plans (user, exercise_id, sets, reps, weight, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user, exercise_id, sets, reps, weight, date))
    
    conn.commit()
    conn.close()

def get_workout_history(user="default_user"):
    """Get all logged workouts for a user"""
    conn = sqlite3.connect('exercises.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, e.title, p.sets, p.reps, p.weight, p.date
        FROM plans p
        JOIN exercises e ON p.exercise_id = e.rowid
        WHERE p.user = ?
        ORDER BY p.date DESC
    """, (user,))
    
    workouts = cursor.fetchall()
    conn.close()
    return workouts

def delete_workout_log(workout_id):
    """Delete a workout log by ID"""
    conn = sqlite3.connect('exercises.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM plans WHERE id = ?", (workout_id,))
    
    conn.commit()
    conn.close()

def get_all_exercise_names():
    """Get list of all exercise names for dropdown"""
    conn = sqlite3.connect('exercises.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT title FROM exercises ORDER BY title")
    exercises = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return exercises