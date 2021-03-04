# where we initialize app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) #just the name of the module
app.config['SECRET_KEY'] = '994fc53fc5ec59d69c69255d31fb4c72'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # relative path rfom current file -> in project directory
db = SQLAlchemy(app) # makes DataBase
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category = 'info'

print("creatring db")

from webapp.models import User, Post
db.create_all()

from webapp import routes # avoids circular importing