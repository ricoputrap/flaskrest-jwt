from api.utils import db

class UserModel(db.Model):
  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(50), nullable=False, unique=True)
  username = db.Column(db.String(50), nullable=False)
  password = db.Column(db.String(80), nullable=False)
  fullname = db.Column(db.String(50), nullable=False)
  is_admin = db.Column(db.Boolean, nullable=False, default=False)
  todos = db.relationship('TodoModel', backref='user', lazy=True)