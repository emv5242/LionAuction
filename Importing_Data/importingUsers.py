import sqlite3 as sql
import csv
import hashlib

conn = sql.connect("../Users.db")

cursor = conn.cursor()
users = open('../csvs/Users.csv')
newUsers = open('../csvs/Users_hashed.csv', 'w')
data = csv.DictReader(users)
for c, r in enumerate(data):
    if c == 0:
        newUsers.write(','.join(r)+'\n')

    r['password'] = hashlib.sha256((r['password']).encode()).hexdigest()
    newUsers.write(','.join(r.values()) + '\n')

hashedusers = open('../csvs/Users_hashed.csv')
readData = csv.reader(hashedusers)
insert_query = """INSERT INTO LoginInfo (email, password) values (?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()