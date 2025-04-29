from flask import render_template,request,redirect,url_for
from base import (userExist,addNewUserToBase,getUserByEmail,check_password_hash,getUserByEmail,
                  getCountryNames, addUserAddress)
from flask_login import login_user, current_user
import requests

def htmlForUserHomeLogOut():
    userLocation = getUserLocation()
    return f"Country: {userLocation['country']}, City: {userLocation['city']}"

def htmlForUserHomeLogIn():
    if current_user.userName == "admin":
        return htmlForAdminDashboard()
    else:
        return render_template("html/index.html")

def htmlForAdminDashboard():
    countryNames = getCountryNames()
    return render_template("html/adminDashboard.html",countryNames = countryNames)

def htmlForSingInErrorMessage(message):
    return render_template("html/signInUserPersonalInfo.html", errorMessage=message)

def htmlForSingInPersonalInfoProblemExists():
    if userExist(request.form["userEmail"]):
        return htmlForSingInErrorMessage(message="Email already exists!")
    if request.form["userPassword"] != request.form["userRepeatePassword"]:
        return htmlForSingInErrorMessage(message="Passwords do not match!")
def htmlForSignInUserPersonalInfo():
    return render_template("html/signInUserPersonalInfo.html")

def htmlForSignInUserAddress():
    countryNames = getCountryNames()
    return render_template("html/signInUserAddress.html", countryNames = countryNames)

def htmlForLogInUser():
    return render_template("html/logInUser.html")

def singInPersonalInfoProblemExists():
    return userExist(request.form["userEmail"]) or request.form["userPassword"] != request.form["userRepeatePassword"]

def makeAndLogInNewUser():
    if singInPersonalInfoProblemExists():
        return htmlForSingInPersonalInfoProblemExists()
    else:
        addNewUserToBase(request.form)
        newUser = getUserByEmail(request.form["userEmail"])
        login_user(newUser, remember=True)

def logInPost():
    password = request.form["userPassword"]
    user = getUserByEmail(request.form["userEmail"])
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
    return {"country":country,"city":city}

def signInAddressForPostMethod():
    try:
        addUserAddress(request.form)
    except AttributeError:
        pass
    finally:
        return redirect(url_for("homeUser"))