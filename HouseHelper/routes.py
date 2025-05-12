from HouseHelper import (app, login_manager, renderHtmlPage,redirect,login_required,wraps,
                         database,request,jsonify,current_user,url_for,simpleFunctions,logout_user,login_user)

def adminRequired(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            return redirect(url_for("homeUser"))
        else:
            return function(*args, **kwargs)
    return wrapper

def workerRequired(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.role != "worker":
            return redirect(url_for("homeUser"))
        else:
            return function(*args, **kwargs)
    return wrapper

def workerJobPending(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        worker = database.getWorkerExtraByUserId(current_user.id)
        if simpleFunctions.workerHavePandingJob(worker.bookedJobs):
            return redirect(url_for("workerBookedJobs"))
        else:
            return function(*args, **kwargs)
    return wrapper

def userJobPending(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if simpleFunctions.userHavePandingJob(current_user.bookedWorkers):
            return redirect(url_for("userBookedWorkers"))
        else:
            return function(*args, **kwargs)
    return wrapper

def userFinishedJobPending(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.finishedJobsPending != []:
            return redirect(url_for("userPayJob"))
        else:
            return function(*args, **kwargs)
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return database.UserById(int(user_id))

@app.route("/")
@app.route("/home")
def homeUser():
    if current_user.is_authenticated:
        return renderHtmlPage.htmlForUserHomeLogIn()
    return redirect(url_for("logInUser"))

@app.route("/userHome")
@userFinishedJobPending
@userJobPending
def userHome():
    return renderHtmlPage.render_template("index.html")

@app.route("/homeWorker")
@workerRequired
@workerJobPending
def homeWorker():
    workerExtra = database.getWorkerExtraByUserId(current_user.id)
    return renderHtmlPage.htmlForWorkerHome(workerExtra)

@app.route("/admin",methods=["POST","GET"])
@login_required
@adminRequired
def admin():
    if request.method == "POST":
        simpleFunctions.handleAdminForms()
    return renderHtmlPage.htmlForAdminDashboard()

@app.route("/signInPersonalInfo",methods= ["GET","POST"] )
@app.route("/signIn",methods= ["GET","POST"] )
def signInUserPersonalInfo():
    if request.method == "POST" and simpleFunctions.correctDataSignInPersonalInfo(request.form):
        form = request.form
        newUser = database.makeNewUser(name=form.get("name"),surName=form.get("surname"),email=form.get("email"),
                                            phone=form.get("phone"),password=form.get("password"),role=form.get("role").lower())
        database.addNewUserToBase(newUser)
        login_user(newUser, remember=True)
        if request.form.get("role").lower() == "worker":
            database.makeNewWorkerExtra(current_user.id)
        return redirect(url_for("homeUser"))
    elif request.method == "POST" and request.form.get("role").lower() == "worker":
        return redirect(url_for("signInWorker"))
    return renderHtmlPage.htmlForSignInUserPersonalInfo(userType="USER")

@app.route("/signInAddress",methods= ["GET","POST"] )
@login_required
@userFinishedJobPending
@userJobPending
def signInUserAddress():
    if request.method == "POST":
        form = request.form
        database.addUserAddress(country=form.get("country"),city=form.get("city"))
        return redirect(url_for("homeUser"))
    if current_user.role == "worker":
        return renderHtmlPage.htmlForSignInUserAddress(userType="WORKER")
    return renderHtmlPage.htmlForSignInUserAddress(userType="USER")

@app.route("/userBookedWorkers",methods= ["GET","POST"] )
@userFinishedJobPending
@login_required
def userBookedWorkers():
    if request.method == "POST" and request.form.get("buttonType")=="decline":
        database.bookedJobDelete(request.form.get("jobId"))
        return redirect(url_for("userBookedWorkers"))
    elif request.method == "POST" and request.form.get("buttonType")=="accept":
        database.bookedJobChangeStatus(jobId=request.form.get("jobId"),status="accepted")
        return redirect(url_for("userBookedWorkers"))
    elif request.method == "POST" and request.form.get("buttonType")=="edit":
        return renderHtmlPage.htmlForJobChangeDateAndTime(request.form.get("jobId"))
    elif request.method == "POST" and request.form.get("buttonType") == "workerChangeDate":
        database.chagneJobDate(jobId=request.form.get("jobId"),date=request.form.get("date-time"))
        database.bookedJobChangeStatus(jobId=request.form.get("jobId"),status="pending")
    if not current_user.bookedWorkers:
        return redirect(url_for("homeUser"))
    return renderHtmlPage.htmlForUserBookedWorkers(bookedWorkers=current_user.bookedWorkers)

@app.route("/userPayJob",methods= ["GET","POST"] )
@login_required
def userPayJob():
    job = current_user.finishedJobsPending[0]
    if request.method == "POST" and request.form.get("formType") == "decline":
        database.bookedJobChangeStatus(jobId=job.id,status="pending")
        database.deleteCompleteJobPending(job)
        return redirect(url_for("userBookedWorkers"))
    elif request.method == "POST" and request.form.get("formType") == "pay":
        database.makeNewCompleteJob(workerId=job.workerId,userId=job.userId,jobDescription=job.jobDescription,
                                    price=job.price,review=request.form.get("review"),rating=request.form.get("rating"))
        database.bookedJobDelete(job.id)
        database.deleteCompleteJobPending(job)
        return redirect(url_for("userHome"))
    return  renderHtmlPage.htmlForUserPay(job)
@app.route("/signInWorker")
def signInWorker():
    return renderHtmlPage.htmlForSignInUserPersonalInfo(userType="WORKER")

@app.route("/workerAddProfession", methods=["GET","POST"])
@login_required
@workerRequired
@workerJobPending
def workerAddProfession():
    if request.method == "POST":
        profession = database.getProfessionByName(request.form.get("professionName"))
        database.addProfessionToWorker(profession=profession)
        return redirect(url_for("homeUser"))
    return renderHtmlPage.htmlForWorkerAddProfession()

@app.route("/workerAddBio",methods = ["GET","POST"])
@login_required
@workerRequired
@workerJobPending
def workerAddBio():
    if request.method == "POST" and simpleFunctions.checkBio(request.form.get("bio")):
        database.addBioToWorker(request.form.get("bio"))
        return redirect(url_for("homeUser"))
    elif request.method == "POST":
        return redirect(url_for("workerAddBio"))
    return renderHtmlPage.htmlForWorkerAddBio()

@app.route("/workerBookedJobs",methods = ["GET","POST"])
@login_required
@workerRequired
def workerBookedJobs():
    if request.method == "POST" and request.form.get("buttonType")=="decline":
        database.bookedJobDelete(request.form.get("jobId"))
        return redirect(url_for("workerBookedJobs"))
    elif request.method == "POST" and request.form.get("buttonType")=="accept":
        database.bookedJobChangeStatus(jobId=request.form.get("jobId"),status="accepted")
        return redirect(url_for("workerBookedJobs"))
    elif request.method == "POST" and request.form.get("buttonType")=="edit":
        return renderHtmlPage.htmlForJobChangeDateAndTime(request.form.get("jobId"))
    elif request.method == "POST" and request.form.get("buttonType") == "workerChangeDate":
        database.chagneJobDate(jobId=request.form.get("jobId"),date=request.form.get("date-time"))
        database.bookedJobChangeStatus(jobId=request.form.get("jobId"),status="userPending")
    worker = database.getWorkerExtraByUserId(current_user.id)
    if not worker.bookedJobs:
        return redirect(url_for("homeUser"))
    return renderHtmlPage.htmlForWorkerBookedJobs(worker.bookedJobs)

@app.route("/workerFinishJob",methods = ["POST"])
@login_required
@workerRequired
def workerFinishJob():
    formType = request.form.get("buttonType")
    if formType == "finish":
        jobId = request.form.get("jobId")
        return renderHtmlPage.htmlForWorkerFinishJob(jobId=jobId)
    elif formType == "workerFinishJob":
        job = database.getBookedJobById(request.form.get("jobId"))
        database.addNewCompleteJobPending(workerId=job.workerId,userId=job.userId,
                                          jobDescription=request.form.get("jobDescription"),
                                          price=request.form.get("price"),date=job.date,address=job.address,id=job.id)
        database.bookedJobChangeStatus(jobId=request.form.get("jobId"),status="userPending")
        return redirect(url_for("workerBookedJobs"))


@app.route("/chooseWorker",methods=["GET","POST"])
@login_required
def chooseWorker():
    if request.method=="POST":
        profession = request.form.get("profession")
        country = current_user.userCountry
        city = current_user.userCity
        workers = database.filterWorkers(professionName=profession,country=country,city=city)
        workersData = simpleFunctions.makeDataForWorkersList(workers=workers)
        return renderHtmlPage.htmlForChooseWorker(profession=profession,country=country,city=city,
                                                  workersData=workersData)
    return redirect(url_for("homeUser"))

@app.route("/seeWorkerProfile/<workerId>")
@login_required
def seeWorkerProfile(workerId):
    worker = database.UserById(workerId)
    workerData = simpleFunctions.makeDataForWorkersList(workers=[worker])[0]
    return renderHtmlPage.htmlForWorkerProfile(workerData=workerData)

@app.route("/userBookWorker/<workerId>/<profession>",methods = ["GET","POST"])
@login_required
def userBookWorker(workerId,profession):
    if request.method == "POST" and not simpleFunctions.userBookedWorkerAlraady(userId=current_user.id,
                                                                            profession=request.form.get("profession"),
                                                                            workerId=request.form.get("workerId")):
        form = request.form
        database.makeNewBookWorker(workerId=form.get("workerId"),userId=current_user.id,address=form.get("address")
                                   ,profession=form.get("profession"),date=form.get("date-time"),
                                   additionalNotes=form.get("additionalNotes"),status=form.get("status"))
        return redirect(url_for("homeUser"))
    elif request.method == "POST":
        return redirect(url_for("homeUser"))
    return renderHtmlPage.htmlBookWorker(workerId,profession)

@app.route("/logIn",methods=["GET","POST"])
def logInUser():
    if request.method == "POST" and simpleFunctions.correctDataLogIn(email=request.form.get("email"),
                                                                     role=request.form.get("role").lower(),
                                                                     password=request.form.get("password")):
        user = database.getUserByEmail(request.form.get("email"),role=request.form.get("role").lower())
        login_user(user, remember=True)
        return redirect(url_for("homeUser"))
    elif request.method == "POST" and request.form.get("role").lower() == "worker":
        return redirect(url_for("logInWorker"))
    return renderHtmlPage.htmlForLogInUser(role="USER")

@app.route("/logInWorker")
def logInWorker():
    return renderHtmlPage.htmlForLogInUser(role="WORKER")

@app.route("/logInAdmin")
def logInAdmin():
    return renderHtmlPage.htmlForLogInUser(role="ADMIN")

@app.route("/logOut")
@login_required
def logOutUser():
    redirectUrl = url_for("logInUser")
    if current_user.role == "worker":
        redirectUrl = url_for("logInWorker")
    elif current_user.role == "admin":
        redirectUrl = url_for("logInAdmin")
    logout_user()
    return redirect(redirectUrl)


@app.route("/getCities")
def getCitiesByCountryName():
    countryName = request.args.get('countryName')
    return database.getJsonWithCitiesNames(countryName)


@app.route('/search')
def search():
    data = database.getProfessionNames()
    query = request.args.get('searchInput', '').lower()
    results = [item for item in data if query in item.lower()]
    return jsonify(results)