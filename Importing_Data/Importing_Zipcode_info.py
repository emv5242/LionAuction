import sqlite3 as sql
import csv

conn = sql.connect("../Users.db")

cursor = conn.cursor()

zips = open('../csvs/Zipcode_Info.csv')
readData = csv.reader(zips)
insert_query = """INSERT INTO Zipcode_Info (zipcode,city,state) values (?,?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()
