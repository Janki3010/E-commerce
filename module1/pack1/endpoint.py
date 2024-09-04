from module1 import api, socketio
from module1.pack1.resources import *

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(AddProduct, '/add_product')
api.add_resource(ProductDetails, '/products')
socketio.on_namespace(ChatBot('/chat'))
