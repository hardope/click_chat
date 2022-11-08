import sqlite3
import os

def query_db(text):
     conn = sqlite3.connect(f"{os.getcwd()}/messenger.db")
     cursor = conn.cursor()
     cursor.execute(f"{text}")
     value = cursor.fetchall()
     conn.commit()
     return value

def text(value):
     return f"{value}"

def change_message():
     a = query_db("SELECT * FROM users")

     for i in a:
          print(f"{i[1]}: {i[0]}")
          query_db(f"UPDATE messages SET sender = '{text(i[0])}' WHERE sender == '{i[1]}'")
          query_db(f"UPDATE messages SET recipient = '{text(i[0])}' WHERE recipient == '{i[1]}'")

def change_read():
     a = query_db("SELECT * FROM users")

     for i in a:
          print(f"{i[1]}: {i[0]}")
          query_db(f"UPDATE read SET sender = '{text(i[0])}' WHERE sender == '{i[1]}'")
          query_db(f"UPDATE read SET recipient = '{text(i[0])}' WHERE recipient == '{i[1]}'")

def change_profile():
     a = query_db("SELECT * FROM users")

     for i in a:
          print(f"{i[1]}: {i[0]}")
          query_db(f"UPDATE profile SET username = '{text(i[0])}' WHERE username == '{i[1]}'")

def change_posts():
     a = query_db("SELECT * FROM users")

     for i in a:
          print(f"{i[1]}: {i[0]}")
          query_db(f"UPDATE posts SET username = '{text(i[0])}' WHERE username == '{i[1]}'")

def change_comments():
     a = query_db("SELECT * FROM users")

     for i in a:
          print(f"{i[1]}: {i[0]}")
          query_db(f"UPDATE comments SET username = '{text(i[0])}' WHERE username == '{i[1]}'")

#change_read()
#change_message()
#change_profile()
#change_posts()
change_comments()