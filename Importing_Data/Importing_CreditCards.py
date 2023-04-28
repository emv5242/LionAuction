import sqlite3 as sql
import csv
import hashlib

conn = sql.connect("../Users.db")

cursor = conn.cursor()

address = open('../csvs/Credit_Cards.csv')
readData = csv.reader(address)
insert_query = """INSERT INTO Credit_Cards (credit_card_num, card_type, expire_month, expire_year, security_code, 
                    owner_email) values (?,?,?,?,?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()