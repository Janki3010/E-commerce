from flask import Flask
from flask_restful import Api
import importlib
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'ecommerce'

mysql = MySQL(app)
app.secret_key = 'your_secret_key'


importlib.import_module('module1.pack1')
