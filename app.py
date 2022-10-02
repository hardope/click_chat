import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
import requests

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = "Messenger"


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
        users = []
        result = query_db(f"SELECT DISTINCT recipient FROM messages WHERE sender == '{session['messenger']}'")
        results = query_db(f"SELECT DISTINCT sender FROM messages WHERE recipient == '{session['messenger']}'")
        for i in result:
            users.append(i[0])
        for i in results:
            if i[0] not in users:
                users.append(i[0])
        return render_template("index.html", username=session['messenger'], users=users, header="Chats")

@app.route("/chat/<query>")
def chat(query):
    if not session.get("messenger"):
        return redirect("/login")
    else:
        messages = query_db(f"SELECT * FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{query}' OR recipient == '{session['messenger']}' AND sender == '{query}'")
        return render_template("chat.html", username=session['messenger'], messages=messages, recipient=query)

@app.route("/api/<query>")
def api(query):
    if not session.get("messenger"):
        return redirect("/login")
    else:
        if 'id-' in query:
            query = query.replace('id-', '')
            print(session['messenger'])
            print(query)
            length = query_db(f"SELECT COUNT(*) FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{query}' OR recipient == '{session['messenger']}' AND sender == '{query}'")
            return length
        messages = query_db(f"SELECT * FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{query}' OR recipient == '{session['messenger']}' AND sender == '{query}'")
        return jsonify(messages)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        users = query_db(f"SELECT * FROM users WHERE username == '{username}' AND password == '{password}'")

        if len(users) < 1:
            return redirect('/login')
        else:
            session['messenger'] = username
            return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')


        if password == confirm:
            pass
        else:
            return redirect("/")
        users = query_db(f"SELECT * FROM users WHERE username == '{username}'")
        if not users:
            pass
        else:
            return redirect('/register')

        available_id = query_db(f"SELECT id FROM users ORDER BY id DESC LIMIT 1")[0][0]

        query_db(f"INSERT INTO users (id, username, password) VALUES ({int(available_id + 1)}, '{username}', '{password}')")
        session['messenger'] = username
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/message/<query>", methods=['POST'])
def message(query):
    if not session.get("messenger"):
        return redirect("/login")
    else:
        message = request.form.get('message')
        print(message)
        query_db(f"INSERT INTO messages VALUES ('{session['messenger']}', '{query}', '{message}', CURRENT_TIMESTAMP)")
        return redirect(f"/chat/{query}")

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
