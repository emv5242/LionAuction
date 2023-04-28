from flask import Flask, render_template, request
import sqlite3 as sql
import hashlib

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/BidderLogin', methods=['POST', 'GET'])
def bidderlogin():
    error = None
    if request.method == 'POST':
        result = valid_bidder(request.form['email'], request.form['password'])
        if result:
            return render_template('BidderPages/BidderWelcomePage.html', error=error, result=result)
        else:
            error = 'invalid input name'
            return render_template('InvalidLogin.html', error=error, result=result)
    return render_template('BidderPages/BidderLogin.html', error=error)


@app.route('/SellerLogin', methods=['POST', 'GET'])
def sellerlogin():
    error = None
    if request.method == 'POST':
        result = valid_seller(request.form['email'], request.form['password'])
        if result:
            return render_template('SellerPages/SellerWelcomePage.html', error=error, result=result)
        else:
            error = 'invalid input name'
            return render_template('InvalidLogin.html', error =error)
    return render_template('SellerPages/SellerLogin.html', error=error)


@app.route('/HelpDeskLogin', methods=['POST', 'GET'])
def helpDesklogin():
    error = None
    if request.method == 'POST':
        result = valid_helpdesk(request.form['email'], request.form['password'])
        if result:
            return render_template('HelpDeskPages/HelpDeskWelcomePage.html', error=error, result=result)
        else:
            error = 'invalid input name'
            return render_template('InvalidLogin.html', error =error)
    return render_template('HelpDeskPages/HelpDeskLogin.html', error=error)


def valid_bidder(email, password):
    connection = sql.connect('users.db')
    connection.text_factory = str
    cursor = connection.cursor()
    temp_pass = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("""SELECT password FROM LoginInfo WHERE email = (?)""", [email])
    passw = cursor.fetchone()
    cursor.execute("""SELECT email FROM Bidders WHERE email = (?)""", [email])
    email1 = cursor.fetchone()
    if passw is None:
        return False
    if email1 is None:
        return False
    connection.execute('Delete from CurrentBidder where rowid = 1;')
    connection.commit()
    connection.execute('Insert into CurrentBidder SELECT * FROM Bidders WHERE email = (?) ', [email])
    connection.commit()
    cursor.execute('Select home_address_id FROM CurrentBidder WHERE ROWID IN (1);')
    curr_address_id = cursor.fetchone()
    connection.execute('Delete from CurrentAddress where rowid = 1;')
    connection.commit()
    connection.execute('Insert into CurrentAddress SELECT * FROM Address WHERE address_ID = (?) ', curr_address_id)
    connection.commit()
    return temp_pass == passw[0]


def valid_seller(email, password):
    connection = sql.connect('users.db')
    connection.text_factory = str
    cursor = connection.cursor()
    temp_pass = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("""SELECT password FROM LoginInfo WHERE email = (?)""", [email])
    passw = cursor.fetchone()
    cursor.execute("""SELECT email FROM Sellers WHERE email = (?)""", [email])
    email1 = cursor.fetchone()
    if passw is None:
        return False
    if email1 is None:
        return False
    connection.execute('Delete from CurrentSeller where rowid = 1;')
    connection.commit()
    connection.execute('Insert into CurrentSeller SELECT * FROM Sellers WHERE email = (?) ', [email])
    connection.commit()
    return temp_pass == passw[0]


def valid_helpdesk(email, password):
    connection = sql.connect('users.db')
    connection.text_factory = str
    cursor = connection.cursor()
    temp_pass = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("""SELECT password FROM LoginInfo WHERE email = (?)""", [email])
    passw = cursor.fetchone()
    cursor.execute("""SELECT email FROM HelpDesk WHERE email = (?)""", [email])
    email1 = cursor.fetchone()
    if passw is None:
        return False
    if email1 is None:
        return False
    connection.execute('Delete from CurrentHelpDesk where rowid = 1;')
    connection.commit()
    connection.execute('Insert into CurrentHelpDesk SELECT * FROM HelpDesk WHERE email = (?) ', [email])
    connection.commit()
    return temp_pass == passw[0]


@app.route('/ShowBidderInfo', methods=['POST', 'GET'])
def show_bidder_info():
    error = None
    result = [display_bidder_info(), display_bidder_info_address(), display_bidder_info_zipcode(), display_bidder_ccs()]
    print(f"Type MonetaryBase: {type(result)}")
    print(f"MonetaryBase: {result}")
    print(f"Type : {type(result[0])}")
    print(f"MonetaryBase: {result[0]}")
    if request.method == 'GET':
        result = [display_bidder_info(), display_bidder_info_address(), display_bidder_info_zipcode(), display_bidder_ccs()]
        print(f"ReUls: {result}")
        if result:
            return render_template('BidderPages/EditBidderInfo.html', error=error, result=result)
        else:
            error = 'invalid input name'
    return render_template('BidderPages/EditBidderInfo.html', error=error, result=result)


def display_bidder_ccs():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Credit_Cards.credit_card_num, Credit_Cards.card_type, Credit_Cards.expire_month, Credit_Cards.expire_year, Credit_Cards.security_code '
                   'FROM Credit_Cards '
                   'INNER JOIN CurrentBidder '
                   'ON CurrentBidder.email = Credit_Cards.owner_email')
    result = cursor.fetchall()
    print(f"CC: {result}")
    newresult = []
    for i in result[0]:
        newresult.append(i)
    print(f"CCnew: {newresult}")
    temp = newresult[0]
    temp1 = newresult[0][-4:]
    print(f"NEw: {temp1}")
    newtemp = "****-****-****-"+temp1
    newresult[0] = newtemp
    print(f"tuple: {[tuple(newresult),]}")
    return [tuple(newresult)]

def display_bidder_ccs_unhidden():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Credit_Cards.credit_card_num, Credit_Cards.card_type, Credit_Cards.expire_month, Credit_Cards.expire_year, Credit_Cards.security_code '
                   'FROM Credit_Cards '
                   'INNER JOIN CurrentBidder '
                   'ON CurrentBidder.email = Credit_Cards.owner_email')
    return cursor.fetchall()


def display_bidder_info():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email, first_name, last_name, gender, age, major FROM CurrentBidder WHERE ROWID in (1)')
    result = cursor.fetchall()
    return result


def display_bidder_info_address():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT home_address_id FROM CurrentBidder WHERE ROWID in (1)')
    addid = cursor.fetchone()
    cursor.execute('SELECT street_name, street_num, zipcode FROM Address WHERE address_ID = (?) ', addid)
    return cursor.fetchall()

def display_bidder_info_zipcode():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT home_address_id FROM CurrentBidder WHERE ROWID in (1)')
    addid = cursor.fetchone()
    cursor.execute('SELECT zipcode FROM Address WHERE address_ID = (?) ', addid)
    zipcode = cursor.fetchone()
    cursor.execute('SELECT city, state, zipcode FROM Zipcode_Info WHERE zipcode = (?)', zipcode)
    return cursor.fetchall()

@app.route('/EditBidderInfo-first', methods=['POST', 'GET'])
def editbidder_info_first():
    error = None
    result = [display_bidder_info(), display_bidder_info_address(), display_bidder_ccs()]
    print(f"Result: {result}")
    if request.method == 'POST':
        result = [display_bidder_info(), display_bidder_info_address(), display_bidder_ccs()]
        edit_bidder_info_first(result[0][0])
        edit_bidder_info_first_address(result[1][0])
        result = [display_bidder_info(), display_bidder_info_address(), display_bidder_ccs()]
        if result:
            return render_template('BidderPages/EditBidderInfo.html', error=error, result=result)
        else:
            error = 'invalid input'
    return render_template('BidderPages/EditBidderInfo.html', error=error, result = result)


@app.route('/ShowSellerInfo', methods=['POST', 'GET'])
def show_seller_info():
    error = None
    result = show_seller_infor()
    if request.method == 'POST':
        if result:
            return render_template('SellerPages/ShowSellerInfo.html', error=error, result=result)
        else:
            error = 'invalid input'
    return render_template('SellerPages/ShowSellerInfo.html', error=error, result = result)


def show_seller_infor():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentSeller WHERE ROWID = 1;')
    email1 = cursor.fetchone()
    cursor.execute('SELECT * FROM Sellers WHERE (email) = (?);', email1)
    return cursor.fetchall()

@app.route('/ShowHelpDeskInfo', methods=['POST', 'GET'])
def show_help_info():
    error = None
    result = show_helpdesk_info()
    if request.method == 'POST':
        if result:
            return render_template('HelpDeskPages/ShowHelpDeskInfo.html', error=error, result=result)
        else:
            error = 'invalid input'
    return render_template('HelpDeskPages/ShowHelpDeskInfo.html', error=error, result = result)


def show_helpdesk_info():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentHelpDesk WHERE ROWID = 1;')
    email1 = cursor.fetchone()
    cursor.execute('SELECT * FROM HelpDesk WHERE (email) = (?);', email1)
    return cursor.fetchall()


def edit_bidder_info_first(result):
    connection = sql.connect('users.db')
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("""SELECT email FROM CurrentBidder WHERE ROWID in (1)""")
    email = cursor.fetchone()
    command1 = """UPDATE Bidders SET (first_name, last_name, gender, age, major) = (?,?,?,?,?) WHERE email = (?)"""
    connection.execute(command1, [result[1], result[2], result[3], result[4], result[5], result[0]])
    connection.commit()
    return True

def edit_bidder_info_first_address(result):
    connection = sql.connect('users.db')
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("""SELECT home_address_id FROM CurrentBidder WHERE ROWID = 1;""")
    add_id = cursor.fetchone()
    connection.execute("""UPDATE Address SET (street_name, street_num, zipcode) = (?,?,?) WHERE address_ID = (?)""", [result[0], result[1], result[2], add_id[0]])
    connection.commit()
    return True

def edit_cc_info():
    connection = sql.connect('users.db')
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("""SELECT email FROM CurrentBidder WHERE ROWID in (1)""")
    email = cursor.fetchone()
    cursor.execute("""SELECT * from Credit_Cards WHERE owner_email = (?)""", email)
    cards = cursor.fetchall()
    return True


@app.route('/NewAuctionListing', methods=['POST', 'GET'])
def newAuctionListing():
    error = None
    categories = get_all_categories()
    if request.method == 'POST':
        result = new_auction_listing(request.form['category'], request.form['auctionTitle'], request.form['productName'], request.form['productDescription'], request.form['quantity'], request.form['reservePrice'], request.form['maxBids'])
        print(f"RESULT: {result}")
        if result:
            return render_template('SellerPages/AddingAuctionListing.html', error=error, result=result, categories=categories)
        else:
            error = 'invalid'
    return render_template('SellerPages/AddingAuctionListing.html', error=error, categories= categories)


def new_auction_listing(category, auction_title, prod_name, prod_description,quantity, reserv_price, max_bid):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT email FROM CurrentSeller WHERE ROWID = 1""")
    email = cursor.fetchone()
    new_counter = 1
    cursor.execute("""SELECT listing_id FROM AuctionListings WHERE seller_email = (?)""", email)
    count = cursor.fetchall()
    while (new_counter,) in count:
        new_counter = new_counter + 1
    connection.execute("""UPDATE CurrentSeller SET auction_counter = (?)""", [new_counter])
    connection.execute('INSERT INTO AuctionListings(Seller_Email,Listing_ID,Category,Auction_Title,'
                       'Product_Name,Product_Description,Quantity,Reserve_Price,Max_bids,Status, Remaining_Bids) VALUES '
                       '(?,?,?,?,?,?,?,?,?,?,?);', (email[0], new_counter, category, auction_title, prod_name,
                                                  prod_description, quantity, reserv_price, max_bid, 1, int(max_bid)))
    connection.commit()
    cursor = connection.execute('SELECT * FROM AuctionListings WHERE seller_email = (?);', email)
    return cursor.fetchall()

@app.route('/ShowMyBids', methods=['POST', 'GET'])
def showbids():
    error = None
    activeresult = showing_my_bids()
    if request.method == 'GET':
        if activeresult:
            return render_template('BidderPages/MyBids.html', error=error, activeresult=activeresult)
        else:
            error = 'invalid'
    return render_template('BidderPages/MyBids.html', error=error, activeresult=activeresult)

def showing_my_bids():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentBidder WHERE ROWID = 1;')
    email1 = cursor.fetchone()
    cursor.execute('SELECT * FROM Bids WHERE (Bidder_Email) = (?);', email1)
    return cursor.fetchall()

@app.route('/ShowHelpDeskRequests', methods=['POST', 'GET'])
def showrequests():
    error = None
    activeresult = showing_my_active_requests()
    inactiveresult = showing_my_inactive_requests()
    print(f"RESULT: {activeresult}")
    print(f"InRESULT: {inactiveresult}")
    if request.method == 'POST':
        if activeresult:
            return render_template('HelpDeskPages/ShowHelpRequests.html', error=error, activeresult=activeresult, inactiveresult=inactiveresult)
        elif inactiveresult:
            return render_template('HelpDeskPages/ShowHelpRequests.html', error=error, activeresult=activeresult,inactiveresult=inactiveresult)
        else:
            error = 'invalid'
    return render_template('HelpDeskPages/ShowHelpRequests.html', error=error, activeresult=activeresult, inactiveresult=inactiveresult)

def showing_my_active_requests():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentHelpDesk WHERE ROWID = 1;')
    email1 = cursor.fetchone()
    cursor.execute('SELECT * FROM Requests WHERE (helpdesk_staff_email, request_status) = (?,?);', [email1[0], 1])
    return cursor.fetchall()

def showing_my_inactive_requests():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentHelpDesk WHERE ROWID = 1;')
    email1 = cursor.fetchone()
    cursor.execute('SELECT * FROM Requests WHERE (helpdesk_staff_email, request_status) = (?,?);', [email1[0], 0])
    return cursor.fetchall()

@app.route('/ShowSellerAuctions', methods=['POST', 'GET'])
def showAuctionListing():
    error = None
    activeresult = showing_my_active_auctions()
    inactiveresult = showing_my_inactive_auctions()

    if request.method == 'POST':
        if activeresult:
            return render_template('SellerPages/DeletingAuctionListing.html', error=error, activeresult=activeresult, inactiveresult=inactiveresult)
        elif inactiveresult:
            return render_template('SellerPages/DeletingAuctionListing.html', error=error, activeresult=activeresult,inactiveresult=inactiveresult)
        else:
            error = 'invalid'
    return render_template('SellerPages/DeletingAuctionListing.html', error=error, activeresult=activeresult, inactiveresult=inactiveresult)



@app.route('/DeleteAuctionListings', methods=['POST', 'GET'])
def delAuctionListing():
    error = None
    activeresult = showing_my_active_auctions()
    inactiveresult = showing_my_inactive_auctions()
    if request.method == 'POST':
        result = valid_bid_delete(request.form['delete'])
        activeresult = showing_my_active_auctions()
        inactiveresult = showing_my_inactive_auctions()
        if result:
            return render_template('SellerPages/DeletingAuctionListing.html', error=error, activeresult = activeresult, inactiveresult = inactiveresult)
        else:
            error = 'invalid input name'
    return render_template('SellerPages/DeletingAuctionListing.html', error=error,activeresult = activeresult, inactiveresult = inactiveresult)

def valid_bid_delete(listing_id):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentSeller WHERE ROWID = 1')
    email = cursor.fetchone()
    cursor.execute('SELECT listing_ID FROM AuctionListings where seller_email = (?);', [email[0]])
    listing_ids = cursor.fetchall()
    for i in listing_ids:
        if int(listing_id) == i[0]:
            connection.execute('UPDATE AuctionListings SET Status = (?) WHERE (seller_email, listing_id) = (?,?);',
                               [0, email[0], listing_id])
            connection.commit()
    return True

def get_all_auction_ids():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentSeller WHERE ROWID = 1;')
    email1 = cursor.fetchone()
    cursor.execute('SELECT listing_id FROM AuctionListings WHERE (seller_email, Status) = (?,?);', [email1[0], 1])
    return cursor.fetchall()

def showing_my_active_auctions():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentSeller WHERE ROWID = 1;')
    email1 = cursor.fetchone()
    cursor.execute('SELECT * FROM AuctionListings WHERE (seller_email, Status) = (?,?);', [email1[0], 1])
    return cursor.fetchall()

def showing_my_inactive_auctions():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM CurrentSeller WHERE ROWID = 1;')
    email1 = cursor.fetchone()
    cursor.execute('SELECT * FROM AuctionListings WHERE (seller_email, Status) = (?,?);', [email1[0], 0])
    result = cursor.fetchall()
    cursor.execute('SELECT * FROM AuctionListings WHERE (seller_email, Status) = (?,?);', [email1[0], 2])
    result += cursor.fetchall()
    return result


@app.route('/BuyingAuctionListing/<email>/<list_id>', methods=['POST', 'GET'])
def buyingAuctionListing(email, list_id):
    error = None
    result = get_auction_listing(email,list_id)
    if request.method == 'POST':
        bid = request.form['bid']
        bidd_on = bidding_on(email, list_id, bid)
        bids = all_bids(email, list_id)
        if bidd_on:
            bids = all_bids(email, list_id)
            result = get_auction_listing(email, list_id)
            cc_info = display_bidder_ccs_unhidden()
            emailID = [(email, list_id)]
            if sold(email, list_id):
                return render_template('BidderPages/SoldPage.html', error=error, cc_info=cc_info, emailID=emailID )
            return render_template('BidderPages/BidderAuctionPage.html', error=error, result=result, bids=bids)
        else:
            error = 'You are unable to Place a Bid until next bidder places their bid'
            return render_template('BidderPages/BidderAuctionPage.html', error=error, result=result, bids=bids)
    return render_template('BidderPages/BidderAuctionPage.html', error=error, result=result)


@app.route('/SoldItemCCInfo/<email>/<list_id>', methods=['POST', 'GET'])
def soldCCinfo(email, list_id):
    error = None
    if request.method == 'POST':
        result = sell_item(email, list_id)
        print("FFFFFFFFFFDSDD")
        if result:
            return render_template('BidderPages/Sold.html', error=error)
        else:
            error = 'invalid input name'
    return render_template('BidderPages/SoldPage.html', error=error)


def sold(seller_email, listing_id):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT Remaining_Bids FROM AuctionListings WHERE (Seller_Email, Listing_ID) =(?,?)""",
                   [seller_email, listing_id])
    result = cursor.fetchall()
    if int(result[0][0]) == 0:
        return True
    return False

def sell_item(seller_email, listing_id):
    connection = sql.connect('users.db')
    print("FFFFFFF")
    connection.execute("""UPDATE AuctionListings SET Status = (?) WHERE (seller_email, listing_id) = (?,?)""",
                   [2, seller_email, listing_id])
    connection.commit()
    return True

def get_auction_listing(seller_email, listing_id):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM AuctionListings WHERE (Seller_Email, Listing_ID) =(?,?)""", [seller_email, listing_id])
    result = cursor.fetchall()
    cursor.execute('SELECT bid_price from Bids WHERE (Seller_Email, Listing_ID) =(?,?)', [seller_email, listing_id])
    bids = cursor.fetchall()
    new_bids = []
    for j in bids:
        new_bids.append(j[0])
    max_bids = 0
    if new_bids:
        max_bids = max(new_bids)
    result[0]+=(max_bids,)
    print(f"RESULT: {result}")
    return result


def bidding_on(seller_email, listing_id, bid):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT Bid_Price FROM Bids WHERE (Seller_Email, Listing_ID) = (?,?)""", [seller_email, listing_id])
    bids = cursor.fetchall()
    cursor.execute("""SELECT Reserve_Price FROM AuctionListings WHERE (Seller_Email, Listing_ID) = (?,?)""",
                   [seller_email, listing_id])
    m = cursor.fetchall()
    min_price = m[0]
    if int(bid) < int(min_price[0][1:]):
        return False
    new_bids = []
    cursor.execute("""SELECT email FROM CurrentBidder WHERE ROWID = 1""")
    curr_email = cursor.fetchone()
    for j in bids:
        new_bids.append(j[0])
    if new_bids:
        max5 = max(new_bids)
        if int(bid) <= max5+1:
            return False
        cursor.execute("""SELECT Bidder_email FROM Bids WHERE Bid_Price = (?)""", [max5])
        email = cursor.fetchone()
        if (email[0] == curr_email[0]):
            return False
    new_counter = 1
    cursor.execute("""SELECT Bid_ID FROM Bids""")
    count = cursor.fetchall()
    while (new_counter,) in count:
        new_counter = new_counter + 1
    connection.execute("""INSERT INTO Bids(Bid_ID, Seller_Email, Listing_ID, Bidder_Email, Bid_Price) VALUES (?,?,?,?,?)""",[new_counter, seller_email, listing_id, curr_email[0], bid])
    connection.commit()
    cursor.execute("""SELECT Remaining_Bids FROM AuctionListings WHERE (seller_email, listing_id) = (?,?)""", [seller_email, listing_id])
    rem_bids = cursor.fetchone()
    r_bids = rem_bids[0]-1
    connection.execute("""UPDATE AuctionListings SET Remaining_Bids = (?) WHERE (seller_email, listing_id) = (?,?)""", [r_bids, seller_email, listing_id])
    connection.commit()
    return True


def all_bids (seller_email, listing_id):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Bids WHERE (Seller_Email, Listing_ID) =(?,?) ORDER BY Bid_Price""", [seller_email, listing_id])
    return cursor.fetchall()


def get_all_categories():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT category_name FROM Categories""")
    return cursor.fetchall()


def get_all_top_parent_categories():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT category_name FROM Categories WHERE parent_category = (?)""", ["Root"])
    return cursor.fetchall()


def get_subcategories(parent_category):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT category_name FROM Categories WHERE parent_category = (?)""", [parent_category])
    return cursor.fetchall()


@app.route('/Browse', methods=['POST', 'GET'])
def browsingAuctionListing():
    error = None
    result = show_all_auctions('')
    categories = get_all_parent_categories()
    if request.method == 'POST':
        result = show_all_auctions(request.form['category'])
        categories = get_all_subcategories(request.form['category'])
        if result:
            return render_template('BrowsingCategories.html', error=error, result=result, categories=categories)
        else:
            error = 'invalid'
            return render_template('BrowsingCategories.html', error=error, result=result, categories=categories)
    return render_template('BrowsingCategories.html', error=error, result=result, categories=categories)


def get_all_subcategories(parent):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT category_name FROM Categories WHERE parent_category = (?)""", [parent])
    return cursor.fetchall()


def get_all_parent_categories():
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT category_name FROM Categories WHERE parent_category = (?)""", ['Root'])
    return cursor.fetchall()


def show_all_auctions(category):
    connection = sql.connect('users.db')
    cursor = connection.cursor()
    result = []
    if category == '':
        cursor.execute("""SELECT * FROM AuctionListings WHERE Status = (?)""", [1])
        result = cursor.fetchall()
    else:
        categories = get_subcategories(category)
        for i in categories:
            cursor.execute("""SELECT * FROM AuctionListings WHERE (Category,Status) = (?,?) """, [i[0], 1])
            result += cursor.fetchall()
        cursor.execute("""SELECT * FROM AuctionListings WHERE (Category,Status) = (?,?) """, [category, 1])
        result += cursor.fetchall()
    return result

if __name__ == "__main__":
    app.run()
