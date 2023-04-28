import sqlite3 as sql
import csv

conn = sql.connect("../Users.db")

cursor = conn.cursor()

address = open('../csvs/Auction_Listings.csv')
readData = csv.reader(address)
insert_query = """INSERT INTO AuctionListings (seller_email, listing_id, Category, Auction_Title, Product_name, 
                    Product_description, Quantity, Reserve_Price, Max_bids, Status)  values (?,?,?,?,?,?,?,?,?,?)"""
cursor.executemany(insert_query, readData)
conn.commit()
delete_query = """Delete from AuctionListings where rowid IN (1);"""
cursor.execute(delete_query)
conn.commit()
conn.close()
