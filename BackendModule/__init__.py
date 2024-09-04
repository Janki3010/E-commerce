from flask_cors import CORS
from flask import Flask
from flask_restful import Api
import importlib
from flask_mysqldb import MySQL
from flask_socketio import SocketIO

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, origins=["http://127.0.0.1:6001"], cors_allowed_origins="*")

CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'ecommerce'

mysql = MySQL(app)
app.secret_key = 'your_secret_key'


importlib.import_module('BackendModule.pack1')
