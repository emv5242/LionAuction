# LionAuction

## Description

### Context

This application so far is the login function of the website
LionAuction. It allows users to input their email and password in to the
system and will check if they are in the database as a registered user.

### Features

This application's home page is the login page that has a
form in which users can put in their email in password in to 
the respective boxes. Each box has a prefilled text that fills the box
for example the email has "your.email@email.com" and the
password has "password" in order to show the user what the website is 
looking for. Both field have their type set respectively, so it will automatically
check if the email entered is even a valid email before checking the database. The password
box will hide the password entered with dots, but you can click on the icon to the 
right in order to see what the user has entered.

In order for the login to work, it selects the row from the database that has 
the email that the user has entered. It then securely hashes the given password. After this, 
it compares the hashed given password to the database's password from the row selected previously, 
if they are the same, then it is a successful login otherwise it redirect the user to a page
that says that it was an unsuccessful login and has a button to go back to the login screen.

### Organization

In this project there are three html files that correspond to the template of the three pages and 
two python files that handles all of the functions and navigating through the pages. In the python 
file, main.py it has one function valid_user that powers what happens when you input the user information
It selects the row from the database that has the email that the user has entered. It then securely hashes the given password. After this, 
it compares the hashed given password to the database's password from the row selected previously, 
if they are the same, then it is a successful login otherwise it redirect the user to a page
that says that it was an unsuccessful login and has a button to go back to the login screen.

### Instructions

After you unzip the file to the preferred location, then open the file in Pycharm you can hit 
the green button in the top corner to run the program and then after going to the localhost 
the home page should appear. Once on the homepage, you will type in your email and password in to 
the respective fields. Once that is done you will click the login button and the website will direct you to 
a page that tells you whether your login was successful or unsuccessful.
