from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

db = SQLAlchemy()
DB_NAME = 'database.db'
UPLOAD_FOLDER = 'py/static/uploads/'

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'haha secret key'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  global upload_folder
  upload_folder = app.config['UPLOAD_FOLDER']

  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from . models import users, books

  create_database(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
    return users.query.get(int(id))

  return app

def create_database(app):
  if not path.exists('py/' + DB_NAME):
    db.create_all(app = app)
    print('Database created.')

