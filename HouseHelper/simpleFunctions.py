from HouseHelper import (database,request,renderHtmlPage, check_password_hash,
                         redirect, url_for,requests,login_user,flash)

def correctDataLogIn(email,role,password):
    user = database.getUserByEmail(userEmail=email,role=role)
    if not user:
        flash("User doesn't exist")
        return False
    elif not check_password_hash(user.userPassword, password):
        flash("Passwords don't match")
        return False
    return True

def correctDataSignInPersonalInfo(form):
    name = form.get("name")
    surname = form.get("surname")
    phone = form.get("phone")
    password = form.get("password")
    email = form.get("email")
    passwordRepeat = form.get("passwordRepeat")
    role = form.get("role").lower()
    if len(name) < 4:
        flash("Your name is too short!")
        return False
    elif len(surname) < 4:
        flash("Your surname is too short!")
        return False
    elif len(phone) < 4:
        flash("Your phone is too short!")
        return False
    elif len(password) < 4:
        flash("Your password is too short!")
        return False
    elif database.getUserByEmail(userEmail=email,role=role):
        flash("Your email has already been used!")
        return False
    elif not (password == passwordRepeat):
        flash("Your passwords do not match.")
        return False
    return True


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

def handleAdminForms():
    formType = request.form.get("formType")
    if formType == "addNewCountry":
        database.addNewCountry(countryName=request.form.get("countryName"))
    elif formType == "addNewCity":
        database.addNewCity(countryName=request.form.get("countryName"), cityName=request.form.get("cityName"))
    elif formType == "addNewProfession":
        database.addNewProfession(professionName=request.form.get("professionName"))
    elif formType == "deleteCountry":
        database.deleateCountry(countryName=request.form.get("countryName"))
    elif formType == "deleteCity":
        database.deleateCity(cityName=request.form.get("cityName"))
    elif formType == "deleteProfession":
        database.deleateProfession(professionName=request.form.get("professionName"))

def checkBio(bio):
    bio = bio.strip()
    if len(bio.replace(" ",""))<10:
        flash("YOUR BIO IS TOO SHORT")
        return False
    elif len(bio)>100:
        flash("YOUR BIO IS TO LONG")
        return False
    if len(bio.replace(" ",""))*2<len(bio):
        flash("Your bio have too many spaces")
        return False
    return True

def getDescriptionForEachWorker(workers):
    descriptions = []
    for worker in workers:
        workerExtra = database.getWorkerExtraByUserId(worker.id)
        descriptions.append(workerExtra.description)
    return descriptions

def getAverageRatingsForEachWorker(workers):
    averageRatings = []
    for worker in workers:
        realWorker = database.getWorkerExtraByUserId(worker.id)
        averageRatings.append(database.getWorkerAverageRating(worker=realWorker))
    return averageRatings

def getAveragePriceForEachWorker(workers):
    averagePrices = []
    for worker in workers:
        realWorker = database.getWorkerExtraByUserId(worker.id)
        averagePrices.append(database.getWorkerAveragePrice(worker=realWorker))
    return averagePrices

def getNumberOfRewievsForEachWorker(workers):
    rewievs = []
    for worker in workers:
        realWorker = database.getWorkerExtraByUserId(worker.id)
        rewievs.append(database.getNumberOfWorkersRewievs(worker=realWorker))
    return rewievs

def makeWorkersData(workers,descriptions,ratings,numberOfReviews,prices):
    workersData = []
    for user,description,rating,reviews,price in list(zip(workers,descriptions,ratings,numberOfReviews,prices)):
        workerExtra = database.getWorkerExtraByUserId(userID=user.id)
        workerProfessions = workerExtra.professions
        workerCompletedJobs = workerExtra.completedJobs
        data = {
            "user":user,
            "description":description,
            "rating":rating,
            "reviews":reviews,
            "price": price,
            "professions":workerProfessions,
            "completedJobs":workerCompletedJobs
        }
        workersData.append(data)
    return workersData

def makeDataForWorkersList(workers):
    descriptions = getDescriptionForEachWorker(workers=workers)
    ratings = getAverageRatingsForEachWorker(workers=workers)
    numberOfReviews = getNumberOfRewievsForEachWorker(workers=workers)
    averagePrices = getAveragePriceForEachWorker(workers=workers)
    workersData = makeWorkersData(workers=workers,descriptions=descriptions,
                                        ratings=ratings,numberOfReviews=numberOfReviews,prices = averagePrices)
    return workersData

def userBookedWorkerAlraady(userId,workerId,profession):
    if database.getBookedJob(workerId=workerId,userId=userId,profession=profession):
        return True
    return False

def workerHavePandingJob(jobs):
    for job in jobs:
        if job.status == "pending":
            return True
    return False

def userHavePandingJob(jobs):
    for job in jobs:
        if job.status == "userPending":
            return True
    return False