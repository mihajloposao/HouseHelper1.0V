from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user

Base = declarative_base()
engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=True)
Session = sessionmaker(bind=engine)

def makingDatabases():
    Base.metadata.create_all(engine)

class User(Base, UserMixin):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    userEmail = Column(String, nullable=False, unique= True)
    userName = Column(String, nullable=False)
    userSurename = Column(String, nullable=False)
    userPhone = Column(String, nullable=False)
    userCountry = Column(String, nullable=True)
    userCity = Column(String, nullable=True)
    userStreet = Column(String, nullable=True)
    userStreetNumber = Column(String, nullable=True)
    userPassword = Column(String, nullable=False)

class Country(Base):
    __tablename__ = "Countries"
    id = Column(Integer, primary_key=True)
    countryName = Column(String, nullable=False, unique= True)
    cities = relationship("City", back_populates="country")

class City(Base):
    __tablename__ = "Cities"
    id = Column(Integer, primary_key=True)
    cityName = Column(String, nullable=False, unique= True)
    countryId = Column(Integer, ForeignKey("Countries.id"), nullable=False)
    country = relationship("Country", back_populates="cities")

def addNewUserToBase(basicUserInfo):
    session = Session()
    newUser = User(
        userEmail=basicUserInfo["userEmail"],
        userName=basicUserInfo["userName"],
        userSurename=basicUserInfo["userSurename"],
        userPhone=basicUserInfo["userPhone"],
        userPassword=generate_password_hash(basicUserInfo["userPassword"])
    )
    session.add(newUser)
    session.commit()
    session.close()

def userExist(userEmail):
    session = Session()
    try:
        return session.query(User).filter_by(userEmail=userEmail).first() is not None
    finally:
        session.close()

def getUserByEmail(userEmail):
    session = Session()
    try:
        return session.query(User).filter_by(userEmail=userEmail).first()
    finally:
        session.close()

def UserById(id):
    session = Session()
    try:
        return session.query(User).filter_by(id=id).first()
    finally:
        session.close()

def addUserAddress(basicUserInfo):
    session = Session()
    user = session.query(User).filter_by(userEmail=current_user.userEmail).first()
    try:
        user.userCountry = basicUserInfo["userCountry"]
        user.userCity = basicUserInfo["userCity"]
        user.userStreet = basicUserInfo["userStreet"]
        user.userStreetNumber = basicUserInfo["userStreetNumber"]
        session.commit()
    finally:
        session.close()

def addNewCountry(countryName):
    session = Session()
    newCounty = Country(countryName = countryName)
    session.add(newCounty)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.close()

def getCountryNames():
    session = Session()
    countryNames = session.query(Country.countryName).all()
    session.close()
    return countryNames

def addNewCity(countryName, cityName):
    countryId = getCountryIdByName(countryName)
    session = Session()
    newCity = City(cityName = cityName,countryId = countryId)
    session.add(newCity)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.close()

def getCountryIdByName(countryName):
    session = Session()
    country = session.query(Country).filter_by(countryName=countryName).first()
    countryId = country.id
    session.close()
    return  countryId