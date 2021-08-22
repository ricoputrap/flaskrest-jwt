import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_restful import Api
from api.utils import db, ma, migrate
from api.controllers.v1.user import User
from api.middleware import AuthMiddleware

def init_app():
  app = Flask(__name__)
  api = Api(app)

  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

  db.init_app(app)
  ma.init_app(app)
  migrate.init_app(app, db)

  api.add_resource(User, "/users/", "/users/<public_id>")
  app.add_url_rule("/login/", endpoint="user", methods=["POST"])
  app.add_url_rule("/register/", endpoint="user", methods=["POST"])

  app.wsgi_app = AuthMiddleware(app.wsgi_app)

  return app