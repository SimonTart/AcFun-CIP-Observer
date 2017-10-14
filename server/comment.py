from flask import Blueprint, request, jsonify
from models.comment import Comment
from db import Session

comment_page = Blueprint('comment_page', __name__)

def is_int(str):
  try:
    int(str)
  except ValueError:
    return False
  return True



@comment_page.route('/comment', methods=['GET'])
def comment():
  id = request.args.get('id')
  if not is_int(id):
    return '', 400
  
  print(int(id))
  session = Session()
  comments = session.query(Comment.content).filter(Comment.id==int(id)).all()
  session.close()
  print(comments)
  if len(comments) == 1:
    return jsonify({ 'content': comments[0].content }), 200
  else:
    return '', 404
