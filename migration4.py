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

csv_path = dir_path + "/Suppliers.csv"


df = pd.read_csv(csv_path)

df = df.replace(np.nan, '', regex=True)
df = df.fillna(0)

for index, row in df.iterrows():
    cursor.execute("INSERT INTO Supplier (id, name, abn, officeAddress, postalAddress, contactName, contactEmail, contactMobileNo, contactOfficeNo, companyWebsite, type, orderTotal) \
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)",
                   (row['PID'], row['Name'], row['ABN'], row['OfficeAddress'], row['PostAddress'], row['ContactName'], row['Email'], row['Phone'], row['PhoneB'], row['WebSite'], row['type'], row['OrderTotal']))

connection.commit()
print("Suppliers Inserted")
