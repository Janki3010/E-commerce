from flask import Blueprint
from BackendModule import app, api, socketio

pack1_bp = Blueprint('pack1', __name__)
api.blueprint_setup = pack1_bp
api.blueprint = pack1_bp

from BackendModule.pack1 import endpoint, resources

app.register_blueprint(pack1_bp)

