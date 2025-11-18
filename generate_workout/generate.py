import sqlite3
import random

class GenerateWorkout:
    def __init__(self, db_path="exercises.db"):
        self.db_path = db_path

    def _get_exercises_by_equipment(self, equipment):
        """Return all exercises matching the selected equipment."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, type, equipment, muscle_group, description, difficulty
            FROM exercises
            WHERE equipment = ?
        """, (equipment,))

        rows = cursor.fetchall()
        conn.close()

        # dictionary
        return [
            {
                "title": r[0],
                "type": r[1],
                "equipment": r[2],
                "muscle_group": r[3],
                "description": r[4],
                "difficulty": r[5]
            }
            for r in rows
        ]

    def generate(self, equipment, min_exercises=5, max_exercises=8):
        """
        Generate a balanced workout from available exercises.
        Returns: list of exercise dicts.
        """

        exercises = self._get_exercises_by_equipment(equipment)

        if not exercises:
            return []

        # muscle group
        groups = {}
        for ex in exercises:
            mg = ex["muscle_group"]
            groups.setdefault(mg, []).append(ex)

        plan = []

        # shuffle
        muscle_groups = list(groups.keys())
        random.shuffle(muscle_groups)

        # Step 1: pick one per muscle group until plan has enough or groups exhausted
        for mg in muscle_groups:
            if len(plan) >= max_exercises:
                break
            plan.append(random.choice(groups[mg]))

        # Step 2: Fill remaining slots with random exercises
        if len(plan) < min_exercises:
            remaining_needed = min_exercises - len(plan)
            extra_pool = [ex for ex in exercises if ex not in plan]
            random.shuffle(extra_pool)
            plan.extend(extra_pool[:remaining_needed])

        # Clip to max limit
        plan = plan[:max_exercises]

        return plan
    

#to do
#get team approval on implementation on this:

# from generate_workout.generate import GenerateWorkout

# generator = GenerateWorkout()
# plan = generator.generate(equipment="Dumbbell")

# for exercise in plan:
#     print(exercise["title"], exercise["muscle_group"])