import sqlite3 as sql
import csv

conn = sql.connect("../Users.db")

cursor = conn.cursor()

bids = open('../csvs/Bids.csv')
readData = csv.reader(bids)
insert_query = """INSERT INTO Bids (Bid_ID,Seller_Email,Listing_ID,Bidder_Email,Bid_Price) 
                        values (?,?,?,?,? )"""
cursor.executemany(insert_query, readData)
conn.commit()
conn.close()
