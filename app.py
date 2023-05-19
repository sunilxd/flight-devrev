from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from sql_cmds import config
import pyrebase

app = Flask(__name__)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

person = {
    "is_logged_in": False, "name": "", "email": "", "uid": "", "admin": False
}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login(msg):
    return render_template("login.html", msg = msg)

@app.route("/signup")
def signup(msg):
    return render_template("signup.html", msg = msg)


if __name__ == "__main__":
    app.run(debug=True)