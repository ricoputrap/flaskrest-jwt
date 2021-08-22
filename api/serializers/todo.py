from api.utils import ma

class TodoSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "is_completed", "user_id")