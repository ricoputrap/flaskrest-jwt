from api.models.user import UserModel
from api.utils import db
from werkzeug.security import generate_password_hash
import uuid

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