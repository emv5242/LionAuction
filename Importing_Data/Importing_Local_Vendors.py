import sqlite3 as sql
import csv

conn = sql.connect("../Users.db")

cursor = conn.cursor()

local_vendors = open('../csvs/Local_Vendors.csv')
readData = csv.reader(local_vendors)
insert_query = """INSERT INTO Local_Vendors (Email,Business_Name,Business_Address_ID,Customer_Service_Phone_Number) 
                        values (?,?,?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()