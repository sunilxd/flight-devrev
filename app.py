from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from sql_cmds import *

app = Flask(__name__)

person = {
    "is_logged_in": False, "email": "", "id": "", "admin": False
}


@app.route("/")
def home(msg = ""):
    return render_template("index.html", msg = msg)

@app.route("/login", methods=["GET", "POST"])
def login_page():

    if person["is_logged_in"]:
        return home("already logged in")

    if request.method == "GET":
        return render_template("login.html", msg = "")
    
    email, password = request.form.get("email"), request.form.get("password")
    response = login(email, password)

    if response["status"] == "good":
        person["is_logged_in"] = True
        person["email"] = email
        person["uid"] = response["id"]

        return home("logged in")

    return render_template("login.html", msg = response["msg"])


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if person["is_logged_in"]:
        return home("already logged in")

    if request.method == "GET":
        return render_template("signup.html", msg = "")
    
    email, password = request.form.get("email"), request.form.get("password")
    response = register(email, password)

    return render_template("signup.html", msg = response["msg"])


@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin_page():

    if person["is_logged_in"]:
        return home("customer account already logged in")

    if request.method == "GET":
        return render_template("adminlogin.html", msg = "")
    
    username, password = request.form.get("username"), request.form.get("password")
    response = admin_login(username, password)

    if response["status"] == "good":
        person["is_logged_in"] = True
        person["email"] = username
        person["uid"] = response["id"]
        person["admin"] = True

        return home("logged in")

    return render_template("adminlogin.html", msg = response["msg"])

# only admin
@app.route("/company", methods=["GET", "POST"])
def company_page():
    if not person["is_logged_in"]:
        return home("please login")
    
    if not person["admin"]:
        return home("only admin can access")

    if request.method == "GET":
        return render_template("company.html", msg = "", company = list_company())
    
    name = request.form.get("name")
    response = add_company(name)

    return render_template("company.html", msg = response["msg"], company = list_company())

# add flights


if __name__ == "__main__":
    app.run(debug=True)