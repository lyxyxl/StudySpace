import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime

from apology import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    name = db.execute(
        "SELECT name FROM users WHERE id = ?", session["user_id"])[0]["name"]

    links = db.execute(
        "SELECT link_id, name, url FROM links WHERE user_id = ?", session["user_id"]
    )

    todolist = db.execute(
        "SELECT activity, deadline, daysleft FROM todolist WHERE user_id = ?", session["user_id"])

    today = date.today().strftime("%Y-%m-%d")
    todaydate = datetime.strptime(today, "%Y-%m-%d")
    formatted_date = date.today().strftime("%d/%m/%Y")
    for activities in todolist:
        deadlinedate = datetime.strptime(activities["deadline"], "%Y-%m-%d")
        activities["daysleft"] = (deadlinedate - todaydate).days
        db.execute("UPDATE todolist SET daysleft = ? WHERE user_id = ? AND activity = ? AND deadline = ?", activities["daysleft"], session["user_id"], activities["activity"], activities["deadline"])

    newtodolist = db.execute(
        "SELECT activity_id, activity, deadline, daysleft FROM todolist WHERE user_id = ? ORDER BY daysleft ASC", session["user_id"])

    return render_template("index.html", name=name, newtodolist=newtodolist, links=links, formatted_date=formatted_date)


@app.route("/todolistadd", methods=["GET", "POST"])
@login_required
def todolistadd():
    if request.method == "POST":
        db.execute(
            "INSERT INTO todolist(user_id, activity, deadline) VALUES(?, ?, ?)", session["user_id"], request.form.get("task"), request.form.get("deadline"))

    return redirect("/")


@app.route("/deleteactivityrow", methods=["GET", "POST"])
@login_required
def deleteactivityrow():
    if request.method == "POST":
        db.execute(
            "DELETE FROM todolist WHERE user_id = ? AND activity_id = ? ", session["user_id"], request.form.get("activityidtodelete"))

    return redirect("/")

@app.route("/linksadd", methods=["GET", "POST"])
@login_required
def linksadd():
    if request.method == "POST":
        db.execute(
            "INSERT INTO links(user_id, name, url) VALUES(?, ?, ?)", session["user_id"], request.form.get("name"), request.form.get("url"))

    return redirect("/")


@app.route("/deletelink", methods=["GET", "POST"])
@login_required
def deletelink():
    if request.method == "POST":
        db.execute(
            "DELETE FROM links WHERE user_id = ? AND link_id = ? ", session["user_id"], request.form.get("linkidtodelete"))

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/forgor", methods=["GET", "POST"])
def forgor():
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

       # ENSURE NAME IS THERE
        elif not request.form.get("name"):
            return apology("must provide your name", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ? AND name = ?", request.form.get("username"), request.form.get("name"))

        if len(rows) == 0:
            return apology("this user does not exist", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("forgorconfirm.html")

    else:
        return render_template("forgor.html")


@app.route("/forgorconfirm", methods=["GET", "POST"])
def forgorconfirm():
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # ensure comfirmed password
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # ensure confirm and password same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("both passwords are not the same", 400)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("password")), session["user_id"])

        return redirect("/")

    else:
        return render_template("forgorconfirm.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # ENSURE NAME IS THERE
        elif not request.form.get("name"):
            return apology("must provide your name", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # ensure comfirmed password
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # ensure confirm and password same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("both passwords are not the same", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 0:
            return apology("username already exists", 400)

        db.execute("INSERT INTO users (username, hash, name) VALUES(?, ?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")), request.form.get("name"))

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

