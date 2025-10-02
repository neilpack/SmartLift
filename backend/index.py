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
def callTableNames():
    database = sqlite3.connect('exercises.db')
    cursor = database.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type ='table';")
    tables = cursor.fetchall()

    for table in tables:
        print(table)

    database.close

def callTable(table):
    database = sqlite3.connect('exercises.db')

    #
    df = pd.read_sql_query(f"SELECT * FROM {table}", database)
    print(df)

    database.close

def callRow(table, row_id):
    return 0

def createExercisePlanned(exercise, quantity, measurement):
    return 0

def deleteExercisePlanned(exercise_id):
    return 0

def editExercisePlanned(exercise, quantity, measurement):
    return 0

callTableNames()