import numpy as np
import pandas as pd
import os
import MySQLdb
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


Desktop_Path = "/Users/Lee/Desktop"
# Categories_Csv_Path = Desktop_Path + "/Category.csv"
# Categories = pd.read_csv(Categories_Csv_Path).values.tolist()

# try:
#     for Category in Categories:
#         if Category[0] == 1:
#             continue
#         elif Category[1] == 1:
#             cursor.execute(
#                 "INSERT INTO Categories (name, id) VALUES (%s, %s)", (Category[2], Category[0]))
#         else:
#             cursor.execute(
#                 "INSERT INTO Categories (name, parentId, id) VALUES (%s, %s, %s)", (Category[2], Category[1], Category[0]))
#     connection.commit()
#     print("Categories Inserted")
# except Exception as e:
#     print(e)

# Products_Csv_Path = Desktop_Path + "/Product.csv"
# Products = pd.read_csv(Products_Csv_Path).values.tolist()

# try:
#     print("Inserting Products")
#     # Replace NaN values with None

#     for Product in Products:
#         Product = ["" if pd.isna(val) else val for val in Product]
#         print(Product)
#         cursor.execute(
#             "INSERT INTO Product (id, name, modelNumber, averageCost, averagePrice, lifeTime, link, updatedAt, categoryId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (Product[0], Product[3], Product[2], Product[5], Product[6], Product[4], Product[9], Product[7], Product[1]))

#     connection.commit()
#     print("Products Inserted")

# except Exception as e:
#     print(e)


# Location_Csv_Path = Desktop_Path + "/Location.csv"
# Locations = pd.read_csv(Location_Csv_Path).values.tolist()

# Type_Dict = {
#     "map-marker": "site",
#     "building": "building",
#     "random": "category",
#     "home": "subcategory",
# }

# Status_Dict = {
#     "danger": "fail",
#     "success": "pass",
#     "warning": "warning",
#     "info": "unknown",
# }


# try:
#     for Location in Locations:
#         # print(Location)
#         # Clean the data for compatbility with new system
#         Location = ["" if pd.isna(val) else val for val in Location]
#         # Trim all strings if they have whitespace
#         Location = [val.strip() if isinstance(val, str) else val
#                     for val in Location]

#         # Set parentId column to None if it is 0
#         if Location[3] == 1:
#             Location[3] = None

#         if Location[0] == 1:
#             continue
#         else:
#             cursor.execute("INSERT INTO Locations (id, name, type, status, parentId, mapLink) VALUES (%s, %s, %s, %s, %s, %s)",
#                            (Location[0], Location[1], Type_Dict[Location[2]], Status_Dict[Location[4]], Location[3], Location[5]))
#         connection.commit()
#         print("Locations Inserted")


# except Exception as e:
#     print(e)

# Condition_Dict = {
#     "battery-4": "Brand New",
#     "battery-3": "Nearly New",
#     "battery-2": "Good Condition",
#     "battery-1": "Satisfactory",
#     "ambulance": "Requires Repair",
#     "trash": "Requires Replacement",
#     "question": "unknown"
# }


# Asset_Csv_Path = Desktop_Path + "/Asset.csv"
# Assets = pd.read_csv(Asset_Csv_Path).values.tolist()

# try:
#     for Asset in Assets:
#         Asset = ["" if pd.isna(val) else val for val in Asset]
#         Asset = [val.strip() if isinstance(val, str) else val
#                  for val in Asset]

#         statement = "INSERT INTO Assets (id, name, description, `check`, serialNumber, status, installDate, locationId, productId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         params = (Asset[0], Asset[1], Asset[8], Status_Dict[Asset[5]],
#                   Asset[2], Condition_Dict[Asset[6]], Asset[7], Asset[3], Asset[4])
#         cursor.execute(statement, params)
#         connection.commit()

#     print("Assets Inserted")

# except Exception as e:
#     print(e)
