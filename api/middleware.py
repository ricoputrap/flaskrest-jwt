import os
from dotenv import load_dotenv
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
load_dotenv()

from werkzeug.wrappers import Request, Response
import jwt
import json

class AuthMiddleware:
  auth_token_not_provided = { "message": "Authentication credentials were not provided." }
  auth_token_not_valid = { "message": "Authentication token is not valid." }
  auth_token_expired = { "message": "Authentication token has expired." }

  def __init__(self, app):
    self.app = app
  
  def __call__(self, environ, start_response):
    req = Request(environ)
    res = Response(mimetype='application/json', status=401)

    path = req.path
    if path == '/users/':
      try:
        header_auth_token = req.headers['Authorization']
        auth_token = header_auth_token.replace('Bearer ', '')
        secret_key = os.getenv('SECRET_KEY')
        jwt.decode(auth_token, secret_key, algorithms=['HS256'])

        return self.app(environ, start_response)

      except ExpiredSignatureError as e:
        res.data = json.dumps(self.auth_token_expired)
        return res(environ, start_response)

      except InvalidTokenError as e:
        res.data = json.dumps(self.auth_token_not_valid)
        return res(environ, start_response)

      except KeyError as e:
        res.data = json.dumps(self.auth_token_not_provided)
        return res(environ, start_response)

      except Exception as e:
        res.data = json.dumps(self.auth_token_not_provided)
        return res(environ, start_response)

    return self.app(environ, start_response)