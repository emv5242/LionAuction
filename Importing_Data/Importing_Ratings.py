import sqlite3 as sql
import csv

conn = sql.connect("../Users.db")

cursor = conn.cursor()

ratings = open('../csvs/Ratings.csv')
readData = csv.reader(ratings)
insert_query = """INSERT INTO Ratings (Bidder_Email,Seller_Email,Dates,Rating,Rating_Desc) 
                        values (?,?,?,?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()