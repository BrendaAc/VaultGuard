# Fernet module is imported from the 
# cryptography package
import sqlite3
from cryptography.fernet import Fernet
import string
import bcrypt
import secrets

class Database():
# Connect to the database (you can use an existing database or create a new one)
    conn = sqlite3.connect('user_passwords.db')
    cursor = conn.cursor()

    #Creating database table
    sql ='''CREATE TABLE IF NOT EXISTS PWDMANAGER(
        [SITENAME] TEXT,
        [PASSWORD] BLOB
        )'''

    cursor.execute(sql)
    print("Table created successfully........")

    conn.commit()
    conn.close()

def generate_key():
    # Generates a Fernet key
    key = Fernet.generate_key()
    # print("Fernet Key:", key)

    # Write the key to "passwords.txt"
    with open("passwords.txt", "ab") as file:
        newline = "\n"
        file.write(key)
        file.write(newline.encode("utf-8"))
    return key # Returns generated key


def reading_keys():
    # Read the key from "passwords.txt"
    with open("passwords.txt", "rb") as file:
        keys = file.read().splitlines()

        key_list = []

        for i in keys:
            key_list.append(i)

        return key_list

def decryption_time(key, token):
    f = Fernet(key)
    return f.decrypt(token).decode()


def encrypt(key, text):
    f = Fernet(key)
    token = f.encrypt(text.encode())
    return token

# MODIFY TO INCLUDE USER INPUTS
def password_generator():
    # input = "hi"
    # sitename = "nah"
    sitename = input("Hello, what website would you like to generate a password for? ")
    length = int(input("How many characters long would you like your password? "))
    char_options = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(char_options) for i in range(length)) 


    key = generate_key()
    token = encrypt(key, password)
    db_addition(sitename, token)

    return token

def db_addition(sitename, token):
    conn = sqlite3.connect('user_passwords.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PWDMANAGER (SITENAME, PASSWORD) VALUES(?, ?)",
                                                               (sitename, token))
    # Commiting changes to database
    conn.commit()
    conn.close()

def db_pwd():
    password_list = []
    #Connecting to sqlite
    conn = sqlite3.connect('user_passwords.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    conn = sqlite3.connect('user_passwords.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    ids = c.execute('SELECT PASSWORD FROM PWDMANAGER').fetchall()
    # print("THE IDS")
    # IDS
    for i in ids:
        # print(i)
        password_list.append(i)
    return password_list

def db_sitenames():
    site_list = []
    #Connecting to sqlite
    conn = sqlite3.connect('user_passwords.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    conn = sqlite3.connect('user_passwords.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    ids = c.execute('SELECT SITENAME FROM PWDMANAGER').fetchall()
    # print("THE SITES")
    # IDS
    for i in ids:
        # print(i)
        site_list.append(i)
    return site_list

def print_passwords():
    a = reading_keys()
    b = db_pwd()
    c = db_sitenames()

    if len(b) != len(a):
        return print("Sorry, the amount of passwords and keys are uneven.")
    
    else:
        for i in range(len(b)):
            print("SITE:", c[i], "PASSWORD:", decryption_time(a[i], b[i]))

print("Hello, welcome to VaultGuard. Here, we'll store all of your passwords for you. Before proceeeing, please make a temporary master key.")

master_key = input()
key_encode = master_key.encode("utf-8")
salt = bcrypt.gensalt()
hash = bcrypt.hashpw(key_encode, salt)


while True:
    user_input = int(input("""
    1. Generate a password
    2. Print passwords
    3. Exit \n  """))
    
    if user_input == 1:
        password_generator()
    elif user_input == 2:
        login_attempt = input(("Please enter your master key: "))
        # if login_attempt
        # login_attempt = input(("\nIn order to proceed, please enter your master key: "))
        login_attempt_encode = login_attempt.encode("utf-8")

        # Checks if hashed login attempt matches master key hash. If so, returns password dictionary.
        if bcrypt.checkpw(login_attempt_encode, hash) == True:
            print_passwords()
        else:
            print("Your input does not match the master key. Please try again.")
    
    else:
        break
