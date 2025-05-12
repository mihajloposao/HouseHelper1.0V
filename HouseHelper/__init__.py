from flask import Flask,redirect,request,jsonify,url_for,render_template,flash
from flask_login import LoginManager,current_user,login_required, UserMixin, logout_user,login_user,user_unauthorized
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey,Table,Double
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash
import requests
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "logInUser"

Base = declarative_base()
engine = create_engine("sqlite:///usersWorkersCompaniesAdmin.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

from HouseHelper import routes, database

Base.metadata.create_all(engine)