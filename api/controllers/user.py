from flask import jsonify, make_response
from flask_restful import Resource, abort
from api.services.user import UserService
from api.serializers.user import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

class User(Resource):

  user_service = UserService()

  def get(self, user_id = None):
    if user_id == None:
      users = self.user_service.get_all_users()
      response = {
        'data': user_list_schema.dump(users)
      }
      return response
    else:
      user = self.user_service.get_user_by_id(user_id)

      if not user:
        # abort(404, message="User not found")
        return make_response(jsonify({
          'errors':[
            {
              "status": 404,
              "source": { "pointer": "/users/<user_id>" },
              "title": "User not found",
              "detail": "User with user_id = %s is not found" % (user_id)
            }
          ]
        }), '404')

      response = {
        'data': user_schema(user)
      }
      return response
    
    
    
    