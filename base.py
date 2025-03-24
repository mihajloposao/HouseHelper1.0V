from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column, String, Integer,  create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()

def makingDatabases():
    engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=True)
    Base.metadata.create_all(engine)

class User(Base,UserMixin):
    __tablename__ = "Users"
    id=Column(Integer,primary_key=True)
    userEmail = Column(String,nullable=False)
    userName = Column(String,nullable=False)
    userSurename = Column(String,nullable=False)
    userPhone = Column(String,nullable=False)
    userCountry = Column(String,nullable=True)
    userCity = Column(String,nullable=True)
    userStreet = Column(String,nullable=True)
    userStreetNumber = Column(String,nullable=True)
    userPassword = Column(String,nullable=False)

def addUser(basicUserInfo):
    userEmail = basicUserInfo["userEmail"]
    userName = basicUserInfo["userName"]
    userSurename = basicUserInfo["userSurename"]
    userPhone = basicUserInfo["userPhone"]
    userPassword = generate_password_hash(basicUserInfo["userPassword"])

    engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    newUser = User(userEmail=userEmail,
                   userName=userName,
                   userSurename=userSurename,
                   userPhone=userPhone,
                   userPassword=userPassword)
    session.add(newUser)
    session.commit()
    session.close()

def userExist(userEmail):
    engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    existing_user = session.query(User).filter_by(userEmail=userEmail).first()
    session.close()
    if existing_user:
        return True
    else:
        return False

def UserByEmail(userEmail):
    engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    existingUser = session.query(User).filter_by(userEmail=userEmail).first()
    return existingUser

def UserById(id):
    engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    existingUser = session.query(User).filter_by(id=id).first()
    return existingUser

def addUserAddress(user,basicUserInfo):
    engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    user.userCountry = basicUserInfo["userCountry"]
    user.userCity = basicUserInfo["userCity"]
    user.userStreet = basicUserInfo["userStreet"]
    user.userStreetNumber = basicUserInfo["userStreetNumber"]
    session.commit()
    session.close()