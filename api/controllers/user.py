from flask import jsonify, make_response, request
from flask_restful import Resource, abort
from api.services.user import UserService
from api.serializers.user import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

class User(Resource):

  user_service = UserService()

  def get(self, public_id = None):
    if public_id == None:
      users = self.user_service.get_all_users()
      response = {
        'data': user_list_schema.dump(users)
      }
      return response
    else:
      user = self.user_service.get_user_by_id(public_id)

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
        'data': user_schema.dump(user)
      }
      return response
    
  def post(self):
    new_user_data = request.get_json()
    new_user = self.user_service.create_new_user(new_user_data)
    response = {
      "message": "New user is successfully created!",
      "data": user_schema.dump(new_user) 
    }
    return response
