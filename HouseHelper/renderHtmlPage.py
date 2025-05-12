from HouseHelper import simpleFunctions,current_user,render_template,database,request,redirect,url_for

def htmlForUserHomeLogIn():
    if current_user.role == "admin":
        return redirect(url_for("admin"))
    elif current_user.role == "worker":
        return redirect(url_for("homeWorker"))
    else:
        return redirect(url_for("userHome"))

def htmlForAdminDashboard():
    countryNames = database.getCountryNames()
    cityNames = database.getCityNames()
    professionNames = database.getProfessionNames()
    return render_template("adminDashboard.html",countryNames = countryNames, cityNames = cityNames,
                           professionNames = professionNames)

def htmlForSignInUserPersonalInfo(userType):
    signInFunction = "signInUserPersonalInfo"
    logInFunction = "logInUser"
    if userType == "WORKER":
        signInFunction = "signInWorker"
        logInFunction = "logInWorker"
    return render_template("signInUserPersonalInfo.html",userType = userType,
                           signInFunction=signInFunction,logInFunction = logInFunction)

def htmlForSignInUserAddress(userType):
    countryNames = database.getCountryNames()
    return render_template("signInUserAddress.html", countryNames = countryNames,userType = userType)

def htmlForLogInUser(role):
    signInFunction = "signInUserPersonalInfo"
    logInFunction = "logInUser"
    if role == "WORKER":
        signInFunction = "signInWorker"
        logInFunction = "logInWorker"
    elif role == "ADMIN":
        signInFunction = "logInAdmin"
        logInFunction = "logInAdmin"
    return render_template("logInUser.html",role=role,signInFunction=signInFunction,
                           logInFunction=logInFunction)

def htmlForWorkerAddProfession():
    professionNames = database.getProfessionNames()
    return render_template("workerAddProfession.html",professionNames=professionNames)

def htmlForWorkerAddBio():
    return render_template("workerAddBio.html")

def htmlForChooseWorker(profession,country,city,workersData):
    return render_template("listOfWorkers.html",profession=profession,country=country,
                           workersData=workersData,city=city)

def htmlForWorkerProfile(workerData):
    return render_template("workerProfile.html",workerData=workerData)

def htmlBookWorker(workerId,profession):
    return render_template("bookWorker.html",workerId=workerId,profession=profession)

def htmlForWorkerBookedJobs(bookedJobs):
    return render_template("workerBookedJobs.html",bookedJobs=bookedJobs)

def htmlForJobChangeDateAndTime(jobId):
    return render_template("jobChangeDateAndTime.html",jobId=jobId)

def htmlForUserBookedWorkers(bookedWorkers):
    return render_template("userBookedWorkers.html",bookedWorkers=bookedWorkers)

def htmlForWorkerFinishJob(jobId):
    return render_template("workerFinishJob.html",jobId=jobId)

def htmlForUserPay(job):
    return render_template("userPayJob.html",job=job)

def htmlForWorkerHome(workerExtra):
    return render_template("workerHome.html",workerExtra=workerExtra)