from HouseHelper import (Base, UserMixin, Column, String, Integer,
                         relationship, ForeignKey, generate_password_hash, session, current_user,
                         IntegrityError,Table,simpleFunctions)

workerProfession = Table(
    'workerProfession',
    Base.metadata,
    Column('workerId', ForeignKey('Workers.id'), primary_key=True),
    Column('professionId', ForeignKey('Professions.id'), primary_key=True)
)

class User(Base, UserMixin):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    userEmail = Column(String, nullable=False)
    userName = Column(String, nullable=False)
    userSurename = Column(String, nullable=False)
    userPhone = Column(String, nullable=False)
    userCountry = Column(String, nullable=False)
    userCity = Column(String, nullable=False)
    userPassword = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")


class Worker(Base):
    __tablename__ = "Workers"
    id = Column(Integer,primary_key=True)
    description = Column(String,default="NO BIO YET")
    professions = relationship('Profession', secondary=workerProfession, back_populates='workers')

class Country(Base):
    __tablename__ = "Countries"
    id = Column(Integer, primary_key=True)
    countryName = Column(String, nullable=False, unique= True)
    cities = relationship("City", back_populates="country", cascade = "all, delete-orphan")

class City(Base):
    __tablename__ = "Cities"
    id = Column(Integer, primary_key=True)
    cityName = Column(String, nullable=False, unique= True)
    countryId = Column(Integer, ForeignKey("Countries.id"), nullable=False)
    country = relationship("Country", back_populates="cities")

class Profession(Base):
    __tablename__ = "Professions"
    id = Column(Integer, primary_key=True)
    professionName = Column(String, nullable=False, unique= True)

    workers = relationship('Worker', secondary=workerProfession, back_populates='professions')

class CompleteJob(Base):
    __tablename__ = "CompletedJobs"
    id = Column(Integer, primary_key=True)
    workerId = Column(Integer,ForeignKey("Workers.id"),nullable=False)
    userId = Column(Integer,ForeignKey("Users.id"),nullable=False)
    jobDescription = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    review = Column(String)
    rating = Column(Integer,nullable=False) #1-5
    worker = relationship("Worker",foreign_keys=[workerId],backref="completedJobs")
    user = relationship("User",foreign_keys=[userId],backref="completedJobs")

class CompleteJobPending(Base):
    __tablename__ = "CompletedJobsPending"
    id = Column(Integer,primary_key=True)
    workerId = Column(Integer, ForeignKey("Workers.id"), nullable=False)
    userId = Column(Integer, ForeignKey("Users.id"), nullable=False)
    jobDescription = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    address = Column(String, nullable=False)
    worker = relationship("Worker", foreign_keys=[workerId], backref="finishedJobsPending")
    user = relationship("User", foreign_keys=[userId], backref="finishedJobsPending")
class BookWorker(Base):
    __tablename__ = "BookWorker"
    id = Column(Integer, primary_key=True)
    workerId = Column(Integer, ForeignKey("Workers.id"), nullable=False)
    userId = Column(Integer, ForeignKey("Users.id"), nullable=False)
    date = Column(String,nullable=False)
    address = Column(String,nullable=False)
    profession = Column(String,nullable=False)
    additionalNotes = Column(String,nullable=True)
    status = Column(String,nullable=False,default="pending")
    worker = relationship("Worker", foreign_keys=[workerId], backref="bookedJobs")
    user = relationship("User", foreign_keys=[userId], backref="bookedWorkers")

def makeNewUser(name,surName,email,phone,password,role,country=None,city=None):
    if country == None:
        userLocation = simpleFunctions.getUserLocation()
        country = userLocation["country"]
        city = userLocation["city"]

    newUser = User(
        userEmail=email,
        userName=name,
        userSurename=surName,
        userPhone=phone,
        userPassword=generate_password_hash(password),
        userCountry = country,
        userCity = city,
        role = role
    )
    return newUser

def addNewUserToBase(newUser):
    session.add(newUser)
    session.commit()

def makeNewWorkerExtra(userId):
    newWorkerExtra = Worker(id=userId)
    session.add(newWorkerExtra)
    session.commit()

def userExist(userEmail):
    try:
        return session.query(User).filter_by(userEmail=userEmail).first() is not None
    except:
        return False

def getUserByEmail(userEmail,role):
    return session.query(User).filter(User.userEmail==userEmail,User.role==role).first()

def UserById(id):
    return session.query(User).filter_by(id=id).first()

def addUserAddress(country,city):
    user = session.query(User).filter_by(userEmail=current_user.userEmail).first()
    user.userCountry = country
    user.userCity = city
    session.commit()

def getWorkerExtraByUserId(userID):
    return session.query(Worker).filter_by(id=userID).first()

def getWorkerAverageRating(worker):
    if not worker.completedJobs:
        return 0
    sum = 0
    count = 0
    for job in worker.completedJobs:
        sum+= job.rating
        count+=1
    return round(sum/count,1)

def getWorkerAveragePrice(worker):
    if not worker.completedJobs:
        return 0
    sum = 0
    count = 0
    for job in worker.completedJobs:
        sum+= job.price
        count+=1
    return round(sum/count,2)

def getNumberOfWorkersRewievs(worker):
    return len(worker.completedJobs)

def addProfessionToWorker(profession):
    workerExtra = getWorkerExtraByUserId(current_user.id)
    if profession not in workerExtra.professions:
        workerExtra.professions.append(profession)
        session.commit()

def addBioToWorker(bio):
    workerExtra = getWorkerExtraByUserId(current_user.id)
    bio = bio.strip()
    workerExtra.description = bio;
    session.commit()

def getOnlyWorkers():
    return session.query(User).filter_by(role="worker").all()

def filterWorkers(professionName,country,city):
    profession = getProfessionByName(professionName=professionName)
    if profession is None:
        return []
    workersByProfessionName = []
    workers = getOnlyWorkers()
    for worker in workers:
        workerExtra = getWorkerExtraByUserId(worker.id)
        if profession in workerExtra.professions and worker.userCountry==country and worker.userCity==city:
            workersByProfessionName.append(worker)
    return workersByProfessionName

def addNewCountry(countryName):
    newCounty = Country(countryName = countryName)
    session.add(newCounty)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()

def getCountryNames():
    countryNames = session.query(Country.countryName).all()
    countryNames = [name[0] for name in countryNames]
    return countryNames

def addNewCity(countryName, cityName):
    countryId = getCountryIdByName(countryName)
    newCity = City(cityName = cityName,countryId = countryId)
    session.add(newCity)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()

def addNewProfession(professionName):
    newProfession = Profession(professionName = professionName)
    session.add(newProfession)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()

def getCountryIdByName(countryName):
    country = session.query(Country).filter_by(countryName=countryName).first()
    countryId = country.id
    return  countryId

def getJsonWithCitiesNames(countryName):
    country = session.query(Country).filter_by(countryName=countryName).first()
    if not country:
        return {"cities": []}
    cities = session.query(City).filter_by(countryId=country.id).all()
    cityNames = [city.cityName for city in cities]
    return {"cities": cityNames}

def getProfessionNames():
    professionNames = session.query(Profession.professionName).all()
    professionNames = [name[0] for name in professionNames]
    return professionNames

def getProfessionByName(professionName):
    return session.query(Profession).filter_by(professionName=professionName).first()

def deleateCountry(countryName):
    countryToDelete = session.query(Country).filter_by(countryName=countryName).first()
    session.delete(countryToDelete)
    session.commit()

def deleateCity(cityName):
    cityToDelete = session.query(City).filter_by(cityName=cityName).first()
    session.delete(cityToDelete)
    session.commit()

def getCityNames():
    cityNames = []
    allCities = session.query(City).all()
    for city in allCities:
        cityNames.append(city.cityName)
    return cityNames

def deleateProfession(professionName):
    professionToDelete = session.query(Profession).filter_by(professionName=professionName).first()
    session.delete(professionToDelete)
    session.commit()

def makeNewBookWorker(workerId,userId,date,address,profession,additionalNotes="",status="pending"):
    newBookWorker = BookWorker(workerId=workerId,
                               userId=userId,
                               date=date,
                               address=address,
                               profession=profession,
                               additionalNotes=additionalNotes,
                               status=status
                               )
    session.add(newBookWorker)
    session.commit()

def getBookedJob(workerId,userId,profession):
    return session.query(BookWorker).filter(BookWorker.workerId==workerId,
                                            BookWorker.userId==userId,BookWorker.profession==profession).first()

def getBookedJobById(jobId):
    return session.query(BookWorker).filter_by(id=jobId).first()

def bookedJobDelete(jobId):
    jobToDelete = session.query(BookWorker).filter_by(id=jobId).first()
    session.delete(jobToDelete)
    session.commit()

def bookedJobChangeStatus(jobId,status):
    job = session.query(BookWorker).filter_by(id=jobId).first()
    job.status = status
    session.commit()

def chagneJobDate(jobId,date):
    job = session.query(BookWorker).filter_by(id=jobId).first()
    job.date = date
    session.commit()

def addNewCompleteJobPending(id,workerId,userId,jobDescription,price,date,address):
    newFinishJob = CompleteJobPending(
        id=id,
        workerId=workerId,
        userId=userId,
        jobDescription = jobDescription,
        price = price,
        date = date,
        address= address
    )
    session.add(newFinishJob)
    session.commit()

def deleteCompleteJobPending(job):
    session.delete(job)
    session.commit()

def makeNewCompleteJob(workerId,userId,jobDescription,price,review,rating):
    newCompleteJob = CompleteJob(
        workerId=workerId,
        userId=userId,
        jobDescription=jobDescription,
        price=price,
        review=review,
        rating=rating
    )
    session.add(newCompleteJob)
    session.commit()
