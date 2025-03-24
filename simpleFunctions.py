from flask import render_template,request,redirect,url_for
from base import userExist,addUser,UserByEmail,check_password_hash,UserByEmail
from flask_login import login_user, current_user

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
        return current_user.userName
    else:
        return redirect(url_for("logInUser"))
