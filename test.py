import sqlite3
import os

def query_db(text):
     conn = sqlite3.connect(f"{os.getcwd()}/messenger.db")
     cursor = conn.cursor()
     cursor.execute(f"{text}")
     value = cursor.fetchall()
     conn.commit()
     return value

def get_name(id):
     return query_db(f"SELECT username FROM users WHERE id == '{id}'")[0][0]

comments = query_db(f"SELECT * FROM comments WHERE pid == {8} ORDER BY time DESC")
# Change user_id to username
new_comments = []
for i in comments:
     i = list(i)
     i[2] = get_name(i[2])
     new_comments.append(i)
print(comments)
print(new_comments)