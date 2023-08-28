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
cursor.execute("select @@version")
version = cursor.fetchone()

if version:
    print('Running version: ', version)
else:
    print('Not connected.')


dir_path = os.path.dirname(os.path.realpath(__file__))

csv_path = dir_path + "/Assets_Junee.csv"

df = pd.read_csv(csv_path)

df = df.fillna(0)
df = df.replace(np.nan, '', regex=True)


Condition_Dict = {
    "battery-4": "Brand New",
    "battery-3": "Nearly New",
    "battery-2": "Good Condition",
    "battery-1": "Satisfactory",
    "ambulance": "Requires Repair",
    "trash": "Requires Replacement",
    "question": "unknown"
}
Status_Dict = {
    "danger": "fail",
    "success": "pass",
    "warning": "warning",
    "info": "unknown",
}

batch_size = 100
batches = 1
try:

    for batch_start in range(0, len(df), batch_size):
        batch_end = min(batch_start + batch_size, len(df))
        batch_df = df.iloc[batch_start:batch_end]

        for index, row in batch_df.iterrows():
            statement = "INSERT INTO Assets (id, name, description, `check`, serialNumber, status, installDate, locationId, productId, topLevelLocationId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            params = (row[0], row[1], row[8], Status_Dict[row[5]],
                      row[2], Condition_Dict[row[6]], row[7], row[3], row[4], 2)
            cursor.execute(statement, params)

        batches += 1

        connection.commit()
        print(f"batch {batches} complete")

except Exception as e:
    print(e)
