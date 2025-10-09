# Install libraries
import os

#os.system("pip install pandas")
#os.system("pip install numpy")
#os.system("pip install matplotlib")
#os.system("pip install seaborn")
#os.system("pip install plotly")
#os.system("pip install SQLAlchemy")

# Call Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine
import sqlite3

# Connect to the Database


# Define Functions
def display_database(db_path="backend/exercises.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        name = table_name[0]
        print(f"\n📁 Table: {name}")
        cursor.execute(f"PRAGMA table_info({name});")
        columns = [col[1] for col in cursor.fetchall()]
        print("Columns:", columns)

        cursor.execute(f"SELECT * FROM {name};")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    conn.close()

display_database()