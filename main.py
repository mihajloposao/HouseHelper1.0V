from base import makingDatabases,UserById,addUserAddress
from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from simpleFunctions import (makeAndLogInNewUser, logInPost,htmlForUserHomeLogOut,
                             htmlForSignInUserPersonalInfo,htmlForSignInUserAddress)

# when server go live this should be deleted
makingDatabases()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "logIn"

@login_manager.user_loader
def load_user(user_id):
    return UserById(int(user_id))

@app.route("/")
def homeUser():
    if current_user.is_authenticated:
        return current_user.userName
    return htmlForUserHomeLogOut()

@app.route("/signInPersonalInfo",methods= ["GET","POST"] )
def signInUserPersonalInfo():
    if request.method == "POST":
        makeAndLogInNewUser()
        return redirect(url_for("signInUserAddress"))
    return htmlForSignInUserPersonalInfo()

@app.route("/signInAddress",methods= ["GET","POST"] )
def signInUserAddress():
    if request.method == "POST":
        addUserAddress(request.form)
        return redirect(url_for("homeUser"))
    return htmlForSignInUserAddress()

@app.route("/logIn",methods=["GET","POST"])
def logInUser():
    if request.method == "POST":
        return logInPost()
    return render_template("html/logInUser.html")

@app.route("/logOut")
@login_required
def logOutUser():
    logout_user()
    return redirect(url_for("logInUser"))

if __name__ == "__main__":
    app.run(debug=True)