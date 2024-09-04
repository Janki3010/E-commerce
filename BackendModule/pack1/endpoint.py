from BackendModule import api, socketio
from BackendModule.pack1.resources import *

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(AddProduct, '/add_product')
api.add_resource(ProductDetails, '/products')
api.add_resource(AddToCart, '/add_to_cart')
api.add_resource(Logout, '/logout')
socketio.on_namespace(ChatBot('/chat'))
