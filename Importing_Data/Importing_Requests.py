import sqlite3 as sql
import csv
import hashlib

conn = sql.connect("../Users.db")

cursor = conn.cursor()

requests = open('../csvs/Requests.csv')
readData = csv.reader(requests)
insert_query = """INSERT INTO Requests (request_id, sender_email, helpdesk_staff_email, request_type, request_desc, 
                    request_status) values (?,?,?,?,?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()