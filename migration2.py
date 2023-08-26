import numpy as np
import pandas as pd
import os
import MySQLdb
from lxml import etree
from io import StringIO
import math
from dotenv import load_dotenv
import ast
import datetime
load_dotenv()

connection = MySQLdb.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USERNAME"),
    passwd=os.getenv("PASSWORD"),
    db=os.getenv("DATABASE"),
    ssl_mode="VERIFY_IDENTITY",
    ssl={
        "ca": "/etc/ssl/cert.pem"
    }
)


Desktop_Path = "/Users/Lee/Desktop/Dev/Work/python_script_tecsim"
Checklist_Path = Desktop_Path + "/Checklist.csv"
Categories = pd.read_csv(Checklist_Path)


cursor = connection.cursor()
cursor.execute("select @@version")
version = cursor.fetchone()

if version:
    print('Running version: ', version)
else:
    print('Not connected.')


# Iterate through DataFrame rows and write to MySQL database
for index, row in Categories.iterrows():
    title = row['Title']
    check_group_id = row['PID']
    category_id = row['CategoryID']  # Will be None if it was nan

    # Skip if title is empty or nan, or if questions are not present, or category_id is nan
    if pd.isnull(title) or not row['Questions'] or math.isnan(category_id):
        continue
    print(f"Title: {title}, CategoryId: {category_id}")

    # Insert into CheckGroupTemplates
    cursor.execute(
        "INSERT INTO CheckGroupTemplates (id, name, categoryId) VALUES (%s, %s, %s)",
        (check_group_id, title, category_id)
    )

    questions = ast.literal_eval(row['Questions'])

    # For each question, insert into CheckItemsTemplate
    for question in questions:
        # Get current time and format it as a string
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if question == "":
            continue
        cursor.execute(
            "INSERT INTO CheckItemsTemplate (name, checkGroupId, updatedAt) VALUES (%s, %s, %s)",
            (question, check_group_id, now)
        )

    # # Commit after each row to save changes
    connection.commit()
