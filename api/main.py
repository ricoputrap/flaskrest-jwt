import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_restful import Api
from api.controllers.user import User

def init_app():
  app = Flask(__name__)
  api = Api(app)

  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

  from api.utils import db, ma, migrate
  db.init_app(app)
  ma.init_app(app)
  migrate.init_app(app, db)

  api.add_resource(User, "/users/", "/users/<user_id>")

  return app