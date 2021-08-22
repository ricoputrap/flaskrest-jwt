from api.utils import db

class TodoModel(db.Model):
  __tablename__ = 'Todo'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  is_completed = db.Column(db.Boolean, nullable=False, default=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)