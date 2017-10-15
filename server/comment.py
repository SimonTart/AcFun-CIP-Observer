from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
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
@cross_origin()
def comment():
  id = request.args.get('id')
  if not is_int(id):
    return '', 400
  
  session = Session()
  comments = session.query(Comment.content).filter(Comment.id==int(id)).all()
  session.close()
  if len(comments) == 1:
    return jsonify({ 'content': comments[0].content }), 200
  else:
    return '', 404
