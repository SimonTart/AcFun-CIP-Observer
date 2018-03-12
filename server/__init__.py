from flask import Flask
from flask_cors import CORS

from .apis.comment import commentApis

server = Flask(__name__)
CORS(server)
server.register_blueprint(commentApis)
