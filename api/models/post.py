from api.utils import db

class PostModel(db.Model):
  __tablename__ = 'Post'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, nullable=False)