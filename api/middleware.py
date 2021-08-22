from werkzeug.wrappers import Request, Response

class AuthMiddleware:
  def __init__(self, app):
    self.app = app
  
  def __call__(self, environ, start_response):
    req = Request(environ)
    path = req.path
    print("===== path: " + path )

    return self.app(environ, start_response)