import sqlite3 as sql
import csv
import hashlib

conn = sql.connect("../Users.db")

cursor = conn.cursor()

bidders = open('../csvs/Sellers.csv')
readData = csv.reader(bidders)
insert_query = """INSERT INTO Sellers (email, routing_number, account_number, balance) values (?,?,?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()