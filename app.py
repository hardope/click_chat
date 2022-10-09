import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
import requests

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = "Messenger"

@app.route("/news")
def news():
    if not session.get("messenger"):
        return redirect("/login")
    return render_template("news.html", username=session['messenger'])

@app.route("/search", methods=["POST"])
def search():
    if not session.get("messenger"):
        return redirect("/login")
    else:
        search = request.form.get("search")
        users = []
        result = query_db(f"SELECT * FROM users WHERE username LIKE '%{search}%'")
        for i in result:
            if i[1] == session['messenger']:
                continue
            users.append(i[1])
        return render_template("index.html", username=session['messenger'], users=users, header="USERS")
@app.route("/users")
def index():
    if not session.get("messenger"):
        return redirect("/login")
    else:
        users = []
        result = query_db("SELECT * FROM users")
        for i in result:
            if i[1] == session['messenger']:
                continue
            users.append(i[1])
        return render_template("index.html", username=session['messenger'], users=users, header="USERS")

@app.route("/")
def chats():
    if not session.get("messenger"):
        return redirect("/login")
    else:
        a = 0
        users = []
        values = []
        result = query_db(f"SELECT DISTINCT recipient FROM messages WHERE sender == '{session['messenger']}'")
        results = query_db(f"SELECT DISTINCT sender FROM messages WHERE recipient == '{session['messenger']}'")
        for i in result:
            users.append(i[0])
            length = query_db(f"SELECT COUNT (*) FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{i[0]}' OR recipient == '{session['messenger']}' AND sender == '{i[0]}'")[0][0]
            try:
                comp = query_db(f"SELECT id FROM read WHERE sender == '{session['messenger']}' AND recipient == '{i[0]}'")[0][0]
            except:
                comp = 0
            if length > comp:
                values.append(f"{length - comp}")
            else:
                values.append("..")
            print(f"New: {length} | old: {comp}")
            a+=1
        for i in results:
            if i[0] not in users:
                users.append(i[0])
                a+=1
        if a < 3:
            return redirect("/users")
        return render_template("index.html", username=session['messenger'], users=users, header="Chats", values=values)
  
@app.route("/chat/<query>")
def chat(query):
    if not session.get("messenger"):
        return redirect("/login")
    else:
        return render_template("chat.html", username=session['messenger'], recipient=query)

@app.route("/api/<query>")
def api(query):
    if not session.get("messenger"):
        return redirect("/login")
    else:
        length = query_db(f"SELECT COUNT (*) FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{query}' OR recipient == '{session['messenger']}' AND sender == '{query}'")
        messages = query_db(f"SELECT * FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{query}' OR recipient == '{session['messenger']}' AND sender == '{query}'")
        length = length[0][0]
        check = query_db(f"SELECT id FROM read WHERE sender == '{session['messenger']}' AND recipient == '{query}'")
        if len(check) > 0:
            query_db(f"UPDATE read SET id = {length} WHERE sender == '{session['messenger']}' AND recipient == '{query}'")
        else:
            query_db(f"INSERT INTO read VALUES({length}, '{session['messenger']}', '{query}')")
        return jsonify(messages)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        try:
            users = query_db(f"SELECT * FROM users WHERE username == '{username}' AND password == '{password}'")
        except:
            return render_template("login.html", error="Invalid Username Or Password")
        if len(users) < 1:
            return render_template("login.html", error="Invalid Username Or Password")
        else:
            session['messenger'] = username
            return redirect("/")
    else:
        return render_template("login.html", error="")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        confirm = request.form.get('confirm').strip()


        if password == confirm:
            pass
        else:
            return render_template("register.html", error="Password does not match confirmation")
        users = query_db(f"SELECT * FROM users WHERE username == '{username}'")
        if not users:
            pass
        else:
            return render_template("register.html", error="Username Unavailable")

        available_id = query_db(f"SELECT id FROM users ORDER BY id DESC LIMIT 1")[0][0]

        query_db(f"INSERT INTO users (id, username, password) VALUES ({int(available_id + 1)}, '{username}', '{password}')")
        session['messenger'] = username
        return redirect("/users")
    else:
        return render_template("register.html", error="")

@app.route("/messages/<query>", methods=['POST'])
def messages(query):
    if not session.get("messenger"):
        return redirect("/login")
    else:
        recipient, message = query.strip().split(':')
        query_db(f"INSERT INTO messages VALUES ('{session['messenger']}', '{recipient}', '{message}', CURRENT_TIMESTAMP)")
        return "Sent"

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session['messenger'] = None
    return redirect('/login')

def query_db(text):
     conn = sqlite3.connect("messenger.db")
     cursor = conn.cursor()
     cursor.execute(f"{text}")
     value = cursor.fetchall()
     conn.commit()
     return value
