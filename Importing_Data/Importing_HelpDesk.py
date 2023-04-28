import sqlite3 as sql
import csv
import hashlib

conn = sql.connect("../Users.db")

cursor = conn.cursor()

helpdesk = open('../csvs/Helpdesk.csv')
readData = csv.reader(helpdesk)
insert_query = """INSERT INTO HelpDesk(email, position) 
                        values (?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()