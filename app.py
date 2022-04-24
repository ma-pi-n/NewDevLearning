from collections import defaultdict
from datetime import datetime
import random
import string
from cs50 import SQL
from flask import Flask, flash, g, redirect, render_template, request, session

# Configure application
app = Flask(__name__)
app.secret_key = 'somesupersecretkeythatshouldideallybeinanenvironmentvarandnotbehere'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///urls.db")

"""BUSINESS LOGIC"""
def generate_random_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def get_user(id):
    print("Getting user with {}".format(id))
    rows = db.execute('SELECT * from users WHERE id = "{}"'.format(id))
    print("Retrieved user rows", rows)
    if len(rows) > 0:
        return rows[0]
    return None

def get_user_by_username(username):
    print("Getting user with {}".format(username))
    rows = db.execute('SELECT * from users WHERE username = "{}"'.format(username))
    print("Retrieved user rows", rows)
    if len(rows) > 0:
        return rows[0]
    return None

def create_user(username, password):
    print("Creating user with {}".format(username))
    user_id = db.execute('INSERT INTO users (username, password) VALUES ("{}", "{}")'.format(username, password))
    print("The user created", user_id)
    return user_id

def validate_user(username, password):
    print("Validating user with {}".format(username))
    user = get_user_by_username(username)
    print("The user found", user)
    if not user or user['password'] != password: return False
    return user

def create_url(long, user_id):
    print("Shortening a new URL", long)
    id = generate_random_id()
    return db.execute('INSERT INTO urls (id, long, user_id) VALUES("{}", "{}", "{}")'.format(id, long, user_id))

def get_user_urls(user_id):
    print("Retrieving urls for user with id {}".format(user_id))
    return db.execute('SELECT * from urls WHERE user_id = "{}"'.format(user_id))

def get_url(id):
    print("Retrieving url by id {}".format(id))
    rows = db.execute('SELECT * from urls WHERE id = "{}"'.format(id))
    print("Retrieved url rows", rows)
    if len(rows) == 0:
        return None
    return rows[0]

def get_url_details(id):
    url = get_url(id)
    print("Retrieving visits for url", url)
    visits_list = db.execute('SELECT * from visits WHERE url_id = "{}"'.format(id))
    visits_by_visitor = defaultdict(list)
    for v in visits_list: visits_by_visitor[v['visitor']].append(v)

    url['totalVisits'] = len(visits_list)
    url['totalVisitors'] = len(visits_by_visitor.items())
    url['visits'] = visits_by_visitor
    print("Retrieved and structured url", url)
    return url

def delete_url(id):
    print("Deleting short url: {} and all corresponding visits data".format(id))
    db.execute('DELETE from visits WHERE url_id = "{}"'.format(id))
    db.execute('DELETE from urls WHERE id = "{}"'.format(id))
    return id

def update_url(id, long):
    print("Updating short url: {}, to point to long url: {}".format(id, long))
    db.execute('UPDATE urls SET long = "{}" WHERE id = "{}"'.format(long, id))
    return id

def log_visit(url, visitor):
    if not visitor or not (visitor in url['visits']):
        visitor = "V-{}".format(generate_random_id())
    
    visit_time = datetime.now().strftime("%a, %d %B %Y,  %H:%M:%S")
    db.execute('INSERT INTO visits (url_id, visitor, time) VALUES("{}", "{}", "{}")'.format(url['id'], visitor, visit_time))
    return visitor

"""ROUTES"""
@app.before_request
def before_request():
    if 'user_id' in session:
        g.user = get_user(session['user_id'])
    elif 'user' in g: g.pop('user')

    if '/urls' in request.path and not 'user' in g:
        return redirect("/login")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    print("Content of g", g)
    if not 'user' in g:
        return redirect("/login")
    return redirect("/urls")


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in g:
        return redirect("/urls")

    if request.method == "GET":
        return render_template("auth.html", username=None, formType = 'login')

    valid_user = validate_user(request.form.get("username"), request.form.get("password"))
    if (valid_user != False):
        session['user_id'] = valid_user['id']
        return redirect("/urls")

    flash("Username or password is incorrect", "danger")
    return render_template(
        "auth.html",
        username=None,
        formType = 'login',
        username_input=request.form.get("username"),
        password_input=request.form.get("password"),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if 'user' in g:
        return redirect("/urls")

    if request.method == "GET":
        return render_template("auth.html", username=None, formType = 'register')

    valid_user = create_user(request.form.get("username"), request.form.get("password"))
    if (valid_user): session['user_id'] = valid_user
    return redirect("/urls")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop('user_id')
    return redirect("/login")


@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == "POST":
        create_url(request.form.get('longURL'), g.user['id'])
        return redirect("/urls")

    else:
        print("Content of g", g)
        urls = get_user_urls(g.user['id'])
        return render_template("index.html", len=len, url_count=len(urls), urls=urls, username=g.user["username"])


@app.route("/urls/new", methods=["GET"])
def url_new():
    return render_template("new.html", username=g.user["username"])


@app.route("/urls/<id>", methods=["GET", "POST"])
def url(id):
    if request.method == "POST":
        update_url(id, request.form.get('longURL'))
        return redirect("/urls/{}".format(id))

    else:
        url = get_url_details(id)
        return render_template("show.html", url=url, username=g.user["username"])

@app.route("/urls/<id>/delete", methods=["POST"])
def delete(id):
    delete_url(id)
    return redirect("/urls")


@app.route("/u/<id>", methods=["GET"])
def url_redirect(id):
    url = get_url_details(id)
    if url == None:
        return render_template("error.html", username=g.user["username"])
    visitor = session['visitor'] if 'visitor' in session else None
    session['visitor'] = log_visit(url, visitor)
    return redirect(url['long'])
