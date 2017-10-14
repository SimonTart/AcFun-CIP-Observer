from flask import Flask
from .comment import comment_page

server = Flask(__name__)
server.register_blueprint(comment_page)
