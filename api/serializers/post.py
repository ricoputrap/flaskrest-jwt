from api.utils import ma

class PostSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "content", "user_id")