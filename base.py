from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer, create_engine
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

Base = declarative_base()
engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=True)
Session = sessionmaker(bind=engine)

def makingDatabases():
    Base.metadata.create_all(engine)

class User(Base, UserMixin):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    userEmail = Column(String, nullable=False)
    userName = Column(String, nullable=False)
    userSurename = Column(String, nullable=False)
    userPhone = Column(String, nullable=False)
    userCountry = Column(String, nullable=True)
    userCity = Column(String, nullable=True)
    userStreet = Column(String, nullable=True)
    userStreetNumber = Column(String, nullable=True)
    userPassword = Column(String, nullable=False)

def addUser(basicUserInfo):
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

def UserByEmail(userEmail):
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

def addUserAddress(userEmail, basicUserInfo):
    session = Session()
    user = session.query(User).filter_by(userEmail=userEmail).first()
    try:
        user.userCountry = basicUserInfo["userCountry"]
        user.userCity = basicUserInfo["userCity"]
        user.userStreet = basicUserInfo["userStreet"]
        user.userStreetNumber = basicUserInfo["userStreetNumber"]
        session.commit()
    finally:
        session.close()
