import sqlite3 as sql

conn = sql.connect("../Users.db")

cursor = conn.cursor()

cursor.execute("""SELECT * FROM AuctionListings""")
listing = cursor.fetchall()
for j in listing:
    cursor.execute("""SELECT Max_bids FROM AuctionListings WHERE (seller_email, listing_id) = (?,?)""", (j[0], j[1]))
    m_bids = cursor.fetchone()
    conn.execute("""UPDATE AuctionListings SET Remaining_Bids = (?) WHERE (seller_email, listing_id) = (?,?)""",(m_bids[0], j[0], j[1]))


cursor.execute("""SELECT * FROM Bids""")
listings = cursor.fetchall()
for i in listings:
    cursor.execute("""SELECT Remaining_Bids FROM AuctionListings WHERE (seller_email, listing_id) = (?,?)""", (i[1], i[2]))
    m_bids = cursor.fetchone()
    if m_bids[0] != 0:
        rem_bids = m_bids[0]-1
    else:
        rem_bids = 0
    conn.execute("""UPDATE AuctionListings SET Remaining_Bids = (?) WHERE (seller_email, listing_id) = (?,?)""",(rem_bids, i[1], i[2]))

conn.commit()

conn.close()