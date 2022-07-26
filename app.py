import sqlite3
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)


username =""


@app.route("/messages")
def index():
    conn = sqlite3.connect("messenger.db")
    db = conn.cursor()

    message = db.execute("SELECT * FROM messages ORDER BY time_date DESC LIMIT 5")

    return render_template("index.html", message=message)


@app.route("/", methods=["GET", "POST"])
def login():

    conn = sqlite3.connect("messenger.db")
    db = conn.cursor()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            message = "You must input username"
            return render_template("error.html", message=message)

        if not password:
            message = "You must input password"
            return render_template("error.html", message=message)

        check = db.execute(f"SELECT * from users WHERE password == '{password}' AND username = '{username}'")

        if not check:
            message = "Invalid username or password"
            return render_template("error.html", message=message)


        return redirect("/messages")
        print(user_name)
    else:
        return render_template("login.html")

@app.route("/new" , methods=["POST"])
def new():
    conn = sqlite3.connect("messenger.db")
    db = conn.cursor()
    new = request.form.get("new")
    db.execute(f"INSERT INTO messages(message) VALUES('{new}')")
    conn.commit()
    return redirect("/messages")
