from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from ..models.comment import Comment
from db import Session
from sentry import ravenClient
from .utils import processEmotion

commentApis = Blueprint('comment', __name__)

def is_int(str):
    try:
        int(str)
    except ValueError:
        return False
    return True



@commentApis.route('/comment', methods=['GET'])
@cross_origin()
def comment():
    id = request.args.get('id')
    if not is_int(id):
        return '', 400

    session = Session()
    comments = session.query(Comment.content).filter(Comment.id==int(id)).all()
    session.close()
    if len(comments) == 1:
        return jsonify({ 'content': comments[0].content + '<br/><a href="http://acfun.trisolaries.com:7070/" target="_blank" style="color: blue;">请点击链接到官网升级插件</a>' }), 200
    else:
        return '', 404


updateTip = """<div data-id="upgrade-tip" style="display: flex; align-items: center; margin-top: 15px;">
<a href="http://acfun.trisolaries.com:7070/" target="_blank" style="color: blue;">请点击链接到官网升级插件</a><span data-id="not-show-update-tip" style="cursor: pointer;">&nbsp;&nbsp;永不提示（包括以后的版本）</span></div>"""
@commentApis.route('/v2/comment', methods=['GET'])
@cross_origin()
def commentV2():
    content_id = request.args.get('content_id')
    count = request.args.get('count')
    if not is_int(content_id) or not is_int(count):
        return '', 400

    session = Session()
    comments = session.query(Comment.content, Comment.userId).filter(Comment.contentId==int(content_id)).filter(Comment.count==int(count)).all()
    session.close()
    if len(comments) == 1:
        return jsonify({
            'content': processEmotion(comments[0].content),
            'userId': comments[0].userId,
            'needUpdateVersion': '1.0',
            'updateTip': updateTip
        }), 200
    else:
        return '', 404
