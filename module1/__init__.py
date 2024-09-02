from flask import Flask
from flask_restful import Api
import importlib

app = Flask(__name__)
api = Api(app)

# app.config['SECRET_KEY'] = 'abc@123$%107'

importlib.import_module('module1.pack1')