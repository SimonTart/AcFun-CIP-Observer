from flask import Flask
from flask_cors import CORS
from .comment import comment_page

server = Flask(__name__)
CORS(server)
server.register_blueprint(comment_page)
