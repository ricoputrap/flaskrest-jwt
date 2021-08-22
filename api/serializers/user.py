from api.utils import ma

class UserSchema(ma.Schema):
  class Meta:
    fields = ("id", "public_id", "username", 
              "password", "fullname", "is_admin")