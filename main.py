from base import makingDatabases,UserById,addUserAddress
from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from simpleFunctions import singInPersonalInfoPost, logInPost
import requests

makingDatabases()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "logIn"

@login_manager.user_loader
def load_user(user_id):
    return UserById(int(user_id))

def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()
    country = data.get("country", "Nepoznata država")
    city = data.get("city", "Nepoznat grad")
    return country, city

@app.route("/")
def homeUser():
    if current_user.is_authenticated:
        return current_user.userName
    #i get ip like this when i test code on local machine but when server start going live i need to use user_ip = request.remote_addr
    user_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    country, city = get_location(user_ip)
    return f"Vaša IP adresa: {user_ip}, Država: {country}, Grad: {city}"

@app.route("/signInPersonalInfo",methods= ["GET","POST"] )
def signInUserPersonalInfo():
    if request.method == "POST":
        return singInPersonalInfoPost()
    return render_template("html/signInUserPersonalInfo.html")

@app.route("/signInAddress",methods= ["GET","POST"] )
def signInUserAddress():
    if request.method == "POST":
        addUserAddress(current_user.userEmail,request.form)
        return redirect(url_for("homeUser"))
    return render_template("html/signInUserAddress.html")

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