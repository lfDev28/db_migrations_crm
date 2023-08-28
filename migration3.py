import numpy as np
import pandas as pd
import os
import MySQLdb
import csv
from dotenv import load_dotenv

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

cursor = connection.cursor()

df = pd.read_csv('output4.csv')


batch_size = 100


for batch_start in range(0, len(df), batch_size):
    batch_end = min(batch_start + batch_size, len(df))
    batch_df = df.iloc[batch_start:batch_end]

    for index, row in batch_df.iterrows():
        record_id = row['id']
        top_level_parent_id = row['4thParent']

        # Build the UPDATE query
        update_query = f'UPDATE Assets SET topLevelLocationId = {top_level_parent_id} where id={record_id}'

        # Execute the query
        cursor.execute(update_query)

    # Commit the changes to the database
    print("batch complete")
    connection.commit()

# Close the cursor and database connection
cursor.close()
connection.close()
