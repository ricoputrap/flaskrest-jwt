from api.models.user import UserModel

class UserService:

  def get_all_users(self):
    users = UserModel.query.all()
    return users

  def get_user_by_id(self, user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    return user