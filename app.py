import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    stocks = db.execute("SELECT name, SUM(shares) as value, price, symbol FROM history WHERE user_id = ? GROUP BY symbol", user_id)

    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total = cash

    for stock in stocks:
        total += stock["price"] * stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, total=total, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("Please enter a symbol")

        buffer_stocks = lookup(symbol)

        if not buffer_stocks:
            return apology("Invalid Symbol!")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Please enter a value")

        if shares <= 0:
            return apology("shares must contain positive numbers")

        user_id = session["user_id"]

        user_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        current_stock_price = buffer_stocks["price"]
        name = buffer_stocks["name"]
        total_shares_bought = current_stock_price * shares
        total_cash_left = user_balance - total_shares_bought

        if total_shares_bought > user_balance:
            return apology("Not enough cash")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", total_cash_left, user_id)

        db.execute("INSERT INTO history (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, name, shares, current_stock_price, "buy", symbol)

        return redirect('/')
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]

    stocks = db.execute(
        "SELECT name, SUM(shares) as value, price, type, symbol, time FROM history WHERE user_id = ? GROUP BY time", user_id)

    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Query database for username
        extra = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(extra) != 1:
            return apology("invalid username and/or password", 400)

        if not check_password_hash(extra[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)
        # Remember which user has logged in

        session["user_id"] = extra[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def increase():

    if request.method == "POST":

        user_id = session["user_id"]

        try:
            pendingVal = int(request.form.get("add"))
        except:
            return apology("Please place a value")

        if pendingVal <= 0 or pendingVal > 10000:
            return apology("value must between 0 and 10000")
        db.execute("UPDATE users SET cash = ? WHERE id = ?", pendingVal, user_id)
        return render_template("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if request is get, get the quote from user.
    if request.method == "POST":

        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Please enter a symbol")

        stock_symbol = lookup(symbol)

        if not stock_symbol:
            return apology("Invalid Symbol")
        return render_template("postquotes.html", stock_symbol=stock_symbol)

    else:
        return render_template("place.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensures that password and re-typed passwords match
        elif password != confirmation:
            return apology("password does not match", 400)

        encrypted_password = generate_password_hash(password)

        # Query database for username
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, encrypted_password)
            return redirect("")
            # Redirect user to/ home page
        except:
            return apology("Username is already taken", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        user_id = session["user_id"]

        stocks = db.execute("SELECT * FROM history WHERE user_id = ? GROUP BY symbol", user_id)

        symbol = request.form.get("symbol")

        stock_name = lookup(symbol)["name"]

        if not symbol:
            return apology("please choose a stock")

        shares = int(request.form.get("shares"))

        user_shares = db.execute("SELECT shares FROM history WHERE symbol = ? AND user_id = ?", symbol, user_id)[0]["shares"]

        if not shares:
            return apology("Invalid")

        if user_shares < shares:
            return apology("Not enough shares")

        if shares <= 0:
            return apology("Shares must be a positive integer")

        stock_price = lookup(symbol)["price"]

        new_value = stock_price * shares
        balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance + new_value, user_id)

        db.execute("INSERT INTO history (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, stock_name, -shares, stock_price, "sell", symbol)

        return redirect("/")
    else:
        user_id = session["user_id"]

        stocks = db.execute("SELECT symbol FROM history WHERE user_id = ? GROUP BY symbol", user_id)

        return render_template("sell.html", stocks=stocks, usd=usd)
