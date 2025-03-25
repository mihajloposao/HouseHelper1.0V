from flask import render_template,request,redirect,url_for
from base import userExist,addUser,UserByEmail,check_password_hash,UserByEmail
from flask_login import login_user, current_user
import requests

def singInErrorMessage(message):
    return render_template("html/signInUserPersonalInfo.html", errorMessage=message)

def singInPersonalInfoPost():
    if userExist(request.form["userEmail"]):
        return singInErrorMessage("Email already exists!")
    if request.form["userPassword"] != request.form["userRepeatePassword"]:
        return singInErrorMessage("Passwords do not match!")
    addUser(request.form)
    user = UserByEmail(request.form["userEmail"])
    login_user(user, remember=True)
    return redirect(url_for("signInUserAddress"))

def logInPost():
    password = request.form["userPassword"]
    user = UserByEmail(request.form["userEmail"])
    if user and check_password_hash(user.userPassword, password):
        login_user(user,remember=True)
        return redirect(url_for("homeUser"))
    else:
        return redirect(url_for("logInUser"))

def getIpAddress():
    # i get ip like this when i test code on local machine but when server start going live i need to use user_ip = request.remote_addr
    user_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    return user_ip

def getUserLocation():
    ip = getIpAddress()
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()
    country = data.get("country", "Nepoznata država")
    city = data.get("city", "Nepoznat grad")
    return country, city