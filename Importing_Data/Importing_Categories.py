import sqlite3 as sql
import csv

conn = sql.connect("../Users.db")

cursor = conn.cursor()

bids = open('../csvs/Categories.csv')
readData = csv.reader(bids)
insert_query = """INSERT INTO Categories (parent_category,category_name) values (?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()