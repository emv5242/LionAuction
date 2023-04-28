import sqlite3 as sql
import csv

conn = sql.connect("../Users.db")

cursor = conn.cursor()

bidders = open('../csvs/Bidders.csv')
readData = csv.reader(bidders)
insert_query = """INSERT INTO Bidders (email, first_name, last_name, gender, age, home_address_id, major) 
                        values (?,?,?,?,?,?,? )"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()
