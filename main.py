from base import (makingDatabases,UserById,addUserAddress, addNewCountry, addNewCity,getJsonWithCitiesNames,
                  addNewProfession,getProfessionNames)
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from simpleFunctions import (makeAndLogInNewUser, logInPost,htmlForUserHomeLogOut,
                             htmlForSignInUserPersonalInfo,htmlForSignInUserAddress,htmlForLogInUser,
                             htmlForUserHomeLogIn, signInAddressForPostMethod)

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

@app.route('/search')
def search():
    data = getProfessionNames()
    query = request.args.get('q', '').lower()
    results = [item for item in data if query in item.lower()]
    return jsonify(results)

@app.route("/")
def homeUser():
    if current_user.is_authenticated:
        return htmlForUserHomeLogIn()
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
        return signInAddressForPostMethod()
    return htmlForSignInUserAddress()

@app.route("/logIn",methods=["GET","POST"])
def logInUser():
    if request.method == "POST":
        return logInPost()
    return htmlForLogInUser()

@app.route("/logOut")
@login_required
def logOutUser():
    logout_user()
    return redirect(url_for("logInUser"))

@app.route("/addNewCountry",methods = ["POST"])
def adminAddNewCounty():
    countryName = request.form.get("countryName")
    addNewCountry(countryName)
    return redirect(url_for("homeUser"))

@app.route("/addNewCity", methods = ["POST"])
def adminAddNewCity():
    countryName = request.form.get("countryName")
    cityName = request.form.get("cityName")
    addNewCity(countryName,cityName)
    return redirect(url_for("homeUser"))

@app.route("/getCities")
def getCitiesByCountryName():
    countryName = request.args.get('countryName')
    return getJsonWithCitiesNames(countryName)

@app.route("/addNewProfession", methods = ["POST"])
def adminAddNewProfession():
    professionName = request.form.get("professionName")
    print(professionName)
    addNewProfession(professionName)
    return redirect(url_for("homeUser"))

if __name__ == "__main__":
    app.run(debug=True)