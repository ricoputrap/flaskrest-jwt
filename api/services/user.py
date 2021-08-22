import os
from dotenv import load_dotenv
load_dotenv()

from api.models.user import UserModel
from api.utils import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime

class UserService:

  def get_all_users(self):
    users = UserModel.query.all()
    return users

  def get_user_by_id(self, public_id):
    user = UserModel.query.filter_by(public_id=public_id).first()
    return user

  def create_new_user(self, new_user_data):
    hashed_password = generate_password_hash(new_user_data['password'], method='sha256')
    public_id = str(uuid.uuid4())
    new_user = UserModel(public_id=public_id, username=new_user_data['username'], password=hashed_password, fullname=new_user_data['fullname'])
    db.session.add(new_user)
    db.session.commit()
    return new_user
  
  def update_user(self, public_id, request_body):
    user = UserModel.query.filter_by(public_id=public_id).first()
    if not user:
      return None

    if "username" in request_body:
      user.username = request_body['username']
    if "fullname" in request_body:
      user.fullname = request_body['fullname']
    if "is_admin" in request_body:
      user.is_admin = request_body['is_admin']
    if "password" in request_body:
      hashed_password = generate_password_hash(request_body['password'], method='sha256')
      user.password = hashed_password
    
    db.session.commit()

    return user

  def delete_user(self, public_id):
    user = UserModel.query.filter_by(public_id=public_id).first()
    if not user:
      return None
    
    db.session.delete(user)
    db.session.commit()
    return True
  
  def login(self, request_body):
    user = UserModel.query.filter_by(username=request_body['username']).first()
    if not user:
      return None
    
    if check_password_hash(user.password, request_body['password']):
      '''
      @TODO implement function to extend the token expiration date automatically if the users are still logged-in at the last second of the exp date
      '''
      payload = {
        'public_id': user.public_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
      }
      secret_key = os.getenv('SECRET_KEY')
      token = jwt.encode(payload, secret_key)
      return {
        "token": token,
        "user": user
      }
    
    return None