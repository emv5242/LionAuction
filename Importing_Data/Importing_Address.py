import sqlite3 as sql
import csv

conn = sql.connect("../Users.db")

cursor = conn.cursor()

address = open('../csvs/Address.csv')
readData = csv.reader(address)
insert_query = """INSERT INTO Address (address_ID, zipcode, street_num, street_name) 
                        values (?,?,?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()