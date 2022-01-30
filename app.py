import os
import re
import string
import random
import urllib.request

from datetime import date
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_mail import Mail,Message
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from datetime import datetime
from werkzeug.utils import secure_filename

theme = "ducks"
code = "abc"
id = 99999
day1 = date.today()
photo = "static/uploads/glance.png"
username = "User"
cclass = "2025"
posts = [
    ["text1", day1, None, 'static/uploads/harvard4.jpg', "User1", "2025"],
    ["text2", day1, None, 'static/uploads/harvard1.jpeg', "User2", "2021"],
    ["text3", day1, None, 'static/uploads/harvard2.jpeg', "User3", "2023"],
    ["text4", day1, None, 'static/uploads/harvard3.png', "User4", "2024"],
    ["text4", day1, None, 'static/uploads/harvard5.jpeg', "User4", "2021"],
    ["text4", day1, None, 'static/uploads/harvard6.jpeg', "User4", "2021"],
    ["text4", day1, None, 'static/uploads/harvard7.jpeg', "User4", "2024"],
    ["text1", day1, None, 'static/uploads/harvard4.jpg', "User1", "2025"],
    ["text2", day1, None, 'static/uploads/harvard1.jpeg', "User2", "2022"],
    ["text3", day1, None, 'static/uploads/harvard2.jpeg', "User3", "2025"],
    ["text4", day1, None, 'static/uploads/harvard3.png', "User4", "2023"],
    ["text4", day1, None, 'static/uploads/harvard5.jpeg', "User4", "2021"],
    ["text4", day1, None, 'static/uploads/harvard6.jpeg', "User4", "2022"],
    ["text4", day1, None, 'static/uploads/harvard7.jpeg', "User4", "2022"]
]
winner = "abc"
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Configure application
app = Flask(__name__)
app.secret_key = "secret-cs50"


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MAIL_DEFAULT_SENDER"] = "noreply.vfc@gmail.com"
app.config["MAIL_PASSWORD"] = "CS50Project"
app.config["MAIL_PORT"] = 465 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USERNAME"] = "noreply.vfc@gmail.com"
mail = Mail(app)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///glance.db")

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



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)
        email = request.form.get("email")
        if not email:
            return apology("must provide email", 400)
        if not email.endswith("@college.harvard.edu"):
            return apology("only harvard students' emails are allowed", 400)
        cclass = request.form.get("class")
        if not cclass:
            return apology("must provide class", 400)
        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)
        if not password == request.form.get("confirmation"):
            return apology("Passwords doesn't match", 400)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        for i in rows:
            if username == i["username"]:
                return apology("username already exists", 400)
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        for i in rows:
            if email == i["email"]:
                return apology("email already exists", 400)
        global code
        code = str(code)
        code = code.join(random.choice(string.ascii_uppercase) for i in range(6))
        new_user = db.execute("INSERT INTO users (username, email, hash, class) VALUES(?, ?, ?, ?)", username, email, generate_password_hash(password), cclass)
        global id
        id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        message = Message("Confirmation code", recipients=[email])
        message.body = f"Your confirmation code is: \n {code}"
        mail.send(message)
        return redirect("/confirmation")
    else:
        return render_template("register.html")

@app.route("/confirmation", methods=["GET", "POST"])
def confirmation():
    if request.method == "POST":
        global code
        if code == request.form.get("code"):
            global id
            session["user_id"] = id
            return redirect("/")
        else:
            return redirect("/confirmation")
    else:
        return render_template("confirmation.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        post = request.form.get("post")
        if not post:
            return apology("Your post cannot be blank", 400)
        global posts
        global posts_old
        day = "date.today()"
        for i in posts:
            if i[2] == session["user_id"]:
                return apology("Your can only post once a day", 400)
        if posts[len(posts) - 1][1] != day:
            global winner
            global photo
            global username
            global theme
            global cclass
            chosen_post = random.choice(posts)
            winner = chosen_post[0]
            photo = chosen_post[3]
            username = chosen_post[4]
            cclass = chosen_post[5]
            with open ("large.txt", "r") as file:
                words = []
                for line in file: 
                    words.append(line.rstrip()) 
                theme = random.choice(words)
            posts.clear()
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        cclass2 = db.execute("SELECT class FROM users WHERE id = ?", session["user_id"])[0]["class"]
        this_post = [post, day, session["user_id"], "", username, cclass2]
        posts.append(this_post)
        return redirect("/")
    else:
        return render_template("home.html", username=username, winner=winner, photo=photo, posts=posts, theme=theme, cclass=cclass)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            global posts
            for i in posts:
                if i[2] == session["user_id"]:
                    i[3] = path
                    file.save(path)
                    flash("Image uploaded and added to your last post")
                    return render_template("upload.html")
                else:
                    return apology("You should submit a post for this day before adding a photo", 400)
        else:
            flash("Only Images ar allowed")
            return redirect(request.url)
    else:
        return render_template("upload.html")
        

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
