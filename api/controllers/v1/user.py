from flask import jsonify, make_response, request
from flask_restful import Resource, abort
from api.services.user import UserService
from api.serializers.user import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

class User(Resource):

  user_service = UserService()

  def get(self, public_id = None):
    try:
      if public_id == None:
        users = self.user_service.get_all_users()
        response = {
          'data': user_list_schema.dump(users),
          'total': len(users)
        }
        return response
      else:
        user = self.user_service.get_user_by_id(public_id)

        if not user:
          return make_response(jsonify({
            'errors': [
              {
                "status": 404,
                "source": { "pointer": "/users/<public_id>", "method": "GET" },
                "title": "User not found",
                "detail": "User with public_id = %s is not found" % (public_id)
              }
            ]
          }), 404)

        response = {
          'data': user_schema.dump(user)
        }
        return response
    except Exception as e:
      return make_response(jsonify({
        'errors': [
          {
            "status": 500,
            "source": { "pointer": "/users/", "method": "GET" },
            "title": "Internal Server Error",
            "detail": str(e)
          }
        ]
      }), 500)

  def post(self):
    try:
      path = request.path
      if path == '/login/':
        result = self.user_service.login(request.get_json())
        if not result:
          return make_response(jsonify({
            'errors': [
              {
                "status": 401,
                "source": { "pointer": "/login/", "method": "POST" },
                "title": "Unauthorized",
                "detail": "Wrong username or password."
              }
            ]
          }), 404)
        
        response = {
          "message": "Login success!",
          "data": {
            "user": user_schema.dump(result['user']),
            "token": result['token']
          }
        }

        return response
      elif path == '/register/':
        # print("===== REGISTER =====")
        return
      
      request_body = request.get_json()
      new_user = self.user_service.create_new_user(request_body)
      response = {
        "message": "New user is successfully created!",
        "data": user_schema.dump(new_user) 
      }
      return response
    except Exception as e:
      return make_response(jsonify({
        'errors': [
          {
            "status": 500,
            "source": { "pointer": "/users/", "method": "POST" },
            "title": "Internal Server Error",
            "detail": str(e)
          }
        ]
      }), 500)
  
  def put(self, public_id):
    try:
      request_body = request.get_json()
      updated_user = self.user_service.update_user(public_id, request_body)

      if not updated_user:
        return make_response(jsonify({
            'errors': [
              {
                "status": 404,
                "source": { "pointer": "/users/<public_id>", "method": "PUT" },
                "title": "User not found",
                "detail": "User with public_id = %s is not found" % (public_id)
              }
            ]
          }), 404)
      
      response = {
        "message": "User data is successfully updated",
        "data": user_schema.dump(updated_user) 
      }
      return response
    except Exception as e:
      return make_response(jsonify({
        'errors': [
          {
            "status": 500,
            "source": { "pointer": "/users/", "method": "PUT" },
            "title": "Internal Server Error",
            "detail": str(e)
          }
        ]
      }), 500)

  def delete(self, public_id):
    try:
      user = self.user_service.delete_user(public_id)

      if not user:
        return make_response(jsonify({
            'errors': [
              {
                "status": 404,
                "source": { "pointer": "/users/<public_id>", "method": "PUT" },
                "title": "User not found",
                "detail": "User with public_id = %s is not found" % (public_id)
              }
            ]
          }), 404)
      
      response = {
        "message": "User with public_id = %s is successfully deleted" % (public_id)
      }
      return response
    except Exception as e:
      return make_response(jsonify({
        'errors': [
          {
            "status": 500,
            "source": { "pointer": "/users/", "method": "DELETE" },
            "title": "Internal Server Error",
            "detail": str(e)
          }
        ]
      }), 500)